from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.utils import timezone
from .models import accounts as acts
def home(request):
    return render(request, 'home.html')
def hume(request):
    return render(request,'accts.html')

def login(request):
    if request.method == 'POST':
        
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        try:
             obj=acts.objects.get(userid=user_id)
             if obj.passwords == password:
                  request.session['user_ids']=obj.userid
                  request.session['user_name']=obj.Name
                  nme=request.session['user_name']
                  usrid=request.session['user_ids']
                  return render(request,'accts.html',{'thro':usrid,'nom':nme})
             else:
                  messages.error(request,'Invalid password')
                  return redirect('home')
        except acts.DoesNotExist:
             messages.error(request,'User does not exist!! pls signup or try again!!!!')
             return redirect('home')
    else:
        return redirect('home')

def signup(request):
    if request.method == 'POST':
        
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        phone_no = request.POST.get('phone_no')
        email=request.POST.get('email')
        password = request.POST.get('password')
        obj = acts(Name=username, userid=user_id, Email=email, phone_no=phone_no,passwords=password)
        obj.save()
    return redirect('home')

def admin_login(request):
    if request.method == 'POST':
        
        admin_id = request.POST.get('admin_id')
        password = request.POST.get('password')
        
        if admin_id == 'admin_user' and password == 'admin_password':
            
            return HttpResponse('Admin Login Successful!')
        else:
           
            return HttpResponse('Invalid admin credentials. Please try again.')
    return redirect('home')
def deps(request, thro):
    amt = request.POST.get('amount')
    if not amt or not amt.isdigit():
        messages.error(request, 'Invalid amount. Please enter a valid number.')
        return redirect('hume')
    
    amt = int(amt)
    current = timezone.now()
    newdate = current.strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        ur = acts.objects.get(userid=thro)
        ur.depost = (ur.depost or 0) + amt
        ur.moneybox = (ur.moneybox or 0) + amt
        ur.timestraps = current
        ur.historys = (ur.historys or '') + f'\nThe Amount of {amt} is added!!! {newdate}'
        ur.save()         
        messages.success(request, f'The Amount of {amt} has been successfully deposited!')

        nme = request.session.get('user_name')
        usrid = request.session.get('user_ids')
        if not nme or not usrid:
            messages.error(request, 'Session expired. Please log in again.')
            return redirect('home')
        return render(request, 'accts.html', {'thro': usrid, 'nom': nme})
    except acts.DoesNotExist:
        messages.error(request, 'Unable to complete the transaction. User does not exist.')
        return redirect('hume')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return redirect('hume')
# def deps(request, thro):
#     amt = request.POST.get('amount')
#     uid = thro
#     current = timezone.now()
#     newdate = current.strftime('%Y-%m-%d %H:%M:%S')
#     try:
#         ur = acts.objects.get(userid=uid)
#         amt = int(amt)
#         if ur.moneybox is not None:
#             ur.depost = (ur.depost or 0) + amt
#             ur.moneybox += amt
#             ur.timestraps = current
#             ur.historys += f'\nThe Amount of {amt} is added!!! {newdate}'
#         else:
#             ur.depost = amt
#             ur.moneybox = amt
#             ur.timestraps = current
#             ur.historys = f'The Amount of {amt} is added!!! {newdate}'
#         ur.save() 
#         currentmgs = ur.historys.split('\n')[-1].strip()
#         messages.success(request, currentmgs)
#         nme = request.session['user_name']
#         usrid = request.session['user_ids']
#         return render(request, 'accts.html', {'thro': usrid, 'nom': nme})
#     except acts.DoesNotExist:
#         messages.error(request, 'Unable to complete the transaction')
#         return redirect('hume')

def withdrw(request, thro):
    amt = int(request.POST.get('amount'))
    uid = thro
    current = timezone.now()
    newdate = current.strftime('%Y-%m-%d %H:%M:%S')
    try:
        ur = acts.objects.get(userid=uid)
        if ur.moneybox and ur.moneybox >= amt:
            ur.withdrawls = (ur.withdrawls or 0) + amt
            ur.moneybox -= amt
            ur.timestraps = current
            ur.historys += f'\nThe Amount of {amt} is withdrawn!!! {newdate}'
            ur.save()  
            currentmgs = ur.historys.split('\n')[-1].strip()
            messages.success(request, currentmgs)
        else:
            messages.error(request, 'Insufficient Balance !!!')
        usrid = request.session['user_ids']
        return render(request, 'accts.html', {'thro': usrid,})
    except acts.DoesNotExist:
        messages.error(request, 'Unable to complete the transaction')
        return redirect('hume')
# def hists(request):
#     uid = request.session.get('user_ids')
#     try:
#         ur = acts.objects.get(userid=uid)
#         history_list = ur.historys.split('\n') if ur.historys else []
#         return render(request, 'accts.html', {'history_list': history_list})
#     except acts.DoesNotExist:
#         messages.error(request, 'User does not exist.')
#         return redirect('hume')
def hists(request,thro):
    # Retrieve the user ID from the session
    uid = thro
    print(f"Session User ID: {uid}")
    if not uid:
        messages.error(request, 'Session expired. Please log in again.')
        return redirect('home')

    try:
        # Fetch the user from the database
        ur = acts.objects.get(userid=thro)

        # Split the transaction history into a list
        history_list = ur.historys.split('\n') if ur.historys else []

        # Get the current balance
        balance = ur.moneybox or 0

        # Pass the history and balance to the template
        return render(request, 'accts.html', {
            'history_list': history_list,
            'balance': balance,
            'thro': ur.userid,
            'nom': ur.Name,
            'uid':uid,
        })

    except acts.DoesNotExist:
        messages.error(request, 'User does not exist. Please log in again.')
        return redirect('home')

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")
        return redirect('home')
def logout(request):
    request.session.flush()  
    return redirect('home')
    
