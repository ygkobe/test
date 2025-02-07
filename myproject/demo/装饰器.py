def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(n)
            func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()