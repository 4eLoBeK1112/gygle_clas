from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import get_object_or_404, render, redirect
from .forms import HomeworkForm, LogingForm, MarkForm, StudentGroupForm
from .models import Homework, Mark, Student, StudentGroup

def login(request):
    if request.method == 'POST':
        form = LogingForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                return redirect('home')
            form.add_error(None, 'Неверное имя пользователя или пароль.')
    else:
        form = LogingForm()
    return render(request, 'user/login.html', {'form': form})

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.is_staff:
        return redirect('staff_home')
    return redirect('student_home')

def student_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff:
        return redirect('staff_home')

    student = Student.objects.filter(user=request.user).first()
    groups = student.groups.all() if student else StudentGroup.objects.none()
    return render(request, 'user/student_home.html', {'user': request.user, 'student_groups': groups})

def staff_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('student_home')

    return render(request, 'user/staff_home.html', {
        'user': request.user,
        'student_groups': StudentGroup.objects.select_related('teacher').prefetch_related('students'),
    })

def student_groups(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('student_home')

    groups = StudentGroup.objects.select_related('teacher').prefetch_related('students')
    return render(request, 'user/student_groups.html', {'groups': groups, 'user': request.user})

def group_detail(request, group_id):
    if not request.user.is_authenticated:
        return redirect('login')

    group = get_object_or_404(
        StudentGroup.objects.select_related('teacher').prefetch_related('students', 'homework', 'marks'),
        id=group_id,
    )
    marks = group.marks.select_related('student__user').all()
    if not request.user.is_staff:
        student = get_object_or_404(Student, user=request.user)
        if not group.students.filter(id=student.id).exists():
            return redirect('student_home')
        marks = marks.filter(student=student)

    return render(request, 'user/group_detail.html', {
        'group': group,
        'marks': marks,
        'user': request.user,
    })

def create_student_group(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('student_home')

    if request.method == 'POST':
        form = StudentGroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            if not request.user.is_superuser:
                group.teacher = request.user
            group.save()
            form.save_m2m()
            return redirect('student_groups')
    else:
        form = StudentGroupForm()
        if not request.user.is_superuser:
            form.fields['teacher'].disabled = True

    return render(request, 'user/create_student_group.html', {'form': form, 'user': request.user})

def edit_student_group(request, group_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('student_home')

    group = get_object_or_404(StudentGroup, id=group_id)
    if request.method == 'POST':
        form = StudentGroupForm(request.POST, instance=group)
        if form.is_valid():
            updated_group = form.save(commit=False)
            if not request.user.is_superuser:
                updated_group.teacher = request.user
            updated_group.save()
            form.save_m2m()
            return redirect('group_detail', group_id=group.id)
    else:
        form = StudentGroupForm(instance=group)
        if not request.user.is_superuser:
            form.fields['teacher'].disabled = True

    return render(request, 'user/create_student_group.html', {'form': form, 'user': request.user, 'editing': True})

def add_homework(request, group_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('student_home' if request.user.is_authenticated else 'login')

    group = get_object_or_404(StudentGroup, id=group_id)
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            homework = form.save(commit=False)
            homework.group = group
            homework.created_by = request.user
            homework.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = HomeworkForm()
    return render(request, 'user/group_form.html', {'form': form, 'group': group, 'title': 'Добавить домашнее задание', 'button': 'Добавить задание'})

def add_mark(request, group_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('student_home' if request.user.is_authenticated else 'login')

    group = get_object_or_404(StudentGroup, id=group_id)
    if request.method == 'POST':
        form = MarkForm(request.POST, group=group)
        if form.is_valid():
            mark = form.save(commit=False)
            mark.group = group
            mark.created_by = request.user
            mark.save()
            return redirect('group_detail', group_id=group.id)
    else:
        form = MarkForm(group=group)
    return render(request, 'user/group_form.html', {'form': form, 'group': group, 'title': 'Добавить оценку', 'button': 'Сохранить оценку'})

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
    return redirect('login')
