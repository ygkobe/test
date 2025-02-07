import pymysql
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from .models import CarNumberInfo
from .serializers import CarNumberInfoSerializers
from rest_framework import viewsets
from django.conf import settings
from rest_framework.decorators import action
from datetime import datetime
from django.http import HttpResponse
import urllib.parse
from .tasks import long_running_task
from celery.result import AsyncResult


class CarNumberGroup(APIView):
    """
    汽车分组
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        group_list = CarNumberInfo.objects.all()
        # 构建序列化器对象  instance: 用于序列化传参
        # 序列化多个实例化对象 many为True ，实例化对象单个时为False
        serializer = CarNumberInfoSerializers(instance=group_list, many=True)
        print(serializer.data)

        return Response(serializer.data)

    def post(self, request):
        # print(request.data)
        group_name = request.data.get('group_name')

        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        file_obj = request.FILES['file']
        try:
            # 读取Excel文件数据流
            df = pd.read_excel(file_obj, engine='openpyxl')
            # print(df.fillna('').to_dict('records'))
            car_number_list = df.fillna('').to_dict('records')
            for item in car_number_list:
                print(item.get('车牌号'))
                car_number = item.get('车牌号')
                CarNumberInfo.objects.create(group_name=group_name, car_number=car_number, create_time=create_time)

            return Response({"status": 'success'}, status=200)
        except Exception as e:
            return Response({"status": 'error', "message": str(e)}, status=400)


class CarHistory(viewsets.ViewSet):
    permission_classes = [AllowAny]
    config = settings.DATABASES.get('default')
    host = config.get('HOST')
    port = config.get('PORT')
    password = config.get('PASSWORD')
    database = config.get('NAME')
    user = config.get('USER')

    @action(detail=False, methods=['get'])
    def group_history(self, request):
        sql = """
           SELECT group_name, COUNT(*) as count, create_time
            FROM car_numbers_group
            GROUP BY group_name, create_time
            ORDER BY create_time DESC;
            """
        # 建立数据库连接
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)

        # 编写 SQL 查询语句

        # 使用 pandas 的 read_sql 函数读取数据
        data = pd.read_sql(sql, conn)
        data = data.fillna('').to_dict('records')
        # print(data)

        data_list = []
        s_id = 1
        for item in data:
            item['id'] = s_id
            s_id = s_id + 1
            data_list.append(item)

        # 关闭数据库连接
        conn.close()

        # 打印读取的数据
        # print(data)
        return Response(data_list)

    @action(detail=False, methods=['delete'])
    def delete_group(self, request):
        print(request.data)
        group_name = request.data.get('group_name')
        create_time = request.data.get('create_time')
        print(group_name, create_time)
        # 构造 SQL 删除语句
        sql = """
            DELETE FROM car_numbers_group 
            WHERE group_name = %s AND create_time = %s
            """

        # 数据库连接
        try:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            with connection.cursor() as cursor:
                # 执行删除操作
                cursor.execute(sql, (group_name, create_time))
                connection.commit()

            connection.close()
            return Response({'message': '删除成功'}, status=200)
        except Exception as e:
            return Response({'message': '删除失败', 'error': str(e)}, status=500)

        # return Response()

    def get_database_car_numbers(self, group_name='', create_time=''):
        sql = """
        select car_number from car_numbers_group WHERE group_name = '{}' AND create_time = '{}'
        """.format(group_name, create_time)
        # 建立数据库连接
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)

        # 编写 SQL 查询语句

        # 使用 pandas 的 read_sql 函数读取数据
        data = pd.read_sql(sql, conn)
        data = data.fillna('').to_dict('records')
        print(data)

    @action(detail=False, methods=['get'])
    def group_name_details(self, request):
        group_name = request.query_params.get('group_name')
        create_time = request.query_params.get('create_time')

        sql = """
                SELECT *
                    FROM car_numbers_group
                    WHERE group_name = '{}' AND create_time = '{}'
                """.format(group_name, create_time)
        # 建立数据库连接
        conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)

        # 编写 SQL 查询语句

        # 使用 pandas 的 read_sql 函数读取数据
        data = pd.read_sql(sql, conn)
        data = data.fillna('').to_dict('records')
        print(data)

        data_list = []
        # s_id = 1
        for item in data:
            # item['id'] = s_id
            data_list.append(item)
            # s_id = s_id + 1

        # 关闭数据库连接
        conn.close()

        # 打印读取的数据
        # print(data)
        return Response(data_list)

    @action(detail=False, methods=['post'])
    def car_number_edit(self, request):

        car_id = request.data.get('id')
        group_name = request.data.get('group_name')
        car_number = request.data.get('car_number')
        create_time = request.data.get('create_time')

        sql = """
                    update car_numbers_group set car_number = %s
                    WHERE group_name = %s AND create_time = %s AND id= %s
            """

        # 数据库连接
        try:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                         port=self.port)
            with connection.cursor() as cursor:
                # 执行删除操作
                cursor.execute(sql, (car_number, group_name, create_time, car_id))
                connection.commit()

            connection.close()
            return Response({'message': '删除成功'}, status=200)
        except Exception as e:
            return Response({'message': '删除失败', 'error': str(e)}, status=500)


class AsyncExecuteTask(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def start_task(self, request):
        # 获取 POST 请求参数
        print(request.data)
        form_data = request.data

        # 启动 Celery 异步任务，并传递参数
        task = long_running_task.delay(form_data)

        return Response({'task_id': task.id})

    @action(detail=False, methods=['get'])
    def get_progress(self, request):
        task_id = request.GET.get('task_id')
        task = AsyncResult(task_id)

        if task.state == 'PROGRESS':
            if isinstance(task.info, dict):
                progress = task.info.get('current', 0)
            else:
                progress = 0
        elif task.state == 'SUCCESS':
            progress = 100
            return Response({'progress': progress})
        else:
            progress = 0

        return Response({'progress': progress})

    @action(detail=False, methods=['get'])
    def download_excel(self, request):
        print(request.query_params)
        task_id = request.query_params.get('task_id')
        group_name = request.query_params.get('group_name')
        date_range = request.query_params.get('date_range')
        start_date = date_range.split(',')[0]
        end_date = date_range.split(',')[1]

        # 自定义文件名
        # excel_name = "{}_{}_{}_{}.xlsx".format(group_name, start_date, end_date, task_id)
        excel_name = "{}_{}_{}.xlsx".format(group_name, start_date, end_date)
        # URL-encode the filename
        encoded_excel_name = urllib.parse.quote(excel_name)

        # Get task result
        task = AsyncResult(task_id)

        if task.state == 'SUCCESS':
            if isinstance(task.info, dict):
                file_data = task.info.get('file_data')  # Assuming file data is stored in task.info
                response = HttpResponse(
                    file_data,
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_excel_name}'
                return response
        else:
            return Response({'error': 'Task not completed or does not exist'}, status=400)
