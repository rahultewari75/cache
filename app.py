from fastapi import FastAPI, HTTPException
from models import (
    CacheConfigureRequest, KeyValueRequest, KeyRequest,
    ExpirationRequest, QueueEnqueueRequest, QueueKeyRequest
)
from server.server import (
    # Cache operations
    ping, configure_cache, reset_cache, set_cache, get_cache,
    get_cache_ttl, set_cache_expiration, scan_cache,
    # Counter operations
    configure_counter, set_counter, get_counter,
    increment_counter, decrement_counter,
    # Queue operations
    configure_queue, set_queue, get_queue,
    enqueue, dequeue
)
from server.error import (
    CacheAlreadyConfiguredError, InvalidInputError,
    KeyNotFoundError, KeyExpiredError
)

app = FastAPI(title="Wish.com Redis Clone", version="1.0.0")

# Health check
@app.get("/ping")
async def health_check():
    """Health check endpoint"""
    message = ping()
    return {"message": message}

# Cache endpoints
@app.put("/cache/configure")
async def configure_cache_endpoint(request: CacheConfigureRequest):
    try:
        configure_cache(request.policy, request.capacity)
        return {"message": "Cache configured successfully"}
    except CacheAlreadyConfiguredError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/cache/set")
async def set_cache_endpoint(request: KeyValueRequest):
    try:
        set_cache(request.key, request.value, request.ttl)
        return {"message": "Value set successfully"}
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cache/get")
async def get_cache_endpoint(request: KeyRequest):
    try:
        value = get_cache(request.key)
        return {"value": value}
    except (KeyNotFoundError, KeyExpiredError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cache/ttl")
async def get_cache_ttl_endpoint(request: KeyRequest):
    try:
        ttl = get_cache_ttl(request.key)
        return {"ttl": ttl}
    except (KeyNotFoundError, KeyExpiredError) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/cache/expire")
async def set_cache_expiration_endpoint(request: ExpirationRequest):
    try:
        timestamp = request.expiry.timestamp()
        set_cache_expiration(request.key, timestamp)
        return {"message": "Expiration set successfully"}
    except KeyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cache/scan")
async def scan_cache_endpoint():
    try:
        keys = scan_cache()
        return {"keys": keys}
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Counter endpoints
@app.put("/counter/configure")
async def configure_counter_endpoint():
    try:
        configure_counter()
        return {"message": "Counter configured successfully"}
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/counter/set")
async def set_counter_endpoint(request: KeyRequest):
    try:
        set_counter(request.key)
        return {"message": "Counter set successfully"}
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/counter/get")
async def get_counter_endpoint(request: KeyRequest):
    try:
        value = get_counter(request.key)
        return {"value": value}
    except KeyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/counter/inc")
async def increment_counter_endpoint(request: KeyRequest):
    try:
        value = increment_counter(request.key)
        return {"value": value}
    except KeyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/counter/dec")
async def decrement_counter_endpoint(request: KeyRequest):
    try:
        value = decrement_counter(request.key)
        return {"value": value}
    except KeyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Queue endpoints
@app.put("/queue/configure")
async def configure_queue_endpoint():
    try:
        configure_queue()
        return {"message": "Queue configured successfully"}
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/queue/set")
async def set_queue_endpoint(request: QueueKeyRequest):
    try:
        set_queue(request.key)
        return {"message": "Queue set successfully"}
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/queue/get")
async def get_queue_endpoint(request: QueueKeyRequest):
    try:
        values = get_queue(request.key)
        return {"values": values}
    except KeyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/queue/enq")
async def enqueue_endpoint(request: QueueEnqueueRequest):
    try:
        size = enqueue(request.key, request.value)
        return {"size": size}
    except KeyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/queue/deq")
async def dequeue_endpoint(request: QueueKeyRequest):
    try:
        value = dequeue(request.key)
        return {"value": value}
    except KeyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e)) 