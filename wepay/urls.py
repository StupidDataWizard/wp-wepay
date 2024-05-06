from django.urls import path
from . import views

app_name = 'wepay'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_user', views.add_user, name='add_user'),
    path('view_payment_form', views.view_payment_form, name='view_payment_form'),
    path('add_payment', views.add_payment, name='add_payment'),
    path('detail_user/<int:user_id>', views.detail_user, name='detail_user'),
    path('matplot_view', views.matplot_view, name='matplot_view'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('detail_payment/<int:payment_id>', views.detail_payment, name='detail_payment'),
    path('delete_payment/<int:payment_id>', views.delete_payment, name='delete_payment'),
    path('edit_payment/<int:payment_id>', views.edit_payment, name='edit_payment'),
]
