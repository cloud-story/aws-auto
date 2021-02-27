import copy

from flask import Blueprint
from flask_restx import Api

from service.resources.aws.ec2.instance import ns as aws_ec2_ns
from service.utils.constants import GENERIC_ERROR_RESPONSE_TEMPLATE
from service.utils.aws_logger import AWSLogger
from service.utils.aws_session_manager import AWSSessionManager
from service.utils.exceptions import AuthenticationError, AuthorizationError, BadRequestException, MissingRequestBodyException

logger = AWSLogger(__name__)

api_blueprint = Blueprint("api", __name__)

api = Api(api_blueprint,
          version="1.0",
          title="AWS resource API manager",
          description="AWS resource API manager",
          doc="/api/v1/aws")

# Removing the default namespace.
api.namespaces.clear()

# Add namespace
api.add_namespace(aws_ec2_ns, path="/api/v1/aws/ec2")

"""Error handlers for handling exceptions"""

@api.errorhandler(AuthenticationError)
def authentication_error_handler(e):
    """Authentication error handler"""
    logger.log_warning(str(e), exc_info=True)
    return get_error_json(e.message_code, e.message, e), 401


@api.errorhandler(AuthorizationError)
def authorization_error_handler(e):
    """Authorization error handler"""
    logger.log_warning(str(e), exc_info=True)
    return get_error_json(e.message_code, e.message, str(e)), 403

@api.errorhandler(BadRequestException)
def bad_request_error_handler(e):
    """Bad request error handler"""
    return get_error_json(e.message_code, e.message, str(e)), 400

@api.errorhandler(MissingRequestBodyException)
def missing_request_body_error_handler(e):
    """Missing request body error handler"""
    return get_error_json(e.message_code, e.message, str(e)), 400


@api.errorhandler(Exception)
def exception_error_handler(e):
    """Exception error handler"""
    logger.log_exception(str(e), exc_info=True)
    return get_error_json(0, "Unable to handle Enroll request.", str(e)), 500


@api.errorhandler
def default_error_handler(e):
    """Default error handler"""
    logger.log_exception(str(e), exc_info=True)
    return get_error_json(0, "Unable to handle Enroll request.", str(e)), 500

def get_error_json(message_code, message, error, msg_detail=None):
    error_resp = copy.deepcopy(GENERIC_ERROR_RESPONSE_TEMPLATE)

    error_resp["status"]["code"] = message_code
    error_resp["status"]["message"] = message if not msg_detail else msg_detail

    return error_resp