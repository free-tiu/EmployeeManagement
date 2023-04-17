from django.shortcuts import render, redirect

from app01.models import Admin
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app01.utils.pagination import Pagination


def admin_list(request):
    """ 管理员列表 """

    # info_dict = request.session["info"]
    # print(info_dict["id"])

    # 判断当前访问用户是否已登录
    info = request.session.get("info")      # 获取请求中的cookie随机字符串
    # print(info)     # 测试输出
    if not info:    # 未登录
        return redirect('/login')

    # 统计管理员人数
    admin_count = Admin.objects.all().count()
    # 获取所有管理员信息
    queryset = Admin.objects.all()
    # 实例化分页组件
    page_object = Pagination(request, queryset, page_size=7)
    # 需要传到前端的数据
    context = {
        "admin_count": admin_count,
        "queryset": page_object.page_queryset,      # 分完页的数据
        "pageNums": page_object.html()              # 生成数据
    }

    return render(request, 'admin_list.html', context)


def admin_add(request):
    """ 管理员添加 """
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        context = {
            "title": title,
            "form": form,
        }
        return render(request, 'change.html', context)

    if request.method == "POST":
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            # print(form.cleaned_data)        # 获取验证通过的信息
            form.save()
            return redirect('/admin/list/')

        context = {
            "title": title,
            "form": form,
        }
        return render(request, 'change.html', context)


def admin_del(request, nid):
    Admin.objects.filter(id=nid).delete()

    return redirect('/admin/list/')


def admin_edit(request, nid):
    """ 管理员编辑 """
    # filter(id=nid)如果能获取到则返回一个对象，反之则返回None
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        context = {"msg": "数据不存在"}
        return render(request, 'error.html', context)
    else:
        pass

    title = "编辑管理员"

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        context = {"title": title, "form": form}
        return render(request, 'change.html', context)

    if request.method == 'POST':
        form = AdminEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')

        context = {"title": title, "form": form}
        return render(request, 'change.html', context)


def admin_reset(request, nid):
    """ 密码重置 """
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = "重置密码 - {}".format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        context = {"title": title, "form": form}
        return render(request, 'change.html', context)

    if request.method == 'POST':
        form = AdminResetModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            form.save()
            return redirect('/admin/list/')

        context = {
            "form": form, "title": title
        }
        return render(request, 'change.html', context)






