from django.shortcuts import render,redirect
from .models import Debt,Transaction,Balance, Account_Transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
# Create your views here.
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('/balance')
    return render(request,'login.html')

def user_login(request):
    if request.method == 'POST':
            mail = request.POST.get('email', '')
            user_password = request.POST.get('pass', '')
            user = authenticate(username=mail, password=user_password)
            if user is not None:
                login(request, user)
                return redirect('/balance')
            else:
                return redirect('/login')

def user_logout(request):
    logout(request)
    return redirect('/login')


def balance(request):
    if request.user.is_authenticated:
        try:
            bal=Balance.objects.get(user=request.user)
            return render(request, 'balance.html', {'bal': bal})
        except:
            pass
        return render(request, 'balance.html')
    else:
        return redirect('/login')

def balance_save(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            cash=request.POST.get('cash')
            acc=request.POST.get('account')
            bal=Balance(user=request.user,cash_bal=cash,acc_bal=acc)
            bal.save()
            return redirect('/balance')
    else:
        return redirect('/login')

def cash(request):
    if request.user.is_authenticated:
        return render(request,'cash.html')
    else:
        return redirect('/login')

def account(request):
    if request.user.is_authenticated:
        return render(request,'account.html')
    else:
        return redirect('/login')

def cash_trans(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            amt=int(request.POST.get('amt'))
            name=request.POST.get('name')
            date=request.POST.get('date')
            type=request.POST.get('type')
            desc=request.POST.get('desc','')
            transer=Transaction(user=request.user ,amt=amt,name=name,date=date,type=type,desc=desc)
            transer.save()
            bal = Balance.objects.get(user=request.user)
            b = bal.cash_bal
            if type=='send':
                b=b-amt
            else:
                b=b+amt
            bal.cash_bal=b
            bal.save()
            debtor=request.POST.get('debt','')
            if debtor:
                debt_name=request.POST.get('debt_name')
                debt_amt=int(request.POST.get('debt_amt'))
                debt=Debt(user=request.user,name=debt_name,amt=debt_amt,date=date,using='cash')
                debt.save()
            return redirect('/balance')
    else:
        return redirect('/login')

def acc_trans(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            amt=int(request.POST.get('amt'))
            name=request.POST.get('name')
            date=request.POST.get('date')
            type=request.POST.get('type')
            desc=request.POST.get('desc','')
            transer=Account_Transaction(user=request.user,amt=amt,name=name,date=date,type=type,desc=desc)
            transer.save()
            bal = Balance.objects.get(user=request.user)
            b = bal.acc_bal
            if type=='send':
                b=b-amt
            else:
                b=b+amt
            bal.acc_bal=b
            bal.save()
            debtor = request.POST.get('debt')
            if debtor:
                debt_name = request.POST.get('debt_name')
                debt_amt = int(request.POST.get('debt_amt'))
                debt = Debt(user=request.user,name=debt_name, amt=debt_amt, date=date, using='account')
                debt.save()
            return redirect('/balance')
    else:
        return redirect('/login')

def view_cash(request):
    if request.user.is_authenticated:
        trans=Transaction.objects.filter(user=request.user).order_by('-date')
        return render(request,'view_trans.html',{'trans':trans})
    else:
        return redirect('/login')

def view_acc(request):
    if request.user.is_authenticated:
        trans=Account_Transaction.objects.filter(user=request.user).order_by('-date')
        return render(request,'view_trans.html',{'trans':trans})
    else:
        return redirect('/login')

def view_debts(request):
    if request.user.is_authenticated:
        debts=Debt.objects.filter(user=request.user).order_by('-date')
        total=0
        for i in debts:
            if not i.paid:
                total=total+i.amt
        return render(request,'debts.html',{'debts':debts,'total':total})
    else:
        return redirect('/login')

def return_debt(request,debt_id):
    if request.user.is_authenticated:
        debt=Debt.objects.get(id=debt_id)
        debt.paid=True
        type=request.POST.get('type')
        bal = Balance.objects.get(user=request.user)
        name = debt.name
        amt = debt.amt
        date = datetime.date.today()
        if type=='cash':
            b = bal.cash_bal
            b=b+debt.amt
            bal.cash_bal=b
            if amt>0:
                cash=Transaction(user=request.user,name=name,amt=amt,date=date,type='recv')
            else:
                amt=amt*-1
                cash = Transaction(user=request.user, name=name, amt=amt, date=date, type='send',desc='debt')
            cash.save()
        elif type=='acc':
            b=bal.acc_bal
            b=b+debt.amt
            bal.acc_bal=b
            if amt > 0:
                acc = Account_Transaction(user=request.user,name=name, amt=amt, date=date, type='recv')
            else:
                amt = amt * -1
                acc = Account_Transaction(user=request.user, name=name, amt=amt, date=date, type='send',desc='debt')
            acc.save()
        bal.save()
        debt.save()
        return redirect('/debt')
    else:
        return redirect('/login')

def debt_save(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            name=request.POST.get('debt_name')
            amt=int(request.POST.get('debt_amt'))
            date=request.POST.get('date')
            amt=amt*-1
            debt=Debt(user=request.user,name=name,amt=amt,date=date)
            debt.save()
            return redirect('/debt')
    else:
        return redirect('/login')



