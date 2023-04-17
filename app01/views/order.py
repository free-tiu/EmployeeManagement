import datetime
import json
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app01.models import Order
from app01.utils.form import OrderModelForm
from datetime import datetime

from app01.utils.pagination import Pagination


def order_list(request):
    """ 订单列表 """
    queryset = Order.objects.all().order_by('-oid')
    # 对数据进行分页
    page_object = Pagination(request, queryset)

    form = OrderModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页后的数据
        "page_string": page_object.html(),  # 生成页码
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 添加订单（Ajax）请求 """
    form = OrderModelForm(data=request.POST)

    if form.is_valid():
        # 自动生成oid —— 订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 设置管理员id —— 设置为当前已登录的管理员id
        form.instance.admin_id = request.session["info"]["id"]

        form.save()     # 将数据保存到数据中
        context = {"status": True}
        return JsonResponse(context)

    # 错误信息
    context = {
        "status": False, 'error': form.errors
    }
    return HttpResponse(json.dumps(context, ensure_ascii=False))


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get("uid")

    # 验证获取的ID是否存在
    exists = Order.objects.filter(id=uid).exists()
    if not exists:
        context = {"status": False, 'errors': "删除失败！该数据不存在！"}
        return JsonResponse(context)
    else:
        Order.objects.filter(id=uid).delete()
        context = {"status": True}
        return JsonResponse(context)


def order_detail(request):
    """ 根据ID获取需要编辑的单条订单详情 """
    uid = request.GET.get("uid")
    # row_data = Order.objects.filter(id=uid).first()       # 获取数据方式一
    row_data = Order.objects.filter(id=uid).values("title", "price", "status").first()    # 获取数据方式二 —— 字典类型
    if not row_data:
        context = {"status": False, 'errors': "该订单数据不存在！"}
        return JsonResponse(context)

    context = {"status": True, 'data': row_data}
    return JsonResponse(context)


@csrf_exempt
def order_edit(request):
    """ 编辑订单信息 """
    uid = request.GET.get("uid")
    print(uid)
    # 根据id获取到当前正在编辑的对象
    row_object = Order.objects.filter(id=uid).first()

    if not row_object:
        context = {"status": False, 'tips': "该订单数据不存在！"}
        return JsonResponse(context)

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        context = {"status": True}
        return JsonResponse(context)

    context = {"status": False, 'error': form.errors}
    return JsonResponse(context)
