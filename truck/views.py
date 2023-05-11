from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Truck, Tour, Spedition
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
import collections, functools, operator
from datetime import datetime
from . import helpers

# Data for dropdown lists
weeks = [(x, x) for x in range(1, 54)]
months =  [("January", "January"), ("Febraury", "Febraury"), ("March", "March"), ("April", "April"), ("May", "May"), 
        ("June", "June"), ("July", "July"), ("August", "August"), ("September", "September"), ("October", "October"), 
        ("November", "November"), ("December", "December")]
years = [(x, x) for x in range(2023, 2031)]

# Forms
class RaportForm(forms.Form):
    Week = forms.CharField(
        max_length=12,
        label='Week', widget=forms.Select(choices=weeks)
        )
    Month = forms.CharField(
        max_length=12,
        label='Month', widget=forms.Select(choices=months)
        )
    Year = forms.CharField(
        max_length=12,
        label='Year', widget=forms.Select(choices=years)
        )


class TruckForm(forms.Form):
    Name = forms.CharField(
        max_length = 20,
        label='Truck',
        widget=forms.TextInput(attrs={'placeholder': 'Add truck', 'required': 'true'})
        )

class SpeditionForm(forms.Form):
    Name = forms.CharField(
        max_length = 40,
        label='Spedition',
        widget=forms.TextInput(attrs={'placeholder': 'Add spedition', 'required': 'true'})
        )

class EditTruckForm(forms.Form):
    New_name = forms.CharField(
        max_length = 20,
        label='Truck',
        widget=forms.TextInput(attrs={'placeholder': 'Edit truck name', 'required': 'true'})
        )
    
class EditSpeditionForm(forms.Form):
    New_name = forms.CharField(
        max_length = 40,
        label='Spedition',
        widget=forms.TextInput(attrs={'placeholder': 'Edit spedition name', 'required': 'true'})
        )


class TourForm(forms.Form):
    Freight = forms.FloatField(
        label = "Freight", min_value = 0.1,
        widget=forms.NumberInput(attrs={'placeholder': 'Freight (€)'})
    )
    Km = forms.IntegerField(
        label='Km', min_value = 1,
        widget=forms.NumberInput(attrs={'placeholder': 'Km'})
        )
    Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    Rate = forms.FloatField(
        label = "Rate", min_value = 0.1,
        widget=forms.NumberInput(attrs={'placeholder': 'Rate (€/km)'})
    )
    Id = forms.IntegerField(
        label='id', min_value = 1, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'id'})
        )

class RateForm(forms.Form):
    Default_rate = forms.FloatField(
        label = "Default rate", min_value = 0.1,
        widget=forms.NumberInput(attrs={'placeholder': 'Default Rate (€/km)'})
    )


# Create your views here.
def index(request):
    return render(request, "truck/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("trucks"))
        else:
            return render(request, "truck/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "truck/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "truck/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "truck/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        if request.POST["spedition"] == "":
            name = "Default"
        spedition = Spedition(user=request.user, name=name)
        spedition.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "truck/register.html")


def trucks(request):
    if request.method == "POST":
        form = TruckForm(request.POST)
        if form.is_valid():
            # Gather data and save truck in database
            name = form.cleaned_data["Name"]
            truck = Truck(user=request.user, name=name)
            truck.save()
            return HttpResponseRedirect(reverse("trucks"))

    else:
        # If user not logged in, direct to login page
        try:
            truck = Truck.objects.filter(user=request.user).order_by("name")
            speditions = Spedition.objects.filter(user=request.user)
        except TypeError:
            return render(request, "truck/login.html", {
                "message": "Required to log in"
            })
        
        return render(request, "truck/trucks.html", {
            "truckform": TruckForm(),
            "trucks": truck,
            "raport": RaportForm(),
            "spedition": SpeditionForm(),
            "speditions": speditions
        })

def truck_view(request, truck_id):
    truck = Truck.objects.get(pk = truck_id)
    if request.method == "POST":
        form = TourForm(request.POST)
        if form.is_valid():

            # Gather variables from form and save tour for this truck
            freight = form.cleaned_data["Freight"]
            km = form.cleaned_data["Km"]
            date = form.cleaned_data["Date"]
            rate = freight/km
            spedition = Spedition.objects.get(pk=int(request.POST["spedition"]))

            tour = Tour(user=request.user, truck=truck, freight=freight, km=km, date=date, rate=rate, spedition=spedition)
            tour.save()
            return HttpResponseRedirect(reverse("truck_view", args=(truck_id,)))
        else:
            return HttpResponseRedirect(reverse("truck_view", args=(truck_id,)))  
    else:
        
        # Set pagination for 30 items per page
        tours = Tour.objects.filter(truck=truck).order_by("-date")
        paginator = Paginator(tours, 30)
        page_number = request.GET.get('page')
        tours_pagin = paginator.get_page(page_number) 

        # Stats for current week and month
        week = []
        month = []
        date = datetime.now() 
        for tour in tours:
            if tour.date.isocalendar().week == date.isocalendar().week and tour.date.isocalendar().year == date.isocalendar().year:
                tour_week = {
                    "km": tour.km,
                    "freight": tour.freight
                }
                week.append(tour_week)
            if datetime.now().month == tour.date.month and tour.date.isocalendar().year == date.isocalendar().year:
                tour_month = {
                    "km": tour.km,
                    "freight": tour.freight
                }
                month.append(tour_month)
        if week:

            # Add values from dictionary by key
            current_week = dict(functools.reduce(operator.add,
            map(collections.Counter, week)))
            
            current_week = {
                "km": current_week["km"],
                "freight": current_week["freight"],
                "rate": "{:.3f}".format(current_week["freight"]/current_week["km"])
            }
        else:
            current_week = {
                "km": 0,
                "freight": 0,
                "rate": "",
            }
        if month:
            # Add values from dictionary by key
            current_month = dict(functools.reduce(operator.add,
            map(collections.Counter, month)))

            current_month = {
                "km": current_month["km"],
                "freight": current_month["freight"],
                "rate": "{:.3f}".format(current_month["freight"]/current_month["km"])
            }
        else:
            current_month = {
                "km": 0,
                "freight": 0,
                "rate": "",
            }


        return render(request, "truck/truck.html", {
            "truck": truck,
            "Tour": TourForm(),
            "Default_rate": RateForm(),
            "tours": tours_pagin,
            "edit": EditTruckForm(),
            "week": current_week,
            "month": current_month,
            "speditions": Spedition.objects.filter(user=request.user)
        })
    
@csrf_exempt
def default_rate(request):
    # Query for user's default rate
    try:
        user = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(user.serialize())
    
    elif request.method == "PUT":

        # Change user's default rate in database
        data = json.loads(request.body)
        if data.get("default_rate") is not None:
            user.default_rate = data["default_rate"]
        user.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
    
def delete_tour(request, tour_id):
    if request.method == "POST":
        truck = Truck.objects.get(tour=tour_id)
        tour = Tour.objects.get(pk=tour_id)
        tour.delete()
        id = truck.id
        return HttpResponseRedirect(reverse("truck_view", args=(id,)))  
    
def get_tour(request, tour_id):
    try:
        tour = Tour.objects.get(pk=tour_id)
    except Tour.DoesNotExist:
        return JsonResponse({"error": "Tour not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(tour.serialize())
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    
def edit_tour(request):
    
    if request.method == "POST":
        form = TourForm(request.POST)
        if form.is_valid():
            tour = Tour.objects.filter(pk=form.cleaned_data["Id"])
            freight = form.cleaned_data["Freight"]
            km = form.cleaned_data["Km"]
            date = form.cleaned_data["Date"]
            rate = freight/km
            spedition = Spedition.objects.get(pk=int(request.POST["spedition"]))
            tour.update(date=date, freight=freight, km=km, rate=rate, spedition=spedition)

            truck_id = tour[0].truck.id
            return HttpResponseRedirect(reverse("truck_view", args=(truck_id,)))
        else:
            return HttpResponseRedirect(reverse("truck_view", args=(truck_id,)))  
        
@csrf_exempt
def edit_truck(request, truck_id):
    try:
        truck = Truck.objects.get(pk=truck_id)
    except Truck.DoesNotExist:
        return JsonResponse({"error": "Truck not found."}, status=404)
    
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("truck_name") is not None:
            truck.name = data["truck_name"]
        truck.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
    

def raport(request):
    if request.method == "POST":
        form = RaportForm(request.POST)
        if form.is_valid():

            # Gather truck ids from checked boxes
            truck_ids = request.POST.getlist("truck_box")
            if len(truck_ids) == 0:
                return render(request, "truck/raport.html", {
                "error": "No truck chosen for the raport",
                }) 

            # Gather spedition ids from checked boxes
            sped_ids = request.POST.getlist("sped_box")
            if len(sped_ids) == 0:
                return render(request, "truck/raport.html", {
                "error": "No spedition chosen for the raport",
                }) 
            sped_ids = [int(i) for i in sped_ids]

            if len(Spedition.objects.filter(user=request.user)) == len(sped_ids):
                spedition_names = "All speditions"
            
            else:
                spedition_names = []

                for id in sped_ids:
                    spedition_names.append(Spedition.objects.get(pk=id).name)


            # Check if raport is for week or a month
            week_or_month = request.POST.get("week_or_month")
            if week_or_month == "week":
                chosen_year = int(form.cleaned_data["Year"])
                chosen_week = int(form.cleaned_data["Week"])

                # Make a list of chosen trucks
                trucks = []

                for id in truck_ids:
                    truck = Truck.objects.get(pk=int(id))
                    trucks.append(truck)
                truck_tours = []

                # Get tours for each truck
                for truck in trucks:
                    tours = Tour.objects.filter(truck=truck)

                    # Filter tours to gather only those during chosen week, add them to the list as a dict
                    week_tour = []
                    for tour in tours:
                        if tour.date.isocalendar().week == chosen_week and tour.date.isocalendar().year == chosen_year and tour.spedition.id in sped_ids:
                            tour_week = {
                                "km": tour.km,
                                "freight": tour.freight
                            }
                            week_tour.append(tour_week)
                    
                    # Add values from dictionaries by key
                    if week_tour:
                        week = dict(functools.reduce(operator.add,
                        map(collections.Counter, week_tour)))
                        
                        # Create a new dict with proper keys 
                        week = {
                            "name": truck.name,
                            "km": week["km"],
                            "freight": week["freight"],
                            "rate": "{:.3f}".format(week["freight"]/week["km"])
                        }
                    # If no tours during that week
                    else:
                        week = {
                            "name": truck.name,
                            "km": 0,
                            "freight": 0,
                            "rate": ""
                        }
                    # Add to the list of dictionaries
                    truck_tours.append(week)

                # Calculate average km, freight and rate
                avg_km = 0 
                avg_freight = 0
                

                for i in truck_tours:
                    avg_km += i["km"]
                    avg_freight += i["freight"]
                try:
                    avg_rate = "{:.3f}".format(avg_freight / avg_km)
                    avg_km = "{:.0f}".format(avg_km / len(truck_tours))
                    avg_freight = "{:.2f}".format(avg_freight / len(truck_tours))
                except ZeroDivisionError:
                    avg_rate = "no data"
                    avg_km = 0
                    avg_freight = 0

                return render(request, "truck/raport.html", {
                    "raport": truck_tours,
                    "period": f"week {chosen_week}",
                    "year": chosen_year,
                    "avg_km": avg_km,
                    "avg_freight": avg_freight,
                    "avg_rate": avg_rate,
                    "speditions": spedition_names,
                })
            else:
                chosen_year = int(form.cleaned_data["Year"])
                chosen_month = helpers.month_convert(form.cleaned_data["Month"])

                # Get list of chosen trucks
                trucks = []

                for id in truck_ids:
                    truck = Truck.objects.get(pk=int(id))
                    trucks.append(truck)
                truck_tours = []

                # Gather spedition ids from checked boxes
                sped_ids = request.POST.getlist("sped_box")
                if len(sped_ids) == 0:
                    return render(request, "truck/raport.html", {
                    "error": "No spedition chosen for the raport",
                    }) 
                sped_ids = [int(i) for i in sped_ids]
                if len(Spedition.objects.filter(user=request.user)) == len(sped_ids):
                    spedition_names = "All speditions"
                
                else:
                    spedition_names = []

                    for id in sped_ids:
                        spedition_names.append(Spedition.objects.get(pk=id).name)

                # Get tours that those trucks have for chosen month
                for truck in trucks:
                    tours = Tour.objects.filter(truck=truck)
                    month_tour = []
                    for tour in tours:
                        if chosen_month == tour.date.month and tour.date.isocalendar().year == chosen_year and tour.spedition.id in sped_ids:
                            tour_month = {
                                "km": tour.km,
                                "freight": tour.freight
                            }
                            month_tour.append(tour_month)

                    # Add values from dictionaries by keys
                    if month_tour:
                        month = dict(functools.reduce(operator.add,
                        map(collections.Counter, month_tour)))
                        
                        # Make a new dict with proper keys
                        month = {
                            "name": truck.name,
                            "km": month["km"],
                            "freight": month["freight"],
                            "rate": "{:.3f}".format(month["freight"]/month["km"])
                        }
                    
                    # If no tours for this month
                    else:
                        month = {
                            "name": truck.name,
                            "km": 0,
                            "freight": 0,
                            "rate": ""
                        }
                    truck_tours.append(month)

            # Average km, freight and rate
            avg_km = 0 
            avg_freight = 0
            

            for i in truck_tours:
                avg_km += i["km"]
                avg_freight += i["freight"]
            avg_rate = "{:.3f}".format(avg_freight / avg_km)
            avg_km = "{:.0f}".format(avg_km / len(truck_tours))
            avg_freight = "{:.2f}".format(avg_freight / len(truck_tours))

            return render(request, "truck/raport.html", {
                "raport": truck_tours,
                "period": form.cleaned_data["Month"],
                "year": chosen_year,
                "avg_km": avg_km,
                "avg_freight": avg_freight,
                "avg_rate": avg_rate,
                "speditions": spedition_names,
            })

        else:
            return render(request, "truck/raport.html", {
        "error": "Invalid form",
    }) 
    else:
        return render(request, "truck/raport.html", {
    "error": "No input data chosen",
        }) 

# Adding spedition from trucks view 
def add_spedition(request):
    if request.method == "POST":
        form = SpeditionForm(request.POST)
        if form.is_valid():
            # Gather data and save spedition in database
            name = form.cleaned_data["Name"]
            spedition = Spedition(user=request.user, name=name)
            spedition.save()
            return HttpResponseRedirect(reverse("trucks"))
        
def speditions(request):
    if request.method == "POST":
        form = SpeditionForm(request.POST)
        if form.is_valid():
            # Gather data and save spedition in database
            name = form.cleaned_data["Name"]
            spedition = Spedition(user=request.user, name=name)
            spedition.save()
            return HttpResponseRedirect(reverse("speditions"))
    else:
        speditions = Spedition.objects.filter(user=request.user)

        return render(request, "truck/speditions.html", {
            "speditions": speditions,
            "form": EditSpeditionForm(),
            "add": SpeditionForm(),
        }) 
    
def delete_truck(request, truck_id):
    if request.method == "POST":
        truck = Truck.objects.get(pk=truck_id)
        truck.delete()
        
        return HttpResponseRedirect(reverse("trucks"))  


def edit_spedition(request, spedition_id):
    if request.method == "POST":
        spedition = Spedition.objects.get(pk=spedition_id)
        form = EditTruckForm(request.POST)
        if form.is_valid():
            spedition.name = form.cleaned_data["New_name"]
            spedition.save()
            return HttpResponseRedirect(reverse("speditions"))  


    
def delete_spedition(request, spedition_id):
    if request.method == "POST":
        if len(Spedition.objects.filter(user=request.user)) == 1:
            return render(request, "truck/speditions.html", {
                "speditions": Spedition.objects.filter(user=request.user),
                "form": EditSpeditionForm(),
                "add": SpeditionForm(),
                "error": "Cannot delete all speditions, please add another spedition before deleting that one",
            })   
        spedition = Spedition.objects.get(pk=spedition_id)
        spedition.delete()
        
        return HttpResponseRedirect(reverse("speditions"))  