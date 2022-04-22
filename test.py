import csv

# from csv_reader.models import User

with open("1.csv", "r") as f:
    csv = csv.reader(f, delimiter=",")
    headers = next(csv)
    # user = User(*headers)
    answers = next(csv)
    for header, answer in zip(headers[:20], answers[:20]):
        print(header, answer)
