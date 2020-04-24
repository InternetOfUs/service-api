from __future__ import absolute_import, annotations


def get_logging_configuration():
    return {
        "version": 1,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": ""
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            }
            # "file": {
            #     "class": "logging.handlers.RotatingFileHandler",
            #     "formatter": "simple",
            #     "filename": os.path.join(os.getenv("LOGS_DIR", "."), file_name),
            #     "maxBytes": 10485760,
            #     "backupCount": 3
            # }
        },
        "root": {
            "level": "DEBUG",
            # "handlers": ["console", "file"],
            "handlers": ["console"],
        },
        "loggers": {
            "uhopper.utils": {
                "level": "DEBUG",
                # "handlers": ["console", "file"],
                "handlers": ["console"],
                "propagate": 0
            },
            "wenet_service_api": {
                "level": "DEBUG",
                # "handlers": ["console", "file"],
                "handlers": ["console"],
                "propagate": 0
            }
        }
    }
