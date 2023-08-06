import uuid

import structlog


class CorelationMiddleWare(object):
    """
    It uses structlog to maintain request_id
    """

    CORELATED_HEADER = 'HTTP_X_CO_REQUEST_ID'

    def __init__(self, app):
        self.app = app
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(),
                structlog.processors.KeyValueRenderer(
                    key_order=["request_id", "event"]
                )
            ],
            context_class=structlog.threadlocal.wrap_dict(dict),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True
        )

    def __call__(self, environ, start_response):

        logger = structlog.getLogger()
        if self.CORELATED_HEADER in environ:
            current_request_id = environ[self.CORELATED_HEADER]

        else:
            current_request_id = uuid.uuid4()
        logger = logger.bind(request_id=current_request_id)
        return self.app(environ, start_response)
