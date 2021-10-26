import json
import os
import datetime
from sam.common.res_obj import *
from sam.model_layer.model import *


class UtilPerfLinux:
    def get_perf_info(self) -> ResPerfInfo:
        host_run_time, host_idle_time = self.__get_host_uptime()
        cpu_count = int(self.__run_shell('cat /proc/cpuinfo | grep "processor" | wc -l'))
        login_user_count = int(self.__run_shell('who | wc -l'))
        # load
        loads, load_level = self.__get_load_info(cpu_count)
        load_info = ResLoadInfo(
            level=load_level
        )
        # process
        proc_count, proc_stat_statistics, proc_user_statistics = self.__get_process_info()
        proc_info = ResProcInfo(
            proc_count=proc_count
        )
        # cpu
        # self.__get_cpu_info()

        # mem
        mem_size, swap_size, _ = self.__get_memory_info()
        memory_info = ResMemoryInfo(
            mem_size=mem_size,
            swap_size=swap_size
        )
        # disk
        disk_size, disk_usage, _ = self.__get_disk_info()
        disk_info = ResDiskInfo(
            disk_size=disk_size,
            disk_usage=disk_usage
        )
        # net

        return ResPerfInfo(0,
                           host_run_time=self.__get_runtime_str(int(host_run_time)),
                           host_idle_rate=int(host_idle_time / (host_run_time * cpu_count) * 100),
                           login_user_count=login_user_count,
                           load_info=load_info,
                           proc_info=proc_info,
                           memory_info=memory_info,
                           disk_info=disk_info
                           )

    def sample_perf_data(self):
        # 1 sample data
        tm = datetime.datetime.now()
        print("D|tm", tm)
        # 1.1 summary info
        host_run_time, host_idle_time = self.__get_host_uptime()
        login_user_count = int(self.__run_shell('who | wc -l'))
        # 1.4 cpu info
        cpu_count, cpu_usage_rate = self.__get_cpu_info()
        # 1.2 load info
        loads, load_level = self.__get_load_info(cpu_count)
        # 1.3 process info
        proc_count, proc_stat_statistics, proc_user_statistics = self.__get_process_info()
        # 1.5 mem info
        mem_size, swap_size, mem_statistics = self.__get_memory_info()
        # 1.6 disk info
        disk_size, disk_usage, disk_io_rate = self.__get_disk_info()
        # 1.7 net info
        net_usage = self.__get_net_info()
        # 2 db op
        session = Session()
        # 2.1 save host_run_time
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_HOST_RUN_TIME).first()
        if item:
            item.value_int = host_run_time
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_HOST_RUN_TIME, value_int=host_run_time)
            session.add(item)
        # 2.2 save host_idle_time
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_HOST_IDLE_TIME).first()
        if item:
            item.value_int = host_idle_time
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_HOST_IDLE_TIME, value_int=host_idle_time)
            session.add(item)
        # 2.3 save login_user_count
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_LOGIN_USER_COUNT).first()
        if item:
            item.value_int = login_user_count
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_LOGIN_USER_COUNT, value_int=login_user_count)
            session.add(item)
        # 2.4 save loads
        # 2.4.2 load_level
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_LOAD_LEVE).first()
        if item:
            item.value_int = load_level
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_LOAD_LEVE, value_int=load_level)
            session.add(item)
        # 2.4.2 loads
        item = PerfLoadsHistory(date=tm, one_min=loads[0], five_min=loads[1], fiften_min=loads[2])
        session.add(item)
        # 2.5 save proc info
        # 2.5.1 proc_count
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_PROC_COUNT).first()
        if item:
            item.value_int = proc_count
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_PROC_COUNT, value_int=proc_count)
            session.add(item)
        # 2.5.2 proc_stat_statistics
        item = PerfProcStatDistributionHistory(date=tm, R=proc_stat_statistics['R'],
                                               S=proc_stat_statistics['S'],
                                               I=proc_stat_statistics['I'],
                                               Z=proc_stat_statistics['Z'],
                                               D=proc_stat_statistics['D'],
                                               T=proc_stat_statistics['T'],
                                               P=proc_stat_statistics['P'],
                                               W=proc_stat_statistics['W'],
                                               X=proc_stat_statistics['X'],
                                               H=proc_stat_statistics['<'],
                                               N=proc_stat_statistics['N'],
                                               L=proc_stat_statistics['L'],
                                               thx_father=proc_stat_statistics['s'],
                                               multi_thx=proc_stat_statistics['l'])
        session.add(item)
        # 2.5.3 proc_user_statistics
        for k in proc_user_statistics:
            item = PerfProcUserDistributionHistory(date=tm, user_name=k, proc_count=proc_user_statistics[k])
            session.add(item)
        # 2.6 save cpu_usage_rate
        # 2.6.1 cpu count
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_CPU_COUNT).first()
        if item:
            item.value_int = cpu_count
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_CPU_COUNT, value_int=cpu_count)
            session.add(item)
        # 2.6.2 cpu_usage_rate
        for k in cpu_usage_rate:
            item = PerfCpuUsageRateHistory(date=tm, cpu_name=k, use_rate=cpu_usage_rate[k])
            session.add(item)
        # 2.7 save mem info
        # 2.7.1 save mem size
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_MEMORY_SIZE).first()
        if item:
            item.value_int = mem_size
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_MEMORY_SIZE, value_int=mem_size)
            session.add(item)
        # 2.7.2 save swap size
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_SWAP_SIZE).first()
        if item:
            item.value_int = swap_size
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_SWAP_SIZE, value_int=swap_size)
            session.add(item)
        # 2.7.3 save mem_statistics
        print('D| 2.7.3 ', mem_statistics)
        item = PerfMemUsageHistory(date=tm, mem_use=mem_statistics['Mem:'][0], mem_free=mem_statistics['Mem:'][1],
                                   mem_buffer=mem_statistics['Mem:'][2], swap_use=mem_statistics['Swap:'][0],
                                   swap_free=mem_statistics['Swap:'][1])
        session.add(item)
        # 2.8 save disk_size, disk_usage, disk_io_rate
        # 2.8.1 save disk_size
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_DISK_SIZE).first()
        if item:
            item.value_int = disk_size
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_DISK_SIZE, value_int=disk_size)
            session.add(item)
        # 2.8.2 disk_usage
        item = session.query(PerfSummaryValues).filter_by(key=SUMMARY_KEY_DISK_USAGE).first()
        if item:
            item.value_str = json.dumps(disk_usage)
        else:
            item = PerfSummaryValues(key=SUMMARY_KEY_DISK_USAGE, value_str=json.dumps(disk_usage))
            session.add(item)
        # 2.8.3 disk_io_rate
        for it in disk_io_rate:
            item = PerfDiskIoRateHistory(date=tm, disk_name=it[0], read_rate=it[1][0], write_rate=it[1][1])
            session.add(item)
        # 2.9 save net_usage
        for it in net_usage:
            item = PerfNetIoRateHistory(date=tm, net_dev_name=it[0], read_rate=it[1][0], write_rate=it[1][1])
            session.add(item)
        # 2.10 save summary
        item = PerfSummaryHistory(date=tm, proc_count=proc_count, login_user_count=login_user_count)
        session.add(item)
        session.commit()

    def __get_net_info(self):
        val = self.__run_shell('ifstat')
        net_list = val.split('\n')
        net_list = net_list[3: -1]
        net_usage = []
        print("D|__get_net_info", net_list)
        for i in range(int(len(net_list) / 2)):
            if not net_list[i * 2]:
                continue
            it_info = net_list[i * 2].split(' ')
            it_info = [x for x in it_info if x != '']
            print('I|', it_info)
            net_usage.append([it_info[0], (int(it_info[5]), int(it_info[7]))])
        return net_usage

    def __get_disk_info(self):
        val = self.__run_shell('df')
        disk_list = val[val.find('\n') + 1:-1].split('\n')
        disk_usage = {}
        disk_size = 0
        for it in disk_list:
            if not it:
                continue
            it_info = it.split(' ')
            it_info = [x for x in it_info if x != '']
            print('I|', it_info)
            disk_usage[it_info[5]] = (int(it_info[2]), int(it_info[3]))
            disk_size = disk_size + int(it_info[1])

        val = self.__run_shell('iostat')
        disk_io_list = val.split('\n')
        disk_io_list = disk_io_list[6: -1]
        disk_io_rate = []
        for it in disk_io_list:
            if not it:
                continue
            it_info = it.split(' ')
            it_info = [x for x in it_info if x != '']
            print('I|', it_info)
            disk_io_rate.append([it_info[0], (float(it_info[2]), float(it_info[3]))])
        print(disk_size, disk_usage, disk_io_rate)
        return disk_size, disk_usage, disk_io_rate

    def __get_memory_info(self):
        val = self.__run_shell('free')
        mem_list = val[val.find('\n') + 1:-1].split('\n')
        mem_statistics = {}
        mem_size = 0
        swap_size = 0
        print('D| __get_memory_info ', mem_list)
        for it in mem_list:
            if not it:
                continue
            it_info = it.split(' ')
            it_info = [x for x in it_info if x != '']
            print('I|', it_info)
            if it_info[0] == 'Mem:':
                mem_size = mem_size + int(it_info[1])
                mem_statistics[it_info[0]] = (int(it_info[2]), int(it_info[3]), int(it_info[5]))
            elif it_info[0] == 'Swap:':
                swap_size = swap_size + int(it_info[1])
                mem_statistics[it_info[0]] = (int(it_info[2]), int(it_info[3]))
        return mem_size, swap_size, mem_statistics

    def __get_cpu_info(self):
        val = self.__run_shell('mpstat -P ALL')
        cpu_list = val.split('\n')
        cpu_list = cpu_list[3: -1]
        cpu_usage_rate = {}
        cpu_count = len(cpu_list)
        print("D|__get_cpu_info ",cpu_list)
        for it in cpu_list:
            if not it:
                continue
            it_info = it.split(' ')
            print('I|', it_info)
            it_info = [x for x in it_info if x != '']
            cpu_usage_rate[it_info[2]] = float(it_info[3])
        return cpu_count, cpu_usage_rate

    def __get_process_info(self):
        val = self.__run_shell('ps -uxa')
        proc_count = val.count('\n') - 1
        # 获取 user 和 stat 分类统计值
        proc_stat_statistics = {
            'R': 0, 'S': 0, 'I': 0, 'Z': 0, 'D': 0, 'T': 0, 'P': 0, 'W': 0, 'X': 0, '<': 0, 'N': 0, 'L': 0, 's': 0,
            'l': 0
        }
        proc_user_statistics = {}
        proc_list = val[val.find('\n') + 1:-1].split('\n')
        # print('I | ', proc_list)
        for it in proc_list:
            if not it:
                continue
            p_info = it.split(' ')
            # print('I|', p_info)
            p_info = [x for x in p_info if x != '']
            proc_stat_statistics[p_info[7][0]] = proc_stat_statistics[p_info[7][0]] + 1
            proc_user_statistics[p_info[0]] = proc_user_statistics.get(p_info[0], 0) + 1
        print('status:', proc_stat_statistics, '\nuser:', proc_user_statistics)

        return proc_count, proc_stat_statistics, proc_user_statistics

    def __get_load_info(self, ncpu):
        val = self.__run_shell('uptime')
        idx = val.find('load average: ')
        loads = val[idx + len('load average: '):-1].split(', ')
        print('I | ', loads)
        loads = [float(i) for i in loads]
        L1 = 1 if loads[0] < 0.7 * ncpu else 2 if 0.7 * ncpu <= loads[0] < 1 * ncpu else 3 if 1 * ncpu <= loads[
            0] < 5 * ncpu else 4
        L5 = 1 if loads[1] < 0.7 * ncpu else 2 if 0.7 * ncpu <= loads[0] < 1 * ncpu else 3 if 1 * ncpu <= loads[
            0] < 5 * ncpu else 4
        L15 = 1 if loads[2] < 0.7 * ncpu else 2 if 0.7 * ncpu <= loads[0] < 1 * ncpu else 3 if 1 * ncpu <= loads[
            0] < 5 * ncpu else 4
        return (loads[0], loads[1], loads[2]), int((L1 + L5 * 5 + L15 * 15) / 84 * 100)

    def __run_shell(self, cmd):
        out = os.popen(cmd)
        msg = ''
        for tmp in out.readlines():
            msg = msg + tmp
        return msg

    def __get_runtime_str(self, host_run_time):
        value = host_run_time
        sec = 0
        min = 0
        hour = 0
        day = 0
        year = 0

        sec = value % 60
        if value > 60:  # 秒
            value = int(value / 60)
            min = value % 60
            if value > 60:  # 分
                value = int(value / 60)
                hour = value % 24
                if value > 24:  # 时
                    value = int(value / 24)
                    day = value % 356
                    if value > 356:
                        year = int(value / 356)
        s_runtime = str(sec) + 's'
        if min > 0:
            s_runtime = str(min) + 'm'
            if hour > 0:
                s_runtime = str(hour) + 'h:' + s_runtime
                if day > 0:
                    s_runtime = str(day) + 'd:' + s_runtime
                    if year > 0:
                        s_runtime = str(year) + 'y:' + s_runtime
        return s_runtime

    def __get_host_uptime(self) -> (float, float):
        val = self.__run_shell('cat /proc/uptime')
        print('yz', val)
        s_host_run_time, s_host_idle_time = val.split(' ')
        return float(s_host_run_time), float(s_host_idle_time)

    def __get_host_idle_rate(self):
        return 60

    def get_test_perf_info(self) -> ResPerfInfo:
        perf_info = ResPerfInfo(host_run_time='13h:14m:41s', host_idle_rate=60, login_user_count=3,
                                load_info=ResLoadInfo(level=1, one_min=[150, 230, 102, 218, 567, 147, 260],
                                                      five_min=[150, 230, 102, 218, 567, 147, 260],
                                                      fiften_min=[150, 230, 102, 218, 567, 147, 260]),
                                proc_info=ResProcInfo(proc_count=20,
                                                      proc_stat_distribution=[  # 按状态分类统计进程数量历史序列
                                                          ["Stat", ["10/21 18:56", "10/21 18:57", "10/21 18:58"]],
                                                          ["T", [12, 17, 5]],
                                                          ["S", [12, 17, 5]],
                                                          ["R", [12, 17, 5]],
                                                      ],
                                                      proc_user_distribution=[  # 按用户分类统计进程数量历史序列
                                                          ["User", ["10/21 18:56", "10/21 18:57", "10/21 18:58"]],
                                                          ["root", [12, 17, 5]],
                                                          ["mysql", [12, 17, 5]]
                                                      ]),
                                cpu_info=ResCpuInfo(cpu_count=8,
                                                    cpu_usage_rate=[  # cpu使用率历史
                                                        "all", [0.54, 0.22, 0.24],
                                                        "0", [0.54, 0.22, 0.24],
                                                        "1", [0.54, 0.22, 0.24],
                                                        "2", [0.54, 0.22, 0.24],
                                                        "3", [0.54, 0.22, 0.24]
                                                    ]),
                                memory_info=ResMemoryInfo(mem_size=1020282828,
                                                          mem_usage=[[26, 91, 281], [26, 91, 281], [26, 91, 281]],
                                                          swap_size=1028848,
                                                          swap_usage=[[26, 91, 281], [26, 91, 281], [26, 91, 281]]),
                                disk_info=ResDiskInfo(disk_size=10291282,
                                                      disk_usage=[["xxx1", 2818, 909], ["xxx2", 2818, 909]],
                                                      disk_io_rate=[  # 磁盘IO速率历史
                                                          ["IoRate", ["10/21 18:56", "10/21 18:57", "10/21 18:58"]],
                                                          ["xxx1", [192, 2919, 291], [192, 2919, 291]],
                                                          ["xxx2", [192, 2919, 291], [192, 2919, 291]]
                                                      ]),
                                net_info=ResNetInfo(
                                    net_io_rate=[  # 网络IO速率历史
                                        ["IoRate", ["10/21 18:56", "10/21 18:57", "10/21 18:58"]],
                                        ["xxx1", [192, 2919, 291], [192, 2919, 291]],
                                        ["xxx2", [192, 2919, 291], [192, 2919, 291]]
                                    ])
                                )
        return ResBase(0, data=perf_info)
