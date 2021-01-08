from django.urls import path, include
from . import views
urlpatterns = [
path('login',views.loginpage,name='loginp'),
path('logging',views.user_login,name='login'),
path('logout',views.user_logout,name='logout'),
path('balance',views.balance,name='balance'),
path('balance_save',views.balance_save,name='balance save'),
path('cash',views.cash,name='cash'),
path('cash_trans',views.cash_trans,name='cash_trans'),
path('view_cash',views.view_cash,name='cash_view'),
path('acc',views.account,name='acc'),
path('acc_trans',views.acc_trans,name='acctrans'),
path('view_acc',views.view_acc,name='acc_view'),
path('debt',views.view_debts,name='debts'),
path('debt_save',views.debt_save,name='debts'),
path('paid/<str:debt_id>',views.return_debt,name='paid')
]