#Shelly Myatt
#000686948
import csv

from datetime import datetime
from address import load_address_data
from distance import load_distance_data, get_distance
from hashtable import HashTable
from package import Package
from truck import Truck


def initialize_data_from_csv(file_path):
    package_hash = HashTable()

    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            package_object = Package(
                package_id=int(row["Package ID"]),
                address=row["Address"],
                city=row["City"],
                state=row["State"],
                zip_code=row["Zip"],
                deadline=row["Deadline"],
                weight=int(row["Weight"]),
                notes=row.get("Notes", None)
            )
            package_hash.insert(package_object.package_id, package_object)
    return package_hash

def manually_load_trucks(package_hash):
    truck1_packages = [1, 4, 7, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 39, 40]
    truck2_packages = [3, 5, 6, 10, 11, 12, 18, 21, 22, 23, 25, 26, 28, 32, 36, 38]
    truck3_packages = [2, 8, 9, 17, 24, 27, 33, 35]


    #Loads the trucks and sets the trucks departure time, capacity and speed.
    def load_truck_with_packages(truck_id, packages, departure_time_str):
        departure_time = datetime.strptime(departure_time_str, "%I:%M %p")

        truck = Truck(truck_id, capacity=16, speed=18, mileage=0.0,location="4001 South 700 East",departure_time=departure_time)


        for package_id in packages:
            if len(truck.packages) < truck.capacity:
                package = package_hash.lookup(package_id)
                if package:
                    truck.add_package(package)
                    package.truck = truck #set the truck reference in the package
                    package.truck_id = truck.truck_id
            else:
                print(f"Truck {truck.truck_id} full capacity limit reached")
        return truck

    truck1 = load_truck_with_packages(1, truck1_packages, "8:00 AM")
    print(f"Truck ID: 1 departs at: {truck1.departure_time.strftime('%I:%M %p')}")
    truck2 = load_truck_with_packages(2, truck2_packages, "9:05 AM")
    print(f"Truck ID: 2 departs at: {truck2.departure_time.strftime('%I:%M %p')}")
    truck3 = load_truck_with_packages(3, truck3_packages, "10:20 AM")
    print(f"Truck ID: 3 departs at: {truck3.departure_time.strftime('%I:%M %p')}")

    return [truck1, truck2, truck3]

def calculate_delivery_time(distance, speed):
    if speed <= 0:
        raise ValueError("speed must be greater than zero")
    travel_time = distance / speed
    travel_time_minutes = travel_time * 60
    return travel_time_minutes

#Nearest Neighbor algorithm
def find_nearest_package(truck, current_location, address_index_map, distance_data):
    #finds the nearest package for a given truck
    nearest_package = None
    shortest_distance = float("inf")  # Start with a very large number for comparison

    # Finds the nearest package by distance
    for package in truck.packages:
        package_address_index = address_index_map.get(package.address.strip().lower())
        current_location_index = address_index_map.get(current_location.strip().lower())

        try:
            if current_location_index < package_address_index:
                temp=current_location_index
                current_location_index=package_address_index
                package_address_index=temp
            distance = float(distance_data[current_location_index][package_address_index])
        except ValueError:
            distance = float("inf")
        # Checks if this package is closer than the previous one
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_package = package
    return nearest_package, shortest_distance



def deliver_packages(trucks, address_data, distance_data):
    address_index_map = {address.strip().lower(): idx for idx, address in enumerate(address_data)}

    for truck in trucks:
        print(f"Starting the delivery route for truck ID: {truck.truck_id} from {truck.location}")
        current_location = truck.location  # The current location (initially HUB)


        while truck.packages:
            nearest_package, shortest_distance = find_nearest_package(truck, current_location, address_index_map, distance_data)

            if nearest_package:
                #Calculate the delivery time
                travel_time_minutes = calculate_delivery_time(shortest_distance, truck.speed)
                truck.deliver_package(nearest_package, shortest_distance, travel_time_minutes)

                #Update the current location to the packages address
                current_location = nearest_package.address


                # Print the delivery information
                print(
                    f"Package ID: {nearest_package.package_id} delivered to {nearest_package.address} at {truck.current_time.strftime('%I:%M %p')}")

            else:
                print(f"No nearest package found.")
                break

        print(f"Truck ID: {truck.truck_id} total mileage: {truck.mileage:.2f} miles.")  # Print the total mileage of the truck


def validate_total_mileage(trucks):
    total_mileage = sum(truck.mileage for truck in trucks)

    if total_mileage > 140:
        print("Warning Total Mileage exceeds 140 miles.")
    else:
        print(f"Total mileage: {total_mileage:.2f} is within the 140 mile limit.")

def parse_time(time_input):
    try:
        return datetime.strptime(time_input, "%I:%M %p")
    except ValueError:
        try:
            return datetime.strptime(time_input, "%H:%M")
        except ValueError:
            raise ValueError("Invalid time format. Please use HH:MM AM/PM format or HH:MM in 24-hour format.")

def display_delivery_summary(trucks):
    print("\nDelivery Summary:")
    print("-" * 50)
    for truck in trucks:
        print(f"Truck ID: {truck.truck_id}")
        for package in truck.delivered_packages:
            print(f"Package ID: {package.package_id} delivered to {package.address} at {package.delivery_time.strftime('%I:%M %p')}")
        print(f"Total mileage for truck {truck.truck_id}: {truck.mileage:.2f} miles\n.")

def display_all_package_status(package_hash, check_time):
    print(f"\nAll the package's statuses at, {check_time.strftime('%I:%M %p')}")
    print("-" * 50)

    for bucket in package_hash.table:
        for key_value_pair in bucket:
            package = key_value_pair[1]

            package_status = package.get_status(check_time)

            print(f"Package ID: {package.package_id} status: {package_status}")

            if package.truck:
                print(f"Truck ID: {package.truck.truck_id}")
            else:
                print(f"No truck ID found.")

def check_all_package_status(package_hash, check_time, package_id):
    print(f"\nPackage ID: {package_id} status at, {check_time.strftime('%I:%M %p')}")
    print("-" * 50)

    package = package_hash.lookup(package_id)
    if package:
        status = package.get_status(check_time)

        print(f"Package ID: {package.package_id}")
        print(f"Status: {status}")
    else:
        print(f"Package ID: {package_id} not found.")

def lookup_all_package_details(package_hash, check_time):
    print("\nALl of the package's details:")
    print("-" * 50)

    correction_time = datetime.strptime ("10:20 AM", "%I:%M %p") #The address should change at 10:20

    for package_id in package_hash.get_all_keys():
        package = package_hash.lookup(package_id)
        if package:
            package.update_status(check_time)

            if package.package_id == 9:
                print(f"Checking package ID 9 address at {check_time.strftime('%I:%M %p')}")

                if check_time >= correction_time:
                    print("Updating package ID 9 address:")
                    package.address = "410 S. State St."
                    package.city = "Salt Lake City"
                    package.state = "UT"
                    package.zip_code = "84111"
                else:
                    print("Package ID 9 address not updated.")

            print("\nPackage Details:")
            print("-" * 50)
            print(f"Package ID: {package.package_id}")
            print(f"Delivery Address: {package.address}")
            print(f"Delivery City: {package.city}")
            print(f"Delivery State: {package.state}")
            print(f"Delivery Zip Code: {package.zip_code}")
            print(f"Delivery Deadline: {package.deadline}")
            print(f"Package Weight: {package.weight} lbs")
            print(f"Package Truck: {package.truck_id}")
            print(f"Package Status: {package.status}")
            if package.delivery_time:
                print(f"Delivery Time: {package.delivery_time.strftime('%I:%M %p')}")
            else:
                print("Package not delivered yet.")
        else:
            print(f"Package ID: {package_id} not found.")

def main():
    #Initialize the hash table and load the package data
    distance_data = load_distance_data("CSV/distanceCSV.csv")
    address_data = load_address_data("CSV/addressCSV.csv")
    package_hash = initialize_data_from_csv('CSV/packageCSV.csv')

    trucks = manually_load_trucks(package_hash)

    deliver_packages(trucks, address_data, distance_data)

    display_delivery_summary(trucks)

    validate_total_mileage(trucks)

    #The user interface with a selection based menu
    while True:
        print("\n1. Look up a single package status at the specified time")
        print("2. View total mileage")
        print("3. Look up the status of all the packages at the specified time")
        print("4. Look up all the package's details:")
        print("5. Exit the program")
        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                #These are the prompts to check the status of a single specific package
                package_id = int(input("Enter package id: "))
                print("Enter time in this format:")
                print("- HH:MM AM/PM (e.g. 4:30 PM)")
                time_input = input("Time: ")
                check_time = parse_time(time_input)

                # This retrieves the package details and displays them in the menu.
                check_all_package_status(package_hash, check_time, package_id)


            except ValueError as e:
                print(f"Invalid input: {e} Please try again.")

        elif choice == '2':
            #This will calculate the total miles traveled for all the trucks.
            total_mileage = sum(truck.mileage for truck in trucks)
            print(f"Total mileage traveled by all the trucks: {total_mileage:.2f} miles.")

        elif choice == '3':
            try:
                #These are the prompts to check the status of all the packages at a specific time.
                print("Enter time in this format:")
                print("- HH:MM AM/PM (e.g. 4:30 PM)")
                time_input = input("Time: ")
                check_time = parse_time(time_input)

                display_all_package_status(package_hash, check_time)

            except ValueError as e:
                print(f"Invalid input: {e} Please try again.")

        elif choice == '4':
            time_input = input("Time: ")
            check_time = parse_time(time_input)
            lookup_all_package_details(package_hash, check_time)

        elif choice == '5':
            break

        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()


#Requirments:
# Each truck can carry 16 packages per trip
# To reload a truck must return to the HUB after finishing delivering its first load.
#There are 40 packages total
# Package ID 9 will have its address changed to the correct address at 10:20 AM so it can not be delivered before then.
#Packages 6,25,28,32 cannot leave until after 9:05 AM.
#Packages 13,14,15,16,19,20 must be delivered together on the same truck.
#Packages 3,18,36,38 must be delivered on truck 2
#Truck 2 does not need to return to the hub after making all of its delivery's unless its necessary to ensure all the packages are delivered.
#Deliver all 40 packages in a few trips as possible to stay within the 140-mile limit.

#My strategy:
#ID and assign the packages with deadlines to the first deliveries.
#Group the packages that need to be delivered together or on the same truck.
#Divide the packages into loads of 16 for each truck based on the requirements listed above.
#Assign the loads sequentially so that truck 1 returns to the HUB for the next load while truck 2 keeps delivering its packages.
#Use truck one for most of the delivery's
#Use truck 2 for overflow and low priority packages
#Make sure all packages are delivered.



