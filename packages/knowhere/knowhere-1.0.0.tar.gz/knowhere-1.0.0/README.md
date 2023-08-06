# knowhere

In memory cache, a python implementation of [`zizou`](https://github.com/arriqaaq/zizou) with a different expiration policy

![knowhere](http://66.42.57.109/knowhere.jpg)

## Features

* Store millions of entries
* High concurrent thread-safe access
* Expiration support
* Shard support to avoid locks on whole db during any concurrent read/writes/deletes

## Installation
```sh
pip install knowhere
```

## Usage

### Initialize
shard_size should be a power of 2. This size must be set according to the number of keys you expect to be there in the cache at any given time.

```python
from datetime import timedelta
from decimal import Decimal

import uuid, time, json, sys, knowhere

c = knowhere.Cache(shard_size=2, eviction_interval=timedelta(seconds=10))

```
### Set
```python
c.set("key", "value", ttl=timedelta(seconds=5))
```
Default expiry will be set to 5 minutes if no ttl is specified

### Get
```python
c.get("key")
```
### Delete
```python
c.delete("key")
```
### Flush
deletes all keys in the cache
```python
c.flush()
```

## Info
gives all shards and number of keys in each shard as a json
```python
c.info()
```

## Keys
gives a list of all keys in the cache
```python
c.keys()
```

## Expiration policy
knowhere expires keys the same way redis does. You can find it [`here`]('https://redis.io/commands/expire#how-redis-expires-keys'). Specifically, this is what knowhere does on every eviction interval for each shard
* Step 1: Get 20 random keys from the shard
* Step 2: Delete all the keys which should be expired.
* Step 3: If more than 4 of the 20 keys were expired, start again from step 1
