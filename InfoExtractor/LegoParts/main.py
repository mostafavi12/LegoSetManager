import os
import PyPDF2
from PyPDF2 import PdfReader
import sqlite3
import re

# Database connection
conn = sqlite3.connect(r'..\db\lego_parts.db')
c = conn.cursor()

def is_parts_list_page(text):
    # Regex pattern to match "n'x'm" where n is 1-2 digits and m is 6-7 digits
    global tmpPartList
    parts_ = []
    pattern = R"\b\d{1,3}x\s*\d{4,9}\b"
    matches = re.findall(pattern, text)
    result = len(matches) >= 3
    if result:
        tmpPartList += text
        for match in matches:
            match = re.split(r'x\s*', match)
            if len(match[1]) > 7:
                match[1] = match[1][:7]
            d = int(match[0])
            f = int(match[1])
            parts_.append([d, f])
    return result, parts_


def extract_parts_from_pdf(pdf_path):
    parts_ = []
    parts_temp = []
    nListPage = 0
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        nPages = len(reader.pages)
        if nPages > 15:
            for page_num in range(nPages-10, nPages):
                page = reader.pages[page_num]
                text = page.extract_text()
                result, parts_temp = is_parts_list_page(text)
                if result:
                    parts_ += parts_temp
                    nListPage += 1
        else:
            for page_num in range(nPages):
                page = reader.pages[page_num]
                text = page.extract_text()
                result, parts_temp = is_parts_list_page(text)
                if result:
                    parts_ += parts_temp
                    nListPage += 1
    return nListPage, parts_


def insert_set_data(set_number, set_name, total_parts, age):
    c.execute("INSERT OR IGNORE INTO sets (set_number, set_name, total_parts, age) VALUES (?, ?, ?, ?)",
              (set_number, set_name, total_parts, age))

def insert_part_data(set_number, part_number, quantity):
    sqlStr = f"INSERT OR IGNORE INTO parts (set_number, part_number, quantity) VALUES ({set_number}, '{part_number}', {quantity})"
    c.execute(sqlStr)

def traverse_directories(root_path):
    global tmpPartList
    totalNumberOfSets = 0
    numberOfSetsWithPartFile = 0
    numberOfSetsWithoutpartFile = 0
    for root, dirs, files in os.walk(root_path):
        folder_name = os.path.basename(root)
        if len(folder_name) < 12:
            continue
        try:
            set_number, set_name, total_parts, age = folder_name.split(', ')
        except:
            print(f'something went wrong for {folder_name}')
            continue
        nPartFilesFound = 0
        totalNumberOfSets += 1
        for file in files:
            if "DONTEXTRACT_" in file:
                continue

            if file.endswith('.pdf'):
                insert_set_data(set_number, set_name, total_parts, age)
                pdf_path = os.path.join(root, file)
                tmpPartList = ""
                nListPages, parts = extract_parts_from_pdf(pdf_path)
                if nListPages > 0:
                    nPartFilesFound += 1
                    nParts = 0
                    nItems = 0
                    for part in parts:
                        part_number = part[1]
                        quantity = part[0]
                        nParts += quantity
                        nItems += 1
                        insert_part_data(set_number, part_number, quantity)
                        '''
                        csvFileName = f"..\\csvFiles\\{set_number}.csv"
                        csvFile = open(csvFileName, "w")
                        csvFile.write(f'{part[1]}; ' + str(part[0]) + '\n')
                        '''
                    if (nParts < int(total_parts)):
                        csvFileName = f"..\\db\\Faulty_sets\\{set_number}.csv"
                        txtFileName = f"..\\db\\Faulty_sets\\{set_number}.txt"
                        csvFile = open(csvFileName, "w")
                        txtFile = open(txtFileName, "w", encoding="utf-8")
                        # Write to the csv file
                        csvFile.write(f'{set_number} has {nListPages} list pages and {nParts} parts, total nr parts is {total_parts}, nItems {nItems}\n')
                        for part in parts:
                            csvFile.write(f'{part[1]}; ' + str(part[0]) + '\n')
                        csvFile.write('\n')
                        csvFile.write('\n')
                        #print(f'{set_number} has {nListPages} list pages and {nParts} parts, total nr parts is {total_parts}, nItems {nItems}')

                        # write to the text file
                        txtFile.write(f'{set_number} has {nListPages} list pages and {nParts} parts, total nr parts is {total_parts}, nItems {nItems}\n')
                        txtFile.write('\n')
                        txtFile.write('\n')
                        txtFile.write(tmpPartList)
                        csvFile.close()
                        txtFile.close()
        if (nPartFilesFound == 0):
            print(f'no part files were found in this directory {folder_name}')
            numberOfSetsWithoutpartFile += 1
        elif(nPartFilesFound > 1):
            print(f'Too many part files in {folder_name}')
            numberOfSetsWithPartFile += 1
        else:
            numberOfSetsWithPartFile += 1
    print(f'There are in total {totalNumberOfSets}, without parts: {numberOfSetsWithoutpartFile} and with parts: {numberOfSetsWithPartFile}')

tmpPartList = ""
#traverse_directories(r'C:\users\mosta\my drive\legos\manuals')
traverse_directories(r'C:\manuals')
conn.commit()
conn.close()
