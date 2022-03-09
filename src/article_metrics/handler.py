from datetime import timedelta
from os.path import join
from django.conf import settings
import inspect
import uuid
from article_metrics import utils
import requests, requests_cache
import logging

LOG = logging.getLogger('debugger') # ! logs to a different file at a finer level

if not settings.TESTING:
    requests_cache.install_cache(**{
        # install cache kwargs
        # - https://github.com/reclosedev/requests-cache/blob/c4b9e4d4dcad5470de4a30464a6ac8a875615ad9/requests_cache/patcher.py#L19
        # this is where 'cache_name' becomes the sqlite backend's 'db_name':
        # - https://github.com/reclosedev/requests-cache/blob/c4b9e4d4dcad5470de4a30464a6ac8a875615ad9/requests_cache/session.py#L39
        'cache_name': settings.CACHE_NAME,
        'backend': 'sqlite',
        'expire_after': timedelta(hours=24 * settings.CACHE_EXPIRY),

        # sqlite-backend kwargs
        # - https://github.com/reclosedev/requests-cache/blob/c4b9e4d4dcad5470de4a30464a6ac8a875615ad9/requests_cache/backends/sqlite.py#L20
        'fast_save': True,
    })

def clear_expired():
    requests_cache.remove_expired_responses()
    return settings.CACHE_NAME

def clear_cache():
    # completely empties the requests-cache database, probably not what you intended
    requests_cache.clear()

def opid(nom=''):
    "return a unique id to track a set of operations"
    # "pmc--2017-01-01-23-59-59--2fb4be3a-911f-4e83-a590-df8ae2c8d691"
    # "2017-01-01-23-59-59--2fb4be3a-911f-4e83-a590-df8ae2c8d691"
    return '--'.join(x for x in [nom, utils.ymdhms(), str(uuid.uuid4())] if x)

def fqfn(fn):
    mod = inspect.getmodule(fn)
    return '.'.join([mod.__name__, fn.__name__])

def writefile(xid, content, fname):
    path = join(settings.DUMP_PATH, xid)
    utils.ensure(utils.mkdirs(path), "failed to create path %s" % path)
    path = join(path, fname) # ll: /tmp/elife-metrics/pmc-asdfasdfasdf-482309849230/log
    if isinstance(content, str):
        content = content.encode('utf8')
    open(path, 'wb').write(content)
    return path

#
#
#

class NoneObj(object):
    pass

def ignore_handler(xid, err):
    "does absolutely nothing"
    pass

def logit_handler(xid, err):
    "writes a comprehensive log entry to a file"
    # err ll: {'request': <PreparedRequest [GET]>, 'response': <Response [404]>}
    payload = {
        'request': err.request.__dict__,
        'response': err.response.__dict__
    }
    fname = writefile(xid, utils.lossy_json_dumps(payload), 'log')
    body = err.response.content
    fname2 = writefile(xid, body, 'body')
    ctx = {
        'id': xid,
        'logged': [fname, fname2],
    }
    LOG.warn("non-2xx response %s" % err, extra=ctx)

def raise_handler(xid, err):
    "logs the error and then raises it again to be handled by the calling function"
    logit_handler(xid, err)
    raise err

RAISE, IGNORE, LOGIT = 'raise', 'ignore', 'log'
HANDLERS = {
    RAISE: raise_handler,
    IGNORE: ignore_handler,
    LOGIT: logit_handler
}
DEFAULT_HANDLER = raise_handler

MAX_RETRIES = 3

def requests_get(*args, **kwargs):
    xid = kwargs.pop('opid', opid())
    ctx = {
        'id': xid
    }
    handler_opts = kwargs.pop('opts', {})

    # set any defaults for requests here
    default_kwargs = {
        'timeout': (3.05, 9), # connect time out, read timeout
    }
    default_kwargs.update(kwargs)
    kwargs = default_kwargs

    try:
        # http://docs.python-requests.org/en/master/api/#request-sessions
        session = requests.Session()
        adaptor = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
        session.mount('https://', adaptor)

        resp = session.get(*args, **kwargs)
        resp.raise_for_status()
        return resp

    except requests.HTTPError as err:
        # non 2xx response
        LOG.warn("error response attempting to fetch remote resource: %s" % err, extra=ctx)

        # these can be handled by passing in an 'opts' kwarg ll:
        # {404: handler.LOGIT}
        status_code = err.response.status_code
        code = handler_opts.get(status_code)
        # supports custom handlers like {404: lambda id, err: print(id, err)}
        fn = code if callable(code) else HANDLERS.get(code, DEFAULT_HANDLER)
        fn(xid, err)

    # handle more fine-grained errors here:
    # http://docs.python-requests.org/en/master/_modules/requests/exceptions/
    # except ConnectionError as err:
    #    pass

    # captures any requests exceptions not caught above
    except requests.RequestException as err:
        # all other requests-related exceptions
        # no request or response objects available for debug
        data = err.__dict__ # urgh, objects.
        payload = {
            'id': xid,
            'dt': utils.ymdhms(),
            'error': str(err),
            'request': (data.get('request') or NoneObj()).__dict__,
            'response': (data.get('response') or NoneObj()).__dict__,
        }
        fname = writefile(xid, utils.lossy_json_dumps(payload), 'log')
        ctx['logged'] = fname
        LOG.exception("unhandled network exception fetching request: %s" % err, extra=ctx)
        raise

    except BaseException:
        LOG.exception("unhandled exception", extra=ctx)
        raise


def capture_parse_error(fn):
    """wrapper around a parse function that captures any errors to a special log for debugger.
    first argument to decorated function *must* be the data that is being parsed."""
    def wrap(data, *args, **kwargs):
        xid = opid()
        ctx = {
            'id': xid,
            'ns': fqfn(fn),
        }
        try:
            return fn(data, *args, **kwargs)

        except BaseException:
            payload = {'data': data, 'args': args, 'kwargs': kwargs}
            fname = writefile(xid, utils.lossy_json_dumps(payload), 'log')
            ctx['log'] = fname
            LOG.exception("unhandled error", extra=ctx)
            return {'bad': data}

    return wrap
