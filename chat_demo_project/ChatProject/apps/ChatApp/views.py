from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from django.http import StreamingHttpResponse


class SparkaiAPI(APIView):

    def get(self, request):
        def generate_data():
            # 模拟逐步生成数据

            messages = [{'role': 'user',
                         'content': "你好, 写50字夸我的"}]

            spark = ChatSparkLLM(
                spark_api_url='wss://spark-api.xf-yun.com/v1.1/chat',
                spark_app_id='ff3feb56',
                spark_api_key='0e3906108bb7ed36da29932705ee563c',
                spark_api_secret='MjQxMDNkYzZlMTM3ODQ1OWU4ZTZjZGFk',
                spark_llm_domain='general',
                streaming=True,
                max_tokens=1024,
            )
            messages = [
                ChatMessage(
                    role="user",
                    content=messages[0]['content']

                )]

            a = spark.stream(messages)
            for message in a:
                yield message.content
                print(type(message), message)

        return StreamingHttpResponse(generate_data())

    def post(self, request):
        try:

            # 模拟处理消息的过程
            def generate_data():
                data = request.data  # 获取 POST 请求的数据
                # print(data)
                messages = data.get('messages', [])

                content = messages[-2].get('content')
                print(content)
                content = '{}, 请模仿东北人语气回复我'.format(content)
                # messages = [{'role': 'user',
                #              'content': "你好, 使用python实现一个快速排序"}]

                spark = ChatSparkLLM(
                    spark_api_url='wss://spark-api.xf-yun.com/v1.1/chat',
                    spark_app_id='ff3feb56',
                    spark_api_key='0e3906108bb7ed36da29932705ee563c',
                    spark_api_secret='MjQxMDNkYzZlMTM3ODQ1OWU4ZTZjZGFk',
                    spark_llm_domain='general',
                    streaming=True,
                    max_tokens=1024,
                )
                messages = [
                    ChatMessage(
                        role="user",
                        content=content

                    )]

                response_data = spark.stream(messages)
                for message in response_data:
                    # yield f"data: 122\n\n"
                    yield str(message.content)
                    # res_stream_data = 'data: {}\n\n'.format(str(message.content))
                    # yield res_stream_data
                    # print(res_stream_data)


            # 返回 SSE 响应
            return StreamingHttpResponse(generate_data(), content_type='text/event-stream')

        except Exception as e:
            return StreamingHttpResponse(f"event: error\ndata: {str(e)}\n\n", content_type='text/event-stream', status=500)