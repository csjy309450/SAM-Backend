import sys
import os
from sam_app.model_layer.model import Session, engine, Base, PerfConfig
from sqlalchemy import inspect
from sam_core.utils_tasks import SchedulerTaskQueue, SchedulerTaskBase, ImmediateTaskQueue
from sam_app.view_layer.view_perf import PerfSchedulerTask

SAM_DB_NAME = 'sam_app.db'
SAM_PWD = os.getcwd()


class GlobalCtl:
    @staticmethod
    def init():
        GlobalCtl.__init_db()
        GlobalCtl.__init_business()

    @staticmethod
    def uninit():
        pass

    @staticmethod
    def __init_db():
        if os.path.isfile(os.path.join(SAM_PWD, SAM_DB_NAME)):
            insp = inspect(engine)
            if not insp.has_table(table_name='sam_perf_config'):
                Base.metadata.create_all(engine)
        else:
            Base.metadata.create_all(engine)

    @staticmethod
    def __init_business():
        ImmediateTaskQueue.start()
        SchedulerTaskQueue.start()
        GlobalCtl.__init_perf_service()

    @staticmethod
    def __init_perf_service():
        session = Session()
        objs = session.query(PerfConfig).filter(PerfConfig.key.in_(['on_off', 'sampling_rate', 'storage_time'])).all()
        on_off = 0
        sampling_rate = 10
        storage_time = 24 * 7
        for it in objs:
            if it.key == 'on_off':
                on_off = it.value_int
            if it.key == 'sampling_rate':
                sampling_rate = it.value_int
            if it.key == 'storage_time':
                storage_time = it.value_int
        if on_off == 1:
            perf_task = PerfSchedulerTask(sampling_rate)
            SchedulerTaskQueue.add(perf_task)
