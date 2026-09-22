from .views import add_homework, add_mark, create_student_group, edit_student_group, group_detail, home, login, logout_view, staff_home, student_groups, student_home
from django.urls import path

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('student/', student_home, name='student_home'),
    path('staff/', staff_home, name='staff_home'),
    path('staff/groups/', student_groups, name='student_groups'),
    path('staff/groups/create/', create_student_group, name='create_student_group'),
    path('groups/<int:group_id>/', group_detail, name='group_detail'),
    path('staff/groups/<int:group_id>/edit/', edit_student_group, name='edit_student_group'),
    path('staff/groups/<int:group_id>/homework/add/', add_homework, name='add_homework'),
    path('staff/groups/<int:group_id>/marks/add/', add_mark, name='add_mark'),
    path('', home, name='home'),
]