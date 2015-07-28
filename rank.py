import operator
from datetime import date

f = open('wagstatscfb2014.csv', 'r')
games = []
headers = [x.strip() for x in f.readline().split(',')]
headers = headers[2:18]
line = f.readline()
start = date(2014, 8, 26)
weeks = 14.0
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
	for j in range(len(headers)):
		game["Home Team"][headers[j]] = line[j+19].strip()
	line = f.readline()
	games.append(game)
f.close()

teamScores = {}

for game in games:
	age = game["Age"]
	winMult = 1
	loseMult = 1
	if (age > 14):
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
	if diff > 0:
		homeTotal += 100 * age * winMult
		visTotal -= 50 * age * loseMult
	else:
		homeTotal -= 60 * age * winMult
		visTotal += 110 * age * loseMult
	
	if homeTeam in teamScores:
		teamScores[homeTeam] += homeTotal
	else:
		teamScores[homeTeam] = homeTotal

	if visTeam in teamScores:
		teamScores[visTeam] += visTotal
	else:
		teamScores[visTeam] = visTotal

def getOutcome(game):
	home = game["Home Team"]
	vis = game["Vis Team"]
	homeTeam = home["Team"]
	visTeam = vis["Team"]
	homeScore = int(home["Score"])
	visScore = int(vis["Score"])
	if (homeScore > visScore):
		return (homeTeam, visTeam)
	else:
		return (visTeam, homeTeam)

sorted_x = sorted(teamScores.items(), key=operator.itemgetter(1), reverse=True)
numTeams = len(sorted_x)

for i in range(800):
	sorted_y = [a for (a, _) in sorted_x]

	for game in games:
		age = float(game["Age"])
		if age > 14:
			age = 16
		age /= 14.0
		result = getOutcome(game)
		loserScore = [item for item in sorted_x if item[0] == result[1]]
		place = sorted_y.index(result[1])
		teamScores[result[0]] += (numTeams - place) * 20 * age
		place1 = sorted_y.index(result[0])
		teamScores[result[1]] -= place1 * 15 * age
	sorted_x = sorted(teamScores.items(), key=operator.itemgetter(1), reverse=True)

for tup in range(30):
	string = "{}: {} {:.0f}".format(tup+1, sorted_x[tup][0], sorted_x[tup][1])
	print(string)
#input()
