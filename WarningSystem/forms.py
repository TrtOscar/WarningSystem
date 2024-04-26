"""
ModelForm表单
"""

from django import forms
from django.core.exceptions import ValidationError

from WarningSystem.models import StuInfo, TeacherInfo, AdminInfo
from WarningSystem.utils.bootstrap import BootStrapModelFrom
from WarningSystem.utils.encrypt import md5


class StudentInfoModelForm(BootStrapModelFrom):
    stuId = forms.CharField(label="学号", min_length=12)

    class Meta:
        model = StuInfo
        fields = ['stuId', 'name', 'password']
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }


class StudentScoreModelForm(BootStrapModelFrom):
    class Meta:
        model = StuInfo
        fields = ['assignScore1', 'assignScore2', 'assignScore3', 'assignScore4', 'assignScore5', 'examScore1',
                  'examScore2', 'examScore3']


class TeacherInfoModelForm(BootStrapModelFrom):
    teacherId = forms.CharField(label="工号", min_length=12)

    class Meta:
        model = TeacherInfo
        fields = ['teacherId', 'name', 'password']
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"})
        }


class AdminInfoModelForm(BootStrapModelFrom):
    adminId = forms.CharField(label="工号", min_length=5)
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = AdminInfo
        fields = ['adminId', 'name', 'password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def clean_password(self):
        # 对密码进行加密
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        # 获取加密后的密码
        pwd = self.cleaned_data.get("password")
        # 确认输入的密码
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("两次密码不一致，请重新输入")
        return confirm

