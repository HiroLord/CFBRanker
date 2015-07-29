from datetime import date

def loadData(f):
    start = date(2014, 8, 26)
    statsPerTeam = 16
    f = open(f, 'r')

    games = [] #list of maps

    headers = [x.strip() for x in f.readline().split(',')]
    headers = headers[2:2+statsPerTeam]
    line = f.readline()

    while len(line) > 0:
        line = line.rstrip().split(',')
        day = line[0].strip()

        #Whats the point of age, playoffs? 
        dateA = [int(x) for x in day.split("-")]
        numDate = date(dateA[0], dateA[1], dateA[2])
        diff = (numDate-start).days
        week = (diff//7) + 1

        game = {"Date": date, "Week": week, "Vis Team": {"Team": line[1].strip()}, "Home Team": {"Team": line[18].strip()}}
        for i in range(len(headers)):
            game["Vis Team"][headers[i]] = line[i+2].strip()
            game["Home Team"][headers[i]] = line[i+19].strip()
        line = f.readline()
        games.append(game)

    f.close()

    return games
