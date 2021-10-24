import json
from pyramid.response import Response
from sam.view_layer.view_base import ViewBase
from sam.common.res_base import ResBase


class ResLogin(ResBase):
    def __init__(self, errorCode, status, type, currentAuthority):
        super(ResLogin, self).__init__(errorCode)
        self.status = status
        self.type = type
        self.currentAuthority = currentAuthority


class ViewLogin(ViewBase):
    def __init__(self, request):
        super(ViewLogin, self).__init__(request)

    def post_login_account(self):
        print(self.req)
        return ResLogin(0, "0", "0", "111111111111111111")

    def get_login_outLogin(self):
        return ResBase(0)
