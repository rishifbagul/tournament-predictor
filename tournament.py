import math
import random
import copy
import matplotlib.pyplot as plt

class ipl_team:
    def __init__(self, name, color, run_rate=0.0, matches_played=0, wins=0, losses=0, draws=0, points=0):
        self.name = name
        self.color = color
        self.matches_played = matches_played
        self.wins = wins
        self.losses = losses
        self.draws = draws
        self.points = points
        self.run_rate = run_rate

        
    def record_win(self,run_rate=0.0):
        self.wins += 1
        self.points += 2
        self.update_run_rate(run_rate)
        self.matches_played += 1

    def record_loss(self,run_rate=0.0):
        self.losses += 1
        self.update_run_rate(-run_rate)
        self.matches_played += 1

    def record_draw(self):
        self.draws += 1
        self.points += 1
        self.matches_played += 1

    def update_run_rate(self, run_rate):
        # update based on the current run rate and number of matches played
        self.run_rate = ((self.run_rate * (self.matches_played)) + run_rate) / (self.matches_played +1)
    def print_stats(self):
        print(f"Team: {self.name}, Wins: {self.wins}, Losses: {self.losses}, Draws: {self.draws}, Points: {self.points}, Run Rate: {self.run_rate:.2f}")
        






class ipl_match:
    def __init__(self, team1, team2, probabilities):
        self.team1 = team1
        self.team2 = team2
        self.probabilities = probabilities
        self.result = None
        self.winner = None
        self.loser = None
        self.run_rate = None

    def play(self,fixed_outcome=None):
        
        if self.team1.name == fixed_outcome:
            outcome = [self.team1, self.team2, "draw"]
            self.run_rate = 3
        elif self.team2.name == fixed_outcome:
            outcome = [self.team2, self.team1, "draw"]
            self.run_rate = 3
        elif fixed_outcome == "draw":
            outcome = ["draw", self.team1, self.team2]
            self.run_rate = 0
        else:
            outcome = random.choices([self.team1, self.team2, "draw"], weights=self.probabilities)
            self.run_rate = self.approximate_run_rate()

        if outcome[0] == self.team1:
            self.team1.record_win(self.run_rate)
            self.team2.record_loss(self.run_rate)
            self.result = f"{self.team1.name} wins"
            self.winner = self.team1
            self.loser = self.team2

        elif outcome[0] == self.team2:
            self.team2.record_win(self.run_rate)
            self.team1.record_loss(self.run_rate)
            self.result = f"{self.team2.name} wins"
            self.winner = self.team2
            self.loser = self.team1

        else:
            self.team1.record_draw()
            self.team2.record_draw()
            self.result = "draw"
    
    def approximate_run_rate(self):
        # completely random guassian run rate between 0 to 3 with mean 0.5
        run_rate = random.gauss(1.5, 0.4)
        if run_rate < 0.05:
            run_rate = 0.05
        elif run_rate > 3:
            run_rate = 3
        return run_rate

    def print_match_result(self):
        print(f"Match Result: {self.result}")
        if self.result != "draw":
            print(f"Winner: {self.winner.name}, Loser: {self.loser.name}")
        else:
            print("Match was a draw")
        print(f"Run Rate: {self.run_rate:.2f}")
        self.team1.print_stats()
        self.team2.print_stats()


class ipl_tournament:
    def __init__(self):
        self.teams = set()
        self.matches = []
    def add_team(self, team):
        if isinstance(team, ipl_team):
            self.teams.add(team)
        else:
            raise ValueError("Invalid team object")
        
    def schedule_match(self, team1, team2, probabilities):
        team1 = self.find_a_team_by_name(team1)
        team2 = self.find_a_team_by_name(team2)
        if team1 is None or team2 is None:
            # raise ValueError with team1 and team2 names
            raise ValueError(f"Team {team1} or {team2} not found in tournament")
        if team1 == team2:
            raise ValueError("Cannot schedule a match between the same team")
        if len(probabilities) != 3:
            raise ValueError("Invalid probabilities")
        if sum(probabilities) != 1:
            raise ValueError(f"Probabilities must sum to 1 for match between {team1.name} and {team2.name}")
        if probabilities[0] < 0 or probabilities[1] < 0 or probabilities[2] < 0:
            raise ValueError("Probabilities must be non-negative")
        match = ipl_match(team1, team2, probabilities)
        self.matches.append(match)

    def play_tournament(self,favorite=None, fixed_result=None):
        if fixed_result == None:
            for match in self.matches:
                match.play(favorite)
                #match.print_match_result()
        else:
            for i in range(len(self.matches)):
                if fixed_result[i] == 0:
                    self.matches[i].play(self.matches[i].team1.name)
                elif fixed_result[i] == 1:
                    self.matches[i].play(self.matches[i].team2.name)
                elif fixed_result[i] == 2:
                    self.matches[i].play("draw")
                else:
                    self.matches[i].play()
                #match.print_match_result()

    def print_points_table(self):
        # print points table baed on points and run rate
        self.teams = sorted(self.teams, key=lambda x: (x.points, x.run_rate), reverse=True)
        print("Points Table:")
        for team in self.teams:
            print(f"Team: {team.name}, Points: {team.points}, Run Rate: {team.run_rate:.2f}")

    def find_a_team_by_name(self, name):
        for team in self.teams:
            if team.name.lower() == name.lower():
                return team
        return None

    def return_points_table(self):
        # return points table as a list of tuples
        points_table = []
        self.teams = sorted(self.teams, key=lambda x: (x.points, x.run_rate), reverse=True)
        for team in self.teams:
            points_table.append([team.name, team.points, team.run_rate])
        return points_table
    
   



class ipl_simulation:
    def __init__(self, teams, num_simulations, schedule_file):
        self.teams = teams
        self.num_simulations = num_simulations
        self.schedule_file = schedule_file
        self.final_points_table = []
    
    def run_one_simulation(self,favorite=None,fixed_result=None):
        # create a new tournament
        tournament = ipl_tournament()
        for team in self.teams:
            tournament.add_team(copy.deepcopy(team))
        # read the schedule from the file
        with open (self.schedule_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                match,team1, team2, prob1, prob2, prob_draw = line.strip().split(",")
                prob1 = float(prob1)
                prob2 = float(prob2)
                prob_draw = float(prob_draw)
                team1 = team1.strip()
                team2 = team2.strip()
                tournament.schedule_match(team1, team2, [prob1, prob2, prob_draw])

        tournament.play_tournament(favorite=favorite,fixed_result=fixed_result)
        #tournament.print_points_table()
        return tournament.return_points_table()
    
    def run_simulation(self,faviorite=None):
        for i in range(self.num_simulations):
            self.final_points_table.append(self.run_one_simulation(favorite=faviorite))
        
        return self.final_points_table
    def get_total_matches_in_schedule(self):
        # return the total number of matches in the schedule
        with open (self.schedule_file, "r") as f:
            lines = f.readlines()
            return len(lines)
    def get_combination(self,n, num_vars):
        n -= 1  # Convert to 0-based index
        digits = []
        for _ in range(num_vars):
            digits.append(n % 3)
            n = n // 3
        # Reverse the digits to get the correct order
        return tuple(reversed(digits))
    def is_team_in_playoffs(self, team_name,points_table):
        # check if the team is in playoffs
        for i in range(len(points_table)):
            if team_name in [points_table[i][0]]:
                if points_table[i][1] >= points_table[3][1]:
                    return True
        return False
    def find_valid_combination_for_a_favorite_team(self, favorite_team):
        # find the combination of matches that will make the favorite endup in playoffs
        cobination_number = 0
        total_matches = self.get_total_matches_in_schedule()
        for i in range(1, int(math.pow(3, total_matches)+1)):
            combination = self.get_combination(i, total_matches)
            if 2 in combination:
                continue
            result=self.run_one_simulation(fixed_result=combination)
            if self.is_team_in_playoffs(favorite_team, result):
                print(f"Combination {cobination_number}: {combination}")
                print(f"Result: {result}")
                return combination
        for i in range(1, math.pow(3, total_matches)+1):
            combination = self.get_combination(i, total_matches)
            if 2 not in combination:
                continue
            result=self.run_one_simulation(fixed_result=combination)
            if self.is_team_in_playoffs(favorite_team, result):
                print(f"Combination {cobination_number}: {combination}")
                print(f"Result: {result}")
                return combination
        print("No valid combination found")
        return None
class simulation_visualizer:
    def __init__(self, points_table, teams):
        self.points_table = points_table
        self.teams = teams

    def calculate_probabilities_of_team_in_top_x(self, x):
        team_name_and_probabilities = []
        # calculate the probability of each team to end in top x
        for team in self.teams:
            team_name = team.name
            print(f"Calculating probability of {team_name} to end in top {x}")
            count = 0
            for i in range(len(self.points_table)):
                for j in range(x):
                    if team_name in [self.points_table[i][j][0]]:
                        count += 1
                        break
            probability = count / len(self.points_table)
            team_name_and_probabilities.append([team_name, probability])
            print(f"Probability of {team_name} to end in top {x}: {probability:.2f}")
        self.plot_probabilities(team_name_and_probabilities, f"Probability of teams to end in top {x}")
        return team_name_and_probabilities
    
    def plot_probabilities(self,array_of_prob, title):
        sorted_probabilities = sorted(array_of_prob, key=lambda x: x[1], reverse=True)
        teams = [x[0] for x in sorted_probabilities]
        probabilities = [x[1] for x in sorted_probabilities]
        plt.bar(teams, probabilities)
        plt.xlabel('Teams')
        plt.ylabel('Probability')
        plt.title(title)
        plt.xticks(rotation=45)
        plt.ylim(0, 1)
        plt.grid(axis='y')
        #make the bars with team colors
        for i in range(len(teams)):
            plt.bar(teams[i], probabilities[i], color=self.find_team_color(teams[i]))
        # add text on top of the bars
        for i in range(len(teams)):
            plt.text(i, probabilities[i] + 0.01, f"{probabilities[i]:.2f}", ha='center', va='bottom', fontsize=8)
        plt.tight_layout()
        plt.show()
    
    def find_team_color(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team.color
        return None
    
    def print_min_and_max_rank_of_each_team(self):
        # print the min and max rank of each team
        for team in self.teams:
            team_name = team.name
            min_rank = 1000
            max_rank = 0
            for i in range(len(self.points_table)):
                for j in range(len(self.points_table[i])):
                    if team_name in [self.points_table[i][j][0]]:
                        if j < min_rank:
                            min_rank = j
                        if j > max_rank:
                            max_rank = j
            print(f"Team: {team_name}, Min Rank: {min_rank + 1}, Max Rank: {max_rank + 1}")



# teams current stats
gt   = ipl_team(name="GT",   color="teal",    run_rate=1.104,  matches_played=8, wins=6, losses=2, draws=0, points=12)
dc   = ipl_team(name="DC",   color="blue",    run_rate=0.482,  matches_played=9, wins=6, losses=3, draws=0, points=12)
rcb  = ipl_team(name="RCB",  color="red",     run_rate=0.521,  matches_played=10, wins=7, losses=3, draws=0, points=14)
pbks = ipl_team(name="PBKS", color="maroon",  run_rate=0.177,  matches_played=9, wins=5, losses=3, draws=1, points=11)
mi   = ipl_team(name="MI",   color="blue",    run_rate=0.889,  matches_played=10, wins=6, losses=4, draws=0, points=12)
lsg  = ipl_team(name="LSG",  color="skyblue", run_rate=-0.325, matches_played=10, wins=5, losses=5, draws=0, points=10)
kkr  = ipl_team(name="KKR",  color="purple",  run_rate=0.212,  matches_played=9, wins=3, losses=5, draws=1, points=7)
srh  = ipl_team(name="SRH",  color="orange",  run_rate=-1.103, matches_played=9, wins=3, losses=6, draws=0, points=6)
rr   = ipl_team(name="RR",   color="pink",    run_rate=-0.625, matches_played=9, wins=2, losses=7, draws=0, points=4)
csk  = ipl_team(name="CSK",  color="yellow",  run_rate=-1.392, matches_played=8, wins=2, losses=6, draws=0, points=4)

teams = [gt, dc, rcb, pbks, mi, lsg, kkr, srh, rr, csk]

simulator= ipl_simulation(teams, num_simulations=1000, schedule_file="schdule.csv")


# final_rankings = simulator.run_simulation()


# view = simulation_visualizer(final_rankings, teams)
# view.calculate_probabilities_of_team_in_top_x(2)
# view.calculate_probabilities_of_team_in_top_x(4)
# view.print_min_and_max_rank_of_each_team()


simulator.find_valid_combination_for_a_favorite_team("CSK")