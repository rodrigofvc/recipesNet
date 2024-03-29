from django.shortcuts import render, redirect
from django.http import JsonResponse
from database.models import Recipe
from database.models import Chef
from database.models import Category
from database.models import Coment
from .forms import *

# Create your views here.

# Get all recipes of current chef
def get_recipes(request):
    form = RecipeForm()
    user = request.user
    chef = user.chef
    recipes = Recipe.objects.filter(owner=chef)
    categories = Category.objects.all()
    context = {
        "recipes" : recipes,
        "form" : form,
        "categories" :categories
    }
    return render (request, "recipes/recipes.html", context)

# Get recipe
def get_recipe(request, id_recipe):
    form = ComentForm()
    recipe = Recipe.objects.get(id_recipe=id_recipe)
    likes_count = recipe.likes.count()
    user = request.user
    chef = user.chef
    if chef in recipe.likes.all():
        has_like = True
    else:
        has_like = False
    context = {
        "recipe" : recipe,
        "ingredients" : recipe.ingredients.all(),
        "coments" : recipe.recipe_coments.all(),
        "likes" : likes_count,
        "has_like" : has_like,
        "form" : form
    }
    return render (request, "recipes/recipe.html", context)

# Create a new recipe
def new_recipe(request):
    if request.method == "POST":
        user = request.user
        chef = user.chef
        form = RecipeForm(request.POST, request.FILES)
        list_ingredients = request.POST.getlist('ingredient')
        list_ingredients = list (set (list_ingredients))
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = chef
            recipe.save()
            for ingredient in list_ingredients:
                recipe.add_ingredient(ingredient)
            recipe.save()
            return redirect("/recipes")
        else:
            raise Exception ("Ocurrio un error con el formulario")
    return redirect("/recipes")

# Show menu to edit recipes or delete
def edit_recipes(request):
    user = request.user
    chef = user.chef
    recipes = Recipe.objects.filter(owner=chef)
    return render (request, "recipes/recipes_edit.html", {"recipes" : recipes})

# Delete the recipe by it's id
def delete_recipe(request, id_recipe):
    deleted = Recipe.objects.get(pk=id_recipe)
    deleted.image.delete()
    deleted.delete()
    return redirect("/recipes/edit")

# Edit the recipe by it's id
def edit_recipe(request, id_recipe):
    user = request.user
    chef = user.chef
    recipe = Recipe.objects.get(id_recipe=id_recipe)
    ingredients = recipe.ingredients.all()
    ingredients_name = [i.ingredient for i in ingredients]
    if request.method == "POST":
        list_ingredients = request.POST.getlist('ingredient')
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            edit_recipe = form.save(commit=False)
            recipe.name = edit_recipe.name
            recipe.image.delete()
            recipe.image = edit_recipe.image
            recipe.description = edit_recipe.description
            recipe.category = edit_recipe.category
            deleted_ingredients = list(set(ingredients_name) - set(list_ingredients))
            recipe.delete_ingredients(deleted_ingredients)
            list_ingredients = list(set(list_ingredients) - set(ingredients_name))
            recipe.add_ingredients(list_ingredients)
            recipe.save()
            return redirect("/recipes/edit")
    else:
        form = RecipeForm()
    context = {
        "recipe" : recipe,
        "ingredients_recipe" : ingredients,
        "form" : form
    }
    return render (request, "recipes/recipe_edit.html", context)

# Coment a recipe
def coment_recipe(request):
    if request.method == "POST":
        form = ComentForm(request.POST)
        if form.is_valid():
            user = request.user
            chef = user.chef
            message = form.cleaned_data.get('message')
            id_recipe = form.cleaned_data.get('id_recipe')
            recipe = Recipe.objects.get(id_recipe=id_recipe)
            coment = Coment(recipe=recipe, chef=chef, message=message)
            coment.save()
            return redirect('/recipes/' + str(id_recipe))

# Like a recipe
def like_recipe(request, id_recipe):
    recipe = Recipe.objects.get(id_recipe=id_recipe)
    user = request.user
    chef = user.chef
    flag = recipe.add_like(chef)
    recipe.save()
    likes_count = recipe.likes.count()
    data = { 'content' : {
        'flag' : flag,
        'likes_count' : likes_count,
    }}
    return JsonResponse(data)
