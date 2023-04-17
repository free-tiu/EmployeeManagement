from django.shortcuts import render, redirect
from app01.models import Department, UserInfo
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


# 用户管理
def user_list(request):
    """ 用户列表 """
    user_lists = UserInfo.objects.all().count()
    # 获取所有用户信息
    queryset = UserInfo.objects.all()

    # 添加分页
    page_object = Pagination(request, queryset, page_size=10)     # 实例化分页组件

    context = {
        "user_lists": user_lists,
        # 分完页后的数据
        "page_queryset": page_object.page_queryset,
        # 生成的页码
        "pageNums": page_object.html()
    }

    return render(request, 'user_list.html', context)


def user_add(request):
    """ 添加用户（原始方式） """
    if request.method == 'GET':
        # 获取所有性别
        gender_choices = UserInfo.gender_choices
        # 获取所有部门信息
        depart_data = Department.objects.all()

        context = {
            'gender_choices': gender_choices,
            'depart_data': depart_data
        }

        return render(request, 'user_add.html', context)

    # 获取用户提交的数据
    if request.method == 'POST':
        name = request.POST.get('user')
        age = request.POST.get('age')
        gender = request.POST.get('sex')
        depart_id = request.POST.get('dp')
        account = request.POST.get('ac')
        password = request.POST.get('pwd')
        create_time = request.POST.get('ctime')

        # 将获取到的数据保存到数据库中
        UserInfo.objects.create(
            name=name, age=age, gender=gender,
            depart_id=depart_id, account=account,
            password=password, create_time=create_time
        )

        return redirect('/user/list/')


def user_add_model(request):
    """ 添加用户（使用ModelForm方式） """
    if request.method == 'GET':
        # 表单实例化
        form = UserModelForm()
        context = {'form': form}
        return render(request, 'user_add_model.html', context)

    # 获取用户提交的数据，并且对数据进行校验
    if request.method == 'POST':
        form = UserModelForm(data=request.POST)
        # 对提交的表单中的数据进行逐一校验
        if form.is_valid():
            # 校验成功获取到的数据
            success_data = form.cleaned_data

            print(success_data)     # 测试输出
            # 将合法的数据保存到数据库中
            form.save()

            return redirect('/user/list/')
        # 数据校验失败
        context = {"form": form}
        return render(request, 'user_add_model.html', context)


def user_edit(request, uid):
    """ 用户编辑 """
    # 根据ID查询到对应需要修改的用户信息
    userData = UserInfo.objects.filter(id=uid).first()

    if request.method == 'GET':
        # 将获取到的用户信息作为默认值放到input输入框中
        form = UserModelForm(instance=userData)

        context = {
            "form": form
        }
        return render(request, 'user_edit.html', context)

    if request.method == 'POST':
        # 对用户提交过来的数据进行校验    instance=userData => 当前操作的用户对象信息
        form = UserModelForm(data=request.POST, instance=userData)
        if form.is_valid():
            # 保存除了用户输入提交过来的信息
            # form.instance.字段名 = 值

            # 数据校验成功后将数据保存到数据库中对应的用户信息中
            form.save()
            return redirect('/user/list')

        # 数据校验不合法时，将页面返回到当前编辑页面
        context = {
            "form": form
        }
        return render(request, 'user_edit.html', context)


def user_del(request, uid):
    """ 删除用户 """
    UserInfo.objects.filter(id=uid).delete()

    return redirect('/user/list')
