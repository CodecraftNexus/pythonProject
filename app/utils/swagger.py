from flask import send_from_directory

import os


def setup_swagger(app):
    SWAGGER_URL = '/python-swagger'
    API_URL = '/apispec.json'  # මෙක HTTP URL එකක් විදිහට තියෙන්න ඕනේ

    try:
        from flask_swagger_ui import get_swaggerui_blueprint
    except ImportError:
        app.logger.warning("flask_swagger_ui not Installed: skipping /swagger UI setup")
        return

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Simple Login Api"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    print(f"✅ Swagger UI available at: http://localhost:3000{SWAGGER_URL}")