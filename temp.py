import csv

csvfile = open('out.csv', 'r')
reader = csv.reader(csvfile, delimiter='|')
outfile = open('queries.csv', 'w')
writer = csv.writer(outfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
words = set()
prev_id = 0

for row in reader:
    if row[0] != prev_id:
        writer.writerow(list(words))
        words.clear()
        words.add(row[1])
        prev_id = row[0]
    words.add(row[2])

csvfile.close()
outfile.close()
