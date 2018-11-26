import pymysql
import request
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.paginator import Paginator


def index(request):
    if request.method == 'GET':
        # 如果请求为get，返回注册页面

        coon = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='baijiaxing')

        # 创建游标
        cursor = coon.cursor()
        urls = []
        sql = """select * from first_name"""
        cursor.execute(sql.encode('utf-8'))
        data = cursor.fetchall()
        print(data)
        coon.close()
        # 创建分页对象
        page_num = request.GET.get('page_num', 1)
        paginator = Paginator(data, 30)
        page = paginator.page(page_num)

        return render(request, 'index.html', {'page': page})
