import traceback
from sam.common.res_obj import ResBase, STATUS_KNOWN

class ViewExceptionBase(Exception):
    def __init__(self, request):
        super(ViewExceptionBase, self).__init__(request)

    def handle_exception(self):
        print('E |', traceback.format_exc())
        return ResBase(STATUS_KNOWN)