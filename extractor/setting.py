"""Debug setting."""

from tools.setting import BaseConfig


class ProdConfig(BaseConfig):
    """Production configuration."""

    SWAGGER = {
        "swagger": "2.0",
        "info": {
            "title": "API",
            "description": "Extractor API.",
            "version": "1.0.0"
        },
        "schemes": [
            "http"
        ]
    }