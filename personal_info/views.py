import requests
import uuid
import time
import json
from django.shortcuts import render,  redirect
from django.contrib import messages
from .forms import ApplyDataForm, LoginForm


def home(request):
    return render(request, 'home.html')


def LoginView(request):
    form = LoginForm()
    if 'token' in request.session:
        del request.session['token']

    if request.method == 'POST':
        form = ApplyDataForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        r = requests.post(
            'https://recruitment.fisdev.com/api/login/', 
            data={
                'username': username,
                 'password': password
                }
            )
        
        if r.status_code == 200:
            response = r.json()
            print(response)
            token = response['token']
            #print(token)
            request.session['token'] = token
            return redirect('apply')
        else:
            messages.error(request, 'Wrong username and password')
            return redirect('login_view')

    else:
        context = {'form': form}
        return render(request, 'login.html', context)


def ApplyView(request):
    if 'token' not in request.session:
        return redirect('login_view')

    form = ApplyDataForm()
    token = request.session['token']

    if request.method == 'POST':
        form = ApplyDataForm(request.POST, request.FILES)
        
        if form.is_valid():
            cv_get_file = request.FILES['cv_file']
            files = {'file': cv_get_file.read()}

            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json',   
            }

            print(uuid.uuid4())
            userData = {'tsync_id': str(uuid.uuid4()),
                        'name': request.POST.get('name'),
                        'email': request.POST.get('email'),
                        'phone': request.POST.get('phone'),
                        'full_address': request.POST.get('full_address'),
                        'name_of_university': request.POST.get('name_of_university'),
                        'graduation_year': request.POST.get('graduation_year'),
                        'cgpa': request.POST.get('cgpa'),
                        'experience_in_months': request.POST.get('experience_in_months'),
                        'current_work_place_name': request.POST.get('current_work_place_name'),
                        'applying_in': request.POST.get('applying_in'),
                        'expected_salary': request.POST.get('expected_salary'),
                        'field_buzz_reference': request.POST.get('field_buzz_reference'),
                        'github_project_url': request.POST.get('github_project_url'),
                        'cv_file': {'tsync_Id': str(uuid.uuid4())},
                        'on_spot_created_time': (round(time.time() * 1000)),
                        'on_spot_updated_time': (round(time.time() * 1000))
                    }

            cv_response = requests.post('https://recruitment.fisdev.com/api/v0/recruiting-entities/', data=userData, headers=headers)
            data_response = cv_response.json()

            print(data_response)

            if cv_response.status_code == 200:
                messages.success(request, 'Form submission successful')
                response = response.json()

                FILE_TOKEN_ID = data_response['cv_file']['id']

                headers = {
                    'Authorization': f'Token {token}'
                }

                file_url = "https://recruitment.fisdev.com/api/file-object/{FILE_TOKEN_ID}/"

                get_file = request.FILES['cv_file']
                files = {'file': get_file.read()}

                file_request = request.put(
                    file_url, files=files, headers=headers)

                if file_request.status_code == 200:
                    messages.success(request, 'File submission successful')
                    return redirect('home')

    context = {'form': form}
    return render(request, 'form.html', context)