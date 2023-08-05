from jennifer.api.format import format_function
from jennifer.agent import jennifer_agent
from jennifer.wrap.wsgi import wrap_wsgi_app

__hooking_module__ = 'flask'

def wrap_error_handler(origin):
    try:
        from werkzeug.exceptions import InternalServerError, NotFound
    except ImportError:
        InternalServerError = None
        NotFound = None

    def handler(*args, **kwargs):
        e = None
        if len(args) >= 2:
            e = args[1]
        else:
            e = kwargs.get('e')
        if e is not None:
            profiler = jennifer_agent().current_transaction().profiler
            if type(e) == InternalServerError:
                profiler.service_error(e)
            elif type(e) == NotFound:
                profiler.not_found(e)
            else:
                profiler.exception(e)
        return origin(*args, **kwargs)
    return handler

def wrap_dispatch_requet(origin, flask):
    def handler(self):
        req = flask.ctx._request_ctx_stack.top.request
        if req is not None and req.url_rule is not None:
            handler = self.view_functions.get(req.url_rule.endpoint, None)
            handler_name = format_function(handler)
            agent = jennifer_agent()
            transaction = agent.current_transaction()
            if transaction is not None and handler_name != '':
                transaction.profiler.set_root_name(handler_name)
        return origin(self)
    return handler

def hook(flask):
    flask.Flask._find_error_handler = wrap_error_handler(
        flask.Flask._find_error_handler)
    flask.Flask.wsgi_app = wrap_wsgi_app(
        flask.Flask.wsgi_app,
        'flask.Flask.wsgi_app')
    flask.Flask.dispatch_request = wrap_dispatch_requet(
        flask.Flask.dispatch_request, flask)
