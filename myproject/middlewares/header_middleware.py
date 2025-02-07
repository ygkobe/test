from django.utils.deprecation import MiddlewareMixin


class HeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 在请求处理之前添加自定义请求头
        # Django 使用 request.META 来存储 HTTP 请求头信息
        # 注意：在 request.META 中，HTTP 头的键名会被转换为大写，并加上 'HTTP_' 前缀
        # 所以我们可以直接修改这个字典来添加自定义请求头
        request.META['HTTP_X_CUSTOM_HEADER'] = 'Request Header'
        print()
        print(request.META)

        # 可以在这里执行其他操作，比如打印日志
        print("Request path:", request.path)
        print()

        # 一般情况下，process_request 方法不需要返回响应对象
        # 它主要用于修改请求对象
        return None

    def process_response(self, request, response):
        # 在响应返回给客户端之前修改响应对象
        # 添加自定义响应头
        response['X-Custom-Header'] = 'My Custom Header'

        # 设置缓存的过期时间为 10 秒
        response['Cache-Control'] = 'max-age=10'

        # 必须返回响应对象，否则客户端将无法收到响应
        return response