# Standard Library Imports
import csv

class Csv:
    def __init__(self, list):
        self.data = list
    
    def exportCSV(self, file_name, file_path):
        
        with open(file_path, mode="w", newline='') as file:
            writer = csv.writer(file)

            row = []

            for entry in self.data:
                row.append(entry)

                if len(row) == 4:
                    writer.writerow(row)
                    row.clear()
            
            # Write remaining entries to csv (should never happen)
            if len(row) > 0:
                writer.writerow(row)

