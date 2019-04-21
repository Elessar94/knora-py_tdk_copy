from knora import KnoraError, knora
import csv

server = "http://0.0.0.0:3333"
user = "root@example.com"
password = "test"
projectcode = "0805"
ontoname = "tdk_onto"
file = "lage_output.csv"
con = knora(server, user, password)
schema = con.create_schema(projectcode, ontoname)
with open(file) as csvfile:
    count = 0
    for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
        for str in line:
            count = count + 1
            if str.find(",") != 0:
                str = str.split(",")
        output = con.create_resource(schema, "lage", "", {"lageNr": count, "lageGrab": line[0], "lageUmgebung": line[1],
                                                          "lageAreal": line[2], "lageRaum": line[3],
                                                          "lageSchnitt": line[4]})
