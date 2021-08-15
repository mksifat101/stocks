from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name="home"),
    path('checkins/',views.Checkins,name="checkins"),
    path('checkins/<int:pk>',views.CheckinDetails,name="checkins"),
    path('checkouts/',views.Checkouts,name="checkins"),
    path('adjustments/',views.Adjustments,name="adjustments"),
    path('transfers/',views.Transfers,name="transfers"),
    path('contacts/',views.Contacts),
    path('categories/',views.Categories),
    path('categories/<int:pk>/edit',views.EditCategory,name="edit-category"),
    path('items/<int:pk>/edit',views.EditItem),
    path('transfers/<int:pk>/edit',views.EditTransfer),
    path('adjustments/<int:pk>/edit',views.EditAdjustment),
    path('checkins/<int:pk>/edit',views.EditCheckin),
    path('checkouts/<int:pk>/edit',views.EditCheckout),
    path('warehouses/<int:pk>/edit',views.EditWarehouse),
    path('units/',views.Units),
    path('warehouses/',views.Warehouses),
    path('users/',views.Users),
    path('items/',views.Items),
   
    path('units/create',views.CreateUnit),
    path('checkouts/create',views.CreateCheckout),
    path('checkins/create',views.CreateCheckin),
    path('transfers/create',views.CreateTransfers),
    path('items/create',views.CreateItem),
    path('adjustments/create',views.CreateAdjustment),
    path('contacts/create',views.CreateContact),
    path('categories/create',views.CreateCategory),
    path('warehouses/create',views.CreateWarehouse),
    path('users/create',views.CreateUser),
    path('contacts/import',views.ImportContacts),
    path('settings',views.SettingsView),

    path('categories/<int:pk>/view',views.ViewCategory,name="view-category"),
    path('items/<int:pk>/view',views.ViewItem, name="view-items"),
    path('transfers/<int:pk>/view',views.ViewTransfer, name="view-transfers"),
    path('adjustments/<int:pk>/view',views.ViewAdjustment, name="view-adjustments"),
    path('checkins/<int:pk>/view',views.ViewCheckin, name="view-checkins"),
    path('checkouts/<int:pk>/view',views.ViewCheckout, name="view-checkouts"),
    path('warehouses/<int:pk>/view',views.ViewWarehouse, name="view-warehouses"),
]