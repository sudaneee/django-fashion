from django.urls import path
from . import views

urlpatterns = [
    path('/', views.dashboard, name='admin-home'),
    path('add-customer/', views.addCustormer, name='add-customer'),
    path('customer-list/', views.customerList, name='customer-list'),
    path('customer-details/<pk>/', views.customerDetails, name='customer-details'),
    path('delete-customer/<pk>/', views.deleteCustomer, name='delete-customer'),
    path('add-measurement/', views.addMeasurement, name='add-measurement'),
    path('edit-measurement/', views.editMeasurement, name='edit-measurement'),
    path('measurement-details/<pk>/<str:m_type>/', views.measurementDetails, name='measurement-details'),
    path('create-job/', views.createJob, name='create-job'),
    path('view-jobs/', views.viewJobs, name='view-jobs'),
    path('view-job-details/<pk>/', views.viewJobDetails, name='view-job-details'),
]