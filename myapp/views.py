from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Customer, UserInfo
from . import models
from django.core.exceptions import ObjectDoesNotExist


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Retrieve the user object by username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if not user.is_active:
                messages.warning(request, f'Account with username {username} is locked. Please contact the Administrator.')
                return redirect('index')
            else:
                # Authenticate the user using Django's authentication system
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    messages.error(request, 'Invalid password. Please try again.')
                    return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid username. Please try again.')
            return render(request, 'login.html')

    return render(request, 'login.html')


# TODO: method to logout users
def logout_user(request):
    logout(request)
    return redirect('login_user')



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mode = request.POST.get('mode')
        user_type = request.POST.get('userType')
        admin_password = request.POST.get('adminPassword')

        if mode == 'admin':
            if admin_password == 'isadmin':
                user = User.objects.create_user(username=username, password=password)
                if user_type == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
                elif user_type == 'staff':
                    user.is_staff = True
                else:
                    messages.error(request, 'Invalid user type.')
                    return redirect('register')

                user.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('index')
            else:
                messages.error(request, 'Incorrect admin password. Please provide the correct password.')
                return redirect('register')
        else:  # Regular user mode
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')

    return render(request, 'register.html')


# Main Dashboard/page
@login_required(login_url='login_user')
def index(request):
    vip_data = []
    try:
         # if the current user is admin then display all owners
        if request.user.is_superuser:
            customers = User.objects.all()
            header = ['ID', 'Username', 'Email', 'Date Joined', 'Last Login', 'Authorized Type', 'Actions']
        else:
            # Try to get the UserInfo object for the current user
            user_info = UserInfo.objects.get(user=request.user)
            # If successful, get the customers created by the current user
            customers = Customer.objects.filter(created_by=user_info.id)
            header = ['ID', 'Username', 'Email', 'Phone Number','Actions']
            vip_data = []

            for customer in customers:
                # Extract customer data
                customer_data = {
                    'VIP Status': customer.vip_status,
                }
                vip_data.append(customer_data)

    except ObjectDoesNotExist:
        # If no UserInfo object is found, return an empty queryset
        customers = Customer.objects.none()
        header = ['ID', 'Username', 'Email', 'Age','Actions']


    return render(request, 'index.html', {'data': customers, 'header': header, 'vip_data': vip_data})

@login_required(login_url='login_user')
def createUser(request):
    if request.method == "POST":
        # Get user inputs from the form
        name = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        address = request.POST.get('address')
        phone_number = request.POST.get('phnumber')
        orders = request.POST.get('orders')
        vip_status = request.POST.get('vip_status')

        # Try to get the UserInfo object for the current user
        try:
            user_info = UserInfo.objects.get(user=request.user)
        except ObjectDoesNotExist:
            # If no UserInfo object is found, create one
            user_info = UserInfo(user=request.user)
            user_info.save()

        # Check if all required fields are provided
        if name and address and orders and vip_status:
            # Save customer to Customer model
            customer_obj = Customer(name=name, email=email, address=address, age=age, phone_number=phone_number,
                                    orders=orders, vip_status=vip_status, created_by=user_info)
            customer_obj.save()

            messages.success(request, "Customer created successfully.")
            return redirect('index')
        else:
            messages.error(request, "Make sure to enter all the required information.")

    return render(request, 'Create.html')


# we don't want unauthenticated user to be able to delete customer information and also they be even sey
# information about the customer only if the have created them
@login_required(login_url='login_user')
def delete(request, id):
    if request.method == 'GET':
        try:
            user_record = Customer.objects.get(id=id)

            # Check if the current user is the creator of the record
            if user_record.created_by.user == request.user:
                return render(request, 'confirm_delete.html', {'user_record': user_record})
            else:
                messages.error(request, "You are not authorized to delete this record.")
                return redirect('index')
        except Customer.DoesNotExist:
            messages.warning(request, f'Record with ID {id} does not exist Or You are not authorized to delete this record.')
            return redirect('index')

    # if the request method is post Then delete the record
    elif request.method == 'POST':
        # If the request is not a GET request, handle the actual deletion logic
        try:
            # raise NotImplementedError('You can only delete records in GET requests')
            user_record = Customer.objects.get(id=id)
            if user_record.created_by == request.user:
                user_record.delete()
                messages.success(request, f'Record with ID {id} and name of {user_record.name} deleted successfully.')
            else:
                messages.error(request, "You are not authorized to delete this record.")
        except Customer.DoesNotExist:
            messages.warning(request, f'Record with ID {id} does not exist.')

        return redirect('index')

def lock_owner(request, id):
    if request.method == 'GET':
        # Fetch the user object with the provided ID
        user_account = User.objects.get(id=id)

        # Check if the user exists
        if user_account is not None:
            # Set the user's is_active attribute to False
            user_account.is_active = False
            # Save the changes to the user object
            user_account.save()
            # Display a success message indicating that the account is locked
            messages.success(request, f' Account with Name {user_account.username} is Ban/Locked.....')
            return redirect('index')
    # If the user does not exist, display a warning message
    messages.warning(request, f' This Account with ID of {id} does not exist...')
    return redirect('index')

# Method to unlock accounts by the admin
def unlock_owner(request, id):
    if request.method == 'GET':
        # Fetch the user object with the provided ID
        user_account = User.objects.get(id=id)
        # Check if the user exists
        if user_account is not None:
            # Set the user's is_active attribute to False
            user_account.is_active = True
            # Save the changes to the user object
            user_account.save()
            # Display a success message indicating that the account is locked
            messages.success(request, f' Account with Name: {user_account.username} is Unlocked.....')
            return redirect('index')
    # If the user does not exist, display a warning message
    messages.warning(request, f' This Account with ID of {id} does not exist...')
    return redirect('index')


@login_required(login_url='login_user')
def update(request, id):
    if request.method == 'GET':
        try:
            # Try to get the Customer object with the given id
            customer = Customer.objects.get(id=id)

            # Check if the current user is the one who created this customer
            if customer.created_by.user == request.user:
                # Prepare the data to be displayed
                customer_data = {
                    'username': customer.name,
                    'email': customer.email,
                    'age': customer.age,
                    'phone_Number': customer.phone_number,
                    'address': customer.address,
                    'order': customer.orders,
                    'vip_status': customer.vip_status
                }

                return render(request, 'update.html', {'User_Record': customer_data, 'userID': id})
            else:
                messages.error(request, "You do not have permission to update this record.")
                return redirect('index')

        except Customer.DoesNotExist:
            messages.error(request, f"Customer record with ID {id} does not exist.")
            return redirect('index')

    if request.method == 'POST':
        try:
            # Get the Customer object with the given id
            customer = Customer.objects.get(id=id)

            # Check if all required fields are provided
            if all(field in request.POST for field in ['username', 'email', 'age', 'address', 'phone_Number', 'order', 'vip_status']):
                # Update the customer record
                customer.name = request.POST.get('username')
                customer.email = request.POST.get('email')
                customer.age = request.POST.get('age')
                customer.address = request.POST.get('address')
                customer.phone_number = request.POST.get('phone_Number')
                customer.orders = request.POST.get('order')
                customer.vip_status = request.POST.get('vip_status')

                # Save the updated customer record
                customer.save()

                messages.success(request, "Customer updated successfully.")
                return redirect('index')
            else:
                messages.error(request, "Make sure to enter all the required information.")
                return redirect('index')

        except Customer.DoesNotExist:
            messages.error(request, f"Customer record with ID {id} does not exist.")
            return redirect('index')


@login_required(login_url='login_user')
def view_record(request, id):
    if request.method == 'GET':
        try:
            # Try to get the Customer object with the given id
            customer = Customer.objects.get(id=id)

            # Check if the current user is the one who created this customer
            if customer.created_by.user == request.user:
                # Prepare the data to be displayed
                customer_data = {
                    'ID': customer.id,
                    'Name': customer.name,
                    'Email': customer.email,
                    'Age': customer.age,
                    'PhoneNumber': customer.phone_number,
                    'Address': customer.address,
                    'Orders': customer.orders,
                    'VIP Status': customer.vip_status,
                }

                return render(request, 'view_record.html', {'User_Record': customer_data})
            else:
                messages.error(request, "You do not have permission to view this record.")
                return redirect('index')

        except Customer.DoesNotExist:
            messages.error(request, f"Customer record with ID {id} does not exist.")
            return redirect('index')

    return render(request, 'Create.html')


def SaveUser(username, email, age):
    if username and email and age:
        obj = models.UserInfo(username=username, email=email, age=age)
        obj.save()
        return True

    return False

def loading(request):
    return render(request, 'loading.html')


if __name__=="__main__":
    debug=True
