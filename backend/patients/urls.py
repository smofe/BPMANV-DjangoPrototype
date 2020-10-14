from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patient_list),
    path('patients/<int:pk>/', views.patient_detail),
    path('patients/<int:pk>/test/', views.test),
    path('patients/<int:pk>/changestate/', views.patient_change_state),
    path('patients/<int:pk>/<str:field>/', views.patient_check_field),
    path('patientstates/', views.patient_state_list),
]