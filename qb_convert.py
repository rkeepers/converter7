#!/usr/bin/env python3.4 
#
# This program wil convert Quickbooks CSV export files into usable data
#
#
# 28dec2017
# rkeepers@sparksonline.net
# v0.01
#
# ToDo: handle account name not found error
#
# https://github.com/rkeepers/converter7.git
#
######################################################################
# Imports
import os
import csv
import sys
#####################################################################
def main():
    
    # line counter for processing/removing header rows 
    count=0
    # Get the name of the input file - ask for it if not provided
    if len(sys.argv) > 1 :
        inputFile = sys.argv[1]
    else:
	# still trying to figure out changes between versions of Python working/not with "input()"
	# it seems like input() sometimes class str and sometimes class int w/python3x
        inputFile = input("Please enter the input filename : ")
    # make sure file exists. If not, exit the program
    if not os.path.exists(inputFile):  
        print( "Sorry, file not found. I'm giving up.")
        return
    accountTable = {'account1':'1','account2':'2','accountZ':'3'}
    months = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06','July':'07', 'August':'08','September':'09','October':'10', 'November':'11', 'December':'12'}
    # open the csv file and iterate line by line
    inputText = csv.reader(open(inputFile, 'rU'), delimiter=',')
    for line in inputText:
        if count == 2:
            date = line[0]
            date = date.split()
            dateField = date[1] + "-" + months[date[0]] + "-00"
            outputFile = open(dateField +'.csv', 'w')
        count += 1
        # skip the first heading lines from the file and then only add lines that have data in the last field
        if count > 4 and line[6] != "":
            # we are ignoring any empty fields below
            line[:] = [item for item in line if item != '']
            # insert the date field for mySQL date filed usage
            line.insert(0,dateField)
            # replace Account names with numeric replacement.
            # we intend to have a SQL table to match account numbers with names
            line[1]= accountTable[line[1]]

            # print the data to file in csv format
            outputFile.write(line[0] + "," + line[1] + "," + line[2] + "\n")
            #print(line)
    # close our file to complete writing        
    outputFile.close()
    print( dateField +'.csv' + " written")
    #exit 
    SystemExit(0)
    
if __name__ == '__main__':
  main()    
