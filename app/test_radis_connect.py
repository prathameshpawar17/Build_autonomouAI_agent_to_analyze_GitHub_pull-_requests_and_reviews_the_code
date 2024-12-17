from .config import settings  # Import your settings
from app.db.redis import get_redis_client


def test_redis_connection():
    """
    Test the Redis connection by setting and getting a key-value pair.
    """
    redis_client = get_redis_client()
    try:
        # Set a key
        redis_client.set("test_key", "test_value")
        # Retrieve the key
        value = redis_client.get("test_key")
        assert value == "test_value", "Redis value mismatch!"
        print("Redis is working correctly!")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")

if __name__ == "__main__":
    test_redis_connection()

