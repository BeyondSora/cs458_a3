#!/usr/bin/python

#
# 1. Build poll data records database
#    a. Read "Poll-Data.csv" line by line
#    b. Convert each record into a record object
#       - Name
#       - Telephone
#       - Day, Month of Birth
#       - Year of Birth
#       - Gender
#       - Postal Code
#    c. Store each record object into a map
#    d. Have functions available to search through the array
#
# 2. Construct Reidentified-Data.csv
#    a. Read "Disease-Records.csv" line by line
#    b. Store each record into a record object and then into an array
#    c. Filter out all records that overlap on the following:
#       - Postal Code
#       - Gender
#       - Year of Birth
#    d. Look up for uniquely matching poll data record based on the above
#       i.e. A single poll data record should only match a single disease
#            record and ignore all other cases
#
# 3. Construct Query-Probs.txt
#    a. Read "Queries.csv" line by line
#    b. Convert each record into a record object and store into an array
#    c. For each record:
#       - Find if the record is identified with a disease.
#       - Else, find all overlapping records and calculate the probability.
#

import csv
import re
import sys

class Record(object):
    def __init__(self,
                 name       = None,
                 telephone  = None,
                 birthDay   = None,
                 birthMonth = None,
                 birthYear  = None,
                 gender     = None,
                 postalCode = None,
                 disease    = None):
        self.name       = name
        self.telephone  = telephone
        self.birthDay   = birthDay
        self.birthMonth = birthMonth
        self.birthYear  = birthYear
        self.gender     = gender
        self.postalCode = postalCode
        self.disease    = disease

    def __str__(self):
        return ("{name: '%s', telephone: '%s', birthDay: '%s', "
                "birthMonth: '%s', birthYear: '%s', gender: '%s', "
                "postalCode: '%s', disease: '%s'}") % (
                         self.name,
                         self.telephone,
                         self.birthDay,
                         self.birthMonth,
                         self.birthYear,
                         self.gender,
                         self.postalCode,
                         self.disease)

    def __eq__(self, rhs):
        if (self.name       == rhs.name       and
            self.telephone  == rhs.telephone  and
            self.birthDay   == rhs.birthDay   and
            self.birthMonth == rhs.birthMonth and
            self.birthYear  == rhs.birthYear  and
            self.gender     == rhs.gender     and
            self.postalCode == rhs.postalCode and
            self.disease    == rhs.disease):
            return True
        else:
            return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    # Match on postal code, gender, year of birth
    def match(self, rhs):
        return (self.birthYear   == rhs.birthYear and
                self.gender      == rhs.gender    and
                self.postalCode  == rhs.postalCode)

def getUnique(records):
    unique = []

    for r in records:
        if (isUnique(records, r)):
            unique.append(r)

    return unique

def isUnique(records, record):
    for r in records:
        if (not r is record and r == record):
            return False

    return True

def getUniqueMatch(records):
    unique = []

    for r in records:
        if (isUniqueMatch(records, r)):
            unique.append(r)

    return unique

def isUniqueMatch(records, record):
    for r in records:
        if (not r is record and r.match(record)):
            return False

    return True

# Sample input: Maliyah Fields,519 537 2516,14-12-1970,F,N2L 6P5
def makePollRecord(csvRow):
    name       = csvRow[0]
    telephone  = csvRow[1]
    gender     = csvRow[3]
    postalCode = csvRow[4]

    result = re.findall('([0-9][0-9]*)', csvRow[2])
    birthDay   = result[0]
    birthMonth = result[1]
    birthYear  = result[2]

    return Record(
            name,
            telephone,
            birthDay,
            birthMonth,
            birthYear,
            gender,
            postalCode,
            0)

def parsePollFile(pollFileName):
    #print("Parsing '" + pollFileName + "'...")

    # Read data from file
    with open(pollFileName) as f:
        csvReader = csv.reader(f, delimiter=',')
        records = []
        for row in csvReader:
            records.append(makePollRecord(row))

    return records

# Sample input: *,*,*,1970,F,N2L 6P5,Gingivitis
def makeDiseaseRecord(csvRow):
    birthYear  = csvRow[3]
    gender     = csvRow[4]
    postalCode = csvRow[5]
    disease    = csvRow[6]

    return Record(
            None,
            None,
            None,
            None,
            birthYear,
            gender,
            postalCode,
            disease)

def parseDiseaseFile(diseaseFileName):
    #print("Parsing '" + diseaseFileName + "'...")

    # Read data from file
    with open(diseaseFileName) as f:
        csvReader = csv.reader(f, delimiter=',')
        records = []
        for row in csvReader:
            records.append(makeDiseaseRecord(row))

    return records

# Sample output: George Georgerson,519 345 9336,1977,M,N2L 7R2,AIDS
def identify(pollRecords, diseaseRecords):
    identified = []

    #
    # An identified entry must match only a single poll record and
    # disease record
    #

    polls    = getUniqueMatch(pollRecords)
    diseases = getUniqueMatch(diseaseRecords)

    for p in polls:
        for d in diseases:
            if (p.match(d)):
                identified.append(Record(
                    p.name,
                    p.telephone,
                    None,
                    None,
                    p.birthYear,
                    p.gender,
                    p.postalCode,
                    d.disease))

    return identified

# Sample output: George Georgerson,519 345 9336,1977,M,N2L 7R2,AIDS
def writeToCSV(records, filename):
    csvWriter = csv.writer(sys.stdout, lineterminator='\n')

    for r in records:
        csvWriter.writerow(
                [r.name]       +
                [r.telephone]  +
                [r.birthYear]  +
                [r.gender]     +
                [r.postalCode] +
                [r.disease])

def main():
    #pollRecords       = parsePollFile("Small-Poll-Data.csv")
    #diseaseRecords    = parseDiseaseFile("Small-Disease-Records.csv")
    pollRecords       = parsePollFile("Poll-Data.csv")
    diseaseRecords    = parseDiseaseFile("Disease-Records.csv")
    identifiedRecords = identify(pollRecords, diseaseRecords)

    writeToCSV(identifiedRecords, "Reidentified-Data.csv")

    #print("\nPoll Records:")
    #for record in pollRecords:
        #print(record)

    #print("\nDisease Records:")
    #for record in diseaseRecords:
        #print(record)

    #print("\nIdentified Records:")
    #for record in identifiedRecords:
        #print(record)

main()
