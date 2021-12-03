from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'application'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('sign-in/', views.sign_in, name="sign_in"),
    path('sign-out', views.sign_out, name='sign_out'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor/<doctor_id>', views.single_doctor, name='doctor'),
    path('profile', views.profile, name='profile'),
    path('save_availability', views.save_availability, name="save_availability"),
    path('confirm_appointment', views.confirm_appointment, name="confirm_appointment"),
    path('mark_as_done/<appointment_id>', views.mark_as_done, name="mark_as_done"),
    
]


urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
