from django.urls import path
from . import views
from rest_framework.authtoken import views as authview

urlpatterns = [
    path('patients/', views.PatientList.as_view()),
    path('patients/<int:pk>/', views.PatientDetail.as_view()),
    path('patients/<int:pk>/changestate/', views.patient_change_state),
    path('patients/<int:pk>/<str:field>/', views.patient_check_field),
    path('patientstates/', views.PatientStateList.as_view()),
    path('patientstates/<int:pk>/', views.PatientStateDetail.as_view()),
    path('api-token-auth/', authview.obtain_auth_token),
]