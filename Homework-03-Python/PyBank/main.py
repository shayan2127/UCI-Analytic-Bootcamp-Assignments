import os
import csv

shayanpath = os.path.join('Resources', 'budget_data.csv')

with open(shayanpath, newline='') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')

    header = next(csvreader)

    length = []
    total = []
    average = []
    maximum = []
    max_date = []
    minimum = []
    min_date = []

    revenue = [int(row[1]) for row in csvreader]

with open(shayanpath, newline='') as csvfile:

    csvreader = csv.reader(csvfile, delimiter=',')

    header = next(csvreader)   
    
    month = [row[0] for row in csvreader]

    max_date_index = revenue.index(max(revenue))
    min_date_index = revenue.index(min(revenue))

    print(f"The total number of months included in the dataset is: {str(len(revenue))}")
    
    print(f"The total net amount of Profit/Losses over the entire period is: {str(sum(revenue))}")

    print(f"The average change in Profit/Losses between months over the entire period is: {str(float(sum(revenue) / len(revenue)))}")

    print(f"The greatest increase in profits (date and amount) over the entire period is: {month[max_date_index]} with value: {str(max(revenue))}")

    print(f"The greatest decrease in losses (date and amount) over the entire period is: {month[min_date_index]} with value: {str(min(revenue))}")

    length.append(str(len(revenue)))
    total.append(str(sum(revenue)))
    average.append(str(float(sum(revenue))/ len(revenue)))
    max_date.append(month[max_date_index])
    maximum.append(str(max(revenue)))
    min_date.append(month[min_date_index])
    minimum.append(str(min(revenue)))

final = zip(length, total, average, max_date, maximum, min_date, minimum)

output_file = os.path.join("output2.csv")

with open(output_file, "w", newline="") as datafile:

	writer = csv.writer(datafile)

	writer.writerow(["Total number of months", "Total net amount of Profit/Losses", 
                     "The average change in Profit/Losses", "Greatest increase (Date)", 
                     "Greatest increase in profits", "Greatest decrease (Date)", "Greatest decrease in losses"
                  ])

	writer.writerows(final)