STATUS_NO_ERROR = 0
STATUS_KNOWN = 1
STATUS_API_DISABLED = 2

g_error_code = {
    STATUS_NO_ERROR: {'ch': '成功', 'en': 'succeed'},
    STATUS_KNOWN: {'ch': '未知错误', 'en': 'unknown error'},
    STATUS_API_DISABLED: {'ch': 'API不可用', 'en': 'api disabled'}
}


class JsonObjBase(object):
    def __init__(self):
        pass

    def __json__(self, request):
        return self.__dict__


class ResBase(JsonObjBase):
    def __init__(self, errorCode, data=None):
        super(ResBase, self).__init__()
        self.errorCode = errorCode
        self.errorMessage = g_error_code.get(errorCode, 1)['en']
        self.data = data


class ResPerfConfig(JsonObjBase):
    def __init__(self, on_off=None, sampling_rate=None, storage_time=None):
        super(ResPerfConfig, self).__init__()
        self.on_off = on_off
        self.sampling_rate = sampling_rate
        self.storage_time = storage_time


class ResLoadInfo(JsonObjBase):
    def __init__(self, level=0, date=[], one_min=[], five_min=[], fiften_min=[]):
        super(ResLoadInfo, self).__init__()
        self.level = level
        self.date = date
        self.one_min = one_min
        self.five_min = five_min
        self.fiften_min = fiften_min


class ResProcInfo(JsonObjBase):
    def __init__(self, proc_count=0, proc_stat_distribution=[], proc_user_distribution=[]):
        super(ResProcInfo, self).__init__()
        self.proc_count = proc_count
        self.proc_stat_distribution = proc_stat_distribution
        self.proc_user_distribution = proc_user_distribution


class ResCpuInfo(JsonObjBase):
    def __init__(self, cpu_count=0, cpu_usage_rate=[]):
        super(ResCpuInfo, self).__init__()
        self.cpu_count = cpu_count
        self.cpu_usage_rate = cpu_usage_rate


class ResMemoryInfo(JsonObjBase):
    def __init__(self, date=[], mem_size=0, mem_usage=[], swap_size=0, swap_usage=[]):
        super(ResMemoryInfo, self).__init__()
        self.date = date
        self.mem_size = mem_size
        self.mem_usage = mem_usage
        self.swap_size = swap_size
        self.swap_usage = swap_usage


class ResDiskInfo(JsonObjBase):
    def __init__(self, disk_size=0, disk_usage=[], disk_io_rate=[]):
        super(ResDiskInfo, self).__init__()
        self.disk_size = disk_size
        self.disk_usage = disk_usage
        self.disk_io_rate = disk_io_rate


class ResNetInfo(JsonObjBase):
    def __init__(self, net_io_rate=[]):
        super(ResNetInfo, self).__init__()
        self.net_io_rate = net_io_rate


class ResPerfInfo(JsonObjBase):
    def __init__(self,
                 host_run_time='', avg_login_user_count=0, history_proc_count=[], history_login_user_count=[],
                 avg_proc_count=0, host_idle_rate=0, login_user_count=0,
                 load_info=ResLoadInfo(), proc_info=ResProcInfo(), cpu_info=ResCpuInfo(),
                 memory_info=ResMemoryInfo(), disk_info=ResDiskInfo(), net_info=ResNetInfo()):
        super(ResPerfInfo, self).__init__()
        self.host_run_time = host_run_time
        self.avg_proc_count = avg_proc_count
        self.history_proc_count = history_proc_count
        self.history_login_user_count = history_login_user_count
        self.avg_login_user_count = avg_login_user_count
        self.host_idle_rate = host_idle_rate
        self.login_user_count = login_user_count
        self.load_info = load_info
        self.proc_info = proc_info
        self.cpu_info = cpu_info
        self.memory_info = memory_info
        self.disk_info = disk_info
        self.net_info = net_info
