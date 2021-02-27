from flask import Blueprint, Flask, request
from flask_ngrok import run_with_ngrok
from flask_swagger_ui import get_swaggerui_blueprint

from service.resources.api_blueprint import api_blueprint
from service.utils.date_util import DateUtil
from service.utils.aws_logger import AWSLogger
from service.utils.aws_session import AWSSession
from service.utils.aws_session_manager import AWSSessionManager

logger = AWSLogger(__name__)

def create_app(configuration=None):
    app = Flask(__name__)

    if configuration:
        app.config.from_object(configuration)
    
    # Allow trailing slashes for all rest endpoints
    app.url_map.strict_slashes = False
    app.register_blueprint(api_blueprint)

    @app.before_first_request
    def initialise_server() -> None:
        """
        Contains code that runs at the start of the server.
        """

        return

    @app.before_request
    def before_request() -> None:
        """
        Contains code to be run before each API request that comes to the server.

        :returns: None
        """
        # skip authentication and authorization for swagger APIs
        if request.endpoint not in ("api.doc"):
            # Creating the enroll session object
            create_enroll_session()

    
    @app.after_request
    def after_request(response):

        # Checking if token was refreshed
        session = AWSSessionManager().get_session()
               
        # using 1 year max-age
        response.headers["Strict-Transport-Security"] = "max-age=31536000 ; includeSubDomains"
        # Define loading policy for all resources type in case of a resource type
        # dedicated directive is not defined (fallback)
        response.headers["X-Content-Type-Options"] = "nosniff"
        # The cache should not store anything about the client request or server response.
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        # For older browsers that do not support Cache-Control.
        response.headers["Pragma"] = "no-cache"
        # Block pages from loading when they detect reflected XSS attacks:
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Define loading policy for all resources type in case of a resource type
        # dedicated directive is not defined (fallback)
        response.headers["Content-Security-Policy"] = "default-src 'none'"
        
        return response


    def create_enroll_session() -> None:
        """
        Creates and sets the session object.

        :returns: None
        """
        # Creating the enroll session object
        session = AWSSession()

        session.uri_info = str(request.url)
        session.operation = str(request.method)
        session.request_path = str(request.path)
        session.request_start_time = DateUtil.current_milli_time()

        # set the session object into session manager so that it can accessed down stream
        AWSSessionManager().set_session(session)

        return
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001, host='0.0.0.0')