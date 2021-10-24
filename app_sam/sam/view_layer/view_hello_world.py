from pyramid.response import Response
from pyramid.view import view_config
from sam.view_layer.view_base import ViewBase
from sam.common.res_base import ResBase


class ResHello(ResBase):
    def __init__(self, errorCode):
        super(ResHello, self).__init__(errorCode)
        self.hello = 'Hello World'


class ViewHelloWorld(ViewBase):
    def __init__(self, request):
        super(ViewHelloWorld, self).__init__(request)

    def get_hello(self):
        return ResHello(0)