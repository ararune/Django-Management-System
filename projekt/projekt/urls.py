# urls.py
from django.contrib import admin
from django.urls import path, include
from app1.views import (
    register, main_page, custom_logout, main_page_admin, main_page_professor,
    main_page_student, update_predmet, delete_predmet, edit_student,
    edit_professor, upisni_list, popis_studenata, upisni_list_student,
    popis_studenata_professor
)
from django.contrib.auth import views as auth_views
from django.views.csrf import csrf_failure



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/profile/', main_page, name='profile'),
    path('accounts/profile/admin/', main_page_admin, name='main_page_admin'),
    path('accounts/profile/professor/', main_page_professor, name='main_page_professor'),
    path('accounts/profile/student/', main_page_student, name='main_page_student'),
    # Catch-all URL pattern for unrecognized URLs, to prevent accessing main page unauthorized
    path('accounts/<path:dummy>/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('csrf-failure/', csrf_failure, name='csrf_failure'),
    
    path('predmet/update/<int:predmet_id>/', update_predmet, name='update_predmet'),   
    path('predmet/delete/<int:predmet_id>/', delete_predmet, name='delete_predmet'),
    path('student/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('professor/edit/<int:professor_id>/', edit_professor, name='edit_professor'),
    path('upisni-list/<int:student_id>/', upisni_list, name='upisni-list'),
    path('popis_studenata/<int:predmet_id>/', popis_studenata, name='popis_studenata'),
    path('upisni-list/student/', upisni_list_student, name='upisni-list-student'),
    path('popis_studenata_professor/<int:predmet_id>/', popis_studenata_professor, name='popis_studenata_professor'),
]
 
