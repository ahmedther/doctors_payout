import json
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from payout_app.task import process_kd
from payout_app.decorators import *
from django.contrib.auth.models import User
from celery.result import AsyncResult


@csrf_exempt  
def index(request):
    try:
        task_id = request.session.get('task_id')  # Retrieve the task ID from the session
        if task_id:
            task_result = AsyncResult(task_id)
            if task_result.status in ['PENDING', 'STARTED']:
                # A task with the same ID is already running
                return JsonResponse({'message': 'A Report is Already being generated. Try Again in sometime'}, status=400)

        rh_data = request.FILES['rh_data']
        transplant_data = request.FILES['transplantData']
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        user = User.objects.get(id=request.POST['userID'])
        process_kd(from_date=from_date,to_date=to_date,rh_data=rh_data,transplant_data=transplant_data,user=user)
        return JsonResponse({'success': 'Success',"email_Id":user.email}, status=200)

    except Exception as e:
        # Return error message with 400 status code
        return JsonResponse({'error': str(e)}, status=400)
    
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