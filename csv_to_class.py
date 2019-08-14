import csv
import time
import sys


def csv_to_class(csvfilename, classFileName, className):
#    tableDir = "/home/jiancong/Desktop/projects/BayesNet/NaiveBayes/BasalGanglia/BG_Bayesian_network_NaiveBayes.xlsx"
#    tableName = "BGnetwork"

    print(csvfilename)
    file = open(classFileName,"w+")
    file.write("from route18 import Player \n")

    file.write( "def " + className + "(): \n ")
    file.write( "   players = [] \n" )

    with open( csvfilename, 'r' ) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            if (count > 0):
                file.write("    p = Player() \n")
                file.write("    p.rank = "+row[0]+"\n")
                file.write("    p.name = \""+row[3]+"\"\n")
                file.write("    p.team = '"+row[4]+"'\n")

                if row[5].find('QB') != -1:
                    file.write("    p.position = 'QB'\n")
                elif row[5].find('RB') != -1:
                    file.write("    p.position = 'RB'\n")
                elif row[5].find('WR') != -1:
                    file.write("    p.position = 'WR'\n")
                elif row[5].find('TE') != -1:
                    file.write("    p.position = 'TE'\n")
                elif row[5].find('K') != -1:
                    file.write("    p.position = 'K'\n")
                else:
                    file.write("    p.position = 'DST'\n")

                file.write("    p.adp = "+row[11]+"\n")
                file.write("    p.pick = int("+row[13]+")\n")
                if int(row[13]) > 0:
                    file.write("    p.owner = '"+row[14]+"'\n")

                file.write("    players.append(p)\n")

            count += 1
    file.write( "    return(players)\n" )
    file.close()
    return 0

def csv_to_draft(csvfilename, classFileName, className):

    print(csvfilename)
    file = open(classFileName,"w+")

    file.write( "def " + className + "(): \n ")
    file.write( "   draft = [] \n" )

    with open( csvfilename, 'r' ) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            if (count > 0):
                file.write("    draft.append(\""+row[1]+"\")\n")
            count += 1
    file.write( "    return(draft)\n" )
    file.close()
    return 0


csv_to_class( "static/players.csv", "players.py", "FantasyPros")

csv_to_draft( "static/draft_order.csv", "draft.py", "Route18_2019")
