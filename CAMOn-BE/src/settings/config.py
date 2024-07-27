# import logging
# import sys
# # from dotenv import dotenv_values, find_dotenv
# from loguru import logger

# from src.settings.logging_config import InterceptHandler
# # # load config from .env file
# # config = dotenv_values(find_dotenv())

# # DEBUG = bool(config.get("DEBUG", "False") if config.get("DEBUG", "") in ["True", "true", "1"] else False)

# MESSAGE_QUEUE = []

# # APPLICATION = {
# #     "version": config.get("VERSION", "1.0.0"),
# #     "project_name": config.get("PROJECT_NAME"),
# #     "debug": DEBUG,
# #     "server_host": config.get("SERVER_HOST", "0.0.0.0"),
# #     "server_port": config.get("SERVER_PORT", "8000"),
# #     "redis_host": config.get("REDIS_HOST", "localhost"),
# #     "redis_port": config.get("REDIS_PORT", "6379"),
# #     "redis_db": config.get("REDIS_DB", "0"),
# #     "redis_password": config.get("REDIS_PASSWORD", ""),
# #     "celery_app_name": config.get("CELERY_APP_NAME", "app"),
# #     "celery_service_worker_username": config.get("CELERY_SERVICE_WORKER_USERNAME", "guest"),
# #     "celery_service_worker_password": config.get("CELERY_SERVICE_WORKER_PASSWORD", "guest"),
# #     "celery_service_worker_host": config.get("CELERY_SERVICE_WORKER_HOST", "localhost"),
# #     "celery_service_worker_port": config.get("CELERY_SERVICE_WORKER_PORT", "5672"),
# #     "celery_task_timeout": config.get("CELERY_TASK_TIMEOUT", "600"),
# #     "host_db": config.get("HOST_DB"),
# #     "port_db": config.get("PORT_DB"),
# #     "username_db": config.get("USERNAME_DB"),
# #     "password_db": config.get("PASSWORD_DB"),
# #     "database": config.get("DATABASE"),
# #     "access_token_secret_key": config.get("ACCESS_TOKEN_SECRET_KEY"),
# #     "algorithm": config.get("ALGORITHM"),
# #     "access_token_expire_minutes": config.get("ACCESS_TOKEN_EXPIRE_MINUTES"),
# #     "refresh_token_secret_key": config.get("REFRESH_TOKEN_SECRET_KEY"),
# #     "refresh_token_expire_minutes": config.get("REFRESH_TOKEN_EXPIRE_MINUTES"),
# #     "minio_end_point": config.get("MINIO_END_POINT"),
# #     "minio_access_key_id": config.get("MINIO_ACCESS_KEY_ID"),
# #     "minio_secret_access_key": config.get("MINIO_SECRET_ACCESS_KEY"),
# #     "minio_bucket_name": config.get("MINIO_BUCKET_NAME"),
# #     "minio_secure": config.get("MINIO_SECURE"),
# #     "mailchimp_api_key": config.get("MAILCHIMP_API_KEY"),
# #     "mailchimp_audience_id": config.get("MAILCHIMP_AUDIENCE_ID"),
# # }

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# # logging configuration
# LOGGING_LEVEL = logging.DEBUG if APPLICATION["debug"] else logging.INFO
# LOGGERS = ("hypercorn.asgi", "hypercorn.access")  # noqa
# logger.level("CUSTOM", no=15, color="<blue>", icon="@")
# logger.level("SERVICE", no=200)

# logging.getLogger().handlers = [InterceptHandler()]

# if APPLICATION["debug"]:
#     logger.configure(
#         handlers=[
#             {"sink": sys.stderr, "level": LOGGING_LEVEL},
#             {
#                 "sink": sys.stderr,
#                 "level": 200,
#                 "format": "<blue>{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}</blue>",
#             },
#         ]
#     )
# else:
#     logger.configure(
#         handlers=[
#             {
#                 "sink": sys.stderr,
#                 "level": 200,
#                 "format": "<blue>{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}</blue>",
#             },
#         ]
#     )

# logger.add("./logs/app.log", rotation='10 MB')
