from knora import KnoraError, knora
import csv
from pprint import pprint
import re

server = "http://0.0.0.0:3333"
user = "root@example.com"
password = "test"
projectcode = "0805"
ontoname = "tdk_onto"
con = knora(server, user, password)
schema = con.create_schema(projectcode, ontoname)

lage_file = "lage_output.csv"
kampagne_file = "DaSCH_Kampagne_190415.csv"


class tdk_create_data:
    def create_lage(self, lage_file):
        lage_store = {}  # stores iris in format {lageNr  : iri}
        with open(lage_file) as csvfile:
            for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
                for i in range(len(line)):

                    if line[i].find(",") != -1:
                        line[i] = line[i].split(",")
                # obj = {"lageNr": line[0], "lageGrab": line[1], "lageUmgebung": line[2],
                #       "lageAreal": line[3], "lageRaum": line[4],
                #       "lageSchnitt": line[5]}
                # pprint(obj)
                lage_store[line[0]] = con.create_resource(schema, "Lage", "",
                                                          {"lageNr": line[0], "lageGrab": line[1],
                                                           "lageUmgebung": line[2],
                                                           "lageAreal": line[3], "lageRaum": line[4],
                                                           "lageSchnitt": line[5]})['iri']
        return lage_store

    def create_kampagne(self, kampagne_file):
        kampagne_store = {}
        with open(kampagne_file, encoding='utf-8') as csvfile:
            for line in csv.reader(csvfile, delimiter=';', quotechar='"'):
                line[1] = self.getDate(line[1])
                line[2] = self.getDate(line[2])
                for i in range(len(line)):
                    if line[i].find("/") != -1:
                        line[i] = line[i].split("/")

                kampagne_store[line[0]] = con.create_resource(schema, "Kampagne", "",
                                                              {"kampagne": line[0], "kampagneStartDatum": line[1],
                                                               "kampagneEndDatum": line[2],
                                                               "kampagneTeilnehmer": line[3], "kampagneGrab": line[4],
                                                               "kampagneUmgebung": line[5],
                                                               "kampagneBemerkung": line[6]})['iri']

    def getDate(self, str):
        #TODO implement this using regular expressions
        str = str.split('.')
        if len(str)!=3:
            raise ValueError
        str = str[2]+"-"+str[1]+"-"+str[0]
        return str