import sys
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from sam.view_layer.view_hello_world import ViewHelloWorld
from sam.view_layer.view_login import ViewLogin
from sam.view_layer.view_perf import ViewPerf
from sam.view_layer.view_exception_base import ViewExceptionBase
import sam.model_layer.model
import sam.common.util_tasks


def main():
    with Configurator() as config:
        config.add_route('hello', '/sam/api/hello')
        config.add_route('login_account', '/sam/api/login/account')
        config.add_route('login_outLogin', '/sam/api/login/outLogin')
        config.add_route('perf_info', '/sam/api/perf/info')
        config.add_route('perf_config', '/sam/api/perf/config')

        config.add_view(ViewHelloWorld, attr='get_hello', route_name='hello', request_method='GET', renderer='json')
        config.add_view(ViewLogin, attr='post_login_account', route_name='login_account', request_method='POST',
                        renderer='json')
        config.add_view(ViewLogin, attr='get_login_outLogin', route_name='login_outLogin', request_method='GET',
                        renderer='json')
        config.add_view(ViewPerf, attr='get_perf_info', route_name='perf_info', request_method='GET',
                        renderer='json')
        config.add_view(ViewPerf, attr='post_perf_config', route_name='perf_config', request_method='POST',
                        renderer='json')
        config.add_view(ViewPerf, attr='get_perf_config', route_name='perf_config', request_method='GET',
                        renderer='json')

        config.add_exception_view(ViewExceptionBase, attr='handle_exception', renderer='json')
        app = config.make_wsgi_app()
    if sys.argv[1] == 'dev':
        server = make_server('0.0.0.0', 6544, app)
    else:
        server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()


if __name__ == '__main__':
    main()
