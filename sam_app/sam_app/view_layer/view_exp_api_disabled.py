import traceback
from sam_core.res_obj import ResBase, STATUS_API_DISABLED


class ViewApiDisabledException(Exception):
    def __init__(self, data=None):
        self.data = data


def handle_exception(context, request):
    return ResBase(STATUS_API_DISABLED)
