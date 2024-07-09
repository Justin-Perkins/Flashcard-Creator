# Standard Library Imports
import csv
import os

# Third-Party Library Imports
import customtkinter
from translate import Translator
import pykakasi

class Csv:
    def __init__(self, list, translator):
        self.data = list

        self.translator = translator
        self.kks = pykakasi.kakasi()
    
    def translate_text(self, text):
        translated_text = self.translator.translate(text)
        result = self.kks.convert(translated_text)
        romanized_text = ''.join([item['hepburn'] for item in result])
        return translated_text, romanized_text
    
    def exportCSV(self, file_name, folder_path, translate_mode_state):
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)

            row = []
            translated_text = ""
            romanized_text = ""

            for i, entry in enumerate(self.data):
                if translate_mode_state == 1 and i % 4 == 0:
                    translated_text, romanized_text = self.translate_text(entry.get())

                if i % 4 == 0:
                    row.append(entry.get())
                elif i % 4 == 1:
                    row.append(entry.get())
                elif i % 4 == 2 and translate_mode_state == 1:
                    row.append(translated_text)
                elif i % 4 == 2 and translate_mode_state == 0:
                    row.append(entry.get())
                elif i % 4 == 3 and translate_mode_state == 1:
                    row.append(romanized_text)
                elif i % 4 == 3 and translate_mode_state == 0:
                    row.append(entry.get())

                if len(row) == 4:
                    writer.writerow(row)
                    row.clear()
            
            # Write remaining entries to csv (should never happen)
            if len(row) > 0:
                writer.writerow(row)

        file.close()
