import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import threading
from functools import partial
import tournament
import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class SimulationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IPL Simulator")
        self.geometry("1000x700")
        
       
        self.create_widgets()
        self.running = False
        self.current_figure = None
        
    
        self.console_redirect = ConsoleRedirect(self.console)
        sys.stdout = self.console_redirect
        sys.stderr = self.console_redirect

        self.sim = tournament.ipl_tournament_simulator()

    def create_widgets(self):
      
        top_frame = ttk.Frame(self)
        top_frame.pack(pady=10, fill=tk.X)
        
      
        self.sim_label = ttk.Label(top_frame, text="Number of Simulations:")
        self.sim_label.pack(side=tk.LEFT, padx=10)
        self.sim_entry = ttk.Entry(top_frame, width=10)
        self.sim_entry.pack(side=tk.LEFT)
        self.sim_entry.insert(0, "10000")
        
   
        self.team_label = ttk.Label(top_frame, text="Favorite Team:")
        self.team_label.pack(side=tk.RIGHT, padx=10)
        self.team_var = tk.StringVar()
        self.team_combobox = ttk.Combobox(top_frame, textvariable=self.team_var, 
                                         values=["--Select Team--", "GT","CSK","RCB","MI","LSG","RR","KKR","SRH","DC","PBKS"],)
        self.team_combobox.current(0)
        self.team_combobox.pack(side=tk.RIGHT)
        
  
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10, fill=tk.X)
        
  
        self.buttons = {
            'top2': ttk.Button(button_frame, text="Top 2 Probability", 
                              command=partial(self.run_in_thread, self.top2_probability)),
            'playoff': ttk.Button(button_frame, text="Play Off Probability", 
                                command=partial(self.run_in_thread, self.playoff_probability)),
            'best_chances': ttk.Button(button_frame, text="Best Chances of My Team", 
                                     command=partial(self.run_in_thread, self.best_chances)),
            'scenarios': ttk.Button(button_frame, text="Find Possible Scenarios", 
                                  command=partial(self.run_in_thread, self.find_scenarios))
        }
        
        for i, btn in enumerate(self.buttons.values()):
            btn.grid(row=0, column=i, padx=5, sticky=tk.NSEW)
            button_frame.columnconfigure(i, weight=1)
        
        self.figure_frame = ttk.Frame(self)
        self.figure_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = None
        

        self.console = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled')
        self.console.pack(pady=10, fill=tk.BOTH, expand=True)

    def run_in_thread(self, func):
        if not self.running:
            self.running = True
            self.toggle_buttons(False)
            thread = threading.Thread(target=self.wrap_function, args=(func,))
            thread.start()

    def wrap_function(self, func):
        try:
            # Get simulation number and validate
            sim_num = int(self.sim_entry.get())
            # Get selected team and validate
            selected_team = self.team_var.get()

            
            plot_data=func(sim_num, selected_team)
            if plot_data != None:
                self.after(0, self.update_plot, plot_data)
            
        except Exception as e:
            print(f"Error: Please enter a valid number of simulations. {e}")
        finally:
            self.running = False
            self.toggle_buttons(True)

    def update_plot(self, plot_data):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        bars = ax.bar(
            plot_data['teams'], 
            plot_data['probabilities'],
            color=plot_data.get('colors', None)
        )
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height + 0.01,
                f'{height:.2f}',
                ha='center', 
                va='bottom',
                fontsize=8
            )

        ax.set_xlabel('Teams')
        ax.set_ylabel('Probability')
        ax.set_title(plot_data.get('title', ''))
        

        plt.xticks(rotation=45)

        ax.set_ylim((0, 1))
        ax.grid(axis='y')

        fig.tight_layout()
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def toggle_buttons(self, state):
        for btn in self.buttons.values():
            btn.state(['!disabled' if state else 'disabled'])

    # YOUR FUNCTIONS TO INTEGRATE HERE ----------------------------------------
    def top2_probability(self, sim_num, team):

        if  not isinstance(sim_num, int) or sim_num <= 0:
            print("Please enter a valid number of simulations.")
            return
        
        print(f"Running Top 2 Probability with {sim_num} simulations for {team}")
        plot_data= self.sim.top2_probability(sim_num)
        print(plot_data)
        plot_data['title'] = 'Top 2 Probabilities of all Teams'
        return plot_data
    
    def playoff_probability(self, sim_num, team):
        if not isinstance(sim_num, int) or sim_num <= 0:
            print("Please enter a valid number of simulations.")
            return
        print(f"Running Play Off Probability with {sim_num} simulations for {team}")
        plot_data = self.sim.playoff_probability(sim_num)
        plot_data['title'] = 'Play Off Probabilities of all Teams'
        return plot_data
    
    def best_chances(self, sim_num, team):
        if sim_num <= 0 or not isinstance(sim_num, int):
            print("Please enter a valid number of simulations.")
            return
        if team == "--Select Team--":
            print("Please select your favorite team to calculate best chances of your team.")
            return
        print(f"Running Best Chances with {sim_num} simulations for {team}")
        plot_data = self.sim.best_chances(sim_num, team)
        plot_data['title'] = f'Best Chances of {team} to play in Play Offs'
        return plot_data
    
    def find_scenarios(self, sim_num, team):
        if team == "--Select Team--":
            print("Please select your favorite team to find scenarios.")
            return
        print(f"Finding Possible Scenarios for {team}")
        self.sim.find_scenarios( team)
        return None

class ConsoleRedirect(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
    
    def flush(self):
        pass

if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()