# -*- coding:utf8 -*-
import time
import json

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from rest_framework.permissions import AllowAny  # 导入需要的权限类
from rest_framework import viewsets
from rest_framework.decorators import action
from django.conf import settings
import datetime

import pandas as pd
import pymysql
from datetime import datetime

from django.http import HttpResponse
import requests
from io import BytesIO
from openpyxl import Workbook
from collections import defaultdict
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, PatternFill, Font
import warnings
# 抑制特定的警告
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable.*")

class GuangDongShenZhenSuriquery(object):
    """
    广东深圳汽车违法查询
    """

    def __init__(self, cookies=None, startDate='20240101', endDate='20240805'):
        self.cookies = cookies
        self.startDate = startDate
        self.endDate = endDate
        self.hpzl = 52
        self.suriquery_url = "https://gd.122.gov.cn/user/m/uservio/suriquery"
        self.Host = "gd.122.gov.cn"
        self.Origin = "https://gd.122.gov.cn"
        self.Referer = "https://gd.122.gov.cn/views/memfyy/violation.html"
        self.querySurvielDetail_url = "https://gd.122.gov.cn/user/m/tsc/vio/querySurvielDetail"

    def get_suriquery(self, car_number="粤BBP2270"):

        payload = {
            "startDate": self.startDate,
            "endDate": self.endDate,
            "hphm": car_number,
            "hpzl": 52,
        }

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Cookie": self.cookies,
            "Host": self.Host,
            "Origin": self.Origin,
            "Referer": self.Referer,
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-Ch-Mobile": '?0',
            "Sec-Ch-Ua-Platform": "macOS"
        }
        response = requests.post(url=self.suriquery_url, data=payload, headers=headers)

        data = json.loads(response.text)
        # print(data)

        if data.get('code') == 200:

            if data.get('data').get('content'):
                data_list = []
                # print(data)
                for item in data.get('data').get('content'):
                    # print(i)
                    jkbj = item.get("jkbj")
                    clbj = item.get("clbj")
                    # data_list.append(item)
                    if int(jkbj) == 0 and int(clbj) == 0:
                        data_list.append(item)

                if len(data_list) >= 1:
                    return data_list
                else:
                    return [{'hphm': car_number, "info": ""}]

            else:
                return [{'hphm': car_number, "info": ""}]

        elif data.get('code') == 500 and data.get('message') == "只能查询已绑定的机动车违法":
            return [{'hphm': car_number, 'info': ': 未绑定'}]
        else:
            return [{'hphm': car_number, 'info': ': 未知错误'}]

    def get_querySurvielDetail(self, car_number="粤BBT2077", xh="4403037902635108", cjjg="440303000000"):

        payload = {
            "hphm": car_number,
            "hpzl": 52,
            "xh": xh,
            "cjjg": cjjg

        }

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Cookie": self.cookies,
            "Host": self.Host,
            "Origin": self.Origin,
            "Referer": self.Referer,
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-Ch-Mobile": '?0',
            "Sec-Ch-Ua-Platform": "macOS",
            "Connection": "keep-alive"
        }
        # response = requests.post(url=url, data=payload, headers=headers)
        response = requests.post(url=self.querySurvielDetail_url, data=payload, headers=headers)
        # print(response.text)

        response_status_code = json.loads(response.text).get('code')
        if response_status_code == 200:
            data = json.loads(response.text).get('data')
            return data

    def get_handle_data_list(self, car_number_list: list):
        data_list = []
        # car_number_list = ["粤BBT2076"]
        for car_number in car_number_list:
            # print(car_number)
            try:
                suriquery_data = self.get_suriquery(car_number=car_number)
                # print(suriquery_data)

                for detail in suriquery_data:
                    # print(detail)
                    xh = detail.get('xh')
                    cjjg = detail.get('cjjg')
                    if xh and cjjg:
                        data = self.get_querySurvielDetail(car_number=car_number, xh=xh, cjjg=cjjg)
                        print(data)
                        data_list.append(data)
                    else:

                        data = {"hphm": detail.get('hphm') + detail.get('info')}
                        print(data)
                        data_list.append(data)
            except Exception as e:
                data_list.append({'hphm': car_number + "_数据错误"})

        grouped_data = defaultdict(list)

        for entry in data_list:

            if entry.get('wjgbj'):
                wjgbj = entry.get('wjgbj')
            else:
                if entry.get('wfms'):
                    wjgbj = 0
                else:
                    wjgbj = ''

            item = {
                'wfms': entry.get('wfms'),
                'wfsj': entry.get('wfsj'),
                'wfdz': entry.get('wfdz'),
                'wjgbj': wjgbj,
                'fkje': entry.get('fkje'),
                'cjjgmc': entry.get('cjjgmc'),
                'hpzlStr': entry.get('hpzlStr'),
                'photos': entry.get('photos')[0] if entry.get('photos') else None,
            }
            grouped_data[entry['hphm']].append(item)
        return grouped_data


class ShenZhenTrafficViolation(object):
    """
    深圳交通违法数据
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = '交通违法数据'
    config = settings.DATABASES.get('default')
    host = config.get('HOST')
    port = config.get('PORT')
    password = config.get('PASSWORD')
    database = config.get('NAME')
    user = config.get('USER')

    def __init__(self, cookies=None, startDate=None, endDate=None, group_name=None, create_time=None):
        self.cookies = cookies
        self.group_name = group_name
        self.create_time = create_time
        self.startDate = startDate
        self.endDate = endDate
        self.hpzl = 52
        self.suriquery_url = "https://gd.122.gov.cn/user/m/uservio/suriquery"
        self.Host = "gd.122.gov.cn"
        self.Origin = "https://gd.122.gov.cn"
        self.Referer = "https://gd.122.gov.cn/views/memfyy/violation.html"
        self.querySurvielDetail_url = "https://gd.122.gov.cn/user/m/tsc/vio/querySurvielDetail"

    @staticmethod
    def extract_city(address: dict):
        """
        获取省市
        :param address:
        :return:
        """
        offer = address.get('offer')
        offer_address = address.get('address')
        if offer and offer_address:

            if "省" in offer:
                return offer.split("省")[0] + "省"
            if "省" in offer_address:
                return offer_address.split("省")[0] + "省"

            if "市" in offer:
                return offer.split("市")[0] + "市"

            if "市" in offer_address:
                return offer_address.split("市")[0] + "市"

            if "县" in offer:
                return offer.split("县")[0] + "县"
            elif "县" in offer_address:
                return offer_address.split("县")[0] + "县"
            else:
                return "未知地点"

    def get_database_car_numbers(self, group_name=None, create_time=None):
        """
        查询数据库车辆数据
        :param group_name:
        :param create_time:
        :return:
        """
        sql = """
        select car_number 
        from car_numbers_group 
        WHERE 
        group_name = '{}' AND create_time = '{}'
        """.format(group_name, create_time)

        # 建立数据库连接
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)

        # 编写 SQL 查询语句

        # 使用 pandas 的 read_sql 函数读取数据
        data = pd.read_sql(sql, conn)
        data = data.fillna('').to_dict('records')

        data_list = list(set([number.get('car_number') for number in data]))
        # print(data_list)
        return data_list

    def get_suriquery(self, car_number="粤BBP2270"):

        payload = {
            "startDate": self.startDate,
            "endDate": self.endDate,
            "hphm": car_number,
            "hpzl": 52,
        }

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Cookie": self.cookies,
            "Host": self.Host,
            "Origin": self.Origin,
            "Referer": self.Referer,
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-Ch-Mobile": '?0',
            "Sec-Ch-Ua-Platform": "macOS"
        }
        response = requests.post(url=self.suriquery_url, data=payload, headers=headers)

        data = json.loads(response.text)
        # print(data)

        if data.get('code') == 200:

            if data.get('data').get('content'):
                data_list = []
                # print(data)
                for item in data.get('data').get('content'):
                    # print(i)
                    jkbj = item.get("jkbj")
                    clbj = item.get("clbj")
                    # data_list.append(item)
                    if int(jkbj) == 0 and int(clbj) == 0:
                        data_list.append(item)

                if len(data_list) >= 1:
                    return data_list
                else:
                    return [{'hphm': car_number, "info": ""}]

            else:
                return [{'hphm': car_number, "info": ""}]

        elif data.get('code') == 500 and data.get('message') == "只能查询已绑定的机动车违法":
            return [{'hphm': car_number, 'info': ': 未绑定'}]
        else:
            return [{'hphm': car_number, 'info': ': 未知错误'}]

    def get_querySurvielDetail(self, car_number="粤BBT2077", xh="4403037902635108", cjjg="440303000000"):

        payload = {
            "hphm": car_number,
            "hpzl": 52,
            "xh": xh,
            "cjjg": cjjg

        }

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Cookie": self.cookies,
            "Host": self.Host,
            "Origin": self.Origin,
            "Referer": self.Referer,
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-Ch-Mobile": '?0',
            "Sec-Ch-Ua-Platform": "macOS",
            "Connection": "keep-alive"
        }
        # response = requests.post(url=url, data=payload, headers=headers)
        response = requests.post(url=self.querySurvielDetail_url, data=payload, headers=headers)
        # print(response.text)

        response_status_code = json.loads(response.text).get('code')
        if response_status_code == 200:
            data = json.loads(response.text).get('data')
            return data

    def get_handle_data_list(self):
        data_list = []
        # car_number_list = ["粤BBT2076"]
        for car_number in self.get_database_car_numbers(group_name=self.group_name):
            # print(car_number)
            try:
                suriquery_data = self.get_suriquery(car_number=car_number)
                # print(suriquery_data)

                for detail in suriquery_data:
                    # print(detail)
                    xh = detail.get('xh')
                    cjjg = detail.get('cjjg')
                    if xh and cjjg:
                        data = self.get_querySurvielDetail(car_number=car_number, xh=xh, cjjg=cjjg)
                        print(data)
                        data_list.append(data)
                    else:

                        data = {"hphm": detail.get('hphm') + detail.get('info')}
                        print(data)
                        data_list.append(data)
            except Exception as e:
                data_list.append({'hphm': car_number + "_数据错误"})

        grouped_data = defaultdict(list)

        for entry in data_list:

            if entry.get('wjgbj'):
                wjgbj = entry.get('wjgbj')
            else:
                if entry.get('wfms'):
                    wjgbj = 0
                else:
                    wjgbj = ''

            item = {
                'wfms': entry.get('wfms'),
                'wfsj': entry.get('wfsj'),
                'wfdz': entry.get('wfdz'),
                'wjgbj': wjgbj,
                'fkje': entry.get('fkje'),
                'cjjgmc': entry.get('cjjgmc'),
                'hpzlStr': entry.get('hpzlStr'),
                'photos': entry.get('photos')[0] if entry.get('photos') else None,
            }
            grouped_data[entry['hphm']].append(item)
        return grouped_data