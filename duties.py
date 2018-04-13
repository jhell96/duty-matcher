"""
Josh Hellerstein
April 6, 2018
Duties Assignment Problem
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
import content


class Brother():
    name = None
    grade = None
    email = None
    year = -1
    ranking = []
    is_upperclassmen = None

    def __init__(self, name, year, email, ranking):

        name = name.lower()
        year = int(year)
        email = email.lower()

        self.name = name
        self.year = year
        self.ranking = ranking
        self.email = email

        if year == 1:
            self.grade = 'freshman'
            self.is_upperclassmen = False
        elif year == 2:
            self.grade = 'sophomore'
            self.is_upperclassmen = True
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
    auto_assign_jobs = []
    brothers = []
    selected_brothers = []
    quota = []
    matches = {}

    def __init__(self, duties, brothers, year_quota=[0, 0, 0, 0]):
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
        stack = [[], [], [], []]

        for b in self.brothers:
            stack[b.year-1].append(b)

        for year in stack:
            np.random.shuffle(year)

        # jobs to force upperclassmen into
        self.auto_assign_jobs = []

        # determines number of upperclassmen required
        num_upperclassmen_required = 0
        for duty_id, duty in enumerate(self.duties):
            if duty.upper_and_lower:
                # majority upper if split required
                num_upperclassmen_required += (duty.num_people+1) // 2

                # gets jobs to autoassign upperclassmen
                for i in range(1, ((duty.num_people+1) // 2) + 1):
                    job = (duty.name+"_"+str(i), duty_id)
                    self.auto_assign_jobs.append(job)

            # creates jobs from duties
            for i in range(1, duty.num_people+1):
                job = (duty.name+"_"+str(i), duty_id)
                self.jobs.append(job)

        selected_brothers = []

        # first fulfill quota required per year
        for i, q in enumerate(self.quota):
            for j in range(q):
                selected_brothers.append(stack[i].pop())

                # if upperclassmen
                if i+1 >= 2:
                    num_upperclassmen_required -= 1

        # fulfill upperclassmen requirement
        for y in [2, 3, 4]:
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
            self._match(assign_brothers, y)

    def _match(self, brothers, year):
        """Find's the optimal assignment by minimizing the total cost.
            The total cost of an assignment is the sum of the ranks of each job
            each brother is assigned to.

        Args:
            brothers (List): List of brothers in a given year to be matched
        """
        cost_matrix = np.zeros((len(brothers), len(self.jobs)))

        # cost of matching brother b to job is their ranking squared of that job
        for i, b in enumerate(brothers):
            for j, job in enumerate(self.jobs):
                cost_matrix[i, j] = (b.ranking[job[-1]]) ** 2

        # if required upperclassmen jobs aren't taken by the last eligible year (2)
        # force into positions by making cost = 0
        if year == 2:
            for auto in self.auto_assign_jobs:
                for i, job in enumerate(self.jobs):
                    if auto == job:
                        cost_matrix[:, i] = 0


        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        # store matches in self.matches
        for i in range(len(row_ind)):
            elem = self.jobs[col_ind[i]]
            self.matches[elem] = brothers[row_ind[i]]

        self.jobs = [v for i, v in enumerate(self.jobs) if i not in col_ind]

    def run(self):
        self.select_brothers()
        self.match_brothers()

        return {x[0]: self.matches[x].name for x in self.matches}


def create_duties(duties_list):
    return [Duty(x[0], int(x[1]), True if x[2].lower() == 'y' else False) for x in duties_list]


def create_brothers(brothers_list):
    return [Brother(" ".join([x[0], x[1]]), int(x[3]), x[2], [int(r) if r != '' else 1 for r in x[4]] ) for x in brothers_list]


if __name__ == '__main__':

    # download content from spreadsheet
    content.get_content()
    d, r = content.parse_content()
    
    # set up
    duties = create_duties(d)
    brothers = create_brothers(r)
    
    # run the matching and display results
    m = Matcher(duties, brothers)
    result = m.run()

    for match in sorted(result):
        print("{0}: {1}".format(match, result[match]))



