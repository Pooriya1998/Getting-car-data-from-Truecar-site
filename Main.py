from bs4 import BeautifulSoup
import requests
import mysql.connector

# Database connection
name_database = input(" Enter the name of the database : ")
cnx = mysql.connector.connect(user= 'root', host= '127.0.0.1', password='', database=name_database)
cursor = cnx.cursor()
print(" You are connected to the database ")

# Get the car name
brand_car = input(" Enter the car brand name : ")
model_car = input(" Enter the name of the car model : ")

# Receive data from the desired site
page_url = "https://www.truecar.com/used-cars-for-sale/listings/%s/%s/"%(brand_car,model_car)
page = requests.get(page_url)
soup = BeautifulSoup(page.content, 'html.parser')
car = soup.find_all("a", class_="linkable order-2 vehicle-card-overlay")

# Project process
name_table = input(" Enter the name of the table : ")
list_1 = list()
for i in car:
    list_1.append(str(i))

list_2 = list()
for car in list_1:
    f1 = car.find("href")
    f2 = car.find('>')

    q = 'https://www.truecar.com/'+car[f1+7:f2-1]
    list_2.append(q)

list_3 = list()
for i in range(1,21):
    name_table = name_table
    page = requests.get(list_2[i])
    soup1 = BeautifulSoup(page.content, 'html.parser')
    car1 = str(soup1.find("div", class_="heading-2 margin-top-1"))
    f1 = car1.find('$')
    f2 = car1.find('</div>')
    carPrice = car1[f1:f2]
    car2 = str(soup1.find("p", class_="margin-top-1"))
    f01 = car2.find('>') + 1
    f02 = car2.find("</p>")
    carMileage = car2[f01:f02]
    car03 = soup1.find_all("img")
    car03 = str(car03[2])
    f001 = car03.find('alt=')
    f002 = car03.find('in')
    cursor.execute("INSERT INTO %s VALUES ( '%s', '%s', '%s')"%(str(name_table),str(car03[f001 + 5:f002-1]),str(carPrice),str(carMileage)))
    print(i)

cnx.close()

