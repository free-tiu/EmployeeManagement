import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django import forms

from app01.models import Boss, City
from app01.utils.bootstrap import BootstrapForm, BootstrapModelForm


def upload_list(request):
    """ 文件列表、上传 """
    if request.method == "GET":
        return render(request, 'upload_list.html')

    if request.method == "POST":
        # print(request.POST)     # 请求中的数据
        # print(request.FILES)    # 请求发过来的文件

        file_object = request.FILES.get('avatar')  # 获取文件对象
        file_name = file_object.name  # 获取文件对象的名字

        # 获取文件内容
        f = open(file_name, mode='wb')
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()  # 文件读取完成后关闭

        return redirect('/file/list/')


def download(request):
    """ 文件下载 """

    return HttpResponse("2")


# Form —— 上传文件和数据
class UPForm(BootstrapForm):
    bootstrap_exclude_fields = ['img']      # 设置 上传图片所在标签 不加相关样式

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    """ 使用Form上传文件 """
    title = "Form文件上传"

    if request.method == "GET":
        form = UPForm()  # 实例化

        context = {
            "form": form, "title": title
        }
        return render(request, 'upload_form.html', context)

    if request.method == "POST":
        form = UPForm(data=request.POST, files=request.FILES)
        if form.is_valid():     # 获取到内容并验证通过后 处理每个字段的数据
            # 1、读取图片内容，写入到文件夹中并获取文件的路径
            img_obj = form.cleaned_data.get("img")
            # db_file_path = os.path.join("static", "img", img_obj.name)      # 设置数据库中的文件路径(保存到static下的img目录中)
            # file_path = os.path.join("media", db_file_path)  # 文件存储位置

            media_path = os.path.join("media", img_obj.name)  # 设置数据库中的文件路径(保存到根目录中的media下)
            f = open(media_path, mode='wb')
            for chunk in img_obj.chunks():  # 读取文件内容，每读一点就往文件内写如一点内容
                f.write(chunk)
            f.close()

            # 2、将获取到的文件路径写入到数据库中
            Boss.objects.create(
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                img=media_path,
            )
            return HttpResponse("数据成功写入数据库！")

        context = {
            "form": form, "title": title
        }
        return render(request, 'upload_form.html', context)


# ModelForm —— 上传文件和数据
class UPModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']      # 设置 上传图片所在标签 不加相关样式

    class Meta:
        model = City
        fields = "__all__"


# 城市管理
def city_list(request):
    if request.method == "GET":
        queryset = City.objects.all()

        context = {
            "queryset": queryset
        }
        return render(request, 'city_list.html', context)


def city_add(request):
    title = "添加城市"
    if request.method == "GET":
        form = UPModelForm()  # 实例化

        context = {
            "form": form, "title": title
        }
        return render(request, 'upload_form.html', context)

    if request.method == "POST":
        form = UPModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/city/list')

        context = {
            "form": form, "title": title
        }
        return render(request, 'upload_form.html', context)





