import json
import os
import pandas as pd

from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.core import serializers

from payout_app.task import process_kd
from payout_app.decorators import *
from celery.result import AsyncResult


@csrf_exempt  
def index(request):
    if request.method == 'GET':
        return render(request, "payout_app/index.html")
    
    if request.method == "POST":

    # try:
        rh_data = request.FILES['rh_data']
        transplant_data = request.FILES['transplantData']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        user = User.objects.get(id=request.POST['userID'])
        user_info = serializers.serialize('json', [user])
        # Read Excel file using Pandas
        rh_df = pd.read_excel(rh_data)
        transplant_df = pd.read_excel(transplant_data)

        # Convert DataFrames to JSON
        rh_data_info = rh_df.to_json(orient='records')
        transplant_data_info = transplant_df.to_json(orient='records')
        process_kd.delay(from_date=from_date,to_date=to_date,rh_data=rh_data_info,transplant_data=transplant_data_info,user=user_info)
        return JsonResponse({'success': 'Success',"email_Id":user.email}, status=200)

    # except Exception as e:
    # #     Return error message with 400 status code
    #     return JsonResponse({'error': str(e)}, status=400)
    
    # # process_kd.delay()
    # return render(request, "payout_app/index.html")


# @csrf_exempt    
# def login_page(request):
#     if request.method == "GET":
#         return render(request, "payout_app/login_page.html")
#     if request.method == "POST":
#         print(request.POST)
#         # Login User
#         user = authenticate(
#             request,
#             username=request.POST["username"],
#             password=request.POST["password"],
#         )
#         if user is None:
#             context= {
#                 "error" :"Wrong User ID or Password. Try again or call 33333 /33330 to reset it.","username":request.POST["username"]}
#             return render(request, "payout_app/login_page.html", context)
#         if user:
#             login(request, user)
#             user_full_name = request.user.get_full_name()
#             context = {"user_fullname": user_full_name}
#             return redirect("index")

@csrf_exempt
def check_task_status(request):
    try:
        task_id = request.session.get('task_id')  # Retrieve the task ID from the session
        if task_id:
            task_result = AsyncResult(task_id)
            if task_result.status in ['PENDING', 'STARTED']:
                # A task with the same ID is already running
                return JsonResponse({'running': 'A report is already being generated. Try again later.'}, status=200)
            else:
                # No running task found
                return JsonResponse({'not_running': 'No running task.'}, status=200)
        else:
            # No task ID in session
            return JsonResponse({'not_running': 'No task ID found.'}, status=200)

    except Exception as e:
        # Return error message with 400 status code
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            return JsonResponse({'error': 'Wrong User ID or Password. Try again or call 33333 /33330 to reset it'}, status=401)
        
        login(request, user)
        return JsonResponse({'success': request.user.get_full_name().title(),"user_id":user.id,"token":default_token_generator.make_token(user) })    
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required(login_url="login_page")
def logout_user(request):
    logout(request)
    return redirect("login_page")


def get_csrf_token(request):
    csrf_token = csrf.get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class FileListView(View):
    def get(self, request):
        try:
            directory = os.path.join(settings.BASE_DIR, 'payout_app', 'excel_files')
            files = os.listdir(directory)
            # Sort files by creation time in descending order
            files.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)), reverse=True)
            # Configure pagination
            paginator = Paginator(files, 5)  # Display 10 files per page
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            file_urls = []
            for file_name in page_obj:
                file_urls.append({
                    'name': file_name,
                    'url': request.build_absolute_uri(reverse('download', args=[file_name]))
                })

            # Create response with paginated file list
            response_data = {
                'files': file_urls,
                'current_page': page_obj.number,
                'num_pages': paginator.num_pages

            }
            return JsonResponse(response_data, status=200)
        except  Exception as e:
            return JsonResponse({'error': e}, status=405)
        



    
@csrf_exempt
def download_file(request, file_name):
    file_path = os.path.join(settings.BASE_DIR, 'payout_app', 'excel_files', file_name)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
