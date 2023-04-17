from django.utils.safestring import mark_safe

from app01.models import PrettyNum


def pages(request):
# ========================== 查询功能 ==========================
    data_dict = {}
    # 获取前端提交的搜索关键字
    value = request.GET.get("queryKey", "")
    if value:   # 当获取不为空时
        # 将搜索关键字赋值给mobile__contains
        data_dict["mobile__contains"] = value

# ========================== 分页功能 ==========================
    # 获取页码数，默认从第1页开始
    page = int(request.GET.get('page', 1))  # 当前页
    # 每页显示条数
    pageSize = 10
    # 计算每页显示条数位置（条数可自定义）
    start = (page - 1) * pageSize      # 起始号码数据条数
    end = page * pageSize             # 结束号码数据条数

    # ========================== 手机号列表展示 ==========================
    # 当data_dict为空时，查询全部手机号，当data_dict不为空时，则查询符合条件的手机号
    numList = PrettyNum.objects.filter(**data_dict).order_by("level")[start:end]

    # ========================== 分页模块-start ==========================
    # 获取总数据条数
    total = PrettyNum.objects.filter(**data_dict).order_by("level").count()
    # 计算总页码数，当div余数大于0时，页码数+1
    totalPage, div = divmod(total, pageSize)
    if div:
        totalPage += 1

    # 页码
    pageNum = []

    # 设置首页
    pageNum.append('<li><a href="/num/list/?page={}">首页</a></li>'.format(1))

    # ======= 设置翻页(上一页) =========
    if page > 1:
        prePage = '<li><a href="/num/list/?page={}">上一页</a></li>'.format(page - 1)
        pageNum.append(prePage)
    else:   # 当当前页为1时，点击上一页按钮，页面依旧为第1页
        prePage = '<li><a href="/num/list/?page={}">上一页</a></li>'.format(1)
        pageNum.append(prePage)

    # 自定义页面显示页码数量 —— 即页面的分页按钮只显示当前页和当前页的前5页和后5页
    plus = 3    # 自定义显示的前n页和后n页

    # 设置极值 —— 即当页码为1时，不会显示前5页(会有负值)；当页码为最后一页时,不会继续往后显示5页(会产生多余的页码数)
    if totalPage <= 2*plus+1:
        start_page = 1  # 显示第一页
        end_page = totalPage  # 显示最后一页
    else:
        # 设置 当前页小于5时 的极值
        if page <= plus:
            # 起始值固定
            start_page = 1
            end_page = page + plus + 1
        else:   # 设置 当前页大于5时 的极值
            if (page + plus) > totalPage:
                start_page = totalPage - 2 * plus
                end_page = totalPage    # 结束页为总页码
            else:
                start_page = page - plus
                end_page = page + plus

    for i in range(start_page, end_page + 1):
        # 对当前页页码进行标记
        if i == page:
            # 将页码数添加到标签中格式化
            ele = '<li class="active"><a href="/num/list/?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="/num/list/?page={}">{}</a></li>'.format(i, i)

        # 将格式化好的标签添加到列表中
        pageNum.append(ele)

    # 下一页翻页
    if page < totalPage:
        prePage = '<li><a href="/num/list/?page={}">下一页</a></li>'.format(page + 1)
        pageNum.append(prePage)
    else:   # 当当前页为1时，点击上一页按钮，页面依旧为第1页
        prePage = '<li><a href="/num/list/?page={}">下一页</a></li>'.format(totalPage)
        pageNum.append(prePage)

    # 尾页
    pageNum.append('<li><a href="/num/list/?page={}">尾页</a></li>'.format(totalPage))

    # 输入页码跳转
    search_page = """
        <li>
            <form method="get" id="position_1">
                <div class="input-group" style="width: 200px;">
                    <input type="text" name="page" class="form-control" placeholder="请输入页码">
                    <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">跳转</button>
                    </span>
                </div>
            </form>
        </li>
    """
    pageNum.append(search_page)

    # 使用mark_safe标记
    pageNums = mark_safe("".join(pageNum))
    # ========================== 分页模块-end ==========================