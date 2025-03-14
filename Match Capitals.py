import pandas as pd
import tkinter as tk
from tkinter import ttk
import requests
from io import StringIO
import tkinter.messagebox as msg
class CapitalsMatcher:
    def __init__(self, master, difficulty):
        self.master = master
        self.difficulty = difficulty
        self.master.title("Capitals Matcher")
        self.create_lists(difficulty)
    def create_lists(self, difficulty):
        self.difficulty = difficulty
        url = "https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Countries/Popular_pages"
        r = requests.get(url)
        html_content1 = StringIO(r.text)
        df_list = pd.read_html(html_content1)
        self.count = 0
        #The list of countries is the first table of the above URL. This is a list of country-related pages which arranged in popularity.
        #Just because this list features an item, it does not mean it is an actual country. Just related to countries.
        self.df1 = pd.DataFrame(df_list[0])
        url2 = "https://en.wikipedia.org/wiki/List_of_national_capitals"
        r2 = requests.get(url2)
        html_content2 = StringIO(r2.text)
        df_list_2 = pd.read_html(html_content2)
        
        #The list of countries and the capital cities is the first table of the above URL.
        self.df2 = pd.DataFrame(df_list_2[1])
        temp_df = self.df2.copy()
        temp_df = temp_df[["Country/Territory"]]

        #This is to ensure that all of the country-related pages in the popularity table are in fact countries and not some other details related to it.
        self.df1 = pd.merge(self.df1, temp_df, how="inner",left_on="Page title",right_on="Country/Territory")
        #self.df1.drop(columns=["Country/Territory"], inplace=True)
        self.df1 = self.df1[["Page title"]]
        self.create_widgets(self.difficulty)
    def create_widgets(self, difficulty):
        #First creating the labels under which the Treeviews will be installed.
        self.label1 = tk.Label(self.master, text = "Countries")
        self.label1.grid(row=0,column=0)
        self.label2 = tk.Label(self.master, text="Capitals")
        self.label2.grid(row=0, column=2)
        self.tree1 = ttk.Treeview(self.master)
        self.tree1['columns'] = tuple(self.df1.columns)
        #Adding column headers.
        for col in self.df1.columns:
            self.tree1.column(col, anchor="w")
            self.tree1.heading(col, text=col)
        self.tree1['show'] = ''
        if difficulty == "random":
            #Getting a random selection of countries.
            random_country_df = self.df1.sample(5)
        elif difficulty == "easy":
            random_country_df = self.df1.head(5)
        else:
            random_country_df = self.df1.sample(5)
        self.new_df1 = random_country_df.copy()
        for index, row in random_country_df.iterrows():
            self.tree1.insert('', 'end', values=tuple(row))
        self.tree1.grid(row=1, column=0, rowspan=6, padx=(10,0))
        self.match_button = tk.Button(self.master, text="Match Rows", command=self.match_rows)
        self.match_button.grid(row=7, column=1)
        self.tree2 = ttk.Treeview(self.master)
        self.tree2["columns"] = tuple(self.df2.columns)
        self.tree2['show'] = ''
        capitals_df = pd.merge(self.df2, random_country_df, left_on="Country/Territory", right_on="Page title", how="inner")
        capitals_df.drop_duplicates(subset="Country/Territory",inplace=True)
        self.correct_answers = dict(zip(capitals_df["Country/Territory"], capitals_df["City/Town"]))
        capitals_df.drop(columns=["Page title", "Country/Territory", "Notes", "Continent"], inplace=True)
        #capitals_df = capitals_df[capitals_df["City/Town"]]
        self.new_df2 =capitals_df.copy()
        for col in capitals_df.columns:
            self.tree2.column(col, anchor="w")
            self.tree2.heading(col, text=col)
        for index, row in capitals_df.iterrows():
            self.tree2.insert('', 'end', values = tuple(row))
        self.tree2.grid(row=1, column=2, rowspan=6, padx=(0,10))
    def match_rows(self):
        selected_item_1 = self.tree1.selection()
        selected_item_2 = self.tree2.selection()
        if len(selected_item_1) == 0 and len(selected_item_2) == 0:
            msg.showinfo(title="No selection", message="Neither city nor country have been selected.")
        elif len(selected_item_1) == 0 or len(selected_item_2) == 0:
            if len(selected_item_1) ==0:
                msg.showinfo(title="No country selected", message="Country has not been selected.")
            else:
                msg.showinfo(title="No city selected", message="City has not been selected.")
        else:
            row_index_1 = int(selected_item_1[0][1:])
            row_index_2 = int(selected_item_2[0][1:])
            self.tree1.delete(selected_item_1)
            self.tree2.delete(selected_item_2)
            if self.count == 0:
                self.chosen_answers = {self.new_df1.iloc[row_index_1 - 1]["Page title"] : self.new_df2.iloc[row_index_2 - 1]["City/Town"]}
            else:
                self.chosen_answers[self.new_df1.iloc[row_index_1 - 1]["Page title"]] = self.new_df2.iloc[row_index_2 - 1]["City/Town"]
            self.count = self.count + 1
            self.check_if_done()
    def check_if_done(self):
        if not self.tree1.get_children():
            print(self.correct_answers)
            print(self.chosen_answers)
            match_count = 0
            for key in self.chosen_answers:
                if self.chosen_answers[key] == self.correct_answers[key]:
                    match_count += 1
            if match_count == len(self.correct_answers):
                success_msg = msg.askquestion(title="Victory!", message="You have managed to get all your answers correct. Well done! Do you want to do it again?")
                if success_msg == "yes":
                    self.create_lists("random")
                else:
                    self.master.destroy()
            else:
                fail_msg = msg.askquestion(title="Defeat!", message="You got only " + str(match_count) + " correct out of " + str(len(self.correct_answers)) + ". The correct answers are: " + str(self.correct_answers) + ". Do you want to retry?")
                if fail_msg == "yes":
                    self.create_lists("random")
                else:
                    self.master.destroy()
class DifficultySelection:
    def __init__(self, master):
        self.master = master
        self.master.title("Difficulty Selector")
        self.create_buttons()
    def create_buttons(self):
        self.random_button = tk.Button(self.master, text="random", command=lambda: self.start_main_app("random"))
        self.random_button.grid(row=1,column=0)

        self.easy_button = tk.Button(self.master, text="easy", command=lambda: self.start_main_app("easy"))
        self.easy_button.grid(row=2,column=0)

        self.medium_button = tk.Button(self.master, text="medium", command=lambda: self.start_main_app("medium"))
        self.medium_button.grid(row=3,column=0)

        self.hard_button = tk.Button(self.master, text="hard", command=lambda: self.start_main_app("hard"))
        self.hard_button.grid(row=4,column=0)
        self.quit_button = tk.Button(self.master, text="quit", command=self.master.destroy)
        self.quit_button.grid(row=5,column=0)

    def start_main_app(self, difficulty):
        self.master.destroy()
        root = tk.Tk()
        app = CapitalsMatcher(root, difficulty)
        root.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    app = DifficultySelection(root)
    root.mainloop()