from django.urls import path
from . import views
from rest_framework import routers
# from .views import TransferViewSet
from . import views
from django.conf.urls import include

router = routers.DefaultRouter()
router.register('transfers', views.TransferViewSet, basename='transfer')
router.register('variants', views.VariantViewSet, basename='transfer')
router.register('checkins', views.CheckinViewSet, basename='checkin')
router.register('checkouts', views.CheckoutViewSet, basename='checkout')
router.register('adjustments', views.AdjustmentViewSet, basename='adjustment')

category_detail = views.CategoryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [   
    #path('transfers/',views.TransferViewSet.as_view(),name="transfers"),
    path('', include(router.urls)),
    path('transfer/create', views.CreateTransfer),
    path('checkin/create', views.CreateCheckin),
    path('checkout/create', views.CreateCheckout),
    path('adjustment/create', views.CreateAdjustment),
    path('warehouse/create', views.CreateWarehouse),
    path('item/create', views.CreateItem),
    path('category/create', views.CreateCategory),
    path('contact/create', views.CreateContact, name="create-contact"),
    path('unit/create', views.CreateUnit, name="create-unit"),
    path(r'items/search/', views.SearchItem),
    path('category/<int:pk>/', category_detail, name='category-detail'),
    path('category/<int:pk>/delete', views.CategoryDetail.as_view(), name="delete-category"),
    path('category/<int:pk>/edit', views.CategoryDetail.as_view(), name="edit-category"),
    path('contact/<int:pk>/delete', views.ContactDetail.as_view(), name="delete-contact"),
    path('contact/<int:pk>/edit', views.ContactDetail.as_view(), name="edit-contact"),

    path('transfer/<int:pk>/delete', views.TransferDetail.as_view(), name="transfer-delete"),
    path('transfer/<int:pk>/edit', views.TransferDetail.as_view(), name="transfer-edit"),

    path('adjustment/<int:pk>/delete', views.AdjustmentDetail.as_view(), name="adjustment-delete"),
    path('adjustment/<int:pk>/edit', views.AdjustmentDetail.as_view(), name="adjustment-edit"),

    path('checkin/<int:pk>/delete', views.CheckinDetail.as_view(), name="checkin-delete"),
    path('checkin/<int:pk>/edit', views.CheckinDetail.as_view(), name="checkin-edit"),

    path('checkout/<int:pk>/delete', views.CheckoutDetail.as_view(), name="checkout-delete"),
    path('checkout/<int:pk>/edit', views.CheckoutDetail.as_view(), name="checkout-edit"),

    path('item/<int:pk>/delete', views.ItemDetail.as_view(), name="item-delete"),
    path('item/<int:pk>/edit', views.ItemDetail.as_view(), name="item-edit"),

    path('warehouse/<int:pk>/delete', views.WarehouseDetail.as_view(), name="warehouse-delete"),
    path('warehouse/<int:pk>/edit', views.WarehouseDetail.as_view(), name="warehouse-edit"),

]