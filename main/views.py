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


@api_view(['GET'])
@permission_classes((AllowAny,))
def serve_purpose_of_trees(request):
    purpose_dict = ['Tender', 'Neera', 'Nut']
    return Response(purpose_dict)


@api_view(['POST'])
@permission_classes((AllowAny,))
def store_subscriber(request):
    print(request.data)
    if not User_profile.objects.filter(phone_number=request.data['phone_number']).exists() and not User_profile.objects.filter(name=request.data['name']).exists():
        user_profile_obj = User_profile(
            name=request.data['name'],
            phone_number=request.data['phone_number'],
            user_type="User",
            pincode=request.data['pincode']
        )
        # purpose of trees
        if request.data['purpose_of_trees'] != 'null':
            user_profile_obj.purpose_of_trees = request.data['purpose_of_trees']
        # no of trees
        if request.data['no_of_trees'] != 'null':
            user_profile_obj.no_of_cocunut_trees = request.data['no_of_trees']
        # email
        if request.data['email'] != 'null':
            user_profile_obj.email = request.data['email']

        if request.data['need_print'] == True:
            user_profile_obj.street = request.data['street_address']
            user_profile_obj.state = request.data['state']
            user_profile_obj.taluk = request.data['taluk']
            user_profile_obj.district = request.data['district']

        user_profile_obj.save()
        return Response(status=status.HTTP_200_OK)
    else:
        error = "phone number or name already exists"
        return Response(error)


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
            "type": "User",
            "need_print": filter_user.need_print
        }
    else:
        user_details_dict = {
            "name": "Guest",
            "need_print": False
        }
    return Response(user_details_dict, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def update_need_pdf(request):
    print(request.data)
    User_profile.objects.filter(name=request.data['user_name']).update(
        need_print=request.data['need_print']
    )
    print("updated")
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_user_detail(request):
    if User_profile.objects.filter(name=request.data['name']).exists():
        filter_user = User_profile.objects.get(name=request.data['name'])
        print(filter_user.name)
        user_details_dict = {
            "name": filter_user.name,
            "need_print": filter_user.need_print
        }
    else:
        user_details_dict = {
            "name": "Guest",
            "need_print": False
        }
    return Response(user_details_dict)

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
        print ("Invalid password.")
        return render(request, "login.html")

def serve_subscribers_list(request):
    user_name = request.session['logged_in']
    subscribers = User_profile.objects.filter(need_print = True)
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
        subscribers_list.append(subscribers_dict)
    print(subscribers_list)
    return render(request, "home.html", {"subscriber":subscribers_list,"user_name":user_name})

def logout(request):
    request.session.pop('logged_in', None)
    return HttpResponseRedirect('/main/login/')