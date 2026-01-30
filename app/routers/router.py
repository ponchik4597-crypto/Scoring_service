import redis.asyncio as redis
from fastapi import APIRouter, Request, Response, Query
from app.schemas.scoring import Score
from prometheus_client import generate_latest
from enum import Enum

from app.routers.metrics import REQUEST_COUNT, REQUEST_LATENCY


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


router = APIRouter()
redis_client = redis.Redis(host='redis')


@router.get("/metrics", summary="Получение метрик системы")
def get_metrics_endpoint():
    return Response(content=generate_latest(), media_type='text/plain; charset=UTF-8')


@router.post("/score", summary="Определение суммы для клиента")
async def calculate_score(data: Score, request: Request):
    endpoint = "/score"
    REQUEST_COUNT.labels(endpoint=endpoint).inc()

    async with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        key = str(data.model_dump())
        cached_result = await redis_client.get(key)
        if cached_result:
            return {"result": int(cached_result)}

        if len(data.loan_history) > 0:
            approved_amount = 30000
        else:
            if data.income_level > 50000:
                approved_amount = 20000
            elif data.income_level > 30000:
                approved_amount = 10000
            else:
                approved_amount = 0

        await redis_client.set(key, approved_amount, ex=300)

        return {"result": approved_amount}
