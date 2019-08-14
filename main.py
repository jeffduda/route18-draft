# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
import csv
from route18 import Player
from route18 import Route18_2019
from route18 import FantasyPros

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
Bootstrap(app)

class Team:

    def __init__(self, name):
        self.name = name
        self.roster = []

def getDraft( filename ):
    draft = []
    count = 0
    with open( filename, 'r' ) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if (count > 0):
                draft.append( row[1] )
            count += 1

    return(draft)

def setRosters(players):
    teams = [
        Team("BITE ME"),
        Team("Devil Cows"),
        Team("Domanick Davis"),
        Team("Food For Anubis"),
        Team("Franks Tanks"),
        Team("Fubar"),
        Team("Gordon Gekko"),
        Team("Have Nots"),
        Team("IronCity"),
        Team("O-Dog"),
        Team("Piss & Vinegar"),
        Team("Secret Squirrels"),
        ]



    teamDict = {
        "BITE ME" : 0,
        "Devil Cows" : 1,
        "Domanick Davis" : 2,
        "Food For Anubis" : 3,
        "Franks Tanks" : 4,
        "Fubar" : 5,
        "Gordon Gekko" : 6,
        "Have Nots" : 7,
        "IronCity" : 8,
        "O-Dog" : 9,
        "Piss & Vinegar" : 10,
        "Secret Squirrels" : 11
        }

    for p in players:
        if (p.pick > 0):
            #print( p.name + " " + str(p.pick) + " " + p.owner)
            teamIdx = teamDict[ p.owner ]
            #print( str(teamIdx) )
            teams[teamIdx].roster.append( p )

    return teams, teamDict

def getPlayers( filename ):
    players = []
    with open( filename, 'r' ) as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        for row in reader:
            if (count > 0) and (len(row)==15):
                p = Player()
                #print(row)
                #print( len(row) )
                p.rank = row[0]
                p.name = row[3]
                p.team = row[4]

                if row[5].find("QB") != -1:
                    p.position = "QB"
                elif row[5].find("RB") != -1:
                    p.position = "RB"
                elif row[5].find("WR") != -1:
                    p.position = "WR"
                elif row[5].find("TE") != -1:
                    p.position = "TE"
                elif row[5].find("K") != -1:
                    p.position = "K"
                else:
                    p.position = "DST"

                p.adp = row[11]
                p.pick = int(row[13])
                if p.pick > 0:
                    p.owner = row[14]

                players.append(p)

            count += 1

    return(players)



@app.route('/', methods=['GET','POST'])
#@app.route('/index', methods=['GET','POST'])
def index():
    #"""Return a friendly HTTP greeting."""
    #return 'Hello World!'

    current = 1
    teams = []
    players = []
    draft = []
    teamDict = {}

    #players = getPlayers( "static/players.csv" )
    players = FantasyPros()
    #draft = getDraft("static/draft_order.csv")
    draft = Route18_2019()
    #teams, teamDict = setRosters(players)
    keepers = []
    for p in players:
        if p.pick > 0:
            keepers.append(p.pick)

    if request.method == "GET":
        print("---GET---")
        teams, teamDict = setRosters(players)

    if request.method == "POST":
        print("---POST---")
        dat = request.form.to_dict()
        print("N players:" + str(len(players)))

        draftIdx = -1

        value = dat['onclock']
        current = int(value)
        print( "Current Pick = " + value)

        pickSubmitted = False
        for key, value in dat.items():

            if value == 'draft':
                draftIdx = int(key)-1
                pickSubmitted = True

            if key.find('status') != -1:
                idx = int(key.split(':')[1])-1
                if ( idx != draftIdx ):
                    inf = value.split(':')
                    players[idx].pick = int(inf[0])
                    players[idx].owner = inf[1]

        if pickSubmitted and current <= 180:
            players[draftIdx].pick = current
            players[draftIdx].owner = draft[current-1]
            previous = current
            current += 1

        if "undo" in dat:
            # FIXME = not working
            print("UNDO LAST PICK")
            if current > 1:
                lastPick = current - 1
                lastOwner = draft[lastPick-1]
                while lastPick > 1 and lastPick in keepers:
                    lastPick = lastPick - 1
                    lawOwner = draft[lastPick-1]
                for p in players:
                    if p.pick == lastPick:
                        p.pick = 0
                current = lastPick

        if "clear" in dat:
            players = FantasyPros()
            draft = Route18_2019()
            current = 1

        teams, teamDict = setRosters(players)


    for p in players:
        if ( p.pick > 0 ):
            draft[p.pick-1] = "K"

    if current <= 180:
        nextOwner = draft[current-1]
        while nextOwner=="K" and current <= 180:
            current += 1
            nextOwner = draft[current-1]

    return render_template('index.html', page='index', players=players, teams=teams, draft=draft, current=current)

@app.route('/rosters', methods=['GET'])
def rosters():

    return render_template

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
