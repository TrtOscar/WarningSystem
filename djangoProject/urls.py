"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from WarningSystem.views import admin, teacher, student, account

urlpatterns = [
    # path("admin/", admin.site.urls),

    # 用户管理相关
    # 教师管理相关接口
    path('teacher/list/', teacher.teacher_list),  # 教师列表
    path('teacher/add/', teacher.teacher_add),  # 教师添加
    path('teacher/delete/', teacher.teacher_delete),  # 教师删除
    path('teacher/<int:nid>/edit/', teacher.teacher_edit),  # 教师删除
    path('teacher/<int:nid>/reset/', teacher.teacher_reset),  # 教师重置密码
    # 学生管理相关接口
    path('student/list/', student.student_list),  # 学生列表
    path('student/add/', student.student_add),  # 学生添加
    path('student/delete/', student.student_delete),  # 学生删除
    path('student/<int:nid>/edit/', student.student_edit),  # 学生编辑
    path('student/<int:nid>/reset/', student.student_reset),  # 学生重置密码
    # 管理员相关接口
    path('admin/list/', admin.admin_list),  # 管理员列表
    path('admin/add/', admin.admin_add),  # 管理员添加
    path('admin/delete/', admin.admin_delete),  # 管理员删除
    path('admin/<int:nid>/edit/', admin.admin_edit),  # 管理员编辑
    path('admin/<int:nid>/reset', admin.admin_reset),  # 管理员重置密码

    # 登录以及注销相关
    path('login/', account.login),  # 登录
    path('logout/', account.logout),  # 注销

    # 主页相关
    path('student/homepage/', student.student_homepage),  # 学生主页
    path('teacher/homepage/', teacher.teacher_homepage),  # 教师主页

]
