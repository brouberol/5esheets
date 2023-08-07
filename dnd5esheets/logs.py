import logging.config
import sys
from collections.abc import MutableMapping

import orjson
import structlog
from asgi_correlation_id import correlation_id as ctxvar_correlation_id

from . import ExtendedFastAPI


def extract_event_dict(_, __, event_dict: MutableMapping) -> MutableMapping:
    """If the 'event' value is a JSON-encoded object, extract its key/values into the event itself"""
    try:
        event_dict = event_dict | orjson.loads(event_dict["event"])
    except ValueError:
        pass
    else:
        if "request" in event_dict:
            event_dict[
                "event"
            ] = f"{event_dict['request']['method']} {event_dict['request']['path']}"
    return event_dict


def inject_request_id(_, __, event_dict: MutableMapping) -> MutableMapping:
    if correlation_id := ctxvar_correlation_id.get(None):
        event_dict["correlation_id"] = correlation_id
    return event_dict


def cleanup_event_dict(_, __, event_dict: MutableMapping) -> MutableMapping:
    event_dict.pop("_logger", None)
    event_dict.pop("_name", None)
    return event_dict


def generate_logging_config(app: ExtendedFastAPI) -> dict:
    """Return a logging dict configuration for all application loggers"""
    processors = [
        # Inject a timestamp in the event
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f"),
        # Inject the log level in the event
        structlog.stdlib.add_log_level,
        # Inject the logger name in the event
        structlog.stdlib.add_logger_name,
        # Inject context variables in the event
        structlog.contextvars.merge_contextvars,
        # Include key/values added to the log record to the event
        structlog.stdlib.ExtraAdder(),
        # Include details about the logging call site
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.PATHNAME,
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.MODULE,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            }
        ),
        # Apply stdlib-like string formatting to the event key
        structlog.stdlib.PositionalArgumentsFormatter(),
        # Add stack information with key 'stack' if stack_info is True
        structlog.processors.StackInfoRenderer(),
        # Replace an 'exc_info' field with an 'exception' string field using
        # Python's built-in traceback formatting
    ]

    common_formatter_processors = processors + [
        extract_event_dict,
        inject_request_id,
        cleanup_event_dict,
        #  Remove '_record' and '_from_structlog' from event_dict
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]
    log_level = getattr(logging, app.settings.LOG_LEVEL)
    structlog.configure(
        processors=processors
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],  # type: ignore
        logger_factory=structlog.stdlib.LoggerFactory(),
        # This increases performance by making sure that logging with a level beneath log_level
        # does nothing at all (return None)
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )

    return {
        "version": 1,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": common_formatter_processors
                + [
                    structlog.processors.format_exc_info,
                    structlog.processors.JSONRenderer(),
                ],
                # Processors applied to non-structlog loggers
                "foreign_pre_chain": processors,
            },
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": common_formatter_processors
                + [
                    structlog.dev.ConsoleRenderer(
                        colors=True, exception_formatter=structlog.dev.rich_traceback
                    ),
                ],
                "foreign_pre_chain": processors,
            },
        },
        "handlers": {
            "console": {
                "level": app.settings.LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "json" if app.settings.LOG_FORMAT == "json" else "colored",
                "stream": sys.stdout,
            }
        },
        "loggers": {
            "root": {
                "level": app.settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.error": {
                "level": app.settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": logging.WARNING,
                "handlers": ["console"],
                "propagate": False,
            },
            "uvicorn": {
                "level": app.settings.LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": app.settings.LOG_LEVEL
                if app.settings.SQLALCHEMY_ECHO
                else logging.WARNING,
                "handlers": ["console"],
                "propagate": False,
            },
        },
    }


def setup_logging(app: ExtendedFastAPI):
    """Configure logging for the application"""
    logging.config.dictConfig(generate_logging_config(app))
    if app.settings.LOG_DEBUG:
        __import__("logging_tree").printout()
