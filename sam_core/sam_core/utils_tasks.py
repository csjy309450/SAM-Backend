import time
import threading
import threadpool
from apscheduler.schedulers.blocking import BlockingScheduler


class SchedulerTaskBase:
    def __init__(self, task_id, seconds):
        self.task_id = task_id
        self.seconds = seconds

    def run(self):
        pass


class SchedulerTaskQueue:
    __scheduler = BlockingScheduler()
    __cs_task_list = threading.Lock()
    __task_list = {}
    __main_thx = None
    __cs_main_thx = threading.Lock()

    @staticmethod
    def __schedular_loop():
        SchedulerTaskQueue.__scheduler.start()

    @staticmethod
    def start():
        if not SchedulerTaskQueue.__main_thx:
            SchedulerTaskQueue.__cs_main_thx.acquire()
            if not SchedulerTaskQueue.__main_thx:
                SchedulerTaskQueue.__main_thx = threading.Thread(target=SchedulerTaskQueue.__schedular_loop, args=())
                SchedulerTaskQueue.__main_thx.start()
            SchedulerTaskQueue.__cs_main_thx.release()

    @staticmethod
    def wait():
        SchedulerTaskQueue.__main_thx.join()
        print('D|wait out')

    @staticmethod
    def stop():
        SchedulerTaskQueue.__scheduler.shutdown()

    @staticmethod
    def add(task: SchedulerTaskBase, *args, **argv) -> int:
        print('D|add in')
        if task.task_id in SchedulerTaskQueue.__task_list:
            return -1
        print('D|add task ', task.task_id)
        SchedulerTaskQueue.__cs_task_list.acquire()
        SchedulerTaskQueue.__task_list[task.task_id] = task
        SchedulerTaskQueue.__scheduler.add_job(task.run, 'interval', seconds=task.seconds, id=task.task_id)
        SchedulerTaskQueue.__cs_task_list.release()
        return 0

    @staticmethod
    def remove(task_id):
        if task_id in SchedulerTaskQueue.__task_list:
            SchedulerTaskQueue.__cs_task_list.acquire()
            SchedulerTaskQueue.__scheduler.remove_job(task_id)
            SchedulerTaskQueue.__task_list.pop(task_id)
            SchedulerTaskQueue.__cs_task_list.release()


class ImmediateTaskQueue:
    """ImmediateTaskQueue"""
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
    def add(fn, *args, **argv):
        ImmediateTaskQueue.__task_list.append((fn, args, argv))


def test_ImmediateTaskQueue():
    def test_fn(a):
        print(a)

    ImmediateTaskQueue.start()
    ImmediateTaskQueue.add(test_fn, 1)
    ImmediateTaskQueue.add(test_fn, 2)
    ImmediateTaskQueue.add(test_fn, 3)
    time.sleep(4)
    ImmediateTaskQueue.stop()
    ImmediateTaskQueue.wait()


def test_SchedulerTaskQueue():
    print('D|test_SchedulerTaskQueue in')

    class SchedulerTaskTest(SchedulerTaskBase):
        def __init__(self, id, sec, x):
            super(SchedulerTaskTest, self).__init__(id, sec)
            self.x = x

        def run(self):
            print('SchedulerTaskTest:', self.task_id, self.x)

    task1 = SchedulerTaskTest('SchedulerTaskTest1', 10, 1)
    task2 = SchedulerTaskTest('SchedulerTaskTest2', 5, 2)
    SchedulerTaskQueue.add(task1)
    SchedulerTaskQueue.add(task2)
    SchedulerTaskQueue.start()
    time.sleep(30)
    SchedulerTaskQueue.stop()
    SchedulerTaskQueue.wait()


if __name__ == '__main__':
    test_SchedulerTaskQueue()
