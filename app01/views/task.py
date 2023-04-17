import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app01.models import Task
from app01.utils.form import TaskModelForm
from app01.utils.pagination import Pagination


# 免除csrf认证
@csrf_exempt
def task_list(request):
    """ 任务管理 """
    # 获取数据库中的所有任务
    queryset = Task.objects.all().order_by('level')

    # 对数据进行分页
    page_object = Pagination(request, queryset)

    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": page_object.page_queryset,      # 分完页后的数据
        "page_string": page_object.html(),          # 生成页码
    }
    return render(request, 'task.html', context)


@csrf_exempt
def task_ajax(request):
    """ 测试获取前端Ajax发送过来的请求 """
    if request.method == 'GET':
        return render(request, 'task_list.html')
    print(request.POST)

    data_dict = {"status": True, 'data': [1, 2, 3]}
    # json_str = json.dumps(data_dict)
    # return HttpResponse(json_str)
    return JsonResponse(data_dict)


@csrf_exempt
def task_add(request):
    add_data = request.POST
    # print(add_data)     # 测试输出

    # 对用户发送过来的数据进行校验(使用ModelForm)
    form = TaskModelForm(data=add_data)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)

    # 错误信息
    data_dict = {
        "status": False, 'error': form.errors
    }
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))






