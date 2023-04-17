import re

from django.core.exceptions import ValidationError

from app01.models import UserInfo, PrettyNum, Admin, Task, Order
from django import forms
from app01.utils.bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5

from app01.utils.bootstrap import BootstrapForm


class UserModelForm(BootstrapModelForm):
    # 进行数据校验
    # name = forms.CharField(min_length=2, label="用户名")

    class Meta:
        # 定义关联模型
        model = UserInfo

        # 定义需要在表单中展示的字段
        fields = ['name', 'password', 'age', 'gender', 'account', 'create_time', 'depart']
        # 给input标签添加样式
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "password": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "account": forms.TextInput(attrs={"class": "form-control"}),
            "create_time": forms.TextInput(attrs={"class": "form-control"}),
            "depart": forms.Select(attrs={"class": "form-control"}),
        }


class PrettyNumModelForm(forms.ModelForm):
    # 添加校验规则 —— 对电话号码进行验证
    # mobile = forms.CharField(
    #     label="手机号",
    #     # 编写正则表达式
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误！')],
    #     error_messages={'required': '手机号码输入不能为空！'},
    #     # 相当于widgets
    #     widget=forms.TextInput(attrs={"class": "form-control"})
    # )

    class Meta:
        # 定义关联模型
        model = PrettyNum
        # 定义需要在表单中展示的字段
        # fields = ['mobile', 'price', 'level', 'status']
        # 获取所有字段
        fields = "__all__"
        # 获取字段并排除字段
        # exclude = ['level']

        # 给input标签添加样式
        widgets = {
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    # 钩子函数
    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]
        # 校验手机号码格式是否正确
        mobile_re = re.compile(r'^(13[0-9]|15[012356789|17[678]|18[0-9]|14[57])[0-9]{8}$')
        if not mobile_re.match(mobile):
            raise ValidationError('手机号码格式错误！')

        # 判断当前号码是否存在
        exists = PrettyNum.objects.filter(mobile=mobile).exists()
        if exists:  # 当前号码已存在
            raise ValidationError("该手机号码已存在！")

        return mobile


class PrettyEditNumModelForm(forms.ModelForm):
    mobile = forms.CharField(
        # 使电话这一栏为禁用状态，既只能看不允许被修改
        disabled=True, label="号码", widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        # 定义关联模型
        model = PrettyNum
        # 定义需要在表单中展示的字段
        fields = ['mobile', 'price', 'level', 'status']
        # 给input标签添加样式
        widgets = {
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    # 钩子函数
    def clean_mobile(self):
        # 获取当前所编辑的数据的ID
        exclude = self.instance.pk

        mobile = self.cleaned_data["mobile"]
        # 判断当前号码是否存在（排除除了自已以外的手机号，在剩下的手机号中查找是否有重复）
        exists = PrettyNum.objects.exclude(id=exclude).filter(mobile=mobile).exists()
        if exists:  # 当前号码已存在
            raise ValidationError("该手机号码已存在！")

        return mobile


class AdminModelForm(BootstrapModelForm):
    """ 管理员 """
    """
        继承BootstrapModelForm基类，可继承也可自定义
    """
    # 自定义添加一个确认密码的输入框
    confirm_password = forms.CharField(
        label="确认密码",
        # render_value=True => 让密码框中的密码在输入不一致时依旧保留在密码框中
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = Admin

        fields = ['username', 'password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # 对密码进行MD5加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 钩子方法
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")     # 第一次密码
        confirm = self.cleaned_data.get("confirm_password")     # 第二次输入的密码
        confirm = md5(confirm)      # 加密
        # 判断两次密码是否相等
        if confirm != pwd:
            raise ValidationError("密码不一致！")

        # 该字段返回 是用于保存到数据库中
        return confirm


class AdminEditModelForm(BootstrapModelForm):
    """ 管理员编辑 """
    class Meta:
        model = Admin
        fields = ['username']


class AdminResetModelForm(BootstrapModelForm):
    """ 重置密码 """
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # 对密码进行MD5加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")

        # 验证修改的密码是否与原来的密码相同
        md5_pwd = md5(pwd)
        nid = self.instance.pk      # 获取当前编辑数据的ID
        exists = Admin.objects.filter(id=nid, password=md5_pwd).exists()
        if exists:
            raise ValidationError("新密码不能与旧密码一致！")

        return md5_pwd

    # 钩子方法
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")     # 第一次密码
        confirm = self.cleaned_data.get("confirm_password")     # 第二次输入的密码
        confirm = md5(confirm)      # 加密
        # 判断两次密码是否相等
        if confirm != pwd:
            raise ValidationError("密码不一致！")

        # 该字段返回 是用于保存到数据库中
        return confirm


class LoginForm(BootstrapForm):
    """ 用户登录 """
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True       # 设置为必填项
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True       # 设置为必填项
    )
    # 验证码
    code = forms.CharField(
        label="请输入验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        # 获取密码
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "details": forms.TextInput
            # "detail": forms.Textarea
        }


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = Order
        # 显示除了oid以外的字段
        exclude = ["oid", "admin"]






