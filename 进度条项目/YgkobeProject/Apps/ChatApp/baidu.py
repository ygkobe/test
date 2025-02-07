# -*- coding:utf8 -*-
import requests
import json
from datetime import datetime
import psutil


class BaiduAPI(object):

    def __init__(self):
        self.API_KEY = "nM3NmWMW9dPAUrYmRUrJFQIg"
        self.SECRET_KEY = "mXCdjcZUk1vhipD1vhUcGQOgaLsLTS6d"

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    def reply(self, content):
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + self.get_access_token()

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        data = json.loads(response.text)
        created = data.get("created")
        created = datetime.fromtimestamp(created)
        result = data.get("result")
        print(created, result)
        return result
        return "{} \n\n {}".format(created, result)


if __name__ == "__main__":
    baidu = BaiduAPI()
    baidu.reply('你好')