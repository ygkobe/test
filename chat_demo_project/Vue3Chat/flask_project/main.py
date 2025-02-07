from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import time
import random
app = Flask(__name__)
CORS(app)  # 允许跨域请求


# 处理函数示例，你可以根据需要修改为与 ChatGPT 模型的实际交互
def process_message(message):
    # 此处模拟处理时间
    python_code = """
```
print(123)    
```
"""
    shell_code = """
```
ls
```    
    """
    # response = random.choice(["你好", "牛逼", "卧槽", "^^^666",python_code, shell_code])
    response = random.choice(["你好 666 ", "牛逼 666", "卧槽 666", "王泽 666"])
#     response = """
# 你好
#     """
    return response


# 处理接收到的消息，并通过 SSE 返回处理结果
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        print(messages)
        messages = [{"content": messages},{"content": messages},{"content": messages},{"content": messages}]
        def generate():
            for message in messages:
                content = message['content']
                processed_message = process_message(content)

                yield f"data: {processed_message}\n\n"
                time.sleep(0.5)  # 模拟处理间隔

        return Response(generate(), content_type='text/event-stream')

    except Exception as e:
        return Response(f"event: error\ndata: {str(e)}\n\n", content_type='text/event-stream', status=500)


if __name__ == '__main__':
    app.run(debug=True)
