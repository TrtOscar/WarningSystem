from django.db import models
from django.forms import ModelForm


# 学生信息
class StuInfo(models.Model):
    # 角色标签，用数字区分，学生0，教师1，管理员2
    role = models.IntegerField(verbose_name="角色标签", default=0)

    # 学生学号，由12位数字组成
    stuId = models.CharField(verbose_name="学生学号", max_length=12, unique=True)

    # 学生姓名，由2-10位中文字符组成
    name = models.CharField(verbose_name="学生姓名", max_length=32)

    # 学生登录密码，由6-16位数字、字母、特殊字符组成
    password = models.CharField(verbose_name="密码", max_length=64, default="123456")

    # 学生第一次作业成绩，保留两位小数
    assignScore1 = models.DecimalField(verbose_name="作业成绩1", max_digits=5, decimal_places=2, default=0.0)

    # 学生第二次作业成绩，保留两位小数
    assignScore2 = models.DecimalField(verbose_name="作业成绩2", max_digits=5, decimal_places=2, default=0.0)

    # 学生第三次作业成绩，保留两位小数
    assignScore3 = models.DecimalField(verbose_name="作业成绩3", max_digits=5, decimal_places=2, default=0.0)

    # 学生第四次作业成绩，保留两位小数
    assignScore4 = models.DecimalField(verbose_name="作业成绩4", max_digits=5, decimal_places=2, default=0.0)

    # 学生第五次作业成绩，保留两位小数
    assignScore5 = models.DecimalField(verbose_name="作业成绩5", max_digits=5, decimal_places=2, default=0.0)

    # 学生第一次阶段考试成绩，保留两位小数
    examScore1 = models.DecimalField(verbose_name="考试成绩1", max_digits=5, decimal_places=2, default=0.0)

    # 学生第二次阶段考试成绩，保留两位小数
    examScore2 = models.DecimalField(verbose_name="考试成绩2", max_digits=5, decimal_places=2, default=0.0)

    # 学生期末考试成绩，保留两位小数
    examScore3 = models.DecimalField(verbose_name="期末成绩", max_digits=5, decimal_places=2, default=0.0)

    # 第一次预测成绩，保留两位小数
    predictScore1 = models.DecimalField(verbose_name="预测成绩1", max_digits=5, decimal_places=2, default=0.0)

    # 第二次预测成绩，保留两位小数
    predictScore2 = models.DecimalField(verbose_name="预测成绩2", max_digits=5, decimal_places=2, default=0.0)


# 教师信息
class TeacherInfo(models.Model):
    # 角色标签，用数字区分，学生0，教师1，管理员2
    role = models.IntegerField(default=1)

    # 教师工号，由12位数字组成
    teacherId = models.CharField(verbose_name="教师工号", max_length=12, unique=True)

    # 教师姓名，由2-10位中文字符组成
    name = models.CharField(verbose_name="教师姓名", max_length=32)

    # 教师登录密码，由6-16位数字、字母、特殊字符组成
    password = models.CharField(verbose_name="密码", max_length=64, default="123456")


# 管理员信息
class AdminInfo(models.Model):
    # 角色标签，用数字区分，学生0，教师1，管理员2
    role = models.IntegerField(default=2)

    # 管理员工号，由5位数字组成
    adminId = models.CharField(verbose_name="管理员工号", max_length=5, unique=True)

    # 管理员姓名，由2-10位中文字符组成
    name = models.CharField(verbose_name="管理员姓名", max_length=32)

    # 管理员登录密码，由6-16位数字、字母、特殊字符组成
    password = models.CharField(verbose_name="密码", max_length=64, default="123456")


# 作业信息
class AssignInfo(models.Model):
    # 作业名称
    assignName = models.CharField(verbose_name="作业名称", max_length=32)

    # 作业描述
    assignDesc = models.CharField(verbose_name="作业描述", max_length=256)


# 考试信息
class ExamInfo(models.Model):
    # 考试名称
    examName = models.CharField(verbose_name="考试名称", max_length=32)

    # 考试描述
    examDesc = models.CharField(verbose_name="考试描述", max_length=256)
