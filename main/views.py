from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect
from .forms import *
from database.models import Chef
from database.models import Recipe
from database.models import Category

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, "main/index.html")
    return redirect("/home")

# Return recipes and chef that have coincidences with the query
def search(request):
    if request.method == "GET":
        user = request.user
        chef = user.chef
        query = request.GET['query']
        recipes = Recipe.objects.filter(name__istartswith=query)
        chefs = Chef.objects.filter(user__username__istartswith=query).exclude(user__username=user.username)
        followees = chef.followees.all()
    return render(request, "main/search.html", {"query" : query, "recipes" : recipes, "chefs" : chefs, "followees" : followees })


# Get all recipes to see
def explore(request, category):
    if category == "all":
        recipes = Recipe.objects.all()
        category_selected = "Todas las categorias"
    else:
        category_selected = Category.objects.get(name=category)
        recipes = Recipe.objects.filter(category=category_selected)
        category_selected = category_selected.name
    categories = Category.objects.all()
    return render (request, "main/explore.html", {"recipes" : recipes, "categories" : categories, "category_selected" : category_selected})


def admin_home(request):
    return render(request, "main/admin_home.html")

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            description = form.cleaned_data.get('description')
            password = form.cleaned_data.get('password')
            User = get_user_model()
            user = User.objects.create_user(email=email, username=username, password=password)
            chef = Chef.objects.create(user=user, description=description)
            login(request, user)
            return redirect("/home")
    else:
        form = SignUpForm()

    return render(request, "main/signup.html", {"form":form})

def login_(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            User = get_user_model()
            user = User.objects.get(email=email)
            login(request, user)
            if user.is_admin:
                return redirect ("/adminsite")
            return redirect("/home")
    else:
        form = LoginForm()
    return render(request, "main/login.html", {"form":form})

def logout_(request):
    logout(request)
    return redirect("/")
