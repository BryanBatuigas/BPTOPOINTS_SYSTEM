from django.shortcuts import render
from django.template.loader import render_to_string
from base64 import b85decode
from multiprocessing import context
from pickle import NONE
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .forms import *
from .models import *
from POINTS_APP.models import *
from xhtml2pdf import pisa
from json import dumps
import serial
import os


# Create your views here.
def Signup(request):
    form1 = Userreg()
    if request.method == "POST":
        form1 = Userreg(request.POST)
        if form1.is_valid():
            form1.save()
            user = form1.cleaned_data.get('username')
            username = request.POST['username']
            new_user = UserPoints(user1=username)
            points = 0
            new_userpoints = UserPoints(user1=username, points=points)
            new_userpoints.save()
            messages.success(request, 'Congratulations! ' + user + ' you have created this account')
            return redirect('UserLogin')
        else:
            messages.success(request, form1.errors)

    context = {'form':form1}
    return render(request, 'html/SIGNUP.html', context)

#LOGIN
def Userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password=password)

        if user is not None and user.Usertype == 'S':
            login(request, user)
            paper_db = PaperPointsEquivalent.objects.count()
            bottle_db = BottlePointsEquivalent.objects.count()
            if paper_db == 0:
                value = PaperPointsEquivalent(paper_weight=0, paper_points=0)
                value.save()
            else:
                pass
            if bottle_db == 0:
                value = BottlePointsEquivalent(bottle_count=0, bottle_points=0)
                value.save()
            else:
                pass
            return redirect('userhomescreen')

        elif user is not None and user.Usertype == 'A':
            login(request, user)
            return redirect('Admin_Page')
            
        else:
            messages.error(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'html/LOGIN.html', context)

@login_required(login_url='UserLogin')
def logoutUser(request):
    logout(request)
    return redirect('UserLogin')

###################### U S E R #########################

@login_required(login_url='UserLogin')
def about(request):
    if request.user.is_authenticated and request.user.Usertype == 'S':
        return render(request, 'html/USER_ABOUT.html')
    else:
        return redirect('Admin_Page')

@login_required(login_url='UserLogin')
def UserHomescreen(request):
    if request.user.is_authenticated and request.user.Usertype == 'S':
        points1 = UserPoints.objects.all()
        product_json = []
        paper_weight = 0
        paper_points = 0
        bottle_count = 0
        bottle_points = 0
        username = request.user
        #new
        user2 = User_Rewards_History1.objects.filter(ur_user=username)
        username = request.user
        
        paper_equivalent = PaperPointsEquivalent.objects.first()
        bottle_equivalent = BottlePointsEquivalent.objects.first()
        user = UserPoints.objects.filter(user1=username )
        if paper_equivalent.paper_weight == 0:
            messages.error(request, "Paper's points are set to 0. Contact admin to fix.")
        else:
            weight = PaperPointsEquivalent.objects.first()
            points = PaperPointsEquivalent.objects.first()
            paper_weight = weight.paper_weight
            paper_points = points.paper_points

        if bottle_equivalent.bottle_count == 0:
            messages.error(request, "Bottle's points are set to 0. Contact admin to fix.")
        else:
            count = BottlePointsEquivalent.objects.first()
            points = BottlePointsEquivalent.objects.first()
            bottle_count = count.bottle_count
            bottle_points = points.bottle_points

        
        context = {'points':user, 'paper_weight':paper_weight, 'paper_points':paper_points, 'bottle_count':bottle_count, 'bottle_points':bottle_points,'user2': user2}
        return render(request, 'html/USER_HOMESCREEN.html', context)

    else:
        return redirect('Admin_Page')

#NEW#
@login_required(login_url='UserLogin')
def Rewards_selection(request, pk):
    if request.user.is_authenticated and request.user.Usertype == 'S':
        order = Rewards_Settings.objects.filter(id=pk)
        product_json = []
        user = request.user
        userr = request.user.first_name
        
        for rewards in order:
            product_json.append({'id':rewards.id, 'name':rewards.Product_Name, 'price':float(rewards.Value_Points), 'color': rewards.Color, 'stocks': rewards.Stocks})
            vp = float(rewards.Value_Points)
            request.method == "POST"  
            qty1 = 0
            total = vp * qty1
            if 'compute' in request.POST:
                qty = request.POST.get('qty')
                qty1 = int(qty)
                total = vp * qty1
                context1 = {
                'total' : total
            }      
            elif 'submit_database' in request.POST:
                user = request.user
                stocks = rewards.Stocks
                item = rewards.Product_Name
                vp = float(rewards.Value_Points)
                qty = request.POST.get('qty')
                qty1 = int(qty)
                total1 = vp * qty1
                total = round(total1,2)
                points = UserPoints.objects.filter(user1=user)
                for i in points:
                    if i.points < total:
                        messages.error(request, 'Not enough points')
                        
                    elif i.points == "":
                        messages.error(request, 'Not enough points')
                        
                    else:
                        formula = i.points - total
                        new_formula = round(formula, 2)
                        print(new_formula, 'ito na yung bago')
                        ##stocks##
                        formula1 = stocks - qty1
                        print(formula1, 'ito na yung print')
                        if stocks < qty1:
                            messages.success(request, 'Not enough Stocks')
                            
                        else:
                            account = UserPoints.objects.get(user1=user)
                            account.points = new_formula
                            account.save()
                            account1 = Rewards_Settings.objects.get(id=pk)
                            account1.Stocks = formula1
                            account1.save()
                            username =request.user
                            status = "Redeem"
                            user1 = User_Rewards_History1(ur_user=username, ur_item=item, ur_quantity=qty, ur_total_points=total, ur_status=status)
                            user1.save()
                            user2 = Admin_Rewards_Queue(ar_user=username, ar_item=item, ar_quantity=qty, ar_total_points=total)
                            user2.save()
                            messages.success(request, 'Congratulations! The ' + item + ' is successfully added')
                            print(qty)   
                            return redirect('userhomescreen')        

        context = {
            'page_title' : "Point of Sale",
            'order' : order,
            'product_json' : product_json,
            'total' : total,
            'qty1' : qty1,
            'user': user,
            'userr': userr
            
        }
        return render(request, 'html/USER_REWARDS_SELECTION.html', context)
    else:
        return redirect('Admin_Page')

@login_required(login_url='UserLogin')
def Rewards(request):
    if request.user.is_authenticated and request.user.Usertype == 'S':
        RewardsSel = Rewards_Settings.objects.all()
        username = request.user
        context = {'RewardsSel':RewardsSel, 'username':username}
        return render(request, 'html/USER_REWARDS.html', context)
    else:
        return redirect('Admin_Page')
# def verify(request, pk):
#     Quot = Rewards_Settings.objects.get(id=pk)
#     if request.method == "POST":
#         user = request.user
#         points = UserPoints.objects.filter(user1=user)
#         for i in points:
#             if i.points < Quot.Value_Points:
#                 messages.error(request, 'Not enough points')
#                 return redirect('userhomescreen')
#             else:
#                 formula = i.points - Quot.Value_Points
#                 print(i.points, "-", Quot.Value_Points, "=" ,formula)
#                 account = UserPoints.objects.get(user1=user)
#                 account.points = formula
#                 account.save()
#                 return redirect('userhomescreen')

#     context = {'item':Quot}
#     return render(request, 'html/verify.html', context)


@login_required(login_url='UserLogin')
def User_Transaction_History(request):
    if request.user.is_authenticated and request.user.Usertype == 'S':
        username = request.user
        data1 = User_Transactionhistory.objects.filter(th_userr=username)
        
        context = {'data1': data1, 'username':username}
        return render(request, 'html/USER_TRANSACTION_HISTORY.html', context)
    else:
        return redirect('Admin_Page')



@login_required(login_url='UserLogin')
def PDF_User_Transaction_History(request):
    username = request.user
    user = User_Transactionhistory.objects.filter(th_userr=username)
    template_path = 'html/PDF_USER_REWARDS_HISTORY.html'
    context = {'user': user}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="TransactionHistory.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='UserLogin')
def User_Rewards_History(request):
    if request.user.is_authenticated and request.user.Usertype == 'S':
        username = request.user
        user = User_Rewards_History1.objects.filter(ur_user=username)
        return render(request, 'html/USER_REWARD_HISTORY.html', {'user': user, 'username':username})
    else:
        return redirect('Admin_Page')

@login_required(login_url='UserLogin')
def PDF_User_Rewards_History(request):
    username = request.user
    user = User_Rewards_History1.objects.filter(ur_user=username)
    template_path = 'html/PDF_USER_REWARDS_HISTORY.html'
    context = {'user': user}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="RewardsHistory.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

###################### A D M I N #########################

@login_required(login_url='UserLogin')

def Admin_Page(request):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        # Arduino = serial.Serial("COM3", 9600)
        # arduino = Arduino.readline()
        # arduino_data = arduino.rstrip().decode('utf')
        transaction = AdminTransactionHistory.objects.all()
        notification_message = Notification.objects.all()
        total_notification = Notification.objects.all().count()
        total_notification1 = Notification.objects.all().count()
        total = Notification.objects.all().count()
        if total_notification > 9:
            total_notification = ('9+')
            
        # Bottlemessage = 'Bottle Bin is full'
        # Papermessage = 'Paper Bin is full'
        # Binpaper = "Paper"
        # Binbottle = "Bottle"
        # Notification1 = Notification.objects.filter(notif_bin=Binpaper)
        # Notification2 = Notification.objects.filter(notif_bin=Binbottle)
        # Notification2 = Notification.objects.filter(notif_bin=Binbottle, notif_message=Bottlemessage)
        # for i in Notification1:
            # jatsen = i.notif_bin
            # jatsen1 = i.notif_message
            # print (i.notif_message)
        
        # for j in Notification2:
        #     print(j.notif_message)

        # account1 = Notification(notif_bin=Binbottle, notif_message=j.notif_message)
        # account = Notification(notif_bin=Binpaper, notif_message=i.notif_message)
        # account1.save()
        # account.save()

        total = dumps(total_notification)
        context = {'transaction':transaction, 'notification_message':notification_message, 'total_notification':total_notification,
                    'total_notification1':total_notification1, 'total':total}
        return render(request, 'html/ADMIN_PAGE.html', context)
    else:
        return redirect('userhomescreen')


@login_required(login_url='UserLogin')
def PDF_Admin_Page(request):
    transaction = AdminTransactionHistory.objects.all()
    template_path = 'html/PDF_ADMIN_PAGE.html'
    context = {'transaction': transaction}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="AdminTransactionHistory.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='UserLogin')
def Admin_Rewards_History(request):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        rewards = AdminRewardsHistory.objects.all()
        if 'searchbutton' in request.POST:
            rewardsearch = request.POST.get('search')
            if rewardsearch!=None:
                rewards = AdminRewardsHistory.objects.filter(user1__icontains=rewardsearch)      
            else:
                rewards = AdminRewardsHistory.objects.all()
        return render(request, 'html/ADMIN_REWARDS_HISTORY.html', {'rewards':rewards})
    else:
        return redirect('userhomescreen')
#notification#
@login_required(login_url='UserLogin')
def Notification_Deletes(request, pk):
    notif_del = Notification.objects.get(id=pk)
    if request.method == 'POST':
        notif_del.delete()
        return redirect('Admin_Page')
    return render(request, 'html/Notification_delete.html', {'notif_del': notif_del})  

@login_required(login_url='UserLogin')
def PDF_Admin_Rewards_History(request):
    rewards = AdminRewardsHistory.objects.all() 
    template_path = 'html/PDF_ADMIN_REWARDS_HISTORY.html'
    context = {'rewards': rewards}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="AdminRewardsHistory.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='UserLogin')
def delete1(request, pk):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        ideletus = AdminRewardsHistory.objects.get(id=pk)
        if request.method == 'POST':
            ideletus.delete()
            return redirect('Admin_Rewards_History')
        return render(request, 'html/delete1.html', {'ideletus': ideletus})
    else:
        return redirect('userhomescreen')

@login_required(login_url='UserLogin')
def delete2(request, pk):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        transacdelete = AdminTransactionHistory.objects.get(id=pk)
        if request.method == 'POST':
            transacdelete.delete()
            return redirect('Admin_Rewards_History')
        return render(request, 'html/delete2.html', {'transacdelete': transacdelete})
    else:
        return redirect('userhomescreen')

### R E W A R D S  Q U E U E ###
@login_required(login_url='UserLogin')
def Admin_Rewards_Queue1(request):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        queue = Admin_Rewards_Queue.objects.all()        
        if 'searchbutton' in request.POST:
            queuesearch = request.POST.get('search')
            if queuesearch!=None:
                queue = Admin_Rewards_Queue.objects.filter(ar_user__icontains=queuesearch)      
            else:
                queue = Admin_Rewards_Queue.objects.all()
            
        context = {'queue':queue}
        return render(request, 'html/ADMIN_REWARDS_QUEUE.html', context)
    else:
        return redirect('userhomescreen')
@login_required(login_url='UserLogin')
def delete(request, pk):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        Quot = Admin_Rewards_Queue.objects.get(id=pk)
        Quot1 = Admin_Rewards_Queue.objects.filter(id=pk)
        product_json = []
        for rewards in Quot1:
            product_json.append({'id':rewards.id, 'name':rewards.ar_user, 'qty':rewards.ar_quantity, 'item': rewards.ar_item, 'total':float(rewards.ar_total_points),  'date': rewards.ar_date_time})
            print(product_json) 
            idx = rewards.id
            total = float(rewards.ar_total_points)
            item = rewards.ar_item
            datetime = rewards.ar_date_time
            qty = rewards.ar_quantity
            if request.method == "POST":
                status = "Redeemed"
                # username =request.user
                username =rewards.ar_user
                user1 = AdminRewardsHistory(user1=username, item1=item, quantity1=qty, totalpoints1=total, timedate1=datetime)
                user1.save()
                user2 = User_Rewards_History1(id=1, ur_item=item, ur_quantity=qty, ur_total_points=total, ur_status=status)
                user2.save()
                Quot.delete()
                return redirect('Admin_Rewards_Queue')

        context = {'item':Quot}
        return render(request, 'html/delete.html', context)
    else:
        return redirect('userhomescreen')
### A D M I N  S E T T I N G S ###
@login_required(login_url='UserLogin')
def Admin_Settings(request):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        form = PaperPointsForm()
        form1 = BottlePointsForm()
        print('kamote')
        if 'bottle1' in request.POST:
            form1 = BottlePointsForm(request.POST)
            if form1.is_valid(): 
                bottle_count_input = form1.cleaned_data.get('bottle_count')
                bottle_points_input = form1.cleaned_data.get('bottle_points')
                bottledb_count = BottlePointsEquivalent.objects.count()
                if bottledb_count == 0:
                    form1.save()
                else:  
                    count = BottlePointsEquivalent.objects.first()
                    count.bottle_count = bottle_count_input
                    count.save()
                    points = BottlePointsEquivalent.objects.first()
                    points.bottle_points = bottle_points_input
                    points.save()
        elif 'paper1' in request.POST:
            form = PaperPointsForm(request.POST)
        if form.is_valid():
            paper_weight_input = form.cleaned_data.get('paper_weight')
            paper_points_input = form.cleaned_data.get('paper_points')
            paperdb_count = PaperPointsEquivalent.objects.count()
            if paperdb_count == 0:
                form.save()
            else:
                weight = PaperPointsEquivalent.objects.first()
                weight.paper_weight = paper_weight_input
                weight.save()
                points = PaperPointsEquivalent.objects.first()
                points.paper_points = paper_points_input
                points.save()
        context = {'form':form, 'form1':form1}
        return render(request, 'html/ADMIN_SETTINGS.html', context)
    else:
        return redirect('userhomescreen')

@login_required(login_url='UserLogin')
def Admin_Rewards_Settings(request):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        RS = Rewards_Settings.objects.all()
        context = {'RS':RS}
        return render(request, 'html/ADMIN_REWARD_SETTINGS.html', context)
    else:
        return redirect('userhomescreen')

@login_required(login_url='UserLogin')
def Rewards_Settings_delete(request, pk):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        RS = Rewards_Settings.objects.get(id=pk)
        if request.method == "POST":
            RS.delete()
            return redirect('Admin_Rewards_Settings')

        context = {'item':RS}
        return render(request, 'html/ADMIN_DELETE_REWARDS_SETTINGS.html', context)
    else:
        return redirect('userhomescreen')

@login_required(login_url='UserLogin')
def Rewards_Settings_add(request):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        form = AddRewardsSettings()
        if request.method == 'POST':
            form = AddRewardsSettings(request.POST)
            if form.is_valid():
                product_name_input = form.cleaned_data.get('Product_Name')
                stocks_input = form.cleaned_data.get('Stocks')
                color_input = form.cleaned_data.get('Color')
                points_value_input = form.cleaned_data.get('Value_Points')
                points_value_input_round = round(points_value_input, 2)
                account = Rewards_Settings(Product_Name=product_name_input, Stocks=stocks_input, Color=color_input, Value_Points=points_value_input_round)
                account.save()
                return redirect('Admin_Rewards_Settings')
            else:
                messages.error(request, 'Must Enter Number on stocks field and points value per piece field')

        context = {'form':form}
        return render(request, 'html/ADMIN_ADD_REWARDS_SETTINGS.html', context)
    else:
        return redirect('userhomescreen')

@login_required(login_url='UserLogin')
def Rewards_Settings_update(request, pk):
    if request.user.is_authenticated and request.user.Usertype == 'A':
        order = Rewards_Settings.objects.get(id=pk)
        form = AddRewardsSettings(instance=order)
        if request.method == "POST":
            form = AddRewardsSettings(request.POST,instance=order)
            if form.is_valid():
                product_name_input = form.cleaned_data.get('Product_Name')
                stocks_input = form.cleaned_data.get('Stocks')
                color_input = form.cleaned_data.get('Color')
                points_value_input = form.cleaned_data.get('Value_Points')
                points_value_input_round = round(points_value_input, 2)
                account = Rewards_Settings(id=pk)
                account.Product_Name = product_name_input
                account.Stocks = stocks_input
                account.Color = color_input
                account.Value_Points = points_value_input_round
                account.save()
                # form.save()
                return redirect('Admin_Rewards_Settings')
                
            else:
                messages.error(request, 'Invalid Input. Make sure stocks is whole number.')

        context = {'form':form}
        return render(request, 'html/ADMIN_1UPDATE_REWARDS_SETTINGS.html', context)
    else:
        return redirect('userhomescreen')

###################### K I O S K #########################

def Kiosk_Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password=password)

        if user is not None and user.Usertype == 'S':
            login(request, user)
            paper_db = PaperPointsEquivalent.objects.count()
            bottle_db = BottlePointsEquivalent.objects.count()
            if paper_db == 0:
                value = PaperPointsEquivalent(paper_weight=0, paper_points=0)
                value.save()
            else:
                pass
            if bottle_db == 0:
                value = BottlePointsEquivalent(bottle_count=0, bottle_points=0)
                value.save()
            else:
                pass
            return redirect('Kiosk_Homescreen')
        else:
            messages.error(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'html/KIOSK_LOGIN.html', context)

@login_required(login_url='Kiosk_Login1')
def kiosklogoutUser(request):
    logout(request)
    return redirect('Kiosk_First_Page')

@login_required(login_url='Kiosk_Login1')
def Kiosk_Home(request):
    if request.user.is_authenticated and request.user.Usertype == 'S':
        paper_weight = 0
        paper_points = 0
        bottle_count = 0
        bottle_points = 0
        username = request.user
        #new
        user2 = User_Rewards_History1.objects.filter(ur_user=username)
        username = request.user

        if 'button1' in request.POST:

            return redirect('Kiosk_bottlenote')

        user = UserPoints.objects.filter(user1=username)
        paper_equivalent = PaperPointsEquivalent.objects.first()
        bottle_equivalent = BottlePointsEquivalent.objects.first()
        if paper_equivalent.paper_weight == 0:
            messages.error(request, "Paper's points are set to 0. Contact admin to fix.")
        else:
            weight = PaperPointsEquivalent.objects.first()
            points = PaperPointsEquivalent.objects.first()
            paper_weight = weight.paper_weight
            paper_points = points.paper_points

        if bottle_equivalent.bottle_count == 0:
            messages.error(request, "Bottle's points are set to 0. Contact admin to fix.")
        else:
            count = BottlePointsEquivalent.objects.first()
            points = BottlePointsEquivalent.objects.first()
            bottle_count = count.bottle_count
            bottle_points = points.bottle_points

        context = {'points':user, 'paper_weight':paper_weight, 'paper_points':paper_points, 'bottle_count':bottle_count, 'bottle_points':bottle_points,'user2': user2}
        return render(request, 'html/KIOSK_HOMESCREEN.html', context)
    else:
        return redirect('Admin_Page')

@login_required(login_url='Kiosk_Login1')
def Paper_Exchange(request):
    paper_weight = 0
    print('a')
    Arduino = serial.Serial("COM9", 9600)
    print('a')
    myData = Arduino.readline()
    print('a')
    while True:
        Arduino.write(b'W\n')
        # if (Arduino.in_waiting == 0):
        #     print('Please enter a bottle.')
        #     break
        print('a')
        myData2 = Arduino.readline()
        print('a')
        result = myData2.rstrip().decode('utf')
        print('a')
        with open('data.txt', 'a') as text:
            print(result)
            text.write(str(result) + "\n")
        Arduino.write(b'B\n')
    
        if (Arduino.in_waiting == 0):
            break

    if os.path.exists('data.txt'):
        file = open('data.txt', 'r')
        read = file.readlines()
        modified = []
        for line in read:
            modified.append(float(line.strip()))
        print(line)
        while("" in modified):
            modified.remove("")
        print(modified)
        # for i in range(0, len(modified)):
            # if i == (len(modified)-1):
        paper_weight = str(modified[0])
        print(paper_weight)
        paper_weight_new = (float(paper_weight) - 598)
        print(paper_weight_new)
        paper_weight_new2 = round(paper_weight_new, 2)
        print(paper_weight_new2)
        file.close()
    else:
        print('file does not exist.')

    username = request.user
    points = PaperPointsEquivalent.objects.first()
    total_points = float(points.paper_points) * float(paper_weight_new2)
    paper_weight_new3 = float(paper_weight_new2)
    print(paper_weight_new3)
    print('palatandaan')
    print(total_points)
    total_points_new = round(total_points, 2)

    if 'button1' in request.POST:
        os.remove('data.txt')
        Arduino.write(b'b\n')

        username = request.user
        points = PaperPointsEquivalent.objects.first()
        total_points = float(points.paper_points) * paper_weight_new3
        print(paper_weight_new3)
        print('ako ito')
        print(total_points, "=", float(points.paper_points), "x", float(str(paper_weight_new3)))
        account = User_Transactionhistory(th_userr=username, th_recyclable="Paper", th_quantity=str(paper_weight)+"g", th_totalpoints=str(total_points)+"pts")
        account.save()
        user_account = UserPoints.objects.filter(user1=username)
        for i in user_account:
            formula = i.points + total_points_new
        user_points = UserPoints.objects.get(user1=username)
        user_points.points = formula
        user_points.save()

        print(user_account)
        print(user_points)
        print(i.points, "+", total_points_new, "=", formula)

        return redirect('Kiosk_papernote')
    elif 'button2' in request.POST:
        os.remove('data.txt')
        Arduino.write(b'b\n')

        username = request.user
        points = PaperPointsEquivalent.objects.first()
        total_points = float(points.paper_points) * paper_weight_new3
        print(paper_weight_new3)
        print('ako ito')
        print(total_points, "=", float(points.paper_points), "x", float(str(paper_weight_new3)))
        account = User_Transactionhistory(th_userr=username, th_recyclable="Paper", th_quantity=str(paper_weight)+"g", th_totalpoints=str(total_points)+"pts")
        account.save()
        user_account = UserPoints.objects.filter(user1=username)
        for i in user_account:
            formula = i.points + total_points_new
        user_points = UserPoints.objects.get(user1=username)
        user_points.points = formula
        user_points.save()

        print(user_account)
        print(user_points)
        print(i.points, "+", total_points_new, "=", formula)

        return redirect('Kiosk_Homescreen')
    context = {'weight':paper_weight_new2, 'points':total_points_new}
    return render(request, 'html/KIOSK_PAPER_EXCHANGE.html', context)

#################  WORKING ##########################

@login_required(login_url='Kiosk_Login1')
def Bottle_Exchange(request):
    bottle_count = 0
    state_text = open('state.txt', 'r')
    read = state_text.readlines()
    for line in read:
        print(line.rstrip())
        state4 = 'A'
        hehe = line.rstrip()
        print(hehe, "lol")
        if str(hehe) == state4:
            print("pasok")
            
            try:
                Arduino = serial.Serial("COM9", 9600)
                Arduino.write(b'a\n')
                Arduino.close()
                state2 = 'a'
                state3 = state2.rstrip()
                with open('state.txt', 'w') as data:
                    data.write(str(state3))
                    print("sarado")
            
            except serial.SerialException as e:
                if e.errno == 13:
                    raise e
                pass
            except OSError:
                pass
        else:
            pass  

    if os.path.exists('data.txt'):
        file = open('data.txt', 'r')
        read = file.readlines()
        modified = []
        for line in read:
            modified.append(int(line.strip()))

        while("" in modified):
            modified.remove("")
        print(modified)
        bottle_count = sum(modified)
        print(bottle_count)
        bottle_count2 = int(bottle_count)
        print(bottle_count2)
        file.close()
    
    else:
        bottle_count2 = int(0)
    
    username = request.user
    count = BottlePointsEquivalent.objects.first()
    total_points = float(count.bottle_points) * float(bottle_count)
    total_points_new = round(total_points, 2)

    Arduino.close()
    if 'button1' in request.POST:
        os.remove('data.txt')
        username = request.user
        count = BottlePointsEquivalent.objects.first()
        total_points = float(count.bottle_points) * float(bottle_count2)
        print(total_points, "=", float(count.bottle_count), "x", float(str(bottle_count2)))
        account = User_Transactionhistory(th_userr=username, th_recyclable="Bottle", th_quantity=str(bottle_count2)+"pcs", th_totalpoints=str(total_points_new)+"pts")
        account.save()
        user_account = UserPoints.objects.filter(user1=username)
        for i in user_account:
            formula = i.points + total_points_new
        user_points = UserPoints.objects.get(user1=username)
        user_points.points = formula
        user_points.save()

        print(user_account)
        print(user_points)
        print(i.points, "+", total_points_new, "=", formula)

        
        return redirect('Kiosk_bottlenote')

    elif 'button2' in request.POST:
        os.remove('data.txt')
        username = request.user
        count = BottlePointsEquivalent.objects.first()
        total_points = float(count.bottle_points) * float(bottle_count2)
        print(total_points, "=", float(count.bottle_count), "x", float(str(bottle_count2)))
        account = User_Transactionhistory(th_userr=username, th_recyclable="Bottle", th_quantity=str(bottle_count2)+"pcs", th_totalpoints=str(total_points_new)+"pts")
        account.save()
        user_account = UserPoints.objects.filter(user1=username)
        for i in user_account:
            formula = i.points + total_points_new
        user_points = UserPoints.objects.get(user1=username)
        user_points.points = formula
        user_points.save()

        print(user_account)
        print(user_points)
        print(i.points, "+", total_points_new, "=", formula)
        return redirect('Kiosk_Homescreen')
    

    context = {'count':bottle_count2, 'total':total_points_new}
    return render(request, 'html/KIOSK_BOTTLE_EXCHANGE.html', context)


def Kiosk_First_Page(request):
    return render(request, 'html/KIOSK_FIRST_PAGE.html')


@login_required(login_url='Kiosk_Login1')
def Kiosk_Paper_Note(request):
    if 'button1' in request.POST:
        ser = serial.Serial("COM9", 9600)
        x = ser.readline()
        print(x.rstrip().decode('utf'))

        ser.close()
        return redirect('Paperexchange')
    elif 'back' in request.POST:
        if os.path.exists('data.txt'):
            os.remove('data.txt')
            return redirect('Kiosk_Homescreen')
        else:
            return redirect('Kiosk_Homescreen')
    return render(request, 'html/KIOSK_PAPER_EXCHANGE_NOTE.html')

@login_required(login_url='Kiosk_Login1')
def Kiosk_Bottle_Note(request):
    if 'button1' in request.POST:
        print("ayy")
        return redirect('Bottleauth')
    return render(request, 'html/KIOSK_BOTTLE_EXCHANGE_NOTE.html')

@login_required(login_url='Kiosk_Login1')
def kiosk_about(request):
    return render(request, 'html/KIOSK_ABOUT.html')

@login_required(login_url='Kiosk_Login1')
def Bottle_Auth(request):
    try:
        Arduino = serial.Serial("COM9", 9600)
        myData2 = Arduino.readline()
        result2 = myData2.rstrip().decode('utf')
        print(result2)
        Arduino.write(b'A\n')
        state = 'A'
        state1 = state.rstrip()
        with open('state.txt', 'w') as file:
            file.write(str(state1))
        print("kamote")
        # (Arduino.write(b"P\n"))
        # myData = Arduino.readline()
        # print('a')
        # Arduino.write(b'X\n')
        while True:
            # if (Arduino.in_waiting == 0):
            #     print('Please enter a bottle.')
            #     break
            print('ito na yun')
            myData = Arduino.readline()
            print('a')
            result = myData.rstrip().decode('utf')
            print('a')
            print(result)
            with open('data.txt', 'a') as text:
                    text.write(str(result) + "\n")
            if int(result)==1:
                Arduino.write(b'a\n')
                state2 = 'a'
                state3 = state2.rstrip()
                with open('state.txt', 'w') as data:
                    data.write(str(state3))
                    state_text = open('state.txt', 'r')
                    read = state_text.readlines()
                    for line in read:
                        print(line.rstrip())
                break
    except serial.SerialException as e:
        if e.errno == 13:
            raise e
        pass
    except OSError:
        pass

        
    return redirect('Kiosk_bottlenote')

# @login_required(login_url='Kiosk_Login1')
# def Paper_Done(request):
#     try:
#         Arduino = serial.Serial("COM9", 9600)
#         Arduino.write(b'b\n')
#     except serial.SerialException as e:
#         if e.errno == 13:
#             raise e
#         pass
#     except OSError:
# #         pass

        
#     return redirect('Kiosk_Homescreen')


def Paper_Exchange_Orig(request):
    form = PaperForm()
    if request.method == 'POST':
        form = PaperForm(request.POST)
        if form.is_valid():
            form.save()
            points = form.cleaned_data.get('points')
            saved_points = request.POST['points']
            username = request.user
            user_id = request.user.id
            user = UserPoints.objects.filter(user1=username)
            account = UserPoints.objects.get(user1=username)
            for i in user:
                formula = i.points + points
                formula1 = round(formula, 2)
            print(i.points, "+", points, "=", formula)
            print(user_id)
            print(account)
            account.points = formula1
            account.save()  
            
    
    context = {'form':form}
    return render(request, 'html/KIOSK_PAPER_EXCHANGE_ORIG.html', context)
