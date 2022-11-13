import csv
import json

csv_file = open('movies_metadata.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
header = []
header = next(csv_reader)
rows_movie = {}
for row in csv_reader:
    rows_movie.update({row[0]: row[1]})
csv_file.close()

csv_file = open('ratings_small.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
header = []
header = next(csv_reader)
rows = []
for row in csv_reader:
    tmp = rows_movie.get(str(row[1]))
    if tmp != None:
        row[1] = tmp
        row[2] = float(row[2])
        rows.append(row)
        print(row)
csv_file.close()

csv_file = open('ratings.csv')
csv_reader = csv.reader(csv_file, delimiter=',')
header = []
header = next(csv_reader)
#print(header)
for row in csv_reader:
    row[2] = int(row[2])/2
    rows.append(row)
#print(rows)
csv_file.close()

new_dict = {}
for row in rows:
    if row[0] not in new_dict:
        new_dict.update({row[0]:{row[1]:row[2]}})
    else:
        new_dict.get(row[0]).update({row[1]:row[2]})

with open("ratings_small.json", "w") as outfile:
    json.dump(new_dict, outfile)
