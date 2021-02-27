"""
Common logger class for logging messages
"""

import json
import logging
import sys
import traceback
from service.utils.aws_session_manager import AWSSessionManager
from service.utils.date_util import DateUtil


class AWSLogger:
    """
    Usage:
    # import aws logger
        from utils.enroll_logger import AWSLogger

    # Get the instance of enroll logger
        logger = AWSLogger(__name__)

    # Log the message
        logger.log_info("Processing Heartbeat request")
    """

    def __init__(self, name):
        self.logger = self.get_logger(name)
        self.log_source = None
        self.json_enabled = True

    def get_logger(self, logger_name=None, logger_level=logging.DEBUG):
        logger = None
        try:
            logging.basicConfig(
                format="%(message)s", level=logging.INFO,)

            if logger_name is None:
                logger_name = "__AWS_API_Service__"
            logger = logging.getLogger(logger_name)
            logger.setLevel(logger_level)
            logger.setFormatter(logging.Formatter(
                fmt="%(message)s"))

        except:
            pass
        return logger

    def msg_to_log(self, attributes, msg):
        if self.json_enabled:
            return json.dumps(attributes)
        else:
            return "[" + self.log_source + "]" + msg

    def log_info(self, msg, **kwargs):
        attributes = self.get_logging_attributes("INFO", **kwargs)
        attributes["message_details"] = msg
        self.logger.info(self.msg_to_log(attributes, msg))

    def log_error(self, err_msg, **kwargs):
        attributes = self.get_logging_attributes("ERROR", **kwargs)
        attributes["message_details"] = err_msg
        self.logger.error(self.msg_to_log(attributes, err_msg))

    def log_exception(self, exc_msg, **kwargs):
        attributes = self.get_logging_attributes("ERROR", **kwargs)
        attributes["message_details"] = exc_msg
        exc_info = kwargs.get("exc_info", False)
        if exc_info is True:
            type_, value_, traceback_ = sys.exc_info()
            attributes["exception"] = "".join(traceback.format_exception(
                type_, value_, traceback_))
        self.logger.error(self.msg_to_log(attributes, exc_msg))

    def log_warning(self, msg, **kwargs):
        attributes = self.get_logging_attributes("WARNING", **kwargs)
        attributes["message_details"] = msg
        exc_info = kwargs.get("exc_info", False)
        if exc_info is True:
            type_, value_, traceback_ = sys.exc_info()
            attributes["exception"] = "".join(traceback.format_exception(
                type_, value_, traceback_))
        self.logger.warning(self.msg_to_log(attributes, msg))

    def log_debug(self, msg, **kwargs):
        attributes = self.get_logging_attributes("DEBUG", **kwargs)
        if attributes.get("debug"):
            attributes["message_details"] = msg
            self.logger.debug(self.msg_to_log(attributes, msg))

    def log_critical(self, msg, **kwargs):
        attributes = self.get_logging_attributes("CRITICAL", **kwargs)
        attributes["message_details"] = msg
        self.logger.critical(self.msg_to_log(attributes, msg))

    def get_logging_attributes(self, level, **kwargs):
        attributes = {}
        sm = AWSSessionManager()
        sess = sm.get_session()

        attributes["component_id"] = "AWS-api-service"
        attributes["log_level"] = level
        attributes["timestamp"] = DateUtil.get_current_datetime()

        fn, lno, func = self.logger.findCaller(False)[0:3]
        self.log_source = fn + ":" + str(lno) + " - " + func
        attributes["filename"] = fn
        attributes["method"] = func
        attributes["line_number"] = str(lno)

        start_time = kwargs.get("start_time", None)
        if start_time:
            elapsed_time = DateUtil.current_milli_time() - start_time
            attributes["response_time"] = elapsed_time
            attributes["perf"] = True

        additional_info = kwargs.get("additional_info", None)
        if additional_info:
            attributes["additional_info"] = additional_info

        if sess:
            if sess.get_session_id():
                attributes["transaction_id"] = sess.get_session_id()
            if sess.get_operation():
                attributes["operation"] = sess.get_operation()
            if sess.get_uri_info():
                attributes["uri_info"] = sess.get_uri_info()

        return attributes
