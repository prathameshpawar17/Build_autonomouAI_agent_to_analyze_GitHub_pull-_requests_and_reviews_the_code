from config import settings

CELERY_BROKER_URL = settings.redis_url
CELERY_RESULT_BACKEND = settings.redis_url
