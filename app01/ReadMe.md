## 员工管理系统
### 数据库方面
1. 用户表存储，使用名称还是ID
    - 名称 —— 直接是各个部门名称
    - ID —— 对应部门表中的ID
2. 部门ID约束
    - 只能是部门中已存在的ID
    - 使用以下进行约束
    ```
       models.ForeignKey(to="需要对应的表名", to_field="需要对应的字段")
    ```
    - 当部门表被删除时，使用了外键关联后的两种情况
        - 级联删除
            ```python
            models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
            ```
        - 置空
            ```python
            models.ForeignKey(to="Department", to_field="id", on_delete=models.SET_NULL)
            ```

#### 补充
##### on_update 和 on_delete 后面可以跟的词语有四个
```
1. no_action：表示 不做任何操作，
2. SET_NULL：表示在外键表中将相应字段设置为null
3. SET_DEFAULT：表示设置为默认值
4. CASCADE：表示级联操作，就是说，如果主键表中被参考字段更新，外键表中也更新，主键表中的记录被删除，外键表中改行也相应删除
```
##### JS 弹窗
```html
<script>
    if(typeof jQuery!='undefined'){
        alert("jquery加载成功")
    }else {
        alert("jquery加载失败")
    }
</script>
```


### 视图函数方面
#### `request`
```
# 拼接url中的参数
request.GET.urlencode()

# 深拷贝
get_obj = copy.deepcopy(request.GET)
```

#### 关于用户登录
- 判断用户是否已登录，并将cookie随机字符串取出比对
```
# 判断当前访问用户是否已登录
    info = request.session.get("info")  # 获取请求中的cookie随机字符串
    if not info:  # 未登录
        return redirect('/login')
```


