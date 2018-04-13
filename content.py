"""
Josh Hellerstein
April 6, 2018
Duties Assignment Problem
"""

import requests


def get_content():
    ranking_url = "http://docs.google.com/spreadsheets/d/1hOTIZJjsX-nFPL_04dN3HHRef0UBYFjYqr9eImStBGc/export?format=csv&id=1hOTIZJjsX-nFPL_04dN3HHRef0UBYFjYqr9eImStBGc&gid=0"
    duties_url = "http://docs.google.com/spreadsheets/d/1hOTIZJjsX-nFPL_04dN3HHRef0UBYFjYqr9eImStBGc/export?format=csv&id=1hOTIZJjsX-nFPL_04dN3HHRef0UBYFjYqr9eImStBGc&gid=875780661"

    r = requests.get(ranking_url)
    d = requests.get(duties_url)

    with open('ranking.csv', 'w') as f:
        f.write(r.text)

    with open('all_duties.csv', 'w') as f:
        f.write(d.text)


def parse_content():

    duties = []
    duties_to_remove = []
    with open('all_duties.csv', 'r') as f:
        _ = f.readline()

        i = 0
        for d in f:
            duty = [x.strip().lower() for x in d.split(",")]

            # if we use the duty this party
            if duty[3] == 'y':
                duties.append((duty[0], int(duty[1]), duty[2]))
            else:
                duties_to_remove.append(i)

            i += 1

    ranking = []
    with open('ranking.csv', 'r') as f:
        _ = f.readline()
        for line in f:
            l = [x.strip().lower() for x in line.split(",")]
            first, last, email, year, avail = l[0], l[1], l[2], l[3], l[4]

            ranks = l[5:-2]
            for i in reversed(duties_to_remove):
                ranks.pop(i)

            # if the brother is available this party
            if avail == 'y':
                ranking.append((first, last, email, int(year), ranks))


    return duties, ranking



