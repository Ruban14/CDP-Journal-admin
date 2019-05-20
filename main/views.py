from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from main.models import *
from base64 import b64encode, b64decode
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
# Create your views here.

# serve all the list of journals
@api_view(['GET'])
@permission_classes((AllowAny,))
def serve_journal_list(request):
    all_journals = Journals.objects.all().order_by('published_date')
    # master_list
    all_journal_list = []
    for journal in all_journals:
        all_journal_dict = {}
        all_journal_dict['name'] = journal.name
        all_journal_dict['published_date'] = journal.published_date
        all_journal_dict['expiry_date'] = journal.expiry_date
        journal_directry = journal.file
        journal_directry = str(journal_directry)
        file_path = 'static/media/' + journal_directry
        try:
            with open(file_path, 'rb') as pdf_file:
                encoded_pdf = b64encode(pdf_file.read())
                all_journal_dict['pdf'] = encoded_pdf
        except Exception as error:
            print('..............')
            print(error)
        thumbnail_directry = journal.Thumbnail
        thumbnail_directry = str(thumbnail_directry)
        file_path = 'static/media/' + thumbnail_directry
        try:
            with open(file_path, 'rb') as pdf_file:
                encoded_pdf = b64encode(pdf_file.read())
                all_journal_dict['thumbnail'] = encoded_pdf
        except Exception as error:
            print('..............')
            print(error)
        all_journal_list.append(all_journal_dict)
    return Response(all_journal_list, status=status.HTTP_200_OK)

# save the name and number
@api_view(['POST'])
@permission_classes((AllowAny,))
def store_name_and_number(request):
    print(request.data)
    if not User_profile.objects.filter(phone_number=request.data['number']).exists() and not User_profile.objects.filter(name=request.data['name']).exists():
        user_profile_obj = User_profile(
            name=request.data['name'],
            phone_number=request.data['number']
        )
        user_profile_obj.save()
        print("saved")
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def serve_purpose_of_trees(request):
    purpose_dict = ['Tender', 'Neera', 'Nut']
    return Response(purpose_dict)


@api_view(['POST'])
@permission_classes((AllowAny,))
def store_subscriber(request):
    print(request.data)
    user = request.data
    User_profile.objects.filter(name=request.data["name"]).update(name=user['name'], street=user['street_address'], state=user['state'],
                                                                  taluk=user['taluk'], district=user['district'], pincode=user['pincode'], email=user['email'], phone_number=user['phone_number'], need_print=user['need_print'])
    print("updated")
    return Response(status=status.HTTP_200_OK)

# get user details
@api_view(['POST'])
@permission_classes((AllowAny,))
def get_user_type(request):
    print(request.data)
    if User_profile.objects.filter(phone_number=request.data['number']).exists():
        filter_user = User_profile.objects.get(
            phone_number=request.data['number'])
        print(filter_user.name)
        user_details_dict = {
            "name": filter_user.name,
            "exist": True
        }
    else:
        user_details_dict = {
            "name": "Guest",
            "exist": False
        }
    return Response(user_details_dict, status=status.HTTP_200_OK)

# update pdf need
@api_view(['POST'])
@permission_classes((AllowAny,))
def update_need_pdf(request):
    print(request.data)
    # filter by name to check for address exists
    user_object = User_profile.objects.get(name=request.data['user_name'])
    if user_object.street == "":
        print("no address found")
        data_for_non_addressed_user = {

        }
    # updation
    User_profile.objects.filter(name=request.data['user_name']).update(
        need_print=request.data['need_print']
    )
    print("updated")
    return Response(status=status.HTTP_200_OK)

# get user type for home page
@api_view(['POST'])
@permission_classes((AllowAny,))
def get_user_detail(request):
    if User_profile.objects.filter(name=request.data['name']).exists():
        filter_user = User_profile.objects.get(name=request.data['name'])
        print(filter_user.name)
        user_details_dict = {
            "name": filter_user.name,
            "need_print": filter_user.need_print,
            "email": filter_user.email,
            "online": filter_user.need_online
        }
    else:
        user_details_dict = {
            "name": "Guest",
            "email": "not_found",
            "need_print": False,
            "need_online": False
        }
    return Response(user_details_dict)


@api_view(['POST'])
@permission_classes((AllowAny,))
def store_email(request):
    print(request.data)
    User_profile.objects.filter(name=request.data['name']).update(
        email=request.data['email'])
    print("email updated")
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def serve_profile_data(request):
    print(request.data)
    user = User_profile.objects.get(name=request.data['name'])
    profile_dict = {
        "name": user.name,
        "street": user.street,
        "state": user.state,
        "taluk": user.taluk,
        "district": user.district,
        "pincode": user.pincode,
        "email": user.email,
        "phone_number": user.phone_number,
        "need_print": user.name,
    }
    print(profile_dict)
    return Response(profile_dict)


#  admin - portal


def admin_login(request):
    return render(request, "login.html")


def login(request):
    username = request.POST.get("username", False)
    password = request.POST.get("password", False)
    print(username)
    print(password)
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        request.session['logged_in'] = username
        print(request.session['logged_in'])
        return HttpResponseRedirect('/main/serve/subscribers/list/')
    else:
        print("Invalid password.")
        return render(request, "login.html")

# home page content
def serve_subscribers_list(request):
    user_name = request.session['logged_in']
    subscribers = User_profile.objects.all().order_by('id')
    subscribers_list = []
    for subscriber in subscribers:
        subscribers_dict = {}
        subscribers_dict['id'] = subscriber.id
        subscribers_dict['name'] = subscriber.name
        subscribers_dict['street'] = subscriber.street
        subscribers_dict['state'] = subscriber.state
        subscribers_dict['taluk'] = subscriber.taluk
        subscribers_dict['district'] = subscriber.district
        subscribers_dict['pincode'] = subscriber.pincode
        subscribers_dict['phone_number'] = subscriber.phone_number
        subscribers_dict['email'] = subscriber.email
        subscribers_dict['active'] = subscriber.active
        if subscriber.need_print == True and subscriber.need_online == True:
            subscribers_dict['subscription'] = "Print + Email"
        if subscriber.need_print == False and subscriber.need_online == True:
            subscribers_dict['subscription'] = "Email"
        if subscriber.need_print == True and subscriber.need_online == False:
            subscribers_dict['subscription'] = "Print"
        if subscriber.need_print == False and subscriber.need_online == False:
            subscribers_dict['subscription'] = "none"
        subscribers_list.append(subscribers_dict)
    all_journals = Journals.objects.all().order_by('published_date')
    # journal list
    all_journal_list = []
    for journal in all_journals:
        all_journal_dict = {}
        all_journal_dict['name'] = journal.name
        all_journal_dict['id'] = journal.id
        all_journal_dict['published_date'] = journal.published_date
        all_journal_dict['expiry_date'] = journal.expiry_date
        journal_directry = journal.file
        journal_directry = str(journal_directry)
        file_path = 'static/media/' + journal_directry
        try:
            with open(file_path, 'rb') as pdf_file:
                encoded_pdf = b64encode(pdf_file.read())
                all_journal_dict['pdf'] = encoded_pdf
        except Exception as error:
            print('..............')
            print(error)
        thumbnail_directry = journal.Thumbnail
        thumbnail_directry = str(thumbnail_directry)
        file_path = 'static/media/' + thumbnail_directry
        try:
            with open(file_path, 'rb') as pdf_file:
                encoded_pdf = b64encode(pdf_file.read())
                all_journal_dict['thumbnail'] = encoded_pdf
        except Exception as error:
            print('..............')
            print(error)
        all_journal_list.append(all_journal_dict)
    return render(request, "home.html", {"subscriber": subscribers_list, "user_name": user_name, "journals": all_journal_list})


def logout(request):
    request.session.pop('logged_in', None)
    return HttpResponseRedirect('/main/login/')


def register_user(request):
    user_name = request.POST.get("user_name", False)
    street = request.POST.get("street", False)
    taluk = request.POST.get("taluk", False)
    district = request.POST.get("district", False)
    state = request.POST.get("state", False)
    pincode = request.POST.get("pincode", False)
    phone_number = request.POST.get("phone_number", False)
    email = request.POST.get("email", False)
    if request.POST.get('need_print'):
        need_print = True
    else:
        need_print = False
    if request.POST.get('need_online'):
        need_online = True
    else:
        need_online = False
    print(need_print)
    print(need_online)
    if not User_profile.objects.filter(phone_number=phone_number).exists() and not User_profile.objects.filter(name=user_name).exists():
        user_profile_obj = User_profile(
            name=user_name,
            phone_number=phone_number,
            street=street,
            state=state,
            taluk=taluk,
            district=district,
            pincode=pincode,
            email=email,
            need_online=need_online,
            need_print=need_print
        )
        user_profile_obj.save()
    return serve_subscribers_list(request)

# re-route
def update_user(request):
    user_id = request.GET.get("user_id")
    user_details = User_profile.objects.get(id=user_id)
    return render(request, 'update_user.html', {'data': user_details, "user_id": user_id})


def update_user_profile(request):
    name = request.POST.get("name", False)
    print("name -", name)
    street = request.POST.get("street", False)
    print("street - ", street)
    taluk = request.POST.get("taluk", False)
    print("taluk -", taluk)
    district = request.POST.get("district", False)
    print("district", district)
    state = request.POST.get("state", False)
    print(state)
    pincode = request.POST.get("pincode", False)
    print(pincode)
    phone_number = request.POST.get("phone_number", False)
    print("phone_number", phone_number)
    email = request.POST.get("email", False)
    print(email)
    if request.POST.get('need_print'):
        need_print = True
    else:
        need_print = False
    if request.POST.get('need_online'):
        need_online = True
    else:
        need_online = False
    print(need_online)
    print(need_print)
    user_id = request.GET.get("user_id")
    User_profile.objects.filter(id=user_id).update(
        name=name,
        street=street,
        taluk=taluk,
        district=district,
        state=state,
        pincode=pincode,
        phone_number=phone_number,
        email=email,
        need_online=need_online,
        need_print=need_print)
    print("updated")
    messages.success(request, 'Your profile was updated !')
    return HttpResponseRedirect('/main/serve/subscribers/list/')


def new_journal(request):
    journal_name = request.POST.get("journal_name", False)
    journal_file = request.FILES.get('journal_file')
    thumbnail_image = request.FILES.get("thumbnail")
    expiry_date = request.POST.get("expiry_date", False)
    published_date = request.POST.get("published_date", False)
    print(thumbnail_image)
    print(journal_file)
    journal_obj = Journals(
        name=journal_name,
        published_date=published_date,
        expiry_date=expiry_date,
        published_by=request.user,
        file=journal_file,
        Thumbnail=thumbnail_image,
    )
    journal_obj.save()
    print('saved')
    return HttpResponseRedirect('/main/serve/subscribers/list/')


def remove_journal(request):
    journal_id = request.GET.get("journal_id")
    print(journal_id)
    journal_obj = Journals.objects.get(id=journal_id)
    journal_obj.delete()
    return HttpResponseRedirect('/main/serve/subscribers/list/')


def update_status_active(request):
    user_id = request.GET.get("user_id")
    print('came')
    print(user_id)
    User_profile.objects.filter(id=user_id).update(
        active=False
    )
    return HttpResponseRedirect('/main/serve/subscribers/list/')


def update_status_inactive(request):
    user_id = request.GET.get("user_id")
    print('came')
    print(user_id)
    User_profile.objects.filter(id=user_id).update(
        active=True
    )
    return HttpResponseRedirect('/main/serve/subscribers/list/')

def print_labels(request):
    subscribers = User_profile.objects.filter(active=True).order_by('id')
    subscribers_list = []
    for subscriber in subscribers:
        subscribers_dict = {}
        subscribers_dict['id'] = subscriber.id
        subscribers_dict['name'] = subscriber.name
        subscribers_dict['street'] = subscriber.street
        subscribers_dict['state'] = subscriber.state
        subscribers_dict['taluk'] = subscriber.taluk
        subscribers_dict['district'] = subscriber.district
        subscribers_dict['pincode'] = subscriber.pincode
        subscribers_dict['phone_number'] = subscriber.phone_number
        subscribers_dict['email'] = subscriber.email
        subscribers_dict['active'] = subscriber.active
        subscribers_list.append(subscribers_dict)
    return render(request, "print.html", {"subscriber": subscribers_list})