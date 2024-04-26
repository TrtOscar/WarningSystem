# 教师列表
from django.shortcuts import render, redirect

from WarningSystem import models
from WarningSystem.forms import TeacherInfoModelForm
from WarningSystem.models import TeacherInfo
from WarningSystem.utils.pagination import Pagination


def teacher_list(request):
    """搜索"""

    # 储存搜索条件
    data_dict1 = {}  # 工号查询
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict1["teacherId__contains"] = search_data

    # 打印查询结果
    print(TeacherInfo.objects.filter(**data_dict1))

    """分页"""
    queryset = TeacherInfo.objects.filter(**data_dict1).order_by("teacherId")
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "search_data": search_data,
        "queryset": page_queryset,  # 分完页的数据
        "page_string": page_string,  # 页码
    }

    """数据展示"""

    # 获取数据库中教师信息
    data_list = TeacherInfo.objects.filter(**data_dict1).order_by("teacherId")
    print(data_list)

    for item in data_list:
        print(item.teacherId, item.name, item.password, item.role)

    return render(request, 'teacher_list.html', context)


# 教师添加
def teacher_add(request):
    if request.method == "GET":
        form = TeacherInfoModelForm()
        return render(request, 'teacher_add.html', {'form': form})

    # 用户POST提交数据，数据校验
    form = TeacherInfoModelForm(data=request.POST)
    if form.is_valid():
        # 若数据合法，将数据添加到数据库
        print(form.cleaned_data)
        form.save()
        return redirect('/teacher/list/')
    else:
        # 校验失败，展示错误信息
        print(form.errors)
        return render(request, 'teacher_add.html', {'form': form})


# 教师删除
def teacher_delete(request):
    # 获取用户提交的数据
    teacherId = request.GET.get("teacherId")

    # 从数据库中删除数据
    TeacherInfo.objects.filter(teacherId=teacherId).delete()

    # 跳转到教师列表页面
    return redirect('/teacher/list/')


# 教师编辑
def teacher_edit(request, nid):
    row_object = models.TeacherInfo.objects.filter(id=nid).first()
    # 如果没有获取到
    if not row_object:
        return redirect('/teacher/list/')
    if request.method == "GET":
        # 根据id获取要编辑的教师信息
        form_GET = TeacherInfoModelForm(instance=row_object)
        return render(request, 'teacher_edit.html', {'form': form_GET})

    form_POST = TeacherInfoModelForm(data=request.POST, instance=row_object)
    if form_POST.is_valid():
        # 若数据合法，将数据添加到数据库
        print(form_POST.cleaned_data)
        form_POST.save()
        return redirect('/teacher/list/')
    else:
        print(form_POST.errors)
        return render(request, 'teacher_edit.html', {'form': form_POST})


# 教师重置密码
def teacher_reset(request, nid):
    row_object = models.TeacherInfo.objects.filter(id=nid).first()
    # 如果没有获取到
    if not row_object:
        return redirect('/teacher/list/')
    row_object.password = "123456"
    row_object.save()
    return redirect('/teacher/list/')


# 教师主页
def teacher_homepage(request):
    return render(request, 'teacher_homepage.html')
