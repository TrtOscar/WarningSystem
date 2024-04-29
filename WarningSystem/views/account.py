from django.shortcuts import render, redirect
from django import forms

from WarningSystem.models import StuInfo, TeacherInfo, AdminInfo
from WarningSystem.utils.encrypt import md5


class LoginForm(forms.Form):
    userId = forms.CharField(
        label="用户ID",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入用户ID"
            }
        )
    )
    password = forms.CharField(
        label="密码",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入密码"
            }
        )
    )
    role = forms.ChoiceField(
        label="角色",
        choices=((0, "学生"), (1, "教师"), (2, "管理员")),
        widget=forms.RadioSelect()
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        role = cleaned_data.get("role")

        # 如果角色为管理员，加密密码
        if role == '2':
            cleaned_data["password"] = md5(password)
        return cleaned_data

    # def clean_password(self):
    #     pwd = self.cleaned_data.get("password")
    #     return md5(pwd)


def login(request):
    """登录页面"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证通过，获取到的用户ID和密码
        # 例：{'userId': '12345', 'password': '123456', 'role': '2'} 2代表管理员
        print(form.cleaned_data)
        userId = form.cleaned_data.get('userId')
        password = form.cleaned_data.get('password')
        role = form.cleaned_data.get('role')

        # 构建查询的基础字典
        query_dict = {
            'password': password
        }

        # 根据角色动态选择数据表和添加对应的ID查询键
        if role == '0':  # 学生
            model = StuInfo
            query_dict['stuId'] = userId
        elif role == '1':  # 教师
            model = TeacherInfo
            query_dict['teacherId'] = userId
        else:  # 管理员
            model = AdminInfo
            query_dict['adminId'] = userId

        # 使用**query_dict进行查询
        user = model.objects.filter(**query_dict).first()
        if not user:
            form.add_error("userId", "用户ID或密码错误")
            return render(request, 'login.html', {"form": form})

        # 用户名和密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie中，再写入到session中
        request.session['info'] = {'id': user.id, 'name': user.name, 'role': user.role}
        # 根据用户角色跳转到不同的页面
        if user.role == 2:
            return redirect("/admin/list/")
        elif user.role == 1:
            return redirect("/teacher/homepage/")
        return redirect("/student/homepage/")

    return render(request, 'login.html', {"form": form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login/")
