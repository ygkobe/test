import redis

# 连接本地 Redis 服务器
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# 写入数据
def write_to_redis(key, value):
    redis_client.set(key, value)
    print(f"成功写入: {key} -> {value}")


# 读取数据
def read_from_redis(key):
    value = redis_client.get(key)
    if value:
        print(f"查询结果: {key} -> {value}")
    else:
        print(f"未找到键: {key}")


if __name__ == "__main__":
    # 测试写入
    write_to_redis("name", "Alice")
    write_to_redis("age", "30")

    # 测试查询
    read_from_redis("name")
    read_from_redis("age")
    read_from_redis("city")  # 这个键不存在
