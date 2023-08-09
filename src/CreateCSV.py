# Standard Library Imports
import csv
import os

class Csv:
    def __init__(self, list):
        self.data = list
    
    def exportCSV(self, file_name, folder_path):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            row = []

            for entry in self.data:
                row.append(entry.get())

                if len(row) == 4:
                    writer.writerow(row)
                    row.clear()
            
            # Write remaining entries to csv (should never happen)
            if len(row) > 0:
                writer.writerow(row)
