import csv

def load_address_data(file_path):
    #Initalize an empty list to store the addresses
    address_data = []
    #Open the CSV file in read mode.
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            #Third column from the row, and remove any spaces then add it to the list.
            address_data.append(str.strip(row[2]))
    return address_data

addressList = load_address_data('data/addressCSV.csv')
