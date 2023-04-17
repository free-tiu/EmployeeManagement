"""
封装分页组件
    后期需要使用此组件时，需进行如下操作：
    一、在views.py视图函数中
        def num_list(request):
            # 1、根据个人实际情况获取筛选出需要的数据
            queryset = PrettyNum.objects.all()【或filter()】
            # 2、实例化分页组件对象
            page_object = Pagination(request, queryset)     # 可以直接将此写到context中对应的键值中
            page_queryset = page_object.page_queryset
            pageNums = page_object.html()

            context = {
                "page_queryset": page_queryset,     # 分完页后的数据
                "pageNums": pageNums                # 生成的页码
            }
            return render(request, 'num_list.html', context)
    二、在HTML页面中
        <!-- 获取数据 -->
        {% for i in page_queryset %}
            {{ i.xxx }}
        {% endfor %}
        
        <!-- 分页，具体标签根据实际情况修改 -->
        <div>
            <ul class="pagination" id="position">
                {{ pageNums }}
            </ul>
        </div>
"""
import copy

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=3):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据该数据进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例：/num/list/?page=6
        :param plus: 显示当前页的 前plus页或后plus页
        """

        # =============== 分页的同时保留搜索条件进行分页 ===============
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param

        # 获取当前页
        page = request.GET.get(page_param, "1")
        # 处理传过来的页码数是否为字符串或者负数等
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        # 当前页
        self.page = page
        # 长度
        self.page_size = page_size
        # 起始号码数据条数
        self.start = (page - 1) * page_size
        # 结束号码数据条数
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 获取总数据条数
        total = queryset.count()
        # 计算总页码数，当div余数大于0时，页码数+1
        total_page_count, div = divmod(total, page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count
        # 除当前页外，还显示前plus页和后plus页
        self.plus = plus


    def html(self):
        # 设置极值 —— 即当页码为1时，不会显示前5页(会有负值)；当页码为最后一页时,不会继续往后显示5页(会产生多余的页码数)
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1  # 显示第一页
            end_page = self.total_page_count  # 显示最后一页
        else:
            # 设置 当前页小于5时 的极值
            if self.page <= self.plus:
                # 起始值固定
                start_page = 1
                end_page = self.page + self.plus + 1
            else:  # 设置 当前页大于5时 的极值
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count  # 结束页为总页码
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        pageNum = []

        self.query_dict.setlist(self.page_param, [1])
        # 设置首页
        pageNum.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prePage = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
            pageNum.append(prePage)
        else:  # 当当前页为1时，点击上一页按钮，页面依旧为第1页
            self.query_dict.setlist(self.page_param, [1])
            prePage = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
            pageNum.append(prePage)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            # 对当前页页码进行标记
            if i == self.page:
                # 将页码数添加到标签中格式化
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)

            # 将格式化好的标签添加到列表中
            pageNum.append(ele)

        # 下一页翻页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prePage = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
            pageNum.append(prePage)
        else:  # 当当前页为1时，点击上一页按钮，页面依旧为第1页
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prePage = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
            pageNum.append(prePage)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        pageNum.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

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

        return pageNums









