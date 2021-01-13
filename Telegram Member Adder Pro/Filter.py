import csv
import os


lines = list()


def main():
    lines = list()
    with open('unf.csv', 'r',encoding='UTF-8') as readFile:

        reader = csv.reader(readFile)

        for row in reader:

            lines.append(row)

            for field in row:

                if field == '':
                    lines.remove(row)
    with open('1.csv', 'w', encoding='UTF-8') as writeFile:
        writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

        writer.writerows(lines)

def main1():
    lines = list()
    with open('1.csv', 'r',encoding='UTF-8') as readFile:

        reader = csv.reader(readFile)

        for row in reader:

            lines.append(row)

            for field in row:

                if field == 'username':
                    lines.remove(row)
    
    with open('2.csv', 'w', encoding='UTF-8') as writeFile:
        writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")

        writer.writerows(lines)

main()
main1()


with open("2.csv","r",encoding='UTF-8') as source:
    rdr = csv.reader(source)

    with open("data.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['sr. no.', 'username', 'user id', 'name', 'group', 'Status'])
        i = 0
        for row in rdr:
            i += 1
            writer.writerow((i,row[1], row[2], row[3], row[4], row[5]))
            
            
os.remove("1.csv")
os.remove("2.csv")
#os.remove("unf.csv")
print("Successfully Filtered And Saved In data.csv")