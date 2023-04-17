from django.shortcuts import render, redirect
from app01.models import PrettyNum
from app01.utils.form import PrettyNumModelForm, PrettyEditNumModelForm
from app01.utils.pagination import Pagination


# 靓号管理
def num_list(request):
    """ 靓号列表 """
    pretty_list = PrettyNum.objects.all().count()

    data_dict = {}
    # =============== 查询功能 ===============
    # 获取前端提交的搜索关键字
    value = request.GET.get("q", "")
    if value:   # 当获取不为空时
        # 将搜索关键字赋值给mobile__contains
        data_dict["mobile__contains"] = value

    # =============== 分页功能 ===============
    queryset = PrettyNum.objects.filter(**data_dict).order_by("level")
    # 实例化分页组件
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    pageNums = page_object.html()

    context = {
        "pretty_list": pretty_list,
        "value": value,
        # 分完页后的数据
        "page_queryset": page_queryset,
        # 生成的页码
        "pageNums": pageNums
    }
    return render(request, 'num_list.html', context)


def num_add_model(request):
    """ 添加靓号 """
    if request.method == 'GET':
        # 表单实例化
        form = PrettyNumModelForm()
        context = {
            'form': form
        }
        return render(request, 'num_add.html', context)

    if request.method == 'POST':
        # 获取表单数据
        form = PrettyNumModelForm(data=request.POST)
        # 对获取到的表单数据进行校验
        if form.is_valid():
            # 校验成功获取到的数据
            success_data = form.cleaned_data
            # 测试输出
            print(success_data)
            # 将合法的数据保存到数据库中
            form.save()
            return redirect('/num/list/')
        # 数据校验失败
        context = {
            "form": form
        }
        return render(request, 'num_add.html', context)


def num_del(request, nid):
    """ 靓号删除 """
    PrettyNum.objects.filter(id=nid).delete()

    return redirect('/num/list')


def num_edit(request, nid):
    """ 编辑靓号 """
    # 根据ID查询到对应需要修改的靓号信息
    numData = PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        pretty = numData
        # 将获取到的用户信息作为默认值放到input输入框中
        form = PrettyEditNumModelForm(instance=numData)
        context = {
            "pretty": pretty,
            "form": form
        }
        return render(request, 'num_edit.html', context)

    if request.method == 'POST':
        # 对用户提交过来的数据进行校验    instance=userData => 当前操作的用户对象信息
        form = PrettyEditNumModelForm(data=request.POST, instance=numData)
        if form.is_valid():
            # 数据校验成功后将数据保存到数据库中对应的用户信息中
            form.save()
            return redirect('/num/list/')

        # 数据校验不合法时，将页面返回到当前编辑页面
        context = {
            "form": form
        }
        return render(request, 'num_edit.html', context)