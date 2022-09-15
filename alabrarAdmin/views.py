from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse
from PIL import Image
import datetime
from djmoney.money import Money
import pytz
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
)
from django.contrib import messages
# Create your views here.

def dashboard(request):
    return render(request, 'alabrarAdmin/dashboard.html')

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
            messages.info(request, 'Customer Created Successfully')
            
        except:
            messages.error(request, 'Customer Already Exists!')
        
        return redirect('customer-list')
    return render(request, 'alabrarAdmin/add_customer.html')


def customerList(request):
    customer_list = Customer.objects.all()
    context = {
        'customers': customer_list,
    }
    return render (request, 'alabrarAdmin/customer_list.html', context)

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

def deleteCustomer(request, pk):
    Customer.objects.get(id=pk).delete()
    return redirect('customer-list')



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


        for item, material in zip(design_id, materials):
            JobItem.objects.create(
                design_type = DesignType.objects.get(id=item),
                material = material


            )

        contxt = {
            'customer_id': customer_id,
            'total_amount': total_amount,
            'design_id': design_id,
        }





        return render(request, 'alabrarAdmin/confirm_job.html', contxt )

    if request.method == 'POST' and 'confirm_job' in request.POST:
        customer_id = request.POST['customer_id']
        amount_charged = request.POST['amount_charged']
        amount_paid = request.POST['amount_paid']
        discount = request.POST['discount']
        collection_date = request.POST['collection_date']
        design_ids = request.POST.getlist('design_ids')

        
        convert_discount = Money(int(discount), 'NGN')
        convert_amount_paid = Money(int(amount_paid), 'NGN')

        total_amount_charges = []    
        for i in design_ids:
            total_amount_charges.append(DesignType.objects.get(id=i).amount)

        amount_charged = sum(total_amount_charges)

        total = amount_charged - convert_discount

        balance = total - convert_amount_paid





        c_month, c_day, c_year = collection_date.split('/')
        c_d = datetime.date(int(c_year), int(c_month), int(c_day))

        job_created = Job.objects.create(
            customer = Customer.objects.get(customer_id=customer_id),
            amount_charged = amount_charged,
            discount = convert_discount,
            amount_paid = convert_amount_paid,
            total = total,
            balance = balance,
            collection_date = c_d,
        )

        for j in design_ids:
            job_item = JobItem.objects.filter(design_type=j)
            for i in job_item:
                i.job = Job.objects.get(id=job_created.id)
                i.save()
        


        messages.info(request, 'Job Created successfully')
 

 
    return render(request, 'alabrarAdmin/create_job.html', context)


def viewJobs(request):
    jobs = Job.objects.all()
    status = []
    utc=pytz.UTC
    

    for job in jobs:

        if job.collection_date <= utc.localize(datetime.datetime.now()):
            status.append('completed')
        else:
            status.append('pending')
    yanxu = utc.localize(datetime.datetime.now())
    context = {
        'jobs': jobs,
        'yanxu': yanxu
    }
    return render(request, 'alabrarAdmin/jobs.html', context)

def viewJobDetails(request, pk):

    job = Job.objects.get(id=pk)
    job_items = JobItem.objects.filter(job=job).all()

    context = {
        'job': job,
        'job_items': job_items,
    }

    return render(request, 'alabrarAdmin/job_details.html', context)