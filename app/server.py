from fastapi import FastAPI

import logging.config

from app.api import router

logger = logging.getLogger(__name__)


def get_app():
    server_app = FastAPI()
    server_app.swagger_ui_parameters = {
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "deepLinking": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "docExpansion": "none",
    }

    server_app.include_router(router)

    return server_app
