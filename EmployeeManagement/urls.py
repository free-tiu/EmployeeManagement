"""EmployeeManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from app01.views import depart, user, pretty, admin, account, task, order, chart, file

urlpatterns = [
    # path('admin/', admin.site.urls),

    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
    path('admin/<int:nid>/delete/', admin.admin_del),
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_del),
    path('depart/<int:nid>/edit/', depart.depart_edit),
    path('depart/upload/', depart.depart_upload),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    # 使用ModelForm进行用户添加
    path('user/add_model/', user.user_add_model),
    path('user/<int:uid>/delete/', user.user_del),
    path('user/<int:uid>/edit/', user.user_edit),

    # 靓号管理
    path('num/list/', pretty.num_list),
    # 使用ModelForm进行用户添加
    path('num/add_model/', pretty.num_add_model),
    path('num/<int:nid>/delete/', pretty.num_del),
    path('num/<int:nid>/edit/', pretty.num_edit),

    # 用户登录、 注销
    path('login/', account.login),
    path('logout/', account.logout),

    # 个人资料
    # path('base/data/', account.data),
    # 我的信息
    # path('messege/', account.messege),

    # 验证码
    path('image/code/', account.image_code),

    # 测试Ajax
    path('task/list/', task.task_list),
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),

    # 订单
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),

    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/default/', chart.chart_default),
    path('chart/line/', chart.chart_line),
    path('chart/bar/', chart.chart_bar),
    path('chart/pie/', chart.chart_pie),

    # 文件上传下载
    path('file/list/', file.upload_list),
    path('file/download/', file.download),
    path('file/form/', file.upload_form),       # Form文件上传

    # 城市管理（上传）
    path('city/list/', file.city_list),
    path('city/add/', file.city_add),      # ModelForm文件上传
]
