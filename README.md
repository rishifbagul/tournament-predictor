# Tournament Predictor Application

This application simulates and predicts outcomes for a sports tournament (such as IPL) based on the current team standings and remaining schedule. It provides probability-based insights to help you understand your team's chances of qualifying for the playoffs or finishing in the top positions.

## Features

The application offers four main options:

1. **Top Two Probability**
   - Calculates the probability for each team to finish in the top two positions at the end of the league stage.

2. **Playoff Probability**
   - Calculates the probability for each team to finish in the top four (i.e., qualify for the playoffs).

3. **Best Chance**
   - Select your favorite team. The application calculates the probability of your team qualifying for the playoffs, assuming it wins all its remaining matches with a high run rate.

4. **Find Scenario**
   - Select your favorite team. The application finds and displays a possible scenario (if any) where your team can still qualify for the playoffs. It tries all possible outcomes, including draws, to find combinations where your team qualifies.

For the first three options, you will be prompted to select the number of simulations to run. Probabilities are calculated after all simulations are completed.

## Required Files

- `teams.csv`: Update this file with the current standings and statistics for each team.
- `schedule.csv`: Update this file with the remaining matches in the tournament. This file also includes the probability of each match outcome, which you can adjust as needed.

**Both files must be in the same folder as the application.**

## How to Use

### Running the Application (Python)
1. Ensure you have Python installed.
2. Place `IPL_Application.py`, `teams.csv`, and `schedule.csv` in the same directory.
3. Run the application:
   ```bash
   python IPL_Application.py
   ```
4. Follow the on-screen prompts to select an option and provide required inputs.

### Creating and Using the .exe File
1. Use a tool like `pyinstaller` to create an executable:
   ```bash
   pyinstaller --onefile IPL_Application.py
   ```
2. The `.exe` file will be created in the `dist` folder.
3. Place `teams.csv` and `schedule.csv` in the same folder as the `.exe` file.
4. Double-click the `.exe` file or run it from the command line to start the application.

### Download preBuild Exe File
**Instructions:**
1. Download the `.exe` file and place it in a folder.
2. Ensure `teams.csv` and `schedule.csv` are in the same folder as the `.exe` file.
3. Double-click the `.exe` file to start the application.


## Notes
- Always update `teams.csv` and `schedule.csv` with the latest information before running the application.
- You can modify the match probabilities in `schedule.csv` to reflect your own predictions or expert opinions.

---

**Enjoy predicting your tournament outcomes!**
