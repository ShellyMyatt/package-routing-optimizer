import csv

#Reads the CSV file and appends each row to distance_data, making it a two-dimensional list (list of Lists)
def load_distance_data(file_path):
    try:
        distance_data = []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                distance_data.append(row)
        return distance_data
    except FileNotFoundError:
        print(f"File not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error loading distance data: {e}")
        return []

# Finds the distance between two addresses
def get_distance(current_location, destination_address, address_data, distance_data):
    if current_location in address_data and destination_address in address_data:
        try:
            index1 = address_data.index(current_location)
            index2 = address_data.index(destination_address)

            return float(distance_data[index1][index2])
        except IndexError:
            print("Invalid index in the distance matrix.")
            return float('inf')
    else:
        print(f"Address not found: {current_location}")
        return float('inf')





