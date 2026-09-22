from django.contrib import admin
from .models import User, Student, Teacher, Admin, StudentGroup, Homework, Mark

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_number', 'course', 'year_of_study')
    search_fields = ('user__username', 'enrollment_number', 'course')
    list_filter = ('course', 'year_of_study')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department')
    search_fields = ('user__username', 'employee_id', 'department')
    list_filter = ('department',)

    def save_model(self, request, obj, form, change):
        obj.user.is_staff = True
        obj.user.save(update_fields=['is_staff'])
        super().save_model(request, obj, form, change)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_id')
    search_fields = ('user__username', 'admin_id')

    def save_model(self, request, obj, form, change):
        obj.user.is_staff = True
        obj.user.save(update_fields=['is_staff'])
        super().save_model(request, obj, form, change)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'created_by', 'created_at', 'student_count')
    search_fields = ('name', 'teacher__username', 'created_by__username')
    list_filter = ('teacher', 'created_at')
    filter_horizontal = ('students',)

    @admin.display(description='Students')
    def student_count(self, obj):
        return obj.students.count()


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'due_date', 'created_by', 'created_at')
    search_fields = ('title', 'group__name')
    list_filter = ('due_date', 'created_at')


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'value', 'created_by', 'created_at')
    search_fields = ('student__user__username', 'group__name')
    list_filter = ('value', 'created_at')