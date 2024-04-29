from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除不需要登录就能访问的url
        if request.path_info in ["/login/", "/register/"]:
            return None
        # 1. 读取当前用户的session信息，若能读取到，说明已经登录过，可以继续访问
        info_dict = request.session.get("info")
        if info_dict:
            print("当前用户已登录，用户信息为：", info_dict)
            return None
        # 2. 没有登录，回到登录页面
        return redirect("/login/")
