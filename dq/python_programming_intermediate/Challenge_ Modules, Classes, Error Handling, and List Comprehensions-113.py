## 2. Introduction to the Data ##

import csv
file = open('nfl_suspensions_data.csv', 'r')
data = csv.reader(file)
nfl_suspensions = list(data)[1:]

years = {}
for row in nfl_suspensions:
    row_year = row[5]
    if row_year in years:
        years[row_year] +=1
    else:
        years[row_year] = 1
print(years)

## 3. Unique Values ##

team = [x[1] for x in nfl_suspensions]
unique_teams = set(team)
game = [x[2] for x in nfl_suspensions]
unique_games = set(game)
print(unique_teams)
print(unique_games)

## 4. Suspension Class ##

class Suspension():
    def __init__(self, x):
        self.name = x[0]
        self.team = x[1]
        self.games = x[2]
        self.year = x[5]
third_suspension = Suspension(nfl_suspensions[2])

## 5. Tweaking the Suspension Class ##

class Suspension():
    def __init__(self,row):
        self.name = row[0]
        self.team = row[1]
        self.games = row[2]
        try:
            self.year = int(row[5])
        except Exception:
            self.year = 0
    def get_year(self):
        return(self.year)
    
missing_year = Suspension(nfl_suspensions[22])
twenty_third_year = missing_year.get_year()