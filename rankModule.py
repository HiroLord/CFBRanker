from datetime import date

def getOutcome(game):
	home = game["Home Team"]
	vis = game["Vis Team"]
	homeTeam = home["Team"]
	visTeam = vis["Team"]
	homeScore = int(home["Score"])
	visScore = int(vis["Score"])
	diff = homeScore - visScore
	if diff > 0:
		return (homeTeam, visTeam, diff)
	else:
		return (visTeam, homeTeam, -diff)

def ParseInput(file, statsPerTeam):
    start = date(2014, 8, 26) 
  
    games = []
    headers = [x.strip() for x in file.readline().split(',')]
    headers = headers[2:2+statsPerTeam]
    line = file.readline()
    while len(line) > 0:
    	line = line.rstrip().split(',')
	day = line[0].strip()
	
        dateA = [int(x) for x in day.split("-")]
	numDate = date(dateA[0], dateA[1], dateA[2])
	diff = (numDate-start).days
	age = (diff//7) + 1
	 
        game = {"Date": date, "Age": age, "Vis Team": {"Team": line[1].strip()}, "Home Team": {"Team": line[18].strip()}}
	for i in range(len(headers)):
		game["Vis Team"][headers[i]] = line[i+2].strip()
		game["Home Team"][headers[i]] = line[i+19].strip()
	line = file.readline()
	games.append(game)

    file.close()

    return games
