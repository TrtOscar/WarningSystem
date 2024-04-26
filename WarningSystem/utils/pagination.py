"""
自定义分页组件，以后想要使用，遵循以下步骤
1. 在视图函数中导入Pagination类
2. 在视图函数中实例化Pagination类，传入request和queryset
3. 在视图函数中获取page_queryset和page_string
4. 在视图函数中将page_queryset和page_string传入render函数
5. 在模板中使用page_queryset展示数据
6. 在模板中使用page_string展示页码
示例代码如下：
def student_list(request):
    # 1.根据自己的情况筛选数据
    queryset = StuInfo.objects.all()

    # 2.实例化Pagination类
    page_object = Pagination(request, queryset)

    # 3.获取page_queryset和page_string
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        "search_data": search_data,
        "queryset": page_queryset,  # 分完页的数据
        "page_string": page_string,  # 页码
    }

    # 4.将page_queryset和page_string传入render函数
    return render(request, 'student_list.html', context)


在html页面中：
<ul class="pagination" style="float: left">
        {{ page_string }}
</ul>
"""
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request:请求的对象
        :param queryset:符合条件的数据（根据这个数据进行分页处理）
        :param page_size:每页显示多少数据
        :param page_param:在url中的页码参数，例如/student/list/?page=2
        :param plus:显示当前页的前几页和后几页
        """

        from django.http.request import QueryDict
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        # 当前页
        self.page = page
        # 每页显示的数据条数
        self.page_size = page_size

        # 根据用户想要访问的页码，计算起止位置
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()
        # 计算总页码
        total_page_count, div = divmod(total_count, page_size)  # divmod()函数返回商和余数
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出，显示当前页的前5页，后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 总页数小于等于11
            start_page = 1
            end_page = self.total_page_count
        else:
            # 总页数大于11
            # 当前页<5
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页>5
                # 当前页+5>总页数
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])

        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page" style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
                                       type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
        """

        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))

        return page_string
