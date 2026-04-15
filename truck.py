from datetime import datetime, timedelta

class Truck:
    def __init__(self, truck_id, capacity, speed, mileage, location, departure_time):
        self.truck_id = truck_id
        self.capacity = capacity
        self.speed = speed
        self.mileage = mileage
        self.location = location
        self.departure_time = departure_time
        self.current_time = departure_time #Initialize the current time to the departure time
        self.packages = [] #The packages currently on the truck
        self.delivered_packages = [] #The packages that have been delivered

        #adds a package to the truck
    def add_package(self, package):
        if len(self.packages) < self.capacity:
            self.packages.append(package)
        else:
            raise ValueError("Truck capacity exceeded")

    def remove_package(self, package_id):
        self.packages = [pkg for pkg in self.packages if pkg.package_id != package_id]

    def deliver_package(self, package, distance, travel_time_minutes):
        self.mileage += distance #update's the truck's mileage and delivery time
        print(f"Truck ID: {self.truck_id}:Distance traveled {distance} miles. Total milage:{self.mileage:.2f} miles.")
        self.current_time += timedelta(minutes=travel_time_minutes )#updates the trucks current time to the delivery time.
        package.delivery_time = self.current_time #Assigns the package's delivery time
        self.location = package.address  #updates the truck's location to the delivery address
        self.remove_package(package.package_id) #Removes the delivered package from the trucks list.

    def __str__(self):
        return f"Truck {self.truck_id}: Location: {self.location}, Departure Time: {self.departure_time.strftime('%I:%M %p')}, Mileage: {self.mileage}, Current Time: {self.current_time}, Packages: {self.packages}"


#How it works:
#Start at the HUB. Initialize the current time with the trucks start time.
#For each package calculate its distance from the current location with: distance = distanceData addressData index current location addressData index package address
#It finds the distance between the truck's current location and each package's delivery address. Then selects the package with the nearest delivery address,to be delivered next.
#Selects the package with the shortest distance.
#It then updates the trucks location and calculates the travel time based on the speed limit of 18 miles per hour.
#Calculate the travel time using the formula: travel time = (distance/0.3 minutes)
#Upadate the current time by adding the travel time to the previous current time.
#Mark the package as Delivered, record the delivery time, and remove the package from the trucks package list.
#update the current location to the address of the delivered package.
#This will repeat until all the packages are delivered.






