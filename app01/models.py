from django.db import models


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(max_length=32, verbose_name='标题')

    # 将模型类以字符串的方式输出（面向对象）
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(max_length=32, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    age = models.IntegerField(verbose_name='年龄')
    # Decimal：准确的小数值，m是是数字总个数（符号不算），最大值为65；d是小数点后长度，最大值为30
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')

    # 外键约束 to="需要对应的表名", to_field="需要对应的字段"
    depart = models.ForeignKey(verbose_name="所属部门", to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)

    # 性别元组
    gender_choices = [
        (1, "男"),
        (2, "女"),
    ]
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name='号码', max_length=11)
    price = models.IntegerField(verbose_name='价格', default=0)

    level_choices = [
        (0, "级别暂定"),
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
    ]
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=0)

    status_choices = [
        (1, "已占用"),
        (2, "未使用"),
        (3, "暂定"),
    ]
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=3)


class Admin(models.Model):
    """ 管理员表 """
    username = models.CharField(verbose_name="账号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)

    def __str__(self):
        return self.username


class Task(models.Model):
    """ 任务模型 """
    title = models.CharField(verbose_name="标题", max_length=64)
    details = models.TextField(verbose_name="详细信息")
    # 任务级别
    level_choice = (
        (0, "暂定"),
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")
    )
    level = models.SmallIntegerField(verbose_name="任务级别", choices=level_choice, default=0)
    user = models.ForeignKey(verbose_name="任务负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单 """
    """
        订单号、商品名称、价格、状态（已支付/待支付）、用户ID
    """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choice = (
        (1, "已支付"),
        (2, "未支付")
    )
    status = models.SmallIntegerField(verbose_name="支付状态", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    """ 老板 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="城市名称", max_length=32)
    count = models.IntegerField(verbose_name="人口数")

    # 本质上在数据库中也是CharField，在ModelForm中会自动保存数据，不需要手动获取数据保存
    img = models.FileField(verbose_name="LOGO", max_length=128, upload_to='city/')









