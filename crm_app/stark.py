from stark.service.stark import site,ModelStark
from .models import *
from django.utils.safestring import mark_safe
site.register(Department)
from django.conf.urls import url
from django.shortcuts import HttpResponse,redirect
class UserConfig(ModelStark):
    list_display = ['name','username','email','depart']

site.register(UserInfo,UserConfig)
site.register(Course)
site.register(School)

class ClassConfig(ModelStark):

    def display_classname(self,obj=None,header=False):
        if header:
            return "班级名称"
        class_name ="%s(%s)"%(obj.course.name,obj.semester)
        return class_name

    list_display = [display_classname,'tutor','teachers']

site.register(ClassList,ClassConfig)

class CustomConfig(ModelStark):

    def display_course(self,obj=None,header=False):
        if header:
            return "咨询课程"
        temp = []
        for course in obj.course.all():
            s = '<a href="/stark/crm_app/customer/cancel/%s/%s" style="border:1px solid #369;padding=3px 6px;">%s</a>'%(obj.pk,course.pk,course.name)
            temp.append(s)
        return mark_safe(','.join(temp))
    def cancel_course(self,request,cunstom_id,course_id):
        print("取消成功")
        obj = Customer.objects.filter(pk=cunstom_id).first()
        obj.course.remove(course_id)

        return redirect(self.get_list_url())
    def extra_url(self):
        temp = []
        temp.append(url(r'cancel/(\d+)/(\d+)',self.cancel_course))
        return temp

    list_display = ['name','gender',display_course,]


site.register(Customer,CustomConfig)

class ConsultConfig(ModelStark):

    list_display = ['customer','consultant','date','note']
site.register(ConsultRecord,ConsultConfig)

class StudentCopnfig(ModelStark):
    list_display = ['customer','class_list']
    list_display_links = ['customer']
site.register(Student,StudentCopnfig)

class CourseConfig(ModelStark):
    def record(self, obj=None, header=False):
        if header:
            return "checked"
        return mark_safe('<a href="/stark/crm_app/studyrecord/?course_record=%s">记录</a>'%obj.pk)
    list_display = ['class_obj','day_num','teacher',record]


    def patch_study(self,request,queryset):
        print(queryset)
        temp = []
        for course_record in queryset:
            student_list = Student.objects.filter(class_list__id=course_record.class_obj.pk)
            for student in student_list:
                obj = StudyRecord(student=student,course_record=course_record)
                temp.append(obj)

        StudyRecord.objects.bulk_create(temp)#批量插入



    patch_study.short_description = "批量生成学习记录"
    actions = [patch_study, ]

site.register(CourseRecord,CourseConfig)

class StudyConfig(ModelStark):

    list_display = ['student','course_record','record','score']

site.register(StudyRecord,StudyConfig)