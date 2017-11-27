import math
import csv as csvOperator
import sys
from random import shuffle
from copy import copy
import glob
import os

OUPTPUT_FILENAME = "Late Days.csv"

# CSV file writer
def writeCSV(filename, header, data): # header = ['name', 'email'], data = rows [[row1], [row2],...]
  # Add extension if necessary
  if not filename.endswith('.csv'):
    filename += '.csv'
  with open(filename, 'w') as csvfile:
    writer = csvOperator.writer(csvfile, delimiter=',', quotechar='|', quoting=csvOperator.QUOTE_MINIMAL)
    # Write header
    writer.writerow(header)
    # Data
    for row in data:
      writer.writerow(row)

# CSV file reader
def readCSV(filename):
  with open(filename) as file:
    csvfile = csvOperator.reader(file, delimiter=',')
    
    csv = {}
    csv['data'] = []
    csv['headers'] = None
    for row in csvfile:
      if (csv['headers'] == None):
        csv['headers'] = row
      else:
        csv['data'].append(row)
    return csv

def getLatedays(lateness, gracePeriod):
    latenessParts = lateness.split(':')
    lateHours = float(latenessParts[0])
    if lateHours == 0:
        return 0
    if (float(latenessParts[1]) <= gracePeriod):
        lateHours -= 1
    return (math.ceil(lateHours / 24))

def get_input(default, message):
    while True:
        value = raw_input(message + ' ')
        if not value:
            return default
        elif value.isdigit():
            return int(value)
        else:
            print('Entered number was invalid. Please try again. Remember to use a number (5) and not a word (five)')



print('Welcome to the Late Day Analyzer!\n')
print('For each relevant assignment in Gradescope, visit the "Review Grades" page and click "Download Grades" to download a CSV.')
print('Put those CSV files in the same directory as this script and make sure there are no other CSV files in this directory.')
print('You\'ll be asked a series of questions: you can choose not to respond and just hit enter, or enter a number (e.g., 5)')
print('Hit ctrl-c at any time to quit\n')
ignoreMe = raw_input('Hit enter to continue')
print(chr(27) + "[2J")

gracePeriod = get_input(5, 'How many long is the grace period, in minutes? (e.g., 5)')
maxLateDaysPerAssignment = get_input(2, 'How many late days can be used for each assignment? (e.g., 2)')
maxTotalLateDays = get_input(6, 'How many total late days do students have for the entire semester? (e.g., 6)')


csvFilenames = glob.glob('*.csv')

#filters out directories and output file
csvFilenames = filter(lambda file: os.path.isfile(file) and file != OUPTPUT_FILENAME, csvFilenames)

assignmentNames = [x.replace('_scores.csv','').replace('_',' ') for x in csvFilenames]

headers = ['Name','SID','Email', 'Late Days Used (total)']
headers.extend(map(lambda filename: 'Late days used for ' + filename, assignmentNames))
headers.append('Exceeded late day max for semester')
headers.extend(map(lambda filename: 'Exceeded late day max for ' + filename, assignmentNames))

lateDayDict = {}
for filename in csvFilenames:
    file = readCSV(filename)

    for row in file['data']:
        SID = row[1]
        if SID not in lateDayDict:
            lateDayDict[SID] = {}
            lateDayDict[SID]['name'] = row[0]
            lateDayDict[SID]['email'] = row[2]

        #maps number of late days to assignment name
        if row[5] == 'Missing':
            lateDayDict[SID][filename] = 0
        else:
            lateDayDict[SID][filename] = getLatedays(row[8], gracePeriod)

data = []

for SID, studentInfo in lateDayDict.iteritems():
    #these two variables serve as placeholders
    totalLateDays = 0
    brokeSemesterMax = False

    row = [studentInfo['name'], SID, studentInfo['email'], totalLateDays]
    #array containing values for what Late Day 'rules' were broken
    exceededMaxLateDays = [brokeSemesterMax]

    for filename in csvFilenames:
        if filename in studentInfo:
            # appends number of late days to that assignment and adds to total number of late days
            row.append(studentInfo[filename])
            totalLateDays += studentInfo[filename]
            #if exceeded Late Day max for assignment
            if studentInfo[filename] > maxLateDaysPerAssignment:
                exceededMaxLateDays.append(True)
            else:
                exceededMaxLateDays.append(False)
        #if they didn't take that course
        else:
            row.append(0)
            exceededMaxLateDays.append(False)

    #if exceeded semester max of late days
    if totalLateDays > maxTotalLateDays:
        exceededMaxLateDays[0] = True

    row[3] = totalLateDays
    row.extend(exceededMaxLateDays)
    data.append(row)


writeCSV(OUPTPUT_FILENAME, headers, data)
print('Done! Open "' + OUPTPUT_FILENAME + '" to see the results.')