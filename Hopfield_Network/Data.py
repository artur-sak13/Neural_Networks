import csv

class Data(object):
    def __init__(self):
        self.file_name = "Async_Updating.txt"
        self.energies = "Energies.csv"

    def save_data(self, data):
        with open(self.file_name, 'a') as file:
            file.write(data)
        file.close()

    def write_energies(self, data):
        with open(self.energies, 'a+') as file:
            writer = csv.writer(file, delimiter=',')
            for num in data:
                file.write(str(num))
                file.write("\n")
            file.write("\n")
            file.write("\n")
        file.close()
