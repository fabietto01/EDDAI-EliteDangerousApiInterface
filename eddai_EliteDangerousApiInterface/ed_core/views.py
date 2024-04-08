from django.shortcuts import render, redirect

# Create your views here.

def redirect_to_admin(request):
    return redirect('/admin/')