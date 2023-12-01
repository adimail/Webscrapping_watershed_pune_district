import csv


def read_csv(file_path):
    items = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            items.append(row[0])
    return items


file_path = './WaterShedIDS-Pune.csv'
watershedids = read_csv(file_path)

print(watershedids)
print("Length of df: ", len(watershedids))
