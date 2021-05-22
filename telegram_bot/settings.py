from pydantic import BaseSettings, SecretStr
from aiocache import cached, Cache
from functools import partial
from dataclasses import dataclass
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
import re


@dataclass
class RedisConfig:
    host: str
    port: str
    password: str

    def __init__(self, url) -> None:
        m = re.match(r"redis://:(.*)@(.*):(.*)", url)
        self.password, self.host, self.port = m.group(1), m.group(2), m.group(3)


class Settings(BaseSettings):
    TELEGRAM_BOT_API_KEY: str = '1879579283:AAGatRkDvH6AdO6OtcOtUl6dn-n-gV9HYUs'
    TELEGRAM_BOT_WEBHOOK_ENDPOINT: str="https://coinpush666.herokuapp.com"
    REDIS_URL: str = "redis://:pcb97fb88ac53b92fc063ce9261657c6d9409316b3b9c8b867a935b57a6f52783@ec2-54-172-142-101.compute-1.amazonaws.com:9800"
    CACHE_TTL: int = 60 * 59
    PROXY: str='http://127.0.0.1:7890'
    DEFAULT_TIMEZONE: str = "Asia/Shanghai"
    DO_RELEASE: bool = False
    DATABASE_URL: str='postgres://hkhfapkqprfffx:96bc80c555a8fe045d8eabeb039824d39a1bece7b3f4417d8e4984126f497ea0@ec2-52-0-114-209.compute-1.amazonaws.com:5432/df00t1odivmjt3'

    @property
    def is_production(self):
        return self.ENV == "production"


settings = Settings()


if settings.REDIS_URL:
    redis_config = RedisConfig(settings.REDIS_URL)
    dispatcher_storage = RedisStorage(host=redis_config.host, port=redis_config.port, password=redis_config.password)
    aio_lru_cache_partial = partial(
        cached,
        cache=Cache.REDIS,
        endpoint=redis_config.host,
        port=redis_config.port,
        password=redis_config.password
    )
    aio_lru_cache_1h = aio_lru_cache_partial(ttl=settings.CACHE_TTL)

else:
    dispatcher_storage = MemoryStorage()
    aio_lru_cache_partial = partial(cached)
    aio_lru_cache_1h = aio_lru_cache_partial(ttl=settings.CACHE_TTL)