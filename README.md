# Wish.com Redis Clone

## HTTP API Routes

### Cache Endpoints

#### Configure Cache
```
PUT /cache/configure
```
**Request Body:**
```json
{
  "policy": "LFU|LRU",
  "capacity": 1000
}
```

#### Set Key-Value
```
PUT /cache/set
```
**Request Body:**
```json
{
  "key": "mykey",
  "value": "myvalue"
}
```

#### Get Value
```
GET /cache/get
```
**Request Body:**
```json
{
  "key": "mykey"
}
```
**Response:**
```json
{
  "value": "myvalue"
}
```

#### Get TTL
```
GET /cache/ttl
```
**Request Body:**
```json
{
  "key": "mykey"
}
```
**Response:**
```json
{
  "ttl": 3600
}
```

#### Set Expiration
```
PUT /cache/expire
```
**Request Body:**
```json
{
  "key": "mykey",
  "timestamp": 1234567890
}
```

#### Scan Keys
```
GET /cache/scan
```
**Response:**
```json
{
  "keys": ["key1", "key2", "key3"]
}
```

### Counter Endpoints

#### Create Counter
```
PUT /counter/configure
```
**Request Body:**
```json
{
  "capacity": 1000
}
```

#### Set Counter
```
PUT /counter/set
```
**Request Body:**
```json
{
  "key": "mycounter"
}
```

#### Increment Counter
```
PUT /counter/inc
```
**Request Body:**
```json
{
  "key": "mycounter"
}
```
**Response:**
```json
{
  "value": 1
}
```

#### Decrement Counter
```
PUT /counter/dec
```
**Request Body:**
```json
{
  "key": "mycounter"
}
```
**Response:**
```json
{
  "value": 0
}
```

### Queue Endpoints

#### Create Queue
```
PUT /queue/configure
```
**Request Body:**
```json
{
  "capacity": 1000
}
```

#### Set Queue
```
PUT /queue/set
```
**Request Body:**
```json
{
  "key": "myqueue"
}
```

#### Enqueue
```
PUT /queue/enq
```
**Request Body:**
```json
{
  "key": "myqueue",
  "value": "item1"
}
```

#### Dequeue
```
POST /queue/deq
```
**Request Body:**
```json
{
  "key": "myqueue"
}
```
**Response:**
```json
{
  "value": "item1"
}
```


## Plan

<!-- 1. Create a folder called `service/cache`
2. Create a file in there called `LFU.py`
3. Create a file in there called `LRU.py`
4. Implement an in memory LFU cache in `LFU.py`
5. Implement an in memory LRU cache in `LRU.py`
6. Create a folder called `service/counter`
7. Create a file in there called `counter.py`
8. Implement an in memory counter dict -> int in `counter.py`
9. Create a folder called `service/queue`
10. Create a file in there called `queue.py`
11. Implement an in memory dict -> deque in `queue.py`
12. Create a folder called `storage`
13. Create a file called `storage/singletons.py`
14. Create singleton instances: one cache (default LRU), one counter, one queue
15. Update `server.py` to contain business logic functions that call the storage singletons
16. Update `app.py` to implement HTTP routes that call functions in `server.py`
18. Add optional CONFIGURE endpoints to change cache policy/capacity at runtime -->

### TODO
1. implement queue
1. add queue tests
1. add errors to all services
1. add storage signletons 
1. add singleton instances
1. update server.py to contain business logic functions that call the storage singletons
1. add api layer in app.py that calls server.py functions


