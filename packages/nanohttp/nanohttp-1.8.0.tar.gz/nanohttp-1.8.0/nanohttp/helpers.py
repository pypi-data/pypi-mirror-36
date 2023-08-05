
import cgi
import ujson
import threading
from os.path import isdir, join

import pymlconf

from .configuration import settings, configure
from . import exceptions


class LazyAttribute:
    """ ``LazyAttribute`` decorator is intended to promote a
        function call to object attribute. This means the
        function is called once and replaced with
        returned value.

        >>> class A:
        ...     def __init__(self):
        ...         self.counter = 0
        ...     @LazyAttribute
        ...     def count(self):
        ...         self.counter += 1
        ...         return self.counter
        >>> a = A()
        >>> a.count
        1
        >>> a.count
        1
    """
    __slots__ = ('f', )

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, t=None):
        f = self.f
        if obj is None:
            return f
        val = f(obj)
        setattr(obj, f.__name__, val)
        return val


def load_controller_from_file(specifier):
    from importlib.util import spec_from_file_location, module_from_spec
    controller = None

    if specifier:
        module_name, class_name = specifier.split(':') \
            if ':' in specifier else (specifier, 'Root')

        if module_name:

            if isdir(module_name):
                location = join(module_name, '__init__.py')
            elif module_name.endswith('.py'):
                location = module_name
                module_name = module_name[:-3]
            else:
                location = '%s.py' % module_name

            spec = spec_from_file_location(module_name, location=location)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            controller = getattr(module, class_name)()

        elif class_name == 'Static':
            from .controllers import Static
            controller = Static()
        else:  # pragma: no cover
            controller = globals()[class_name]()

    return controller


def quickstart(controller=None, application=None, host='localhost', port=8080,
               block=True, config=None):
    from wsgiref.simple_server import make_server

    try:
        settings.debug
    except pymlconf.ConfigurationNotInitializedError:
        configure()

    if config:
        settings.merge(config)

    if application is not None:
        app = application
    elif controller is None:
        from wsgiref.simple_server import demo_app
        app = demo_app
    else:
        from nanohttp.application import Application
        app = Application(root=controller)

    port = int(port)
    httpd = make_server(host, port, app)

    print("Serving http://%s:%d" % (host or 'localhost', port))
    if block:  # pragma: no cover
        httpd.serve_forever()
    else:
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()

        def shutdown():
            httpd.shutdown()
            httpd.server_close()
            t.join()

        return shutdown


def get_cgi_field_value(field):
    # noinspection PyProtectedMember
    return field.value if isinstance(field, cgi.MiniFieldStorage) \
        or (isinstance(field, cgi.FieldStorage) and not field._binary_file) \
        else field


def parse_any_form(environ, content_length=None, content_type=None):

    if content_length and content_type == 'application/json':
        fp = environ['wsgi.input']
        data = fp.read(content_length)
        try:
            return ujson.decode(data)
        except ValueError:
            raise exceptions.HTTPBadRequest('Cannot parse the request')

    try:
        storage = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=environ,
            strict_parsing=False,
            keep_blank_values=True
        )
    except TypeError:
        raise exceptions.HTTPBadRequest('Cannot parse the request.')

    result = {}
    if storage.list is None or not len(storage.list):
        return result

    for k in storage:
        v = storage[k]

        if isinstance(v, list):
            result[k] = [get_cgi_field_value(i) for i in v]
        else:
            result[k] = get_cgi_field_value(v)

    return result
