import json
from pyramid.response import Response
from sam.view_layer.view_base import ViewBase
from sam.common.res_obj import *
from sam.common.util_perf import UtilPerfLinux
from sam.model_layer.model import PerfConfig, Session
from sam.common.util_tasks import SchedulerTaskQueue, SchedulerTaskBase


class PerfSchedulerTask(SchedulerTaskBase):
    perf_scheduler_task_id = 'PerfSchedulerTask'

    def __init__(self, seconds):
        super(PerfSchedulerTask, self).__init__(PerfSchedulerTask.perf_scheduler_task_id, seconds)

    def run(self):
        print('I|run PerfSchedulerTask')


class ViewPerf(ViewBase):
    def __init__(self, request):
        super(ViewPerf, self).__init__(request)

    def get_perf_info(self):
        return UtilPerfLinux().get_test_perf_info()

    def post_perf_config(self):
        json_body = self.req.json_body
        on_off = json_body.get('on_off', 0)
        sampling_rate = json_body.get('sampling_rate', 10)
        storage_time = json_body.get('storage_time', 24 * 7)
        session = Session()
        obj_on_off = session.query(PerfConfig).filter(PerfConfig.key == 'on_off').first()
        is_on_off_changed = False
        if not obj_on_off:
            obj_on_off = PerfConfig(key='on_off', value_int=0)
            session.add(obj_on_off)
        else:
            if obj_on_off.value_int != on_off:
                obj_on_off.value_int = on_off
                is_on_off_changed = True
        obj_sampling_rate = session.query(PerfConfig).filter(PerfConfig.key == 'sampling_rate').first()
        is_sampling_rate_changed = False
        if not obj_sampling_rate:
            obj_sampling_rate = PerfConfig(key='sampling_rate', value_int=10)
            session.add(obj_sampling_rate)
        else:
            if obj_sampling_rate.value_int != sampling_rate:
                obj_sampling_rate.value_int = sampling_rate
                is_sampling_rate_changed = True
        obj_storage_time = session.query(PerfConfig).filter(PerfConfig.key == 'storage_time').first()
        is_storage_time_changed = False
        if not obj_storage_time:
            obj_storage_time = PerfConfig(key='storage_time', value_int=168)
            session.add(obj_storage_time)
        else:
            if obj_storage_time.value_int != storage_time:
                obj_storage_time.value_int = storage_time
                is_storage_time_changed = True
        session.commit()
        if is_on_off_changed:
            if on_off == 1:
                perf_task = PerfSchedulerTask(sampling_rate)
                SchedulerTaskQueue.add(perf_task)
            else:
                SchedulerTaskQueue.remove(PerfSchedulerTask.perf_scheduler_task_id)
        elif is_sampling_rate_changed and on_off == 1:
            SchedulerTaskQueue.remove(PerfSchedulerTask.perf_scheduler_task_id)
            perf_task = PerfSchedulerTask(sampling_rate)
            SchedulerTaskQueue.add(perf_task)
        return ResBase(0)

    def get_perf_config(self):
        session = Session()
        objs = session.query(PerfConfig).filter(PerfConfig.key.in_(['on_off', 'sampling_rate', 'storage_time'])).all()
        on_off = None
        sampling_rate = None
        storage_time = None
        for it in objs:
            if it.key == 'on_off':
                on_off = it.value_int
            if it.key == 'sampling_rate':
                sampling_rate = it.value_int
            if it.key == 'storage_time':
                storage_time = it.value_int
        return ResBase(0,
                       data=ResPerfConfig(on_off=on_off, sampling_rate=sampling_rate, storage_time=storage_time))
