from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
import requests, pprint, json
from selenium.webdriver.common.by import By
from selenium import webdriver

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def go_login(request):
    user = User.objects.filter(email = request.POST['form_em'])

    if user:
        cur_user_id = user[0]
        print("Current User ID: " + str(cur_user_id.id))
# Check Password / Validate
        if bcrypt.checkpw(request.POST['form_pw'].encode(), cur_user_id.password.encode()):
            request.session['login'] = "Successfully logged in!"
            request.session['user_id'] = cur_user_id.id
            print(request.session['user_id'])
            print("* " * 30)
            print("User ID: " + str(cur_user_id.id) + ", Name: " + cur_user_id.first_name + " " + cur_user_id.last_name)
            return redirect('/dashboard')

        else:
            messages.error(request, "Invalid password.")
            return redirect('/')

    else:
        messages.error(request, "Email not found.")
        return redirect('/')

def go_register(request):
# Validation / Errors
    errors = User.objects.register_validate(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print("* " * 30)
            print("Error: " + value)
        return redirect('/register')
# Create
    fn = request.POST['form_fn']
    ln = request.POST['form_ln']
    em = request.POST['form_em']
    pw = request.POST['form_pw']
    cpw = request.POST['form_cpw']

# Password Hash
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(first_name = fn, last_name = ln, email = em, password = pw_hash)
    print("* " * 30)
    print(new_user)
# Store in session
    request.session['register'] = "Successfully registered!"
    request.session['user_id'] = new_user.id
    print(request.session['user_id'])

    return redirect('/dashboard')

def dashboard(request):
    cur_user_id = request.session['user_id']
    cur_user = User.objects.get(id = request.session['user_id'])
    if cur_user_id == request.session['user_id']:

        context = {
            "user" : User.objects.get(id = cur_user_id)
            }

        return render(request, 'dashboard.html', context)

def add_route(request, route_id):
    route_id = route_id
    response = requests.get("https://www.mountainproject.com/data/get-routes?routeIds="+str(route_id)+"&key=106838734-05344d7002476a0d76531a206c4c4ba3")
    json_res = response.json()
    pprint.pprint(json_res)
    
    context = {
        "route_info" : json_res
    }

    trail_name = json_res.get('routes')[0].get('name')
    location = json_res.get('routes')[0].get('location')
    elevation = json_res.get('routes')[0].get('type')
    difficulty = json_res.get('routes')[0].get('name')
    desc = json_res.get('routes')[0].get('url')
    creator = User.objects.get(id=request.session['user_id'])

    Trail.objects.create(trail_name = trail_name, location = location, elevation = elevation, difficulty = difficulty, desc = desc, creator = creator)


    # driver = webdriver.Safari()
    # driver.back()
    return render(request, 'dashboard.html', context)

def view_climbs(request):

    context = {
        "user" : User.objects.get(id = request.session['user_id']),
        "climbs" : Trail.objects.filter(creator = request.session['user_id'])
    }

    return render(request, 'view_climbs.html', context)

def remove_climb(request, trail_id):
    remove_climb = Trail.objects.get(id = trail_id)
    remove_climb.delete()
    return(redirect('/view_climbs'))

#Trail Validation and create
def validate_trail(request):

    errors = Trail.objects.validate_trail(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/create_trail')

    trail_name = request.POST['trail_name']
    location= request.POST['location']
    elevation = request.POST['elevation']
    difficulty = request.POST['difficulty']
    desc = request.POST['desc']
    user = User.objects.get(id=request.session['user_id'])

    Trail.objects.create(trail_name = trail_name, location = location, elevation = elevation, difficulty = difficulty, desc = desc, creator = user)
    
    return redirect('/view_climbs')

def create_trail(request):
    cur_user_id = request.session['user_id']
    cur_user = User.objects.get(id = request.session['user_id'])
    context = {
        "user" : User.objects.get(id = cur_user_id),
        'all_trails' : Trail.objects.all()
    }
    return render(request, "create.html", context)

# LOGOUT   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   

def logout(request):
    request.session.clear()
    return redirect('/')