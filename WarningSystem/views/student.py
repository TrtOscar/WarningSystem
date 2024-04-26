# 学生列表
from django.shortcuts import render, redirect

from WarningSystem import models
from WarningSystem.forms import StudentInfoModelForm, StudentScoreModelForm
from WarningSystem.models import StuInfo
from WarningSystem.utils.pagination import Pagination


def student_list(request):
    """搜索"""

    # 储存搜索条件
    data_dict1 = {}  # 学号查询
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict1["stuId__contains"] = search_data

    # 打印查询结果
    print(StuInfo.objects.filter(**data_dict1))

    """分页"""
    queryset = StuInfo.objects.filter(**data_dict1).order_by("stuId")
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()

    context = {
        "search_data": search_data,
        "queryset": page_queryset,  # 分完页的数据
        "page_string": page_string,  # 页码
    }

    """数据展示"""

    # 获取数据库中学生信息
    data_list = StuInfo.objects.filter(**data_dict1).order_by("stuId")
    print(data_list)

    for item in data_list:
        print(item.stuId, item.name, item.password, item.role)

    return render(request, 'student_list.html', context)


# 学生添加
def student_add(request):
    if request.method == "GET":
        form = StudentInfoModelForm()
        return render(request, 'student_add.html', {'form': form})

    # 用户POST提交数据，数据校验
    form = StudentInfoModelForm(data=request.POST)
    if form.is_valid():
        # 若数据合法，将数据添加到数据库
        print(form.cleaned_data)
        form.save()
        return redirect('/student/list/')
    else:
        # 校验失败，展示错误信息
        print(form.errors)
        return render(request, 'student_add.html', {'form': form})


# 学生删除
def student_delete(request):
    # 获取学号
    stuId = request.GET.get("stuId")

    # 从数据库中删除数据
    StuInfo.objects.filter(stuId=stuId).delete()

    # 重定向到学生列表页面
    return redirect('/student/list/')


# 学生编辑
def student_edit(request, nid):
    row_object = models.StuInfo.objects.filter(id=nid).first()
    # 如果没有获取到
    if not row_object:
        return redirect('/student/list/')
    if request.method == "GET":
        # 根据id获取要编辑的学生信息
        form_GET = StudentScoreModelForm(instance=row_object)
        return render(request, 'student_edit.html', {'form': form_GET})

    form_POST = StudentScoreModelForm(data=request.POST, instance=row_object)
    if form_POST.is_valid():
        # 若数据合法，将数据添加到数据库
        print(form_POST.cleaned_data)
        form_POST.save()
        return redirect('/student/list/')
    else:
        print(form_POST.errors)
        return render(request, 'student_edit.html', {'form': form_POST})


# 学生重置密码
def student_reset(request, nid):
    row_object = models.StuInfo.objects.filter(id=nid).first()
    # 如果没有获取到
    if not row_object:
        return redirect('/student/list/')
    row_object.password = "123456"
    row_object.save()
    return redirect('/student/list/')


# 学生主页
def student_homepage(request):
    return render(request, 'student_homepage.html')
