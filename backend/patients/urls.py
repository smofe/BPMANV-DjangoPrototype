from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.PatientList.as_view()),
    path('patients/all/', views.all_patients_view),
    path('patients/start/', views.all_patients_start),
    path('patients/<int:pk>/', views.PatientDetail.as_view()),
    path('patients/<int:pk>/state/', views.patient_check_state),
    path('patients/<int:pk>/changestate/', views.patient_change_state),
    path('patients/<int:pk>/<str:field>/', views.patient_check_field),
    path('patientstates/', views.PatientStateList.as_view()),
    path('patientstates/<int:pk>/', views.PatientStateDetail.as_view()),
    path('entity/<int:pk>/', views.EntityDetail.as_view()),
    path('entity/<int:pk>/inventory/', views.entity_inventory_details),
    path('entity/<int:sender_pk>/inventory/exchange/<int:receiver_pk>/', views.inventory_exchange),
    path('inventory/<int:pk>/', views.InventoryDetail.as_view()),
    path('instance/', views.GameInstanceList.as_view()),
    path('instance/<int:pk>/', views.game_instance_detail),
]