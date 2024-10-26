# TruckRaport

http://truckraport.pythonanywhere.com - sometimes loads on a 2nd try, server side issue

## Video: https://youtu.be/x7GzCzwvY14

## Setup

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Go to provided link (http://127.0.0.1:8000/ by default)

## Introduction

TruckRaport is a web-application created using Django framework for transport companies to generate weekly and monthly raports on how many kilometers were made, and for what price. It was designed to meet my particular needs in my current job where my boss needs me to prepare raports like that each week and each month. Before, I had been doing this using excel where this process was semi-automated but still required some manual calculations when for example some truck was being repaired and should not be taken into account. Moreover, when we got a new truck, I had to add some new fields, change some calculations so the process was a bit tedious at times. TruckRaport makes all of this much more convienient.

## How to use

### Create an account

To start using TruckRaport user is required to create an account providing username, password, and e-mail address. There is also a field to input name of spedition that you work with. It is possible to leave this field empty, then the name will be set to Default. Later it is possible to change it, and also add more speditions but it is required to have at least one. After successful registration, user is automatically logged in and redirected to home page that includes short description of the page and a link to enter the tool itself, which is also available on the navigation bar above.

### Add trucks and speditions

After opening the tool, user is presented with an interface that contains a variety of options. On top left corner there are two input fields where user can add new trucks and speditions providing names for them. After adding any of them, new element appears in one of the tables below - left is for trucks, right for speditions. When click on any spedition name, he is taken to a page where he can change or delete speditions.

### Add tours (meaning deliveries, orders)

If user added a truck and it is visible in the trucks table below, he can click on the name of the truck to enter its page that also comes with different possibilities. A lot of the times in transport, speditions offer fixed price per kilometer. That is set on 1.3 € per 1 km on default, as it is somewhat of a standard in today's market (having that set will make it easier to add tours). On top left corner of the screen, has a possibility to change this value. That setting is associated with his account, whenver he/she changes it, new value is saved. There is also a field to change name of the truck, and button to delete the truck - after pressing it, another button to confirm that appears.

Below that section, there are input fields to add tour for this particular truck. First of them is date that uses Django's form template for dates. Next is kilometers, where user specifies how long the tour is. After inputting a value for km, next field with a price is already being filled, calculated using the default price rate. For example, if price rate is set on 1.3€/1km, after inputting 100 in kilometers field, price field is automatically set to 130€ but it is possible to override that, and put price manually. Next input field is for price per km rate for this particular tour, as it is not always default. It is being calculcated automatically from kilometers and price input fields. Last thing is to choose a spedition from a dropdown list. Here, user sees all of his speditions that he added earlier, or at the least the one that was created during registration. After providing all required data, user can press the button to add the tour, that will appear in the tour table beneath, ordering them chronologically, having the latest on top.

Last column of the table offers buttons to edit or delete highlighted tour. After pressing edit, the form previously meant for adding new tour, now has set values of the chosen tour with possibility to change them. The background of the form is now yellow to signal that. User can now save changes or cancel this operation. Next to edit button, there is a button to delete the tour. After pressing it, another button appears to confirm that.


Additionally, on top right corner of this page, user sees data for how many kilometers, and for what price that truck did current week and current month.

## Generate a raport

When user has at least one truck, it is possible to generate a raport. On the previous page, where user could add trucks and speditions, on top right corner are input fields for a raport. First of all, user has to choose whether this raport is suppose to be for a week or for a month selecting from the so-called radio buttons. Then, he/she chooses date from DateField that he needs raport for. Another required element is to choose for which truck, and for which speditions, user wants this raport. In both of the tables below - for trucks, and speditions - there are checkboxes to select. On the top of the tables, there is a checkbox that if clicked on, selects all elements below for easier usage. Finally, when all this is set, user clicks on a button to generate raport which opens new page with all of the data. On top of the page, there is a summary that shows kilometers, price and rate on average per truck. Below, there is a table showing data for each truck seperately.


## Technologies

- Django (Python, sqlite3)
- HTML
- CSS
- JavaScript
- Bootstrap

## Files

Project contains mostly default Django files and structures, modifying mainly views.py, urls.py, and models.py. Besides that, I created several HTML templates and JavaScript files.

### HTML

- index.html - HTML template for main page
- layout.html - HTML template for layout that other templates use
- login.html - HTML template for login page
- raport.html - HTML template to see generated raport
- register.html - HTML template for register page
- speditions.html - HTML template to edit or  delete speditions
- truck.html - HTML template for a single truck view, where user can add tours
- trucks.html - HTML template for a view of all trucks, speditions, and input fields for raport

### JavaScript

- speditions.js - JavaScript for speditions page (show/hide delete button)
-truck.js - JavaScript for single truck page (fetching tours from database, fetching change names of the truck, show/hide buttons)
- trucks.js - JavaScript for page with all trucks an speditions (Select All checkboxes)

### CSS

- styles.css - CSS for whole website

Styles contain mainly setting marigins, paddings, background color of the body, and div elements, also having two tables side by side

### Python

- helpers.py - created to store helpers functions, however, turned out to have only one function at the moment - function that converts name of the month to the corresponding number, that was needed generating raports for a specific month. More functions may be added in the future.

### Database

#### Models for this website include: User, Truck, Tour, Spedition

#### User

User is a default AbstractUser model from Django with an additional DecimalField to store user's default price per km rate.

#### Truck

Each truck element contains an AutoField primary key as an id, name as a CharfField, and also is related to some user using Foreign Key

#### Spedition

Each spedition element contains an AutoField primary key as an id, name as a CharfField, and also is related to some user using Foreign Key

#### Tour

Each tour element contains an AutoField primary key as an id, DecimalField called freight to store price, IntegerField called km to store kilometers, DecimalField called rate to store price per km rate, DateField to store date, and is also related to other models - User, Truck, and Spedition - using ForeignKeys.

## Usage

Install django by inputting `pip install django`, then use the standard `python manage.py runserver` command to run the application. No need for any other additional packages or set up.