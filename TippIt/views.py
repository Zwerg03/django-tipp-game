from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import livegames, userwerte



# Create your views here.
def Home(request):
    return render(request, "index.html")

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  # Django checkt Hash
        if user is not None:
            login(request, user)  # Session wird gesetzt!
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})

    return render(request, "login.html")


@login_required(login_url="/login/")
def Voting(request):
    if request.method == "POST":
        user = request.user
        TA = request.POST.get("TA")
        TB = request.POST.get("TB")
        i = request.POST.get("Nr")
        aktuell = request.POST.get("aktiv")
        
        
        userdata, created = userwerte.objects.get_or_create(user=user)

        aktuelldat = str(userdata.aktiv)
        
        print("Der aktuelle benutzer ist" + aktuelldat)
        if aktuelldat == "True":
            if aktuell == "false":
                userdata.aktiv = False
                setattr(userdata, f"wertT{i}A", TA)
                setattr(userdata, f"wertT{i}B", TB)
                userdata.save()
            else:
                setattr(userdata, f"wertT{i}A", TA)
                setattr(userdata, f"wertT{i}B", TB)
                userdata.save()
        
        return JsonResponse({"aktiv": userdata.aktiv})
    

    game = livegames.objects.get()
    context = {
        "Team1A" : game.Team1A,
        "Team1B" : game.Team1B,
        "Team2A" : game.Team2A,
        "Team2B" : game.Team2B,
        "Team3A" : game.Team3A,
        "Team3B" : game.Team3B,
        "Team4A" : game.Team4A,
        "Team4B" : game.Team4B,
        "Team5A" : game.Team5A,
        "Team5B" : game.Team5B,
        "Team6A" : game.Team6A,
        "Team6B" : game.Team6B,
        "Team7A" : game.Team7A,
        "Team7B" : game.Team7B,
        "Team8A" : game.Team8A,
        "Team8B" : game.Team8B,
        "Team9A" : game.Team9A,
        "Team9B" : game.Team9B
    }
    
    return render(request, "select.html", context)

def Logout(request):
    logout(request)
    return redirect("/login/")