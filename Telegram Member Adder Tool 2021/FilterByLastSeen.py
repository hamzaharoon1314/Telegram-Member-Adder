import csv
import os


lines = list()


def main():
    lines = list()
    with open('data.csv', 'r',encoding='UTF-8') as readFile:

        reader = csv.reader(readFile)

        for row in reader:

            lines.append(row)

            for field in row:

                if field == '31634268763763':
                    lines.remove(row)
    with open('11.csv', 'w', encoding='UTF-8') as writeFile:
        writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

        writer.writerows(lines)

def main1():
    lines = list()
    with open('11.csv', 'r',encoding='UTF-8') as readFile:

        reader = csv.reader(readFile)

        for row in reader:

            lines.append(row)

            for field in row:

                if field == 'username':
                    lines.remove(row)
    
    with open('22.csv', 'w', encoding='UTF-8') as writeFile:
        writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

        writer.writerows(lines)

main()
main1()


with open("22.csv","r",encoding='UTF-8') as source:
    rdr = csv.reader(source)

    with open("data.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['sr. no.', 'username', 'user id', 'name', 'group', 'Status'])
        i = 0
        for row in rdr:
            i += 1
            writer.writerow((i,row[1], row[2], row[3], row[4], row[5]))
            
            
os.remove("11.csv")
os.remove("22.csv")
#os.remove("unf.csv")
print("Successfully Filtered And Saved In data.csv")