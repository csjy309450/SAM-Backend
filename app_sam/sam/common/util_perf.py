import json
import os
import datetime
from sam.common.res_obj import *
from sam.model_layer.model import *


class UtilPerfLinux:
    def get_perf_info(self) -> ResPerfInfo:
        host_run_time = None
        host_idle_time = None
        login_user_count = None
        cpu_count = None
        load_level = None
        proc_count = None
        mem_size = None
        swap_size = None
        disk_size = None
        disk_usage = []
        session = Session()
        db_item = session.query(PerfSummaryValues).all()
        print("T|db_item", db_item)
        for it in db_item:
            if it.key == SUMMARY_KEY_HOST_RUN_TIME:
                host_run_time = it.value_int
                print('T|host_run_time ', host_run_time)
            elif it.key == SUMMARY_KEY_HOST_IDLE_TIME:
                host_idle_time = it.value_int
                print('T|host_idle_time ', host_idle_time)
            elif it.key == SUMMARY_KEY_LOGIN_USER_COUNT:
                login_user_count = it.value_int
                print('T|login_user_count ', login_user_count)
            elif it.key == SUMMARY_KEY_CPU_COUNT:
                cpu_count = it.value_int
                print('T|cpu_count ', cpu_count)
            elif it.key == SUMMARY_KEY_LOAD_LEVE:
                load_level = it.value_int
                print('T|load_level ', load_level)
            elif it.key == SUMMARY_KEY_PROC_COUNT:
                proc_count = it.value_int
                print('T|proc_count ', proc_count)
            elif it.key == SUMMARY_KEY_MEMORY_SIZE:
                mem_size = it.value_int
                print('T|mem_size ', mem_size)
            elif it.key == SUMMARY_KEY_SWAP_SIZE:
                swap_size = it.value_int
                print('T|swap_size ', swap_size)
            elif it.key == SUMMARY_KEY_DISK_SIZE:
                disk_size = it.value_int
                print('T|disk_size ', disk_size)
            elif it.key == SUMMARY_KEY_DISK_USAGE:
                disk_usage = json.loads(it.value_str)
                print('T|disk_usage ', disk_usage)
        str_runtime = '' if not host_run_time else self.__get_runtime_str(int(host_run_time))
        print("T|str_runtime", str_runtime)
        host_idle_rate = None if not host_idle_time and not host_run_time else int(
            host_idle_time / (host_run_time * cpu_count) * 100)
        print("T|host_idle_rate", host_idle_rate)

        # get loads
        '''TODO [BUG] 时间获取应该是获取最近30个采样'''
        last_30_loads_date = session.query(PerfLoadsHistory.date).order_by(
            PerfLoadsHistory.date.desc()).distinct().limit(
            30).all()
        last_30_loads_date = [i[0] for i in last_30_loads_date]
        last_30_loads_date.sort()
        print('T|last_30_loads_date ', last_30_loads_date)
        last_30_loads = session.query(PerfLoadsHistory).filter(PerfLoadsHistory.date.in_(last_30_loads_date)).all()
        print('T|last_30_loads ', last_30_loads)
        date = []
        one_min = []
        five_min = []
        fiften_min = []
        for it in last_30_loads:
            date.append(it.date.strftime('%c'))
            one_min.append(it.one_min)
            five_min.append(it.five_min)
            fiften_min.append(it.fiften_min)
        one_min = [0] * (len(date) - len(one_min)) + one_min
        five_min = [0] * (len(date) - len(five_min)) + five_min
        fiften_min = [0] * (len(date) - len(fiften_min)) + fiften_min
        load_info = ResLoadInfo(
            level=load_level,
            date=date,
            one_min=one_min,
            five_min=one_min,
            fiften_min=one_min
        )

        # get process
        # last_30_proc_stat
        last_30_proc_stat_date = session.query(PerfProcStatDistributionHistory.date).order_by(
            PerfProcStatDistributionHistory.date.desc()).distinct().limit(
            30).all()
        last_30_proc_stat_date = [i[0] for i in last_30_proc_stat_date]
        last_30_proc_stat_date.sort()
        print('T|last_30_loads_date ', last_30_proc_stat_date)
        last_30_proc_stat = session.query(PerfProcStatDistributionHistory).filter(
            PerfProcStatDistributionHistory.date.in_(last_30_proc_stat_date)).all()
        print('T|last_30_proc_stat ', last_30_proc_stat)
        proc_stat_distribution = [
            ["Stat", []],
            ["T", []],
            ["S", []],
            ["I", []],
            ["Z", []],
            ["D", []],
            ["P", []],
            ["W", []],
            ["X", []],
            ["<", []],
            ["N", []],
            ["L", []],
            ["s", []],
            ["l", []]
        ]
        for it in last_30_proc_stat:
            proc_stat_distribution[0][1].append(it.date.strftime('%c'))
            proc_stat_distribution[1][1].append(it.T)
            proc_stat_distribution[2][1].append(it.S)
            proc_stat_distribution[3][1].append(it.I)
            proc_stat_distribution[4][1].append(it.Z)
            proc_stat_distribution[5][1].append(it.D)
            proc_stat_distribution[6][1].append(it.P)
            proc_stat_distribution[7][1].append(it.W)
            proc_stat_distribution[8][1].append(it.X)
            proc_stat_distribution[9][1].append(it.H)
            proc_stat_distribution[10][1].append(it.N)
            proc_stat_distribution[11][1].append(it.L)
            proc_stat_distribution[12][1].append(it.thx_father)
            proc_stat_distribution[13][1].append(it.multi_thx)
        for it in proc_stat_distribution:
            it[1] = [0] * (len(last_30_proc_stat_date) - len(it[1])) + it[1]
        # proc_user_distribution
        last_30_proc_user_date = session.query(PerfProcUserDistributionHistory.date).order_by(
            PerfProcUserDistributionHistory.date.desc()).distinct().limit(
            30).all()
        last_30_proc_user_date = [i[0] for i in last_30_proc_user_date]
        last_30_proc_user_date.sort()
        print('T|last_30_proc_user_date ', last_30_proc_user_date)
        last_30_proc_user = session.query(PerfProcUserDistributionHistory).filter(
            PerfProcStatDistributionHistory.date.in_(last_30_proc_user_date)).all()
        print('T|last_30_proc_user ', last_30_proc_user)
        proc_user_distribution = {}
        proc_user_distribution['User'] = [i.strftime('%c') for i in last_30_proc_user_date]
        for it in last_30_proc_user:
            if it.user_name not in proc_user_distribution:
                proc_user_distribution[it.user_name] = []
            proc_user_distribution[it.user_name].append(it.proc_count)
        for it in proc_user_distribution:
            proc_user_distribution[it] = [0] * (len(last_30_proc_user_date) - len(proc_user_distribution[it])) + \
                                         proc_user_distribution[it]
        proc_info = ResProcInfo(
            proc_count=proc_count,
            proc_stat_distribution=proc_stat_distribution,
            proc_user_distribution=proc_user_distribution
        )

        # cpu
        last_30_cpu_date = session.query(PerfCpuUsageRateHistory.date).order_by(
            PerfCpuUsageRateHistory.date.desc()).distinct().limit(
            30).all()
        last_30_cpu_date = [i[0] for i in last_30_cpu_date]
        last_30_cpu_date.sort()
        print('T|last_30_cpu_date ', last_30_cpu_date)
        last_30_cpu_usage = session.query(PerfCpuUsageRateHistory).filter(
            PerfCpuUsageRateHistory.date.in_(last_30_cpu_date)).all()
        print('T|last_30_cpu_usage ', last_30_cpu_usage)
        cpu_usage_rate = {}
        cpu_usage_rate['Cpu'] = [i.strftime('%c') for i in last_30_cpu_date]
        for it in last_30_cpu_usage:
            if it.cpu_name not in last_30_cpu_usage:
                cpu_usage_rate[it.cpu_name] = []
            cpu_usage_rate[it.cpu_name].append(it.use_rate)
        for it in cpu_usage_rate:
            cpu_usage_rate[it] = [0] * (len(last_30_cpu_date) - len(cpu_usage_rate[it])) + \
                                 cpu_usage_rate[it]
        cpu_info = ResCpuInfo(
            cpu_count=cpu_count,
            cpu_usage_rate=cpu_usage_rate
        )

        # mem
        last_30_mem_usage_date = session.query(PerfMemUsageHistory.date).order_by(
            PerfMemUsageHistory.date.desc()).distinct().limit(
            30).all()
        last_30_mem_usage_date = [i[0] for i in last_30_mem_usage_date]
        last_30_mem_usage_date.sort()
        print('T|last_30_mem_usage_date ', last_30_mem_usage_date)
        last_30_mem_usage = session.query(PerfMemUsageHistory).filter(
            PerfMemUsageHistory.date.in_(last_30_mem_usage_date)).all()
        print('T|last_30_mem_usage ', last_30_mem_usage)
        date = []
        mem_usage = []
        swap_usage = []
        for it in last_30_mem_usage:
            date.append(it.date.strftime('%c'))
            mem_usage.append([it.mem_use, it.mem_free, it.mem_buffer])
            swap_usage.append([it.swap_use, it.swap_free])
        memory_info = ResMemoryInfo(
            date=date,
            mem_size=mem_size,
            mem_usage=mem_usage,
            swap_size=swap_size,
            swap_usage=swap_usage
        )

        # disk
        last_30_disk_io_rate_date = session.query(PerfDiskIoRateHistory.date).order_by(
            PerfDiskIoRateHistory.date.desc()).distinct().limit(
            30).all()
        last_30_disk_io_rate_date = [i[0] for i in last_30_disk_io_rate_date]
        last_30_disk_io_rate_date.sort()
        print('T|last_30_disk_io_rate_date ', last_30_disk_io_rate_date)
        last_30_disk_io_rate = session.query(PerfDiskIoRateHistory).filter(
            PerfDiskIoRateHistory.date.in_(last_30_disk_io_rate_date)).all()
        print('T|last_30_disk_io_rate ', last_30_disk_io_rate)
        date = []
        disk_io_rate = {}
        for it in last_30_disk_io_rate:
            date.append(it.date.strftime("%c"))
            if it.disk_name not in disk_io_rate:
                disk_io_rate[it.disk_name] = []
            disk_io_rate[it.disk_name].append([it.read_rate, it.write_rate])
        for it in disk_io_rate:
            disk_io_rate[it] = [[0.0, 0.0]] * (len(date) - len(disk_io_rate[it])) + disk_io_rate[it]
        disk_io_rate['IoRate'] = date
        disk_info = ResDiskInfo(
            disk_size=disk_size,
            disk_usage=disk_usage
        )

        # net
        last_30_net_io_rate_date = session.query(PerfNetIoRateHistory.date).order_by(
            PerfNetIoRateHistory.date.desc()).distinct().limit(
            30).all()
        last_30_net_io_rate_date = [i[0] for i in last_30_net_io_rate_date]
        last_30_net_io_rate_date.sort()
        print('T|last_30_net_io_rate_date ', last_30_net_io_rate_date)
        last_30_net_io_rate = session.query(PerfNetIoRateHistory).filter(
            PerfNetIoRateHistory.date.in_(last_30_net_io_rate_date)).all()
        print('T|last_30_net_io_rate ', last_30_net_io_rate)
        date = []
        net_io_rate = {}
        for it in last_30_net_io_rate:
            date.append(it.date.strftime("%c"))
            if it.net_dev_name not in net_io_rate:
                net_io_rate[it.net_dev_name] = []
            net_io_rate[it.net_dev_name].append([it.read_rate, it.write_rate])
        for it in net_io_rate:
            net_io_rate[it] = [[0.0, 0.0]] * (len(date) - len(net_io_rate[it])) + net_io_rate[it]
        net_io_rate['IoRate'] = date
        net_info = ResNetInfo(
            net_io_rate=net_io_rate
        )

        # perf info
        perf_info = ResPerfInfo(host_run_time=str_runtime,
                                host_idle_rate=host_idle_rate,
                                login_user_count=login_user_count,
                                load_info=load_info,
                                cpu_info=cpu_info,
                                proc_info=proc_info,
                                memory_info=memory_info,
                                disk_info=disk_info,
                                net_info=net_info)
        return ResBase(0, data=perf_info)

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
        print("D|__get_cpu_info ", cpu_list)
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
            s_runtime = str(min) + 'm:' + s_runtime
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
