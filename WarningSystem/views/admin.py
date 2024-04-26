# 管理员列表
from django.shortcuts import render, redirect

from WarningSystem import models
from WarningSystem.forms import AdminInfoModelForm
from WarningSystem.models import AdminInfo
from WarningSystem.utils.encrypt import md5
from WarningSystem.utils.pagination import Pagination


def admin_list(request):
    """搜索"""

    # 储存搜索条件
    data_dict1 = {}  # 工号查询
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict1["adminId__contains"] = search_data

    # 打印查询结果
    print(AdminInfo.objects.filter(**data_dict1))

    """分页"""
    queryset = AdminInfo.objects.filter(**data_dict1).order_by("adminId")
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "search_data": search_data,
        "queryset": page_queryset,  # 分完页的数据
        "page_string": page_string,  # 页码
    }

    """数据展示"""

    # 获取数据库中管理员信息
    data_list = AdminInfo.objects.filter(**data_dict1).order_by("adminId")
    print(data_list)

    for item in data_list:
        print(item.adminId, item.name, item.password, item.role)

    return render(request, 'admin_list.html', context)


# 教师添加
def admin_add(request):
    if request.method == "GET":
        form = AdminInfoModelForm()
        return render(request, 'admin_add.html', {'form': form})

    # 用户POST提交数据，数据校验
    form = AdminInfoModelForm(data=request.POST)
    if form.is_valid():
        # 若数据合法，将数据添加到数据库
        print(form.cleaned_data)
        form.save()
        return redirect('/admin/list/')
    else:
        # 校验失败，展示错误信息
        print(form.errors)
        return render(request, 'admin_add.html', {'form': form})


# 管理员删除
def admin_delete(request):
    # 获取用户提交的数据
    adminId = request.GET.get("adminId")

    # 从数据库中删除数据
    AdminInfo.objects.filter(adminId=adminId).delete()

    # 跳转到管理员列表页面
    return redirect('/admin/list/')


# 管理员编辑
def admin_edit(request, nid):
    row_object = models.AdminInfo.objects.filter(id=nid).first()
    # 如果没有获取到
    if not row_object:
        return redirect('/admin/list/')
    if request.method == "GET":
        # 根据id获取要编辑的管理员信息
        form_GET = AdminInfoModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form': form_GET})

    form_POST = AdminInfoModelForm(data=request.POST, instance=row_object)
    if form_POST.is_valid():
        # 若数据合法，将数据添加到数据库
        print(form_POST.cleaned_data)
        form_POST.save()
        return redirect('/admin/list/')
    else:
        print(form_POST.errors)
        return render(request, 'admin_edit.html', {'form': form_POST})


# 管理员重置密码
def admin_reset(request, nid):
    row_object = models.AdminInfo.objects.filter(id=nid).first()
    # 如果没有获取到
    if not row_object:
        return redirect('/admin/list/')
    row_object.password = md5("123456")
    row_object.save()
    return redirect('/admin/list/')
