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
  "policy": "LRU|LFU",
  "capacity": 10
}
```

#### Set Key-Value
```
PUT /cache/set
```
**Request Body:**
```json
{
  "key": "user",
  "value": "John Doe",
  "ttl": 3600  
}
```

#### Get Value
```
POST /cache/get
```
**Request Body:**
```json
{
  "key": "user"
}
```
**Response:**
```json
{
  "value": "John Doe"
}
```

#### Get TTL
```
POST /cache/ttl
```
**Request Body:**
```json
{
  "key": "user"
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
  "key": "user",
  "expiry": "2025-01-01T00:00:00Z"  
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

#### Set Counter
```
PUT /counter/set
```
**Request Body:**
```json
{
  "key": "user"
}
```

#### Get Counter
```
POST /counter/get
```
**Request Body:**
```json
{
  "key": "user"
}
```
**Response:**
```json
{
  "value": 0
}
```

#### Increment Counter
```
POST /counter/inc
```
**Request Body:**
```json
{
  "key": "user"
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
POST /counter/dec
```
**Request Body:**
```json
{
  "key": "user"
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

#### Set Queue
```
PUT /queue/set
```
**Request Body:**
```json
{
  "key": "notifications"
}
```

#### Get Queue
```
POST /queue/get
```
**Request Body:**
```json
{
  "key": "notifications"
}
```
**Response:**
```json
{
  "values": ["item1", "item2"]
}
```

#### Enqueue
```
POST /queue/enq
```
**Request Body:**
```json
{
  "key": "notifications",
  "value": "New message from user"
}
```
**Response:**
```json
{
  "size": 1
}
```

#### Dequeue
```
POST /queue/deq
```
**Request Body:**
```json
{
  "key": "notifications"
}
```
**Response:**
```json
{
  "value": "New message from user"
}
```

