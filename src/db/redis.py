import aioredis
from src.config import Config

token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True,
    username=Config.REDIS_USERNAME,
    password=Config.REDIS_PASSWORD
)

JTI_EXPIRY = 3600

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(jti, "", ex=JTI_EXPIRY)

async def token_in_blocklist(jti: str) -> bool:
    jti = await token_blocklist.get(jti)
    return  jti is not None