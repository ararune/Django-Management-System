# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import KorisnikRegistrationForm, PredmetForm, EditStudentForm, EditProfessorForm, UpisForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Korisnik, Upis, Uloga, Predmet
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_protect
from django.middleware.clickjacking import XFrameOptionsMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.template.context_processors import csrf
from django.views.decorators.csrf import requires_csrf_token
from django.template import RequestContext
from django.contrib.sessions.backends.db import SessionStore
from django.db import IntegrityError
from django.http import HttpResponseBadRequest

from django.db import transaction

@csrf_protect
@transaction.atomic
@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator' , login_url='login')
def register(request):
    if request.method == 'POST':
        form = KorisnikRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.uloga = form.cleaned_data['uloga']
            user.save()

            if user.uloga.ime == 'administrator':
                User = get_user_model()
                admin_user = User.objects.get(pk=user.pk)
                admin_user.is_staff = True  # Grant admin privileges
                admin_user.save()

                # Grant specific permissions to the admin user
                content_types = [
                    ContentType.objects.get_for_model(Korisnik),
                    ContentType.objects.get_for_model(Upis),
                    ContentType.objects.get_for_model(Uloga),
                    ContentType.objects.get_for_model(Predmet),
                ]
                permissions = Permission.objects.filter(content_type__in=content_types)
                admin_user.user_permissions.set(permissions)
            
            elif user.uloga.ime == 'student':
                predmeti = Predmet.objects.all()
                upisi = []
                for predmet in predmeti:
                    upis = Upis.objects.create(student=user, predmet=predmet, status='upisan')
                    upisi.append(upis)

            return redirect(reverse('main_page_admin'))
    else:
        form = KorisnikRegistrationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def main_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    role = user.uloga
    if role.ime == 'administrator' or request.user.is_staff:
        return redirect('main_page_admin')
    elif role.ime == 'professor':
        return redirect('main_page_professor')
    elif role.ime == 'student':
        return redirect('main_page_student')
    else:
        return redirect('login')

@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator' , login_url='login')
def main_page_admin(request):
    predmeti = Predmet.objects.all()
    students = Korisnik.objects.filter(uloga__ime='student')
    professors = Korisnik.objects.filter(uloga__ime='professor')
    success_message = None

    if request.method == 'POST':
        form = PredmetForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                success_message = 'Predmet successfully added.'
                return render(request, 'main_page_admin.html', {'form': form, 'success_message': success_message, 'predmeti': predmeti, 'active_tab': 'add-predmet'})
            except IntegrityError:
                form.add_error('kod', 'A Predmet with this kod already exists.')
                form.add_error('ime', 'A Predmet with this ime already exists.')
        else:
            active_tab = 'add-predmet'
            fail_message = 'Failed to add Predmet.'
    else:
        form = PredmetForm()
        active_tab = 'home'
        fail_message = None

    return render(request, 'main_page_admin.html', {'form': form, 'predmeti': predmeti, 'active_tab': active_tab, 'fail_message': fail_message, 'students': students, 'professors': professors})


@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator', login_url='login')
def update_predmet(request, predmet_id):
    predmet = Predmet.objects.get(pk=predmet_id)
    
    if request.method == 'POST':
        form = PredmetForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            return redirect(reverse('main_page_admin'))
    else:
        form = PredmetForm(instance=predmet)
        
    context = {
        'form': form,
        'predmet_id': predmet_id,
        'predmet_ime': predmet.ime,
    }
    return render(request, 'update_predmet.html', context)

@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator', login_url='login')
def delete_predmet(request, predmet_id):
    predmet = get_object_or_404(Predmet, pk=predmet_id)
    if request.method == 'POST':
        predmet.delete()
        return redirect(reverse('main_page_admin'))
    else:
        return HttpResponseBadRequest("Invalid request method")
    
@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator', login_url='login')
def edit_student(request, student_id):
    student = Korisnik.objects.get(pk=student_id)

    if request.method == 'POST':
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect(reverse('main_page_admin'))
    else:
        form = EditStudentForm(instance=student)

    return render(request, 'edit_student.html', {'form': form, 'student_id': student_id})

@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator', login_url='login')
def edit_professor(request, professor_id):
    professor = Korisnik.objects.get(pk=professor_id)

    if request.method == 'POST':
        form = EditProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect(reverse('main_page_admin'))
    else:
        form = EditProfessorForm(instance=professor)

    return render(request, 'edit_professor.html', {'form': form, 'professor_id': professor_id})


@login_required
def view_details(request, identifier):
    predmet = get_object_or_404(Predmet, ime=identifier)
    return render(request, 'predmet_details.html', {'predmet': predmet})


@login_required
@user_passes_test(lambda u: u.uloga.ime == 'professor', login_url='login')
def main_page_professor(request):
    active_tab = 'home'
    professor = request.user
    predmeti = Predmet.objects.filter(nositelj=professor)
    context = {
        'active_tab': active_tab,
        'predmeti': predmeti,
    }
    return render(request, 'main_page_professor.html', context)



@login_required
@user_passes_test(lambda u: u.uloga.ime == 'student', login_url='login')
def main_page_student(request):

    student = request.user
    predmeti = Predmet.objects.filter(upis__student=student)
    predmeti_upis = Predmet.objects.filter(upis__student=student, upis__status__in=['upisan', 'neupisan'])
    statusi = ['upisan', 'neupisan']

    active_tab = 'home'
    context = {
        'active_tab': active_tab,
        'predmeti': predmeti,
        'upis_queryset': Upis.objects.filter(student=student),
        'predmeti_upis': predmeti_upis,
        'statusi': statusi
    }
    return render(request, 'main_page_student.html', context)



@csrf_protect
def login(request):
    if request.method == 'POST':
        # Check CSRF token
        csrf_middleware = CsrfViewMiddleware()
        csrf_token = csrf(request)['csrf_token']
        if not csrf_middleware._sanitize_token(request, csrf_token):
            # CSRF verification failed due to session mismatch
            error_message = 'Logging in with multiple users in the same browser is not allowed.'
            return render(request, 'login.html', {'error_message': error_message})

        # Handle login logic here

    # Render login page
    return render(request, 'login.html')


@requires_csrf_token
def custom_logout(request):
    logout(request)
    request.session.flush()  # Invalidates the current user's session
    return redirect('login')


@requires_csrf_token
def csrf_failure(request, reason=""):
    return render(request, 'csrf_failure.html', {'reason': reason})

@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator', login_url='login')
def upisni_list(request, student_id):
    student = get_object_or_404(Korisnik, pk=student_id, uloga__ime='student')

    if student.status == 'redovni':
        predmeti = Predmet.objects.filter(sem_redovni__isnull=False).order_by('sem_redovni')
    elif student.status == 'izvanredni':
        predmeti = Predmet.objects.filter(sem_izvanredni__isnull=False).order_by('sem_izvanredni')
    else:
        predmeti = Predmet.objects.none()

    upisi = Upis.objects.filter(student=student)

    success_message = None

    if request.method == 'POST':
        for predmet in predmeti:
            predmet_status = request.POST.get('status_' + str(predmet.id))
            if predmet_status is not None:
                upis, created = Upis.objects.get_or_create(student=student, predmet=predmet)
                upis.status = predmet_status
                upis.save()

        success_message = 'Enrollment form filled out.'

    # Fetch the existing status values for the student's Upis objects
    upis_status = {upis.predmet.id: upis.status for upis in upisi}
    status_choices = [choice[0] for choice in Upis.STATUS_CHOICES]

    # Filter predmeti based on the status in Upis
    predmeti = predmeti.exclude(id__in=upisi.filter(status__in=['polozen', 'dobio_potpis', 'izgubio_potpis']).values('predmet_id'))

    context = {
        'student': student,
        'predmeti': predmeti,
        'upisi': upisi,
        'upis_status': upis_status,
        'status_choice': status_choices,
        'success_message': success_message
    }
    
    return render(request, 'upisni_list.html', context)




@login_required
@user_passes_test(lambda u: u.uloga.ime == 'administrator', login_url='login')
def popis_studenata(request, predmet_id):
    predmet = Predmet.objects.get(pk=predmet_id)
    upisi = Upis.objects.filter(predmet=predmet, status__in=['upisan', 'dobio_potpis', 'izgubio_potpis'])

    status_filter = request.GET.get('status')
    if status_filter:
        upisi = upisi.filter(status=status_filter)

    students_by_status = {}
    for upis in upisi:
        status = upis.get_status_display()  # Get the display value of the status
        if status in students_by_status:
            students_by_status[status].append(upis.student.username)
        else:
            students_by_status[status] = [upis.student.username]

    context = {
        'students_by_status': students_by_status,
        'predmet': predmet,
    }

    return render(request, 'popis_studenata.html', context)

@login_required
@user_passes_test(lambda u: u.uloga.ime == 'student', login_url='login')
def upisni_list_student(request):
    student = request.user
    if student.status == 'redovni':
        predmeti = Predmet.objects.filter(sem_redovni__isnull=False).order_by('sem_redovni')
    elif student.status == 'izvanredni':
        predmeti = Predmet.objects.filter(sem_izvanredni__isnull=False).order_by('sem_izvanredni')
    else:
        predmeti = Predmet.objects.none()

    upisi = Upis.objects.filter(student=student)

    success_message = None

    if request.method == 'POST':
        for predmet in predmeti:
            predmet_status = request.POST.get('status_' + str(predmet.id))
            if predmet_status is not None:
                upis, created = Upis.objects.get_or_create(student=student, predmet=predmet)
                upis.status = predmet_status
                upis.save()

        success_message = 'Enrollment form filled out.'

    # Fetch the existing status values for the student's Upis objects
    upis_status = {upis.predmet.id: upis.status for upis in upisi}
    status_choices = [choice[0] for choice in Upis.STATUS_CHOICES]

    # Filter predmeti based on the status in Upis
    predmeti = predmeti.exclude(id__in=upisi.filter(status__in=['polozen', 'dobio_potpis', 'izgubio_potpis']).values('predmet_id'))

    context = {
        'student': student,
        'predmeti': predmeti,
        'upisi': upisi,
        'upis_status': upis_status,
        'status_choices': status_choices,
        'success_message': success_message
    }

    return render(request, 'upisni_list_student.html', context)

@login_required
@user_passes_test(lambda u: u.uloga.ime == 'professor', login_url='login')
def popis_studenata_professor(request, predmet_id):
    predmet = Predmet.objects.get(pk=predmet_id)
    upisi = Upis.objects.filter(predmet=predmet, status__in=['upisan', 'dobio_potpis', 'izgubio_potpis'])

    status_filter = request.GET.get('status')
    if status_filter:
        upisi = upisi.filter(status=status_filter)

    students_by_status = {}
    for upis in upisi:
        status = upis.get_status_display()
        if status in students_by_status:
            students_by_status[status].append(upis)
        else:
            students_by_status[status] = [upis]

    if request.method == 'POST':
        predmet_id = request.POST.get('predmet_id')
        student = request.POST.get('student')
        status_value = request.POST.get('status_value')

        if predmet_id and student and status_value:
            predmet = Predmet.objects.get(pk=predmet_id)
            upis = Upis.objects.get(predmet=predmet, student__username=student)
            upis.status = status_value
            upis.save()

    context = {
        'students_by_status': students_by_status,
        'predmet': predmet,
    }

    return render(request, 'popis_studenata_professor.html', context)
