import os
import sys
import linecache
import logging

from datetime import datetime
from collections import Mapping, Sequence

from ._compat import urlparse, text_type, implements_str


epoch = datetime(1970, 1, 1)


# The logger is created here but initializde in the debug support module
logger = logging.getLogger("sentry_sdk.errors")


def to_timestamp(value):
    return (value - epoch).total_seconds()


class EventHint(object):
    """Extra information for an event that can be used during processing."""

    def __init__(self, exc_info=None):
        self.exc_info = exc_info

    @classmethod
    def with_exc_info(cls, exc_info=None):
        """Creates a hint with the exc info filled in."""
        if exc_info is None:
            exc_info = sys.exc_info()
        else:
            exc_info = exc_info_from_error(exc_info)
        if exc_info[0] is None:
            exc_info = None
        return cls(exc_info=exc_info)


class BadDsn(ValueError):
    """Raised on invalid DSNs."""


@implements_str
class Dsn(object):
    """Represents a DSN."""

    def __init__(self, value):
        if isinstance(value, Dsn):
            self.__dict__ = dict(value.__dict__)
            return
        parts = urlparse.urlsplit(text_type(value))
        if parts.scheme not in (u"http", u"https"):
            raise BadDsn("Unsupported scheme %r" % parts.scheme)
        self.scheme = parts.scheme
        self.host = parts.hostname
        self.port = parts.port
        if self.port is None:
            self.port = self.scheme == "https" and 443 or 80
        self.public_key = parts.username
        if not self.public_key:
            raise BadDsn("Missig public key")
        self.secret_key = parts.password
        if not parts.path:
            raise BadDsn("Missing project ID in DSN")
        try:
            self.project_id = text_type(int(parts.path[1:]))
        except (ValueError, TypeError):
            raise BadDsn("Invalid project in DSN (%r)" % (parts.path or "")[1:])

    @property
    def netloc(self):
        """The netloc part of a DSN."""
        rv = self.host
        if (self.scheme, self.port) not in (("http", 80), ("https", 443)):
            rv = "%s:%s" % (rv, self.port)
        return rv

    def to_auth(self, client=None):
        """Returns the auth info object for this dsn."""
        return Auth(
            scheme=self.scheme,
            host=self.netloc,
            project_id=self.project_id,
            public_key=self.public_key,
            secret_key=self.secret_key,
            client=client,
        )

    def __str__(self):
        return "%s://%s%s@%s/%s" % (
            self.scheme,
            self.public_key,
            self.secret_key and "@" + self.secret_key or "",
            self.netloc,
            self.project_id,
        )


class Auth(object):
    """Helper object that represents the auth info."""

    def __init__(
        self,
        scheme,
        host,
        project_id,
        public_key,
        secret_key=None,
        version=7,
        client=None,
    ):
        self.scheme = scheme
        self.host = host
        self.project_id = project_id
        self.public_key = public_key
        self.secret_key = secret_key
        self.version = version
        self.client = client

    @property
    def store_api_url(self):
        """Returns the API url for storing events."""
        return "%s://%s/api/%s/store/" % (self.scheme, self.host, self.project_id)

    def to_header(self, timestamp=None):
        """Returns the auth header a string."""
        rv = [("sentry_key", self.public_key), ("sentry_version", self.version)]
        if timestamp is not None:
            rv.append(("sentry_timestamp", str(to_timestamp(timestamp))))
        if self.client is not None:
            rv.append(("sentry_client", self.client))
        if self.secret_key is not None:
            rv.append(("sentry_secret", self.secret_key))
        return u"Sentry " + u", ".join("%s=%s" % (key, value) for key, value in rv)


def get_type_name(cls):
    return getattr(cls, "__qualname__", None) or getattr(cls, "__name__", None)


def get_type_module(cls):
    mod = getattr(cls, "__module__", None)
    if mod not in (None, "builtins", "__builtins__"):
        return mod


def iter_stacks(tb):
    while tb is not None:
        skip = False
        for flag_name in "__traceback_hide__", "__tracebackhide__":
            try:
                if tb.tb_frame.f_locals[flag_name]:
                    skip = True
            except Exception:
                pass

        if not skip:
            yield tb
        tb = tb.tb_next


def slim_string(value, length=512):
    if not value:
        return value
    if len(value) > length:
        return value[: length - 3] + "..."
    return value[:length]


def get_lines_from_file(filename, lineno, loader=None, module=None):
    context_lines = 5
    source = None
    if loader is not None and hasattr(loader, "get_source"):
        try:
            source = loader.get_source(module)
        except (ImportError, IOError):
            source = None
        if source is not None:
            source = source.splitlines()

    if source is None:
        try:
            source = linecache.getlines(filename)
        except (OSError, IOError):
            return None, None, None

    if not source:
        return None, None, None

    lower_bound = max(0, lineno - context_lines)
    upper_bound = min(lineno + 1 + context_lines, len(source))

    try:
        pre_context = [
            slim_string(line.strip("\r\n")) for line in source[lower_bound:lineno]
        ]
        context_line = slim_string(source[lineno].strip("\r\n"))
        post_context = [
            slim_string(line.strip("\r\n"))
            for line in source[(lineno + 1) : upper_bound]
        ]
        return pre_context, context_line, post_context
    except IndexError:
        # the file may have changed since it was loaded into memory
        return [], None, []


def get_source_context(frame, tb_lineno):
    try:
        abs_path = frame.f_code.co_filename
    except Exception:
        abs_path = None
    try:
        module = frame.f_globals["__name__"]
    except Exception:
        return [], None, []
    try:
        loader = frame.f_globals["__loader__"]
    except Exception:
        loader = None
    lineno = tb_lineno - 1
    if lineno is not None and abs_path:
        return get_lines_from_file(abs_path, lineno, loader, module)
    return [], None, []


def skip_internal_frames(frame):
    tb = frame
    while tb is not None:
        try:
            mod = tb.tb_frame.f_globals["__name__"]
            if not mod.startswith("sentry_sdk."):
                break
        except (AttributeError, KeyError):
            pass
        tb = tb.tb_next
    return tb


def safe_str(value):
    try:
        return text_type(value)
    except Exception:
        return safe_repr(value)


def safe_repr(value):
    try:
        rv = repr(value)
        if isinstance(rv, bytes):
            rv = rv.decode("utf-8", "replace")
        try:
            return rv.encode("utf-8").decode("unicode-escape")
        except Exception:
            return rv
    except Exception:
        return u"<broken repr>"


def object_to_json(obj):
    def _walk(obj, depth):
        if depth < 4:
            if isinstance(obj, Sequence) and not isinstance(obj, (bytes, text_type)):
                return [_walk(x, depth + 1) for x in obj]
            if isinstance(obj, Mapping):
                return {safe_str(k): _walk(v, depth + 1) for k, v in obj.items()}
        return safe_repr(obj)

    return _walk(obj, 0)


def extract_locals(frame):
    rv = {}
    for key, value in frame.f_locals.items():
        rv[key] = object_to_json(value)
    return rv


def frame_from_traceback(tb, with_locals=True):
    frame = tb.tb_frame
    f_code = getattr(frame, "f_code", None)
    if f_code:
        abs_path = frame.f_code.co_filename
        function = frame.f_code.co_name
    else:
        abs_path = None
        function = None
    try:
        module = frame.f_globals["__name__"]
    except Exception:
        module = None

    pre_context, context_line, post_context = get_source_context(frame, tb.tb_lineno)

    rv = {
        "filename": abs_path and os.path.basename(abs_path) or None,
        "abs_path": abs_path,
        "function": function or "<unknown>",
        "module": module,
        "lineno": tb.tb_lineno,
        "pre_context": pre_context,
        "context_line": context_line,
        "post_context": post_context,
    }
    if with_locals:
        rv["vars"] = extract_locals(frame)
    return rv


def stacktrace_from_traceback(tb, with_locals=True):
    return {"frames": [frame_from_traceback(tb, with_locals) for tb in iter_stacks(tb)]}


def single_exception_from_error_tuple(exc_type, exc_value, tb, with_locals=True):
    return {
        "module": get_type_module(exc_type),
        "type": get_type_name(exc_type),
        "value": safe_str(exc_value),
        "stacktrace": stacktrace_from_traceback(tb, with_locals),
    }


def exceptions_from_error_tuple(exc_info, with_locals=True):
    exc_type, exc_value, tb = exc_info
    rv = []
    while exc_type is not None:
        rv.append(
            single_exception_from_error_tuple(exc_type, exc_value, tb, with_locals)
        )
        cause = getattr(exc_value, "__cause__", None)
        if cause is None:
            break
        exc_type = type(cause)
        exc_value = cause
        tb = getattr(cause, "__traceback__", None)
    return rv


def to_string(value):
    try:
        return text_type(value)
    except UnicodeDecodeError:
        return repr(value)[1:-1]


def iter_event_frames(event):
    stacktraces = []
    if "stacktrace" in event:
        stacktraces.append(event["stacktrace"])
    if "exception" in event:
        for exception in event["exception"].get("values") or ():
            if "stacktrace" in exception:
                stacktraces.append(exception["stacktrace"])
    for stacktrace in stacktraces:
        for frame in stacktrace.get("frames") or ():
            yield frame


def handle_in_app(event, in_app_exclude=None, in_app_include=None):
    any_in_app = False
    for frame in iter_event_frames(event):
        in_app = frame.get("in_app")
        if in_app is not None:
            if in_app:
                any_in_app = True
            continue

        module = frame.get("module")
        if not module:
            continue

        if _module_in_set(module, in_app_exclude):
            frame["in_app"] = False
        if _module_in_set(module, in_app_include):
            frame["in_app"] = True
            any_in_app = True

    if not any_in_app:
        for frame in iter_event_frames(event):
            frame["in_app"] = True

    return event


def exc_info_from_error(error):
    if isinstance(error, tuple) and len(error) == 3:
        exc_type, exc_value, tb = error
    else:
        tb = getattr(error, "__traceback__", None)
        if tb is not None:
            exc_type = type(error)
            exc_value = error
        else:
            exc_type, exc_value, tb = sys.exc_info()
            if exc_value is not error:
                tb = None
                exc_value = error
                exc_type = type(error)

    if tb is not None:
        tb = skip_internal_frames(tb)

    return exc_type, exc_value, tb


def event_from_exception(exc_info, with_locals=False, processors=None):
    exc_info = exc_info_from_error(exc_info)
    hint = EventHint.with_exc_info(exc_info)
    return (
        {
            "level": "error",
            "exception": {"values": exceptions_from_error_tuple(exc_info, with_locals)},
        },
        hint,
    )


def _module_in_set(name, set):
    if not set:
        return False
    for item in set or ():
        if item == name or name.startswith(item + "."):
            return True
    return False


class AnnotatedValue(object):
    def __init__(self, value, metadata):
        self.value = value
        self.metadata = metadata


def flatten_metadata(obj):
    def inner(obj):
        if isinstance(obj, Mapping):
            rv = {}
            meta = {}
            for k, v in obj.items():
                # if we actually have "" keys in our data, throw them away. It's
                # unclear how we would tell them apart from metadata
                if k == "":
                    continue

                rv[k], meta[k] = inner(v)
                if meta[k] is None:
                    del meta[k]
                if rv[k] is None:
                    del rv[k]
            return rv, (meta or None)
        if isinstance(obj, Sequence) and not isinstance(obj, (text_type, bytes)):
            rv = []
            meta = {}
            for i, v in enumerate(obj):
                new_v, meta[i] = inner(v)
                rv.append(new_v)
                if meta[i] is None:
                    del meta[i]
            return rv, (meta or None)
        if isinstance(obj, AnnotatedValue):
            return obj.value, {"": obj.metadata}
        return obj, None

    obj, meta = inner(obj)
    if meta is not None:
        obj[""] = meta
    return obj


def strip_event(event):
    old_frames = event.get("stacktrace", {}).get("frames", None)
    if old_frames:
        event["stacktrace"]["frames"] = [strip_frame(frame) for frame in old_frames]

    old_request_data = event.get("request", {}).get("data", None)
    if old_request_data:
        event["request"]["data"] = strip_databag(old_request_data)

    return event


def strip_frame(frame):
    if "vars" in frame:
        frame["vars"] = strip_databag(frame["vars"])
    return frame


def convert_types(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(obj, Mapping):
        return {k: convert_types(v) for k, v in obj.items()}
    if isinstance(obj, Sequence) and not isinstance(obj, (text_type, bytes)):
        return [convert_types(v) for v in obj]
    return obj


def strip_databag(obj, remaining_depth=20):
    assert not isinstance(obj, bytes), "bytes should have been normalized before"
    if remaining_depth <= 0:
        return AnnotatedValue(None, {"rem": [["!limit", "x"]]})
    if isinstance(obj, text_type):
        return strip_string(obj)
    if isinstance(obj, Mapping):
        return {k: strip_databag(v, remaining_depth - 1) for k, v in obj.items()}
    if isinstance(obj, Sequence):
        return [strip_databag(v, remaining_depth - 1) for v in obj]
    return obj


def strip_string(value, assume_length=None, max_length=512):
    # TODO: read max_length from config
    if not value:
        return value
    if assume_length is None:
        assume_length = len(value)

    if assume_length > max_length:
        return AnnotatedValue(
            value=value[: max_length - 3] + u"...",
            metadata={
                "len": assume_length,
                "rem": [["!limit", "x", max_length - 3, max_length]],
            },
        )
    return value[:max_length]


try:
    from contextvars import ContextVar
except ImportError:
    from threading import local

    class ContextVar(object):
        # Super-limited impl of ContextVar

        def __init__(self, name):
            self._name = name
            self._local = local()

        def get(self, default):
            return getattr(self._local, "value", default)

        def set(self, value):
            setattr(self._local, "value", value)
