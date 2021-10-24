import time
import threading
import threadpool
from apscheduler.schedulers.blocking import BlockingScheduler


class SchedulerTaskQueue:
    __scheduler = BlockingScheduler()
    __cs_task_list = threading.Lock()
    __task_list = {}

    @staticmethod
    def start():
        SchedulerTaskQueue.__scheduler.start()

    @staticmethod
    def stop():
        SchedulerTaskQueue.__scheduler.stop()

    @staticmethod
    def post(task_id, minutes, task_fn, *args, **argv) -> int:
        if task_id in SchedulerTaskQueue.__task_list:
            return -1
        SchedulerTaskQueue.__cs_task_list.acquire()
        SchedulerTaskQueue.__task_list[task_id] = {'status': 0, 'interval': minutes, 'param': [args, argv]}
        SchedulerTaskQueue.__scheduler.add_job(task_fn, 'interval', minutes=minutes, id=task_id)
        SchedulerTaskQueue.__cs_task_list.release()
        return 0


class ImmediateTaskQueue:
    __thx_pool = threadpool.ThreadPool(10)
    __task_list = []
    __cs_thx_list = threading.Lock()
    __is_stop = True
    __cs_is_stop = threading.Lock()

    @staticmethod
    def start():
        print('D|start in')
        requests_ = threadpool.makeRequests(ImmediateTaskQueue.__pool_thx, [1])
        print('D|', requests_)
        [ImmediateTaskQueue.__thx_pool.putRequest(req) for req in requests_]
        ImmediateTaskQueue.__cs_is_stop.acquire()
        ImmediateTaskQueue.__is_stop = False
        ImmediateTaskQueue.__cs_is_stop.release()

    @staticmethod
    def stop():
        print('D|stop in')
        ImmediateTaskQueue.__cs_is_stop.acquire()
        ImmediateTaskQueue.__is_stop = True
        ImmediateTaskQueue.__cs_is_stop.release()

    @staticmethod
    def wait():
        print('D|wait in')
        ImmediateTaskQueue.__thx_pool.wait()

    @staticmethod
    def __pool_thx(_):
        print('D|__pool_thx in')
        while not ImmediateTaskQueue.__is_stop:
            if len(ImmediateTaskQueue.__task_list) == 0:
                print('D|empty list wait 2s')
                time.sleep(2)
                continue
            ImmediateTaskQueue.__cs_thx_list.acquire()
            fn, args, argv = ImmediateTaskQueue.__task_list.pop(0)
            ImmediateTaskQueue.__cs_thx_list.release()
            try:
                fn(*args, **argv)
            except Exception as e:
                continue

    @staticmethod
    def post(fn, *args, **argv):
        ImmediateTaskQueue.__task_list.append((fn, args, argv))


__task_queue = ImmediateTaskQueue()


def test_ImmediateTaskQueue():
    def test_fn(a):
        print(a)
    ImmediateTaskQueue.start()
    ImmediateTaskQueue.post(test_fn, 1)
    ImmediateTaskQueue.post(test_fn, 2)
    ImmediateTaskQueue.post(test_fn, 3)
    time.sleep(4)
    ImmediateTaskQueue.stop()
    ImmediateTaskQueue.wait()


if __name__ == '__main__':
    pass
