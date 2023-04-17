import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def chart_default(request):
    """ 数据统计图表 """

    return render(request, 'echart.html')


def chart_line(request):
    """ 构造折线图的数据 """
    # 数据集
    legend_data = ['本部']
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']

    series_list = [
        {"name": '邮件营销', "type": 'line', "stack": '总量', "areaStyle": {}, "data": [120, 132, 101, 134, 90, 230, 210]}
    ]
    results = {
        "status": True,
        "data": {
            "series_list": series_list,
            "x_axis": x_axis,
            "legend_data": legend_data
        }
    }
    return JsonResponse(results)


def chart_bar(request):
    """ 构造柱状图的数据 """
    # 颜色说明标题(与数据集中的name相对应)
    legend = ["张三", "李四"]
    # 数据集
    series_list = [
        {
            "name": '张三',
            "type": 'bar',
            "data": [5, 26, 30, 10, 40, 20]
        },
        {
            "name": '李四',
            "type": 'bar',
            "data": [5, 26, 30, 10, 40, 20]
        }
    ]
    # x轴
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    results = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series_list,
            "x_axis": x_axis
        }
    }
    return JsonResponse(results)


def chart_pie(request):
    """ 构造饼图的数据 """
    # 数据集
    series_list = [
        {"value": 1048, "name": '开发部'},
        {"value": 735, "name": '运营部'},
        {"value": 580, "name": '财务部'},
    ]
    results = {
        "status": True,
        "data": series_list
    }
    return JsonResponse(results)




