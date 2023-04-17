from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """ 登录中间件 """
    def process_request(self, request):
        """ 该方法没有返回值的情况下，会继续往下走； 如果有返回值，则将返回值返回到页面中，而不会继续往下 """
        # 将不需要登录就可以直接访问的页面排除在外
        url_list = ["/login/", "/image/code/"]
        if request.path_info in url_list:
            # 返回一个空值，继续往下走
            return

        # 获取当前访问的用户的session信息，如有 则为已登录，反之则不能继续
        info_dict = request.session.get("info")
        if info_dict:
            return
        else:
            return redirect('/login/')








