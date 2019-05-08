from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from main.models import *
from base64 import b64encode, b64decode
from django.contrib import auth
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
        all_journal_dict['journal_expiry_date'] = journal.journal_expiry_date
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
    User_profile.objects.filter(name=request.data["name"]).update(name=user['name'], street=user['street_address'],state=user['state'],
    taluk=user['taluk'],district=user['district'],pincode=user['pincode'],email=user['email'],phone_number=user['phone_number'],need_print=user['need_print'])
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
            "email": filter_user.email
        }
    else:
        user_details_dict = {
            "name": "Guest",
            "email": "not_found",
            "need_print": False
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

# @api_view(['POST'])
# @permission_classes((AllowAny,))
# def store_profile(request):
#     print(request.data)
#     User_profile.objects.filter(name=request.data['name']).update()

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


def serve_subscribers_list(request):
    user_name = request.session['logged_in']
    subscribers = User_profile.objects.all()
    print(subscribers)
    subscribers_list = []
    for subscriber in subscribers:
        print(subscriber.name)
        subscribers_dict = {}
        subscribers_dict['name'] = subscriber.name
        subscribers_dict['street'] = subscriber.street
        subscribers_dict['state'] = subscriber.state
        subscribers_dict['taluk'] = subscriber.taluk
        subscribers_dict['district'] = subscriber.district
        subscribers_dict['pincode'] = subscriber.pincode
        subscribers_dict['phone_number'] = subscriber.phone_number
        subscribers_dict['email'] = subscriber.email
        if subscriber.need_print == True and subscriber.need_online == True:
            subscribers_dict['subscription'] = "Print + Email" 
        if subscriber.need_print == False and subscriber.need_online == True:
            subscribers_dict['subscription'] = "Email"
        if subscriber.need_print == True and subscriber.need_online == False:
            subscribers_dict['subscription'] = "Print"
        if subscriber.need_print == False and subscriber.need_online == False:
            subscribers_dict['subscription'] = "none"
        subscribers_list.append(subscribers_dict)
    print(subscribers_list)
    return render(request, "home.html", {"subscriber": subscribers_list, "user_name": user_name})


def logout(request):
    request.session.pop('logged_in', None)
    return HttpResponseRedirect('/main/login/')

def navigate_to_add_user(request):
    return render(request, "add_user.html")
