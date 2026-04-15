from datetime import datetime

class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes=None):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes if notes else ""
        self.status = "At Hub" #Status when the package is created.
        self.departure_time = None #The time when the package leaves the HUB
        self.delivery_time = None #The time when the package is delivered.
        self.truck_id = None

    def update_status(self, check_time):
        if isinstance(check_time, str):
            check_time = datetime.strptime(check_time, "%I:%M %p")
        #Finds the status of the package based on its delivery time and departure time.
        if self.delivery_time and check_time >= self.delivery_time:
            self.status = "Delivered"
        elif self.departure_time and check_time >= self.departure_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"
        return self.status

    def get_status(self, check_time):
        if not isinstance(check_time, datetime):
            raise ValueError("check_time must be of type datetime")

        if self.delivery_time and check_time >= self.delivery_time:
            return f"Delivered at {self.delivery_time.strftime('%I:%M %p')}"
        elif self.departure_time and check_time >= self.departure_time:
            return "En route"
        else:
            return "At Hub"

    # Package details
    def __str__(self):
        return (f"package {self.package_id}: {self.address}, {self.city}, {self.state} {self.zip_code}," 
               f"Deadline: {self.deadline}, Weight: {self.weight}, Status: {self.status}, " 
               f"Departure Time: {self.departure_time}, Delivery Time: {self.delivery_time}")



