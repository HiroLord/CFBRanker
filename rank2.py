from loadData import loadData
import operator
import math

# Ranks the scores into a list
def rankScores(scores):
    return sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

# Adds the teams new score
def addScore(team, score, weight):
    if team in teamScores:
        teamScores[team] = teamScores[team] * (1.0-weight) + score * weight
    else:
        teamScores[team] = score

# Counts number of games a team played, total
def addPlays(game):
    teams = [game["Home Team"]["Team"], game["Vis Team"]["Team"]]
    for team in teams:
        if team in numGames:
            numGames[team] += 1
        else:
            numGames[team] = 1

def printScores(num):
    ranked = rankScores(teamScores)
    for i in range(num):
        print("{}: {}, {:.5f}".format(i+1, ranked[i][0], ranked[i][1]))

games = loadData('wagstatscfb2014.csv')

teamScores = {}
numGames = {}

for game in games:
    addPlays(game)
    home = game["Home Team"]
    away = game["Vis Team"]

    weight = 1.0/game["Week"]

    homeTeam = home["Team"]
    awayTeam = away["Team"]

    homeTotal = 0
    awayTotal = 0

    diff = int(home["Score"]) - int(away["Score"])
    if diff > 0:
        homeTotal = 100
        awayTotal = 0
    else:
        homeTotal = -10
        awayTotal = 110

    addScore(homeTeam, homeTotal, weight)
    addScore(awayTeam, awayTotal, weight)

for t in numGames:
    if numGames[t] < 11:
        del teamScores[t]

printScores(25)
teamScores2 = teamScores.copy()

for team in teamScores:
    teamScores[team] = 0.5;

print("Re ranking...")
for i in range(100):
    for game in games:
        home = game["Home Team"]
        away = game["Vis Team"]

        week = game["Week"]
        if (week > 15):
            week = 15
        weight = week/200.0
        rankWeight = 0

        homeTeam = home["Team"]
        awayTeam = away["Team"]

        if homeTeam not in teamScores2 or awayTeam not in teamScores2:
            continue

        diffPercent = (teamScores2[homeTeam] - teamScores2[awayTeam]) / 100.0
        homeScore = int(home["Score"])
        awayScore = int(away["Score"])
        diffScore = homeScore - awayScore

        if diffScore > 0:
            homeTotal = 100
            awayTotal = 0
            if diffPercent > 0:
                rankWeight = 1.0 - diffPercent
            else:
                rankWeight = -1.0 * diffPercent
        else:
            homeTotal = 0
            awayTotal = 100
            if diffPercent > 0:
                rankWeight = diffPercent
            else:
                rankWeight = 1.0 + diffPercent
        scoreWeight = abs(diffScore) / (float(homeScore + awayScore) / 2.0)
        if (scoreWeight > 1.0):
            scoreWeight = 1.0
        addScore(homeTeam, homeTotal, weight * rankWeight * scoreWeight)
        addScore(awayTeam, awayTotal, weight * rankWeight * scoreWeight)
    teamScores2 = teamScores.copy()
print("Done!")
printScores(25)
