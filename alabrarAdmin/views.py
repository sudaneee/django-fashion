from multiprocessing import context
from sys import exec_prefix
from django.shortcuts import redirect, render
from django.http import HttpResponse
from PIL import Image
from datetime import timedelta, date, datetime
# import datetime
from djmoney.money import Money
import pytz
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sms import send_sms
from django.core.paginator import Paginator
import requests
from django.conf import settings

from .models import (
    Customer,
    KaftanMeasurement,
    TrouserMeasurement,
    SuitMeasurement,
    ShirtMeasurement,
    DesignType,
    Job,
    JobItem,
    Staff,
    StaffWage,
    Consumables,
    ItemExpenditure,
    WorkType,
    StaffActivity,
    SellsItem,
    SellItemRestock,
    Sell,
)
from django.contrib import messages
# Create your views here.


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('admin-home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin-home')

        else:
            messages.error(request, 'Incorrect login credentails')
    context = {'page': page}
    return render(request,'alabrarAdmin/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):

    enddate = datetime.today()
    sending_date = datetime.now().date()


    sms_query = Job.objects.filter(collection_date=sending_date, sms_text=False).all()

    try:
        for i in sms_query:
            customer = Customer.objects.get(id=i.customer.id)
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                "to": f"{(customer.phone_number)[1:]}",
                "from": "Al-abrar",
                "sms": f"Dear {customer.name} ! \nThis is to inform that your comfy and elegant dress are set for picked up @al-abrar fashion design limited. \nThanks for your partronage. \nWe are your best plug!",
                "type": "plain",
                "channel": "generic",
                "api_key": "TLNWhmgMzn58KliQo5X83RwvYsoJ81AbhxuxToMMmFdBwSRRLIUTQnDxUL9jPC"

            }

            response = requests.post(url=url, data=payload)
            i.sms_text = True
            i.save()
            print(response.text)
    except:
        pass
        



    startdate = enddate - timedelta(days=6)

    item_expenses = ItemExpenditure.objects.filter(incurred_on__range=[startdate, enddate]).all()
    wages_expenses = StaffWage.objects.filter(paid_on__range=[startdate, enddate]).all()
    general_income = Job.objects.filter(recieved__range=[startdate, enddate]).all()
    outstanding_expenses = StaffWage.objects.filter(paid_on__range=[startdate, enddate]).all()
    expected_income = Job.objects.all()

    all_expenses = []
    all_income = []
    outstanding_expenditure = []
    awaiting_payments = []

    for i in item_expenses:
        all_expenses.append(i.amount)
    
    for j in wages_expenses:
        all_expenses.append(j.amount_paid)

    for k in general_income:
        all_income.append(k.amount_paid)

    for l in outstanding_expenses:
        outstanding_expenditure.append(l.total_amount - l.amount_paid)

    for m in expected_income:
        awaiting_payments.append(m.balance)

   
    
    context = {
        'expenditure': sum(all_expenses),
        'income': sum(all_income),
        'outstanding_expenditure': sum(outstanding_expenditure),
        'awaiting_payments': sum(awaiting_payments)
    }
    

    return render(request, 'alabrarAdmin/dashboard.html', context)


@login_required(login_url='login')
def addCustormer(request):
    if request.method == "POST":
        name = request.POST['name']
        customer_id = request.POST['customer_id']
        phone_number = request.POST['phone_number']
        contact_address = request.POST['contact_address']
        email  = request.POST['email']

        try:
            Customer.objects.create(
                name = name,
                customer_id = customer_id,
                phone_number = phone_number,
                contact_address = contact_address,
                email  = email,
            )
            url = "https://api.ng.termii.com/api/sms/send"
            payload = {
                "to": f"{phone_number[1:]}",
                "from": "Al-abrar",
                "sms": f"Dear {name} ! \nWelcome to Al-Abrar Fashion Design, \nLocated at Faisalco Conference Hall, Kauran Juli Kano-Kaduna Express Way, Zaria. \nThanks. ",
                "type": "plain",
                "channel": "generic",
                "api_key": "TLNWhmgMzn58KliQo5X83RwvYsoJ81AbhxuxToMMmFdBwSRRLIUTQnDxUL9jPC"

            }

            response = requests.post(url=url, data=payload)
            print(response.text)

            messages.info(request, 'Customer Created Successfully')
            
        except:
            messages.error(request, 'Customer Already Exists!')
        
        return redirect('customer-list')
    return render(request, 'alabrarAdmin/add_customer.html')

@login_required(login_url='login')
def customerList(request):
    customer_list = Customer.objects.all()
    context = {
        'customers': customer_list,
    }
    return render (request, 'alabrarAdmin/customer_list.html', context)

@login_required(login_url='login')
def customerDetails(request, pk):
    customer_detail = Customer.objects.get(id=pk)
    context = {
        'customer': customer_detail,
    }

    if request.method == "POST":
        name = request.POST['name']
        customer_id = request.POST['customer_id']
        phone_number = request.POST['phone_number']
        contact_address = request.POST['contact_address']
        email  = request.POST['email']

        customer_detail.name = name
        customer_detail.customer_id = customer_id
        customer_detail.phone_number = phone_number
        customer_detail.contact_address = contact_address
        customer_detail.email = email
        customer_detail.save()

        messages.info(request, 'Customer Updated Successfully')
        return redirect('customer-details', customer_detail.id)


    return render (request, 'alabrarAdmin/customer_details.html', context)

@login_required(login_url='login')
def deleteCustomer(request, pk):
    Customer.objects.get(id=pk).delete()
    return redirect('customer-list')


@login_required(login_url='login')
def addMeasurement(request):

    if request.method == 'POST' and 'kaftan_measurement' in request.POST:
        customer_id = request.POST['k_customer_id'] 
        tag = request.POST['k_tag'] 
        shoulder = request.POST['k_shoulder'] 
        long_hand = request.POST['h_long'] 
        short_hand = request.POST['h_short'] 
        short_length = request.POST['l_short'] 
        jampa_length = request.POST['jampa'] 
        full_length = request.POST['full'] 
        neck = request.POST['k_neck'] 
        burst = request.POST['k_burst'] 
        
        # customer = Customer.objects.get(customer_id=customer_id).id

        KaftanMeasurement.objects.create(
            customer = Customer.objects.get(customer_id=customer_id),
            tag = tag,
            shoulder = shoulder,
            long_hand = long_hand,
            short_hand = short_hand,
            short_length = short_length,
            jampa_length = jampa_length,
            full_length = full_length,
            neck = neck,
            burst = burst,
        )

        messages.info(request, 'Record added successfully')
        return redirect('add-measurement')



    if request.method == 'POST' and 'trouser_measurement' in request.POST:
        customer_id = request.POST['t_customer_id']
        tag = request.POST['t_tag']
        length = request.POST['t_length']
        waist = request.POST['t_waist']
        hip = request.POST['hip']
        thigh = request.POST['thigh']
        knee = request.POST['knee']
        calf = request.POST['calf']
        ankle = request.POST['ankle']

        TrouserMeasurement.objects.create(
            customer = Customer.objects.get(customer_id=customer_id), 
            tag = tag, 
            length = length, 
            waist = waist, 
            hip = hip, 
            thigh = thigh, 
            knee = knee, 
            calf = calf, 
            ankle = ankle, 
        )

        messages.info(request, 'Record added successfully')
        return redirect('add-measurement')


    if request.method == 'POST' and 'shirt_measurement' in request.POST:
        customer_id = request.POST['sh_customer_id']
        tag = request.POST['sh_tag']
        shoulder = request.POST['sh_shoulder']
        burst = request.POST['sh_burst']
        length = request.POST['sh_length']
        sleeve = request.POST['sh_sleeve']
        neck = request.POST['sh_neck']

        ShirtMeasurement.objects.create(
            customer = Customer.objects.get(customer_id=customer_id),  
            tag = tag, 
            length = length, 
            shoulder = shoulder, 
            neck = neck, 
            burst = burst, 
            sleeve = sleeve, 
        )

        messages.info(request, 'Record added successfully')
        return redirect('add-measurement')
    
    if request.method == 'POST' and 'suit_measurement' in request.POST:
        customer_id = request.POST['s_customer_id']
        tag = request.POST['s_tag']
        shoulder = request.POST['s_shoulder']
        chest = request.POST['chest']
        length = request.POST['s_length']
        sleeve = request.POST['s_sleeve']
        neck = request.POST['s_neck']
        waist = request.POST['s_waist']

        SuitMeasurement.objects.create(
            customer = Customer.objects.get(customer_id=customer_id),
            tag = tag,
            length = length,
            shoulder = shoulder,
            neck = neck,
            chest = chest,
            sleeve = sleeve,
            waist = waist,
        )

        messages.info(request, 'Record added successfully')
        return redirect('add-measurement')

    return render(request, 'alabrarAdmin/add_measurement.html')

@login_required(login_url='login')
def editMeasurement(request):

    if request.method == 'POST' and 'search_measurement' in request.POST:
        customer_id = request.POST['customer_id']
        measurement_type = request.POST['measurement_type']


        try:
            if measurement_type == 'Kaftan':
                measurements = KaftanMeasurement.objects.filter(customer=Customer.objects.get(customer_id=customer_id)).all() 
            elif measurement_type == 'Trouser':
                measurements = TrouserMeasurement.objects.filter(customer=Customer.objects.get(customer_id=customer_id)).all() 
            elif measurement_type == 'Suit':
                measurements = SuitMeasurement.objects.filter(customer=Customer.objects.get(customer_id=customer_id)).all() 
            else:
                measurements = ShirtMeasurement.objects.filter(customer=Customer.objects.get(customer_id=customer_id)).all() 
            
            context = {
                'measurements': measurements,
                'type': measurement_type,
            }
            
        except: 
                context = {
                    'type': measurement_type,
                }

        return render(request, 'alabrarAdmin/measurement_list.html', context)

    return render(request, 'alabrarAdmin/edit_measurement.html')

@login_required(login_url='login')
def measurementDetails(request, pk, m_type):
    try: 
        if m_type == 'Kaftan':
            measurement = KaftanMeasurement.objects.get(id=pk)
        elif m_type == 'Trouser':
            measurement = TrouserMeasurement.objects.get(id=pk)
        
        elif m_type == 'Suit':
            measurement = SuitMeasurement.objects.get(id=pk)
        else:
            measurement = ShirtMeasurement.objects.get(id=pk)
        
        context = {
            'measurement': measurement,
            'm_type': m_type,
        }
        
    except:
        context = {
            'm_type': m_type,
        }
    
    if request.method == 'POST' and m_type == 'Kaftan':
        customer_id = request.POST['k_customer_id'] 
        tag = request.POST['k_tag'] 
        shoulder = request.POST['k_shoulder'] 
        long_hand = request.POST['h_long'] 
        short_hand = request.POST['h_short'] 
        short_length = request.POST['l_short'] 
        jampa_length = request.POST['jampa'] 
        full_length = request.POST['full'] 
        neck = request.POST['k_neck'] 
        burst = request.POST['k_burst']

        kaftan_object = KaftanMeasurement.objects.get(id=pk)

        kaftan_object.customer = Customer.objects.get(customer_id=customer_id)
        kaftan_object.tag = tag
        kaftan_object.shoulder = shoulder
        kaftan_object.long_hand = long_hand
        kaftan_object.short_hand = short_hand
        kaftan_object.short_length = short_length
        kaftan_object.jampa_length = jampa_length
        kaftan_object.full_length = full_length
        kaftan_object.neck = neck
        kaftan_object.burst = burst
        kaftan_object.save()

        messages.info(request, 'Record updated successfully')
        return redirect('measurement-details', measurement.id, m_type)


    if request.method == 'POST' and m_type == 'Trouser':
        customer_id = request.POST['t_customer_id']
        tag = request.POST['t_tag']
        length = request.POST['t_length']
        waist = request.POST['t_waist']
        hip = request.POST['hip']
        thigh = request.POST['thigh']
        knee = request.POST['knee']
        calf = request.POST['calf']
        ankle = request.POST['ankle']

        trouser_object = TrouserMeasurement.objects.get(id=pk)

        trouser_object.customer = Customer.objects.get(customer_id=customer_id)
        trouser_object.length = length
        trouser_object.waist = waist
        trouser_object.hip = hip
        trouser_object.thigh = thigh
        trouser_object.knee = knee
        trouser_object.calf = calf
        trouser_object.ankle = ankle
        trouser_object.save()

        messages.info(request, 'Record updated successfully')
        return redirect('measurement-details', measurement.id, m_type)
    
    if request.method == 'POST' and m_type == 'Shirt':
        customer_id = request.POST['sh_customer_id']
        tag = request.POST['sh_tag']
        shoulder = request.POST['sh_shoulder']
        burst = request.POST['sh_burst']
        length = request.POST['sh_length']
        sleeve = request.POST['sh_sleeve']
        neck = request.POST['sh_neck']

        shirt_object = ShirtMeasurement.objects.get(id=pk)
        shirt_object.customer = Customer.objects.get(customer_id=customer_id)
        shirt_object.tag = tag
        shirt_object.shoulder = shoulder
        shirt_object.burst = burst
        shirt_object.length = length
        shirt_object.sleeve = sleeve
        shirt_object.neck = neck
        shirt_object.save()

        messages.info(request, 'Record updated successfully')
        return redirect('measurement-details', measurement.id, m_type)


    if request.method == 'POST' and m_type == 'Suit':
        customer_id = request.POST['s_customer_id']
        tag = request.POST['s_tag']
        shoulder = request.POST['s_shoulder']
        chest = request.POST['chest']
        length = request.POST['s_length']
        sleeve = request.POST['s_sleeve']
        neck = request.POST['s_neck']
        waist = request.POST['s_waist']

        suit_object = SuitMeasurement.objects.get(id=pk)
        suit_object.customer = Customer.objects.get(customer_id=customer_id)
        suit_object.tag = tag
        suit_object.shoulder = shoulder
        suit_object.chest = chest
        suit_object.length = length
        suit_object.sleeve = sleeve
        suit_object.neck = neck
        suit_object.waist = waist
        suit_object.save()

        messages.info(request, 'Record updated successfully')
        return redirect('measurement-details', measurement.id, m_type)



    return render(request, 'alabrarAdmin/edit_measurement_form.html', context)

@login_required(login_url='login')
def createJob(request):
       
    design_type = DesignType.objects.all()
    context = {
        'design_type':design_type,
    }
    if request.method == 'POST' and 'create_job' in request.POST:
        
        customer_id = request.POST['customer_id']
        design_id = request.POST.getlist('design')
        materials = request.FILES.getlist('material')

  
        amount_list = []
        for i in design_id:
            amount_per_item = DesignType.objects.get(id=i).amount
            amount_list.append(amount_per_item)

        total_amount = sum(amount_list)

        jobItem_ids = []

        for item, material in zip(design_id, materials):
            created = JobItem.objects.create(
                design_type = DesignType.objects.get(id=item),
                material = material
            )
            jobItem_ids.append(created.id)
        


        contxt = {
            'customer_id': customer_id,
            'total_amount': total_amount,
            'jobItems': jobItem_ids,
            
        }





        return render(request, 'alabrarAdmin/confirm_job.html', contxt )

    if request.method == 'POST' and 'confirm_job' in request.POST:
        customer_id = request.POST['customer_id']
        amount_charged = request.POST['amount_charged']
        amount_paid = request.POST['amount_paid']
        discount = request.POST['discount']
        collection_date = request.POST['collection_date']
        jobItems = request.POST.getlist('job_items')

      


        
        convert_discount = Money(int(discount), 'NGN')
        convert_amount_paid = Money(int(amount_paid), 'NGN')

        total_amount_charges = []    
        for i in jobItems:
            total_amount_charges.append(JobItem.objects.get(id=i).design_type.amount)

        amount_charged = sum(total_amount_charges)

        total = amount_charged - convert_discount

        balance = total - convert_amount_paid





        c_month, c_day, c_year = collection_date.split('/')
        c_d = date(int(c_year), int(c_month), int(c_day))

        job_created = Job.objects.create(
            customer = Customer.objects.get(customer_id=customer_id),
            amount_charged = amount_charged,
            discount = convert_discount,
            amount_paid = convert_amount_paid,
            total = total,
            balance = balance,
            collection_date = c_d,
        )

        for j in jobItems:
            job_item = JobItem.objects.get(id=j)
            job_item.job = Job.objects.get(id=job_created.id)
            job_item.save()

        

        messages.info(request, 'Job Created successfully')
 

 
    return render(request, 'alabrarAdmin/create_job.html', context)

@login_required(login_url='login')
def viewJobs(request):
    jobs = Job.objects.all()
    status = []
    utc=pytz.UTC
    

    for job in jobs:

        if job.collection_date <= utc.localize(datetime.now()):
            status.append('completed')
        else:
            status.append('pending')
    yanxu = utc.localize(datetime.now())
    context = {
        'jobs': jobs,
        'yanxu': yanxu
    }
    return render(request, 'alabrarAdmin/jobs.html', context)

def viewJobDetails(request, pk):

    job = Job.objects.get(id=pk)
    job_items = JobItem.objects.filter(job=job).all()

    if request.method == 'POST' and 'reschedule_date' in request.POST:
        reschedule_date = request.POST['collection_date']
        c_month, c_day, c_year = reschedule_date.split('/')
        c_d = date(int(c_year), int(c_month), int(c_day))

        job.collection_date = c_d
        job.save()


        customer = Customer.objects.get(id=job.customer.id)
        url = "https://api.ng.termii.com/api/sms/send"
        payload = {
            "to": f"{(customer.phone_number)[1:]}",
            "from": "Al-abrar",
            "sms": f"Dear {customer.name} ! This is to notify you that your appointment with our gallery(Al-abrar fashion design limited) has been postponed to {c_day}/{c_month}/{c_year} we sincerely apologise for the inconveniences Thank you.",
            "type": "plain",
            "channel": "generic",
            "api_key": "TLNWhmgMzn58KliQo5X83RwvYsoJ81AbhxuxToMMmFdBwSRRLIUTQnDxUL9jPC"

        }

        response = requests.post(url=url, data=payload)
        print(response)



        return redirect('view-jobs')
    
    if request.method == 'POST' and 'deposit' in request.POST:
        amount_deposited = request.POST['amount_deposited']
        job.amount_paid = job.amount_paid + Money(int(amount_deposited), 'NGN')
        job.balance = job.balance - Money(int(amount_deposited), 'NGN')
        job.save()

    context = {
        'job': job,
        'job_items': job_items,
    }

    return render(request, 'alabrarAdmin/job_details.html', context)

@login_required(login_url='login')
def createStaff(request):
    if request.method == 'POST' and 'create_staff' in request.POST:
        name = request.POST['name']
        staff_id = request.POST['staff_id']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        contact_address = request.POST['contact_address']
        print(name)

        Staff.objects.create(
            name = name,
            staff_number = staff_id,
            phone_number = phone_number,
            address = contact_address,
            email = email
        )
        messages.info(request, 'Staff Created successfully')
        return redirect('create-staff')
        
    return render(request, 'alabrarAdmin/create_staff.html')

@login_required(login_url='login')
def staffList(request):
    staff_list = Staff.objects.all()
    context = {
        'staff_list': staff_list,
    }



    return render(request, 'alabrarAdmin/staff_list.html', context)

@login_required(login_url='login')
def staffDetails(request, pk):
    staff = Staff.objects.get(id=pk)

    context = {
        'staff': staff,
    }

    if request.method == 'POST' and 'update_staff' in request.POST:
        name = request.POST['name']
        staff_id = request.POST['staff_id']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        contact_address = request.POST['contact_address']

        staff.name = name
        staff.phone_number = phone_number
        staff.staff_number = staff_id
        staff.email = email
        staff.address = contact_address
        staff.save()

        messages.info(request, 'Staff Updated successfully')
        return redirect('staff-details', staff.id)

    return render(request, 'alabrarAdmin/staff_details.html', context)

@login_required(login_url='login')
def deleteStaff(request, pk):
    Staff.objects.get(id=pk).delete()
    return redirect('staff-list')


@login_required(login_url='login')
def staffActivity(request):
    activity_items = WorkType.objects.all()

    context = {
        'activity_items': activity_items
    }

    if request.method == 'POST' and 'create_activity' in request.POST:
        staff_id = request.POST['staff_id']
        qty = request.POST['qty']
        activity = request.POST['activity']

        StaffActivity.objects.create(
            staff = Staff.objects.get(staff_number=staff_id),
            quantity = qty,
            activitity = WorkType.objects.get(id=int(activity)),

        )

        messages.info(request, 'Staff Payment successfully')
        return redirect('create-staff-activity')
    return render(request, 'alabrarAdmin/staff_activity.html', context)
    

@login_required(login_url='login')
def addConsumable(request):

    if request.method == 'POST' and 'add_item' in request.POST:
        item = request.POST['item']
        amount = request.POST['amount']

        Consumables.objects.create(
            item = item,
            amount = Money(int(amount), 'NGN')
        )

        messages.info(request, 'Item Added successfully')
        return redirect('items-list')

    return render(request, 'alabrarAdmin/add_consumable.html')

@login_required(login_url='login')
def itemsList(request):
    items_list = Consumables.objects.all()
    context = {
        'items': items_list,
    }

    return render(request, 'alabrarAdmin/items_list.html', context)

@login_required(login_url='login')
def itemDetails(request, pk):
    item = Consumables.objects.get(id=pk)
    context = {
        'item': item,
    }

    if request.method == 'POST' and 'update_item' in request.POST:
        item_name = request.POST['item']
        amount = request.POST['amount']

        if 'NGN' in amount:
            price_currency = amount[0:3]
            actual_currency = amount[3:-3]
            final_price = int(actual_currency.replace(',', ''))
            item.item = item_name
            item.amount = item.amount + Money(final_price, price_currency)
            item.save()


        
        else:
            item.item = item_name
            item.amount = item.amount + Money(int(amount), 'NGN')
            item.save()


        
        messages.info(request, 'Item Updated successfully')
        return redirect('items-list')



    return render(request, 'alabrarAdmin/item_details.html', context)

@login_required(login_url='login')
def deleteItem(request, pk):
    Consumables.objects.get(id=pk).delete()
    return render(request, 'alabrarAdmin/items_list.html')

@login_required(login_url='login')
def createExpenditure(request):
    items = Consumables.objects.all()
    context = {
        'items': items
    }

    if request.method == 'POST' and 'add_expenditure' in request.POST:
        item = request.POST['item']
        amount_collected = request.POST['amount_collected']
        staff_id = request.POST['staff_id']

        ItemExpenditure.objects.create(
            item = Consumables.objects.get(id=item),
            amount = Money(int(amount_collected), 'NGN'),
            recieved_by = Staff.objects.get(staff_number=staff_id)
        )

        item_sub = Consumables.objects.get(id=item)
        item_sub.amount -= Money(int(amount_collected), 'NGN')
        item_sub.save()

        messages.info(request, 'Expenditure Recorded successfully')
        return redirect('expenses-list')

    return render(request, 'alabrarAdmin/create_expenditure.html', context)

@login_required(login_url='login')
def expensesList(request):
    items_expenses = ItemExpenditure.objects.all()
    context = {
        'items_expenses': items_expenses,
    }
  
    return render(request, 'alabrarAdmin/expenses_list.html', context)


@login_required(login_url='login')
def payStaff(request):
    if request.method == 'POST' and 'proceed' in request.POST:
        staff_id = request.POST['staff_id']
        start_date = request.POST['from']
        end_date = request.POST['to']

        return redirect('confirm-payment', staff_id, start_date, end_date)      

    return render(request, 'alabrarAdmin/pay_staff.html')


@login_required(login_url='login')
def confirmPayment(request, pk, start_date, end_date):
    new_end_date = date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10])) + timedelta(days=1)
    query = StaffActivity.objects.filter(
        done_on__range=[start_date, new_end_date],
        staff=Staff.objects.get(staff_number=pk),
        wages_group=None
        ).all()

    grand_total = []
    for i in query:
        grand_total.append(i.activitity.amount*i.quantity)
    
    staff = Staff.objects.get(staff_number=pk)
    context = {
        'staff': staff,
        'g_total': sum(grand_total),
        'activities': query,
    }

    if request.method == 'POST' and 'pay' in request.POST:
        amount_paid = request.POST['amount_paid']
        
        qry = StaffWage.objects.create(
            staff = Staff.objects.get(staff_number=pk),
            total_amount = sum(grand_total),
            amount_paid = Money(int(amount_paid), 'NGN')
        )

        for i in query:
            i.wages_group = StaffWage.objects.get(id=qry.id)
            i.save()

    return render(request, 'alabrarAdmin/confirm_staff_payment.html', context)




@login_required(login_url='login')
def activityList(request):
    activities = StaffActivity.objects.all()
    context = {
        'activities': activities,
    }
    return render(request, 'alabrarAdmin/activity_list.html', context)

@login_required(login_url='login')
def wagesList(request):
    wages = StaffWage.objects.all()
    context = {
        'wages': wages,
    }
    return render(request, 'alabrarAdmin/wages_list.html', context)


@login_required(login_url='login')
def editActivity(request, pk):
    activity = StaffActivity.objects.get(id=pk)
    activity_items = WorkType.objects.all()
    context = {
        'activity': activity,
        'activity_items': activity_items,
    }

    if request.method == 'POST' and 'update_activity' in request.POST:
        staff_id = request.POST['staff_id']
        activity_item = request.POST['activity']
        qty = request.POST['qty']

        activity.staff = Staff.objects.get(staff_number=staff_id)
        activity.activitity = WorkType.objects.get(id=activity_item)
        activity.quantity = qty
        activity.save()

        return redirect('activity-list')



    return render(request, 'alabrarAdmin/update_staff_activity.html', context)



@login_required(login_url='login')
def editWages(request, pk):
    wage = StaffWage.objects.get(id=pk)
    activites = StaffActivity.objects.filter(wages_group=wage).all()
    context = {
        'activities': activites,
        'wage': wage,
    }

    if request.method == 'POST' and 'update_payment' in request.POST:
        amount_paid = request.POST['amount_paid']
        wage.amount_paid = wage.amount_paid + Money(int(amount_paid), 'NGN')
        wage.save()


        return redirect('wages-list')
    return render(request, 'alabrarAdmin/edit_staff_payment.html', context)



@login_required(login_url='login')
def generalExpenditure(request, month=None, year=None):
    if request.method == 'POST' and 'filter' in request.POST:
        filter_date = request.POST['filter_date']
        c_month, c_day, c_year = filter_date.split('/')
        return redirect('general-expenditure', c_month, c_year)
        
        # c_d = datetime.date(int(c_year), int(c_month), int(c_day))

    if month and year:


        staff_wages = StaffWage.objects.filter(paid_on__year=year, paid_on__month=month).all()
        item_expenses = ItemExpenditure.objects.filter(incurred_on__year=year, incurred_on__month=month).all()
    else:
        staff_wages = StaffWage.objects.all()
        item_expenses = ItemExpenditure.objects.all()
    
    wages_sum = []
    item_sum = []


    


    for i in staff_wages:
        wages_sum.append(i.amount_paid)

    for j in item_expenses:
        item_sum.append(j.amount)

    context = {
        'staff_wages': staff_wages,
        'wages_sum': sum(wages_sum),
        'item_expenses': item_expenses,
        'item_sum': sum(item_sum),

    }
    return render(request, 'alabrarAdmin/general_expenditures.html', context)

@login_required(login_url='login')
def generalIncome(request, month=None, year=None):
    if request.method == 'POST' and 'filter' in request.POST:
        filter_date = request.POST['filter_date']
        c_month, c_day, c_year = filter_date.split('/')
        return redirect('general-income', c_month, c_year)
        
        # c_d = datetime.date(int(c_year), int(c_month), int(c_day))

    if month and year:


        general_income = Job.objects.filter(recieved__year=year, recieved__month=month).all()
       
    else:
        general_income = Job.objects.all()

    
    income_sum = []
    charged_amount_sum = []
    expected_income_sum = []
    


    for i in general_income:
        charged_amount_sum.append(i.amount_charged)
        income_sum.append(i.amount_paid)
        expected_income_sum.append(i.balance)


    context = {
        'income': general_income,
        'amount_charged': sum(charged_amount_sum),
        'income_sum': sum(income_sum),
        'expected_income': sum(expected_income_sum),

    }
    return render(request, 'alabrarAdmin/general_income.html', context)


@login_required(login_url='login')
def createSells(request):
    sells_item = SellsItem.objects.all()
    
    if request.method == 'POST' and 'create_sells' in request.POST:
        item = request.POST['item']
        amount_sold = request.POST['amount_sold']

        Sell.objects.create(
            item = SellsItem.objects.get(id=item),
            amount = Money(int(amount_sold), 'NGN')
        )

        item_query = SellsItem.objects.get(id=item)
        item_query.available = item_query.available - Money(int(amount_sold), 'NGN')
        item_query.save()



    context = {
        'sells_item': sells_item,
    }
    return render(request, 'alabrarAdmin/create_sells.html', context)


@login_required(login_url='login')
def sellsRecord(request, month=None, year=None):
    if request.method == 'POST' and 'filter' in request.POST:
        filter_date = request.POST['filter_date']
        c_month, c_day, c_year = filter_date.split('/')
        return redirect('sells-record', c_month, c_year)
        
        # c_d = datetime.date(int(c_year), int(c_month), int(c_day))

    if month and year:


        sells = Sell.objects.filter(sold_on__year=year, sold_on__month=month).all()
       
    else:
        sells = Sell.objects.all()

    paginator = Paginator(sells, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total = sum(i.amount for i in page_obj)
    context = {
        'sells': page_obj,
        'total': total,
    }

    return render(request, 'alabrarAdmin/sells_record.html', context)

@login_required(login_url='login')
def addSellsItem(request):
    if request.method == 'POST' and 'add_item' in request.POST:
        item = request.POST['item']
        amount = request.POST['amount']

        query = SellsItem.objects.create(
            description = item,
            available = Money(int(amount), 'NGN')
        )

        SellItemRestock.objects.create(
            sells_item = SellsItem.objects.get(id=query.id),
            amount_stocked = amount
        )
        return redirect('sells-item-list')
    return render(request, 'alabrarAdmin/add_sells_item.html')

@login_required(login_url='login')
def sellsItemList(request):
    sells_item = SellsItem.objects.all()
    context = {
        'sells_item': sells_item,
    }
    return render(request, 'alabrarAdmin/sells_item_list.html', context)

@login_required(login_url='login')
def updateSellsItem(request, pk):
    item = SellsItem.objects.get(id=pk)

    if request.method == 'POST' and 'update_item' in request.POST:
        amount = request.POST['amount']
        item.available = item.available + Money(int(amount), 'NGN')
        item.save()
        
        SellItemRestock.objects.create(
            sells_item = SellsItem.objects.get(id=pk),
            amount_stocked = Money(int(amount), 'NGN')
        )
        
        return redirect('sells-item-list')


    context = {
        'item': item
    }
    return render(request, 'alabrarAdmin/update_sells_item.html', context)


@login_required(login_url='login')
def workTypeItem(request):
    if request.method == 'POST' and 'add_work_type':
        name = request.POST['name']
        amount = request.POST['amount']

        WorkType.objects.create(
            name = name,
            amount = Money(int(amount), 'NGN')
        )

        return redirect('create-work-type')
    return render(request, 'alabrarAdmin/add_worktype.html')


@login_required(login_url='login')
def workTypeList(request):
    works = WorkType.objects.all()
    context = {
        'items': works,
    }
    return render(request, 'alabrarAdmin/work_type_list.html', context)



@login_required(login_url='login')
def workTypeDetail(request, pk):
    item = WorkType.objects.get(id=pk)

    if request.method == 'POST' and 'update_work_type' in request.POST:
        name = request.POST['name']
        amount = request.POST['amount']
        item.name = name
        item.amount = Money(int(amount), 'NGN')
        item.save()

        return redirect('work-type-list')
    context = {
        'item': item,
    }
    return render(request, 'alabrarAdmin/work_type_detail.html', context)

@login_required(login_url='login')
def deleteWorkType(request, pk):
    item = WorkType.objects.get(id=pk)
    item.delete()

    return redirect('work-type-list')