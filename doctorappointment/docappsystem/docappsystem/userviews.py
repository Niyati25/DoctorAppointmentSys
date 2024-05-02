from django.shortcuts import render,redirect,HttpResponse
from dasapp.models import DoctorReg,Specialization,CustomUser,Appointment,Page
import random
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Appointment
from .forms import AppointmentForm  # Import the form for creating an appointment

def usersignup()
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        specialization_id = request.POST.get('specialization_id')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email already exist')
            return redirect('usersignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,'Username already exist')
            return redirect('usersignup')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=3,
                profile_pic = pic,
            )
            user.set_password(password)
            user.save()
            spid =Specialization.objects.get(id=specialization_id)
            doctor = DoctorReg(
                admin = user,
                
                mobilenumber = mobno,
                specialization_id = spid,
                
            )
            doctor.save()            
            messages.success(request,'Signup Successfully')
            return redirect('docsignup')
    

    return render(request,'cust/userreg.html',context)

@login_required(login_url='/')
def USERHOME(request):
    # Your implementation for the user home view here
    user_admin = request.user
    user_reg = UserReg.objects.get(admin=user_admin)
    allaptcount = Appointment.objects.filter(user_id=user_reg).count
    newaptcount = Appointment.objects.filter(status='0',user_id=user_reg).count
    appaptcount = Appointment.objects.filter(status='Approved',user_id=user_reg).count
    canaptcount = Appointment.objects.filter(status='Cancelled',user_id=user_reg).count
    context = {
        'newaptcount':newaptcount,
        'allaptcount':allaptcount,
        'appaptcount':appaptcount,
        'canaptcount':canaptcount


    }
    return render(request,'cust/userhome.html',context)


def Index(request):
    # Your implementation for the index view here
    pass

def AddPatient(request):
        if request.method == "POST":
        # Extract patient details from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        # You can add more fields as needed

        # Create a new Patient object with the extracted details
        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            # Assign other fields similarly
        )

        # Save the new patient object to the database
        new_patient.save()

        # Optionally, you can add a success message
        messages.success(request, 'Patient added successfully')

        # Redirect to a success page or any other appropriate page
    return render(request, 'cust/add_patient.html')

def Patient_Details(request, id):
    # Your implementation for viewing patient details here
    patient = get_object_or_404(Patient, id=id)

    # Pass the patient object to the template for rendering
    context = {
        'patient': patient,
    }

    # Render the template with patient details
    return render(request, 'cust/patient_details.html', context)

def Update_Patient_Details(request, id):
    # Your implementation for updating patient details here
    patient = get_object_or_404(Patient, id=id)

    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = PatientForm(request.POST, instance=patient)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the updated patient details to the database
            form.save()

            # Optionally, you can add a success message
            messages.success(request, 'Patient details updated successfully')

            # Redirect to the patient details page
            return redirect('patientdetails', id=id)
    else:
        # If it's a GET request, create a form instance with the current patient data
        form = PatientForm(instance=patient)

    # Render the template with the form for updating patient details
    return render(request, 'cust/update_patient_details.html', {'form': form})

def User_Search_Appointments(request):
    # Your implementation for searching appointments here
    user_admin = request.user
    user_reg = UserReg.objects.get(admin=doctor_admin)
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query) & Appointment.objects.filter(doctor_id=doctor_reg)
            messages.success(request, "Search against " + query)
            return render(request, 'cust/search-appointment.html', {'patient': patient, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'cust/search-appointment.html', {})

def User_Edit_Appointment(request):
    # Your implementation for editing appointments here
    def User_Edit_Appointment(request, id):
    # Retrieve the appointment object from the database based on the provided ID
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = AppointmentForm(request.POST, instance=appointment)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the updated appointment details to the database
            form.save()

            # Optionally, you can add a success message
            messages.success(request, 'Appointment details updated successfully')

            # Redirect to the user's appointments page or any other appropriate page
            return redirect('view_appointment')
    else:
        # If it's a GET request, create a form instance with the current appointment data
        form = AppointmentForm(instance=appointment)

    # Render the template with the form for updating appointment details
    return render(request, 'cust/edit_appointment.html', {'form': form})

def User_Cancel_Appointment(request):
    # Your implementation for canceling appointments here
    appointment = get_object_or_404(Appointment, id=id)

    # Check if the appointment exists and has not already been cancelled
    if appointment.status != 'Cancelled':
        # Update the status of the appointment to 'Cancelled'
        appointment.status = 'Cancelled'
        appointment.save()

        # Optionally, you can add a success message
        messages.success(request, 'Appointment cancelled successfully')
    else:
        # Optionally, you can add a warning message if the appointment has already been cancelled
        messages.warning(request, 'Appointment has already been cancelled')

    # Redirect to the user's appointments page or any other appropriate page
    return redirect('view_appointment')


def create_appointment(request):
    # Your implementation for creating appointments here
    if request.method == "POST":
        # Create a form instance and populate it with data from the request
        form = AppointmentForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Save the appointment details to the database
            form.save()

            # Optionally, you can add a success message
            messages.success(request, 'Appointment created successfully')

            # Redirect to a success page or any other appropriate page
            return redirect('create_appointment')
    else:
        # If it's a GET request, create a blank form instance
        form = AppointmentForm()

    # Render the template with the form for creating an appointment
    return render(request, 'cust/create_appointment.html', {'form': form})

def USERBASE(request):
    
    return render(request, 'userbase.html',context)

def Index(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    context = {'doctorview': doctorview,
    'page':page,
    }
    return render(request, 'index.html',context)




def create_appointment(request):
    userview = UserReg.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        appointmentnumber = random.randint(100000000, 999999999)
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        date_of_appointment = request.POST.get('date_of_appointment')
        time_of_appointment = request.POST.get('time_of_appointment')
        doctor_id = request.POST.get('doctor_id')
        additional_msg = request.POST.get('additional_msg')

        # Retrieve the DoctorReg instance using the doctor_id
        doc_instance = DoctorReg.objects.get(id=doctor_id)

        # Validate that date_of_appointment is greater than today's date
        try:
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date <= today_date:
                # If the appointment date is not in the future, display an error message
                messages.error(request, "Please select a date in the future for your appointment")
                return redirect('appointment')  # Redirect back to the appointment page
        except ValueError:
            # Handle invalid date format error
            messages.error(request, "Invalid date format")
            return redirect('appointment')  # Redirect back to the appointment page

        # Create a new Appointment instance with the provided data
        appointmentdetails = Appointment.objects.create(
            appointmentnumber=appointmentnumber,
            fullname=fullname,
            email=email,
            mobilenumber=mobilenumber,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id=doc_instance,
            additional_msg=additional_msg
        )

        # Display a success message
        messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")

        return redirect('appointment')

    context = {'doctorview': doctorview,
    'page':page}
    return render(request, 'appointment.html', context)


def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)
def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)




