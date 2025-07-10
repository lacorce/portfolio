import redis 


redis = redis.Redis(host='localhost', port=6379, db=0)
redis.flushall()

redis.set('rub_usd_rate', 0.01)
