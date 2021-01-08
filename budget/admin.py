from django.contrib import admin
from .models import Balance,Account_Transaction,Transaction,Debt
# Register your models here.
admin.site.register(Balance)
admin.site.register(Account_Transaction)
admin.site.register(Transaction)
admin.site.register(Debt)