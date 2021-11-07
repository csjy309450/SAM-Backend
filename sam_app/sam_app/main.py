import sys
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from sam_app.view_layer.view_hello_world import ViewHelloWorld
from sam_app.view_layer.view_login import ViewLogin
from sam_app.view_layer.view_perf import ViewPerf
import sam_app.view_layer.view_exp_unkown as view_exp_unkown
import sam_app.view_layer.view_exp_api_disabled as view_exp_api_disabled
from sam_core.global_ctl import GlobalCtl
from sam_core.api_switch import ApiSwitch


def main():
    with Configurator() as config:
        with config.route_prefix_context('/sam/api'):
            config.add_route('hello', '/hello')
            config.add_route('login_account', '/login/account')
            config.add_route('login_outLogin', '/login/outLogin')
            config.add_route('perf_info', '/perf/info')
            config.add_route('perf_config', '/perf/config')

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

        config.add_exception_view(view=view_exp_unkown.handle_exception,
                                  context=view_exp_unkown.ViewUnkownException, renderer='json')
        config.add_exception_view(view=view_exp_api_disabled.handle_exception,
                                  context=view_exp_api_disabled.ViewApiDisabledException, renderer='json')
        app = config.make_wsgi_app()
    if sys.argv[1] == 'dev':
        server = make_server('0.0.0.0', 6544, app)
        ApiSwitch.add_disabled_api('/sam/api/hello')
        # ApiSwitch.remove_disabled_api('/sam/api/hello')
    else:
        server = make_server('0.0.0.0', 6543, app)
    GlobalCtl.init()
    server.serve_forever()


if __name__ == '__main__':
    main()
