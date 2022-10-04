from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin-home'),
    path('login/', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
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
    path('create-staff/', views.createStaff, name='create-staff'),
    path('staff-list/', views.staffList, name='staff-list'),
    path('staff-details/<pk>/', views.staffDetails, name='staff-details'),
    path('delete-staff/<pk>/', views.deleteStaff, name='delete-staff'),
    path('create-staff-activity/', views.staffActivity, name='create-staff-activity'),
    path('add-consumable/', views.addConsumable, name='add-consumable'),
    path('items-list/', views.itemsList, name='items-list'),
    path('item-details/<pk>/', views.itemDetails, name='item-details'),
    path('delete-item/<pk>/', views.deleteItem, name='delete-item'),
    path('create-expenditure/', views.createExpenditure, name='create-expenditure'),
    path('expenses-list/', views.expensesList, name='expenses-list'),
    
    
]