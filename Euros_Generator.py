
# importing the required module
import random
from itertools import zip_longest

# Method to carry out 

def generate_all_teams(names):

    # list of items
    teams = ['Turkey',
            'Italy',
            'Wales',
            'Switzerland',
            'Denmark',
            'Finland',
            'Belgium',
            'Russia',
            'Netherlands',
            'Ukraine',
            'Austria',
            'North Macedonia',
            'England',
            'Croatia',
            'Scotland',
            'Czech Republic',
            'Spain',
            'Sweden',
            'Poland',
            'Slovakia',
            'Hungary',
            'Portugal',
            'France',
            'Germany']

    lads_draw = {name: [] for name in names}    # Convert name to dictionary with empty list for teams

    number_of_teams = int(len(teams)/len(names))    # Teams divided by number of players, rounded down
    remainder = int(len(teams)%len(names))          # Here we have the modulus (remainder) of the division above

    if len(teams) < len(names):

        print('More players than teams')

    else:

        teams_spread = [a + b for a, b in zip_longest([number_of_teams]*len(names), [1]*(remainder), fillvalue=0)]
        random.shuffle(teams_spread)

        lads_draw_count = {names[i]: teams_spread[i] for i in range(len(names))}

        for i in range(0, len(names)):

            name_pulled = random.choice(names)
            names.remove(name_pulled)

            teams_pulled = random.sample(teams, lads_draw_count[name_pulled])
            for team in teams_pulled:
                teams.remove(team)

            lads_draw[name_pulled].extend(teams_pulled)

    print(lads_draw)
        
generate_all_teams(['Adam','Darsh','Greg','Kenneth','Josh'])
generate_all_teams(['Adam','Darsh','Greg','Kenneth','Josh','Matt','Nav','Rob', 'John'])
print(remainder)

# Method to generate one team per person

def generate_team(name):
    if len(Lads[name]) >= 3:
        print("This lad has enough teams")
    else:
        elem = random.choice(teams) # Define randomly drawn team
        teams.remove(elem) # Remove the ream from the list

        Lads[name].append(elem) # Add the team to the name

def repeat_fun(times, generate_team, *args):
    for i in range(times): generate_team(*args)

repeat_fun(3, generate_team, 'Adam')
repeat_fun(3, generate_team, 'Darsh')
repeat_fun(3, generate_team, 'Greg')
repeat_fun(3, generate_team, 'Josh')
repeat_fun(3, generate_team, 'Matt')
repeat_fun(3, generate_team, 'Nav')
repeat_fun(3, generate_team, 'Rob')
repeat_fun(3, generate_team, 'Kenneth')

print(Lads)
