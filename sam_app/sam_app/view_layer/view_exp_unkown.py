import traceback
from sam_core.res_obj import ResBase, STATUS_KNOWN


class ViewUnkownException(Exception):
    def __init__(self, data=None):
        self.data = data


def handle_exception(context, request):
    return ResBase(STATUS_KNOWN)
