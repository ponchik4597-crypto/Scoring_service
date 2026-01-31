import redis.asyncio as redis
from fastapi import APIRouter, Request, Response, Query, status
from app.schemas.scoring import Score
from prometheus_client import generate_latest, Counter, Summary

router = APIRouter()
redis_client = redis.Redis(host='redis')

REQUEST_COUNT = Counter(
    'app_request_count', 'Количество запросов к API', ['endpoint', 'status']
)

REQUEST_LATENCY = Summary(
    'app_request_latency_seconds', 'Время обработки запросов в секундах', ['endpoint', 'status']
)


@router.get("/metrics", summary="Получение метрик системы")
async def get_metrics_endpoint():
    return Response(content=generate_latest(), media_type='text/plain; charset=UTF-8')


@router.post("/score", summary="Определение суммы для клиента")
async def calculate_score(data: Score) -> dict:
    endpoint = "/score"
    try:
        response_status = status.HTTP_200_OK
        REQUEST_COUNT.labels(endpoint=endpoint, status=response_status).inc()

        with REQUEST_LATENCY.labels(endpoint=endpoint, status=response_status).time():
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

    except Exception as e:
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        REQUEST_COUNT.labels(endpoint=endpoint, status=response_status).inc()
        raise e
    finally:
        REQUEST_LATENCY.labels(endpoint=endpoint, status=response_status).observe(0)
