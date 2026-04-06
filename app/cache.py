import redis
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_EXPIRY = 3600  # 1 hour

def get_redis_client():
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
        client.ping()
        return client
    except:
        return None

def generate_cache_key(complaint_text: str, image_path: str) -> str:
    content = f"{complaint_text}_{image_path}"
    return hashlib.md5(content.encode()).hexdigest()

def get_cached_response(complaint_text: str, image_path: str) -> str:
    client = get_redis_client()
    if not client:
        return None
    
    cache_key = generate_cache_key(complaint_text, image_path)
    cached = client.get(cache_key)
    
    if cached:
        print("Cache HIT - returning cached response")
        return json.loads(cached)
    
    print("Cache MISS - calling OpenAI")
    return None

def set_cached_response(complaint_text: str, image_path: str, response: str):
    client = get_redis_client()
    if not client:
        return
    
    cache_key = generate_cache_key(complaint_text, image_path)
    client.setex(
        cache_key,
        CACHE_EXPIRY,
        json.dumps(response)
    )
    print(f"Response cached for {CACHE_EXPIRY} seconds")