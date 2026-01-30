from prometheus_client import Counter, Summary

REQUEST_COUNT = Counter(
    'app_request_count', 'Количество запросов к API', ['endpoint']
)

REQUEST_LATENCY = Summary(
    'app_request_latency_seconds', 'Время обработки запросов в секундах', ['endpoint']
)
