import csv

file_name = 'Intervention_Strategies'
with open(file_name, 'r', newline='', encoding='utf-8') as tsvfile, \
     open(file_name + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    writer = csv.writer(csvfile)
    for row in reader:
        writer.writerow(row)