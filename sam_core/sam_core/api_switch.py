import threading


class ApiSwitch:
    __disabled_api_list = set()
    __cs_disabled_api_list = threading.Lock()

    @staticmethod
    def add_disabled_api(url: str):
        ApiSwitch.__cs_disabled_api_list.acquire()
        ApiSwitch.__disabled_api_list.add(url)
        ApiSwitch.__cs_disabled_api_list.release()

    @staticmethod
    def remove_disabled_api(url: str):
        ApiSwitch.__cs_disabled_api_list.acquire()
        ApiSwitch.__disabled_api_list.remove(url)
        ApiSwitch.__cs_disabled_api_list.release()

    @staticmethod
    def is_api_disabled(url: str) -> bool:
        print('D|url ', url)
        print('D|ApiSwitch.__disabled_api_list ', ApiSwitch.__disabled_api_list)
        return url in ApiSwitch.__disabled_api_list
