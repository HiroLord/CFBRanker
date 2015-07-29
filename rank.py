import operator
import math
from rankModule import getOutcome, ParseInput

#********************
# Constants
#********************
weeks = 14.0
statsPerTeam = 16
numRankings = 30
numIterations = 100
f = open('wagstatscfb2014.csv', 'r')

#**************************
# Initialize arrays
#**************************

#********************************
# Eventually in a function call:  ParseInput("file.csv"):
#********************************
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
	age = (diff//7) + 1
	
        
	game = {"Date": date, "Age": age, "Vis Team": {"Team": line[1].strip()}, "Home Team": {"Team": line[18].strip()}}
	for i in range(len(headers)):
		game["Vis Team"][headers[i]] = line[i+2].strip()
	#for j in range(len(headers))
		game["Home Team"][headers[i]] = line[i+19].strip()
	line = f.readline()
	games.append(game)
teamScores = {}

games = ParseInput(f, statsPerTeam) #list of maps
                                    #keys = Date, age, Vis Team, Home Team
                                    #age = weighting to make more recent games count more

for game in games:
	age = game["Age"]
	winMult = 1
	loseMult = 1
	if (age > weeks): #used to be 14
		winMult = 1.2
		loseMult = 0.8
	age = float(age)
	home = game["Home Team"]
	vis = game["Vis Team"]
	homeTeam = home["Team"]
	visTeam = vis["Team"]
	homeTotal = 0;
	visTotal = 0;

	homeScore = int(home["Score"])
	visScore = int(vis["Score"])
	diff = homeScore - visScore;
	homeTotal += diff*2 * age;
	visTotal -= diff*2 * age;
	
        #Home team win counts less than visiting team win 
        if diff > 0:
		homeTotal += 200 * age * winMult
		visTotal -= 150 * age * loseMult
	else:
		homeTotal -= 160 * age * winMult
		visTotal += 210 * age * loseMult
	
	if homeTeam in teamScores:
		teamScores[homeTeam] += homeTotal
	else:
		teamScores[homeTeam] = homeTotal

	if visTeam in teamScores:
		teamScores[visTeam] += visTotal
	else:
		teamScores[visTeam] = visTotal

sorted_x = sorted(teamScores.items(), key=operator.itemgetter(1), reverse=True)
numTeams = len(sorted_x) + 1

for i in range(numIterations):
	sorted_y = [a for (a, _) in sorted_x]

	for game in games:
		age = float(game["Age"])
		if age > weeks: #used to be 14
			age = weeks + 2
		age /= float(weeks)
		result = getOutcome(game)
		place = sorted_y.index(result[1]) + 1
		teamScores[result[0]] += ((numTeams - place) ** 3) * age
		place1 = sorted_y.index(result[0]) + 1
		teamScores[result[1]] -= (place1 ** 2) * age
	sorted_x = sorted(teamScores.items(), key=operator.itemgetter(1), reverse=True)

for tup in range(numRankings):
	string = "{}: {}".format(tup+1, sorted_x[tup][0])
	print(string)

