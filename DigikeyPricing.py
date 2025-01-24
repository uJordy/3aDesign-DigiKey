import csv

with open('Bill Of Materials PowerPortMax-v5.csv', newline='') as csvfile:

    bomreader = csv.reader(csvfile, delimiter=' ')

    for row in bomreader:
        print(row)
    