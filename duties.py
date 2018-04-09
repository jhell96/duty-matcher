"""
Josh Hellerstein
April 6, 2018
Duties Assignment Problem
"""

import numpy as np
from scipy.optimize import linear_sum_assignment

class Brother():
    name = None
    grade = None
    year = -1
    ranking = []
    is_upperclassmen = None

    def __init__(self, name, year, ranking):

        name = name.lower()
        year = int(year)

        self.name = name
        self.year = year
        self.ranking = ranking

        if year == 1:
            self.grade = 'freshman'
            self.is_upperclassmen = False
        elif year == 2:
            self.grade = 'sophomore'
            self.is_upperclassmen = False
        elif year == 3:
            self.grade = 'junior'
            self.is_upperclassmen = True
        elif year == 4:
            self.grade = 'senior'
            self.is_upperclassmen = True

class Duty():
    name = None
    num_people = -1
    upper_and_lower = None

    def __init__(self, name, number_of_people, upperclassmen_and_lower_required=False):
        self.name = name
        self.num_people = number_of_people
        self.upper_and_lower = upperclassmen_and_lower_required

class Matcher():
    duties = []
    jobs = []
    brothers = []
    selected_brothers = []
    quota = []
    matches = {}

    def __init__(self, duties, brothers, year_quota=[0,0,0,0]):
        self.duties = duties
        self.brothers = brothers
        self.quota = year_quota

    def select_brothers(self):
        """ Selects brothers to be chosen for duty.
            Chooses randomly from freshman, sophomore, juniors, and then seniors,
            unless there's a quota on number of people per year, or a duty requires
            an upperclassmen.
        """ 

        # creates bins by year
        stack = [[],[],[],[]]

        for b in self.brothers:
            stack[b.year-1].append(b)

        for year in stack:
            np.random.shuffle(year)

        # determines number of upperclassmen required
        num_upperclassmen_required = 0
        for duty_id, duty in enumerate(self.duties):
            if duty.upper_and_lower:
                # majority upper if split required
                num_upperclassmen_required += (duty.num_people+1) // 2 

            # creates jobs from duties
            for i in range(1, duty.num_people+1):
                job = (duty.name+"_"+str(i), duty_id)
                self.jobs.append(job)

        selected_brothers = []

        # first fulfill quota required per year
        for i,q in enumerate(self.quota):
            for j in range(q):
                selected_brothers.append(stack[i].pop())
                if i+1 >= 3:
                     num_upperclassmen_required -= 1

        # fulfill upperclassmen requirement
        for y in [3, 4]:
            for i in range(num_upperclassmen_required):
                if len(stack[y-1]) > 0:
                    selected_brothers.append(stack[y-1].pop())
                    num_upperclassmen_required -= 1
                else:
                    break

        # else pick people starting from freshman
        q = []
        for i in stack:
            q.extend(i)
        selected_brothers.extend(q[:len(self.jobs)-len(selected_brothers)])

        self.selected_brothers = selected_brothers

    def match_brothers(self):
        """ Matches brothers, starting with senior's preferences, then junior...
            Does so in 4 rounds, where seniors go first.
        """
        for y in [4, 3, 2, 1]:
            assign_brothers = []
            for b in self.selected_brothers:
                if b.year == y:
                    assign_brothers.append(b)
            self._match(assign_brothers)


    def _match(self, brothers):
        """Find's the optimal assignment by minimizing the total cost.
            The total cost of an assignment is the sum of the ranks of each job
            each brother is assigned to.
        
        Args:
            brothers (List): List of brothers in a given year to be matched
        """
        cost_matrix = np.zeros((len(brothers), len(self.jobs)))
        
        # cost of matching brother b to job is their ranking of that job
        for i,b in enumerate(brothers):
            for j,job in enumerate(self.jobs):
                cost_matrix[i,j] = b.ranking[job[-1]]

        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        # store matches in self.matches
        for i in range(len(row_ind)):
            elem = self.jobs.pop(col_ind[i])
            self.matches[elem] = brothers[row_ind[i]]


    def run(self):
        self.select_brothers()
        self.match_brothers()
        return {x[0]:self.matches[x].name for x in self.matches}

if __name__ == '__main__':
    duties = [Duty('inside_door', 1), Duty('outside_door', 2, True), Duty('bar', 2)]

    brothers = [Brother('josh', 3, [2, 3, 1]), Brother('noah', 1, [3, 2, 1]), Brother('andres', 2, [3, 2, 1])]

    m = Matcher(duties, brothers)
    res = m.run()
    print(res)
