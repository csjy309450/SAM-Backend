import json
from pyramid.response import Response
from sam.view_layer.view_base import ViewBase
from sam.common.res_obj import *
from sam.common.util_perf import UtilPerfLinux


class ViewPerf(ViewBase):
    def __init__(self, request):
        super(ViewPerf, self).__init__(request)

    def get_perf_info(self):
        return UtilPerfLinux().get_test_perf_info()

    def post_perf_config(self):
        return ResBase(0)
