from pyramid.response import Response
from pyramid.view import view_config
from sam_core.view_base import ViewBase
from sam_core.res_obj import ResBase


class ResHello(ResBase):
    def __init__(self, errorCode):
        super(ResHello, self).__init__(errorCode)
        self.hello = 'Hello World'


class ViewHelloWorld(ViewBase):
    def __init__(self, request):
        super(ViewHelloWorld, self).__init__(request)

    def get_hello(self):
        return ResHello(0)