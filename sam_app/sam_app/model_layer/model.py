from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean

engine = create_engine('sqlite:///sam_app.db', echo=True)
Session = sessionmaker(bind=engine)  # create session
Base = declarative_base()


class PerfConfig(Base):
    __tablename__ = 'sam_perf_config'
    key = Column(String, primary_key=True, unique=True)
    value_bool = Column(Boolean)
    value_int = Column(Integer)
    value_float = Column(Float)
    value_str = Column(String)


SUMMARY_KEY_HOST_RUN_TIME = 'HOST_RUN_TIME'
SUMMARY_KEY_HOST_IDLE_TIME = 'HOST_IDLE_TIME'
SUMMARY_KEY_LOGIN_USER_COUNT = 'LOGIN_USER_COUNT'
SUMMARY_KEY_LOAD_LEVE = 'LOAD_LEVE'
SUMMARY_KEY_PROC_COUNT = 'PROC_COUNT'
SUMMARY_KEY_CPU_COUNT = 'CPU_COUNT'
SUMMARY_KEY_MEMORY_SIZE = 'MEMORY_SIZE'
SUMMARY_KEY_SWAP_SIZE = 'SWAP_SIZE'
SUMMARY_KEY_DISK_SIZE = 'DISK_SIZE'
SUMMARY_KEY_DISK_USAGE = 'DISK_USAGE'


class PerfSummaryValues(Base):
    __tablename__ = 'sam_perf_summary_values'
    key = Column(String, primary_key=True)
    value_int = Column(Integer)
    value_float = Column(Float)
    value_str = Column(String)
    

class PerfSummaryHistory(Base):
    __tablename__ = 'sam_perf_summary_history'
    date = Column(DateTime, primary_key=True, unique=True)
    proc_count = Column(Integer)
    login_user_count = Column(Integer)


class PerfLoadsHistory(Base):
    __tablename__ = 'sam_perf_loads_history'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    one_min = Column(Float, default=0)
    five_min = Column(Float, default=0)
    fiften_min = Column(Float, default=0)


class PerfProcStatDistributionHistory(Base):
    __tablename__ = 'sam_perf_proc_stat_history'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    R = Column(Integer, default=0)
    S = Column(Integer, default=0)
    I = Column(Integer, default=0)
    Z = Column(Integer, default=0)
    D = Column(Integer, default=0)
    T = Column(Integer, default=0)
    P = Column(Integer, default=0)
    W = Column(Integer, default=0)
    X = Column(Integer, default=0)
    H = Column(Integer, default=0)
    N = Column(Integer, default=0)
    L = Column(Integer, default=0)
    thx_father = Column(Integer, default=0)
    multi_thx = Column(Integer, default=0)


class PerfProcUserDistributionHistory(Base):
    __tablename__ = 'sam_perf_proc_user_history'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    user_name = Column(String, nullable=False)
    proc_count = Column(Integer, default=0)


class PerfCpuUsageRateHistory(Base):
    __tablename__ = 'sam_perf_cpu_usage_rate_history'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    cpu_name = Column(String, nullable=False)
    use_rate = Column(Float, default=0)


class PerfMemUsageHistory(Base):
    __tablename__ = 'sam_perf_mem_usage_history'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    mem_use = Column(Integer, default=0)
    mem_free = Column(Integer, default=0)
    mem_buffer = Column(Integer, default=0)
    swap_use = Column(Integer, default=0)
    swap_free = Column(Integer, default=0)


class PerfDiskIoRateHistory(Base):
    __tablename__ = 'sam_perf_disk_io_rate_history'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    disk_name = Column(String, nullable=False)
    read_rate = Column(Float, default=0)
    write_rate = Column(Float, default=0)


class PerfNetIoRateHistory(Base):
    __tablename__ = 'sam_perf_net_io_rate_history'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    net_dev_name = Column(String, nullable=False)
    read_rate = Column(Float, default=0)
    write_rate = Column(Float, default=0)


