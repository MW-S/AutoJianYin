import time


def retry_function(retry_times=3, delay=2):
    """
    一个装饰器函数，用于实现重试机制。
    :param retry_times: 重试次数
    :param delay: 每次重试之间的等待时间（秒）
    :return: 被装饰的函数
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retry_times:
                try:
                    return func(*args, **kwargs)  # 尝试执行被装饰的函数
                except Exception as e:
                    print(f"尝试 {attempts + 1} 失败，错误信息：{e}")
                    attempts += 1
                    if attempts < retry_times:
                        print(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)  # 等待一段时间后再次尝试
                    else:
                        raise  # 所有重试次数用完，重新抛出异常
        return wrapper
    return decorator