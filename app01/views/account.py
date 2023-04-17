from django.http import HttpResponse
from django.shortcuts import render, redirect

from app01.models import Admin
from app01.utils.code import check_code
from app01.utils.form import LoginForm
from io import BytesIO


def login(request):
    """ 用户登录 """
    if request.method == 'GET':
        form = LoginForm()      # 实例化

        context = {'form': form}
        return render(request, 'login.html', context)

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # 验证码校验
            user_input_code = form.cleaned_data.pop('code')
            code = request.session.get('image_code', "")
            # 判断用户输入的验证码与生成的验证码是否一致
            if code.upper() != user_input_code.upper():
                form.add_error("password", "验证码输入错误!")
                return render(request, 'login.html', {"form": form})

            # 数据库校验账号和密码是否正确,获取用户对象
            admin_obj = Admin.objects.filter(**form.cleaned_data).first()
            if not admin_obj:
                # 密码错误时的错误提示信息
                print(form.cleaned_data.get("password"))
                form.add_error("password", "用户名或密码错误!")
                return render(request, 'login.html', {"form": form})

            # 当用户名密码输入正确时，将用户信息及随机字符串写入到Session中
            request.session["info"] = {
                'id': admin_obj.id, 'name': admin_obj.username
            }
            # 重新设置session时限（保留七天）
            request.session.set_expiry(60 * 60 * 24 * 7)
            # 信息写入成功后（即登录成功）重定向
            return redirect("/admin/list")

        context = {'form': form}
        return render(request, 'login.html', context)


def image_code(request):
    """ 生成图片验证码 """
    # 调用pillow函数，生成图片
    img, code_str = check_code()
    # 写入到session中，便于后续获取验证码进行校验
    request.session['image_code'] = code_str
    # 设置时限（60S）
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


def logout(request):
    """ 用户注销 """
    # 将当前登录的用户的session清除
    request.session.clear()

    return redirect('/login')











