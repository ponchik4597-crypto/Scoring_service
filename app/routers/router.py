import redis.asyncio as redis
from fastapi import APIRouter
from app.schemas.scoring import Score

router = APIRouter()
redis_client = redis.Redis(host='redis')


@router.post("/score", summary="Определение суммы для клиента")
async def calculate_score(data: Score):
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
