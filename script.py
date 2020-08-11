import csv
import locale
import pprint
import os

locale.setlocale(locale.LC_ALL, '')

columnString = ""
category = ""
columnsToHandle = []
overageArrays = []
columnsAndValuesDict = {}
id = ''
isSlab = False

def place_value(number):
    return "{:,}".format(number).replace(',', '.')

def place_value_currency(number):
    return float(number.replace('.', '').replace(',', '.'))

def writeToCSV(insertDictionary):
    with open('toInsert.csv', 'a', newline='') as f:
        fieldnames = ['KIT_Product__c', 'KIT_Price_Category__c', 'KIT_Lower_Bound__c', 'KIT_Upper_Bound__c',
                      'KIT_Price__c', 'KIT_Overage_Block_Size__c', 'KIT_Overage_Price__c', 'KIT_Slab__c']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        if os.stat('toInsert.csv').st_size == 0:
            thewriter.writeheader()

        lastRememberedLowerBound = 0

        for column in insertDictionary:
            currentDictionaryValue = insertDictionary.get(column)
            if not isinstance(columnsAndValuesDict.get(column), list):
                if currentDictionaryValue:
                    thewriter.writerow({
                        'KIT_Product__c': id,
                        'KIT_Price_Category__c': category,

                        'KIT_Lower_Bound__c':  lastRememberedLowerBound + 1,
                        'KIT_Upper_Bound__c': columnsAndValuesDict.get(column),
                        'KIT_Price__c': place_value_currency(currentDictionaryValue),

                        'KIT_Overage_Block_Size__c': '',
                        'KIT_Overage_Price__c': '',

                        'KIT_Slab__c': isSlab
                    })
                    lastRememberedLowerBound = columnsAndValuesDict.get(column)
            else:
                if currentDictionaryValue:
                    tmpArray = columnsAndValuesDict.get(column)
                    thewriter.writerow({
                        'KIT_Product__c': id,
                        'KIT_Price_Category__c': category,

                        'KIT_Lower_Bound__c':  tmpArray[0],
                        'KIT_Upper_Bound__c': '',
                        'KIT_Price__c': '',

                        'KIT_Overage_Block_Size__c': tmpArray[1],
                        'KIT_Overage_Price__c': place_value_currency(currentDictionaryValue),
                        'KIT_Slab__c': isSlab
                    })

with open('toInsert.csv', 'w'):
    pass
# clearing files

print('Column Naming : \nx bis 5.000 \t\nx bis 7.000 \t\t\nx ab 7.000 \t\t\nx ab 10.000 per 15')
print('filename without .csv: ')
filename = input()

with open(filename + '.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    insertDictionary = {}

    print('Indicator: ')
    columnString = input()
    if not columnString:
        columnString = 'A'

    print('Which category (1/2/3/4/A/B/C/D): ')
    category = input()
    if category:
        category = 'Category ' + category

    print('Is Slab? (y/n):')
    answer = input()
    if answer == 'y':
        isSlab = True
    else:
        isSlab = False

    for column in csv_reader.fieldnames:
        if(column.startswith(columnString)):
            columnsToHandle.append(column)

    for column in columnsToHandle:
        if 'ab' not in column:
            tmpNumber = ''
            for char in column:
                if char.isdigit():
                    tmpNumber += char
            columnsAndValuesDict.update({column: int(tmpNumber)})
        else:
            tmpAbNumber = ''
            tmpOverageArray = []
            for char in column:
                if char.isdigit():
                    tmpAbNumber += char
                if char == 'p':
                    tmpOverageArray.append(int(tmpAbNumber))
                    tmpAbNumber = ''
            tmpOverageArray.append(int(tmpAbNumber))
            if len(tmpOverageArray) == 1:
                tmpOverageArray.append(1)
            columnsAndValuesDict.update({column: tmpOverageArray})

    for line in csv_reader:

        id = line['Id']

        for column in columnsToHandle:
            insertDictionary.update({column: line[column]})

        writeToCSV(insertDictionary)
        # break
