from sam_core.api_switch import ApiSwitch
from sam_app.view_layer.view_exp_api_disabled import ViewApiDisabledException


class ViewBase:
    def __init__(self, request):
        print('I|in ViewBase')
        self.req = request
        self.__is_available()

    def __is_available(self):
        if ApiSwitch.is_api_disabled(self.req.path):
            raise ViewApiDisabledException()
