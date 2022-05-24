"""
Author: Ibrahim Al-Hindi
Purpose: FIT9136 Assignment 2
Date created: 12/5/2021
Date last edited: 21/05/2021

This python script takes a file that contains a collection of chess games and their respective moves, then goes through
several methods to ultimately plot the top 10 most common first moves by either white or black
"""

#import required libraries
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#create ChessGame class
class ChessGame:
    
    #create constructor
    def __init__(self):
        
        #take filename as input and validate that file exists in directory
        while True:
            self.filename = input("Please enter file name (don't forget to add format (such as .pgn) at the end of the name)")                                                            
            #check if file is present in directory
            if self.filename in os.listdir():
                break                             
            else:
                print("This file name does not exist in the current directory, please enter another file name")        
        
        #initialize tuple that will be used later to hold the two dataframes
        self.df_tuple = ()
    
    #task 3.2: remove metadata then write each game as a separate string in output file
    def filter_games(self):        
        
        #read input file
        with open(self.filename, "r") as games:                                                                       
            #read the games as a list
            games_list = games.readlines()
        
        #initialize 2 lists: one for each game, and one for all the games
        all_games = []
        new_game = []

        #exclude metadata (lines that begin with "["). Each game is separated by empty lines from the next game,
        #therefore if the next line is not empty, it is still part of the same game and that line will be appended to the
        #same "new_game" list
        for line in games_list:
            if line[0] != "[" and line[0] != "\n":
                new_game.append(line)                            
            #if the line is an empty line, the current game is finished
            else:                                                                   
                #check for empty new_game lists that were created as a result of some empty lines
                if len(new_game) != 0:                                        
                    #convert the game list into a string
                    game_str = "".join(new_game)
                    #split individual moves in the game and put inside a list
                    moves_list = game_str.split()
                    #remove the last item in the list which is the score of the game
                    moves_list.pop()
                    #rejoin the list into one string
                    clean_game = " ".join(moves_list)
                    #append each clean game to the clean_games list
                    all_games.append(clean_game)
                    #re-initialize "new_game" and continue to the next line
                    new_game = []
                    continue
                        
        #create output file
        with open("game_string.txt", "w") as out_file:                        
            #write each game to the output file. The last game is separated because we don't want to create an empty line at
            #the end
            for game in all_games[:-1]:
                out_file.write(game + "\n")                

            out_file.write(all_games[-1])
         
    #task 3.3: for each game, separate white moves and black moves into their own files
    def separate_moves(self):
        
        try:
            #read file generated from filter_games method
            with open("game_string.txt", "r") as filtered_games:                
                #read the games as a list
                list_games = filtered_games.readlines()

            #create new folder "game_moves" that will contain the moves files
            os.mkdir("game_moves")

            for game in range(len(list_games)):                                               
                #split individual moves in the game and put inside a list
                split_game = list_games[game].split()                                                               
                #create a new file for white moves and another file for black moves
                with open(f"game_moves/{game+1}w.txt", "w") as w_moves:
                    with open(f"game_moves/{game+1}b.txt", "w") as b_moves:                                                                        
                        #if index of a move in a game is even, write to the white file; if odd, write to the black file
                        for move in range(len(split_game)):                            
                            if move % 2 == 0:                                                                
                                #use regex to remove count of move (e.g. "1." from 1.e3)
                                split_game[move] = re.sub(r"^\d+.", "", split_game[move])
                                w_moves.write(split_game[move] + " ")                                                        
                            else:
                                b_moves.write(split_game[move] + " ")
            
        except FileNotFoundError:
            print("Please run filter_games method first")            
        except FileExistsError:
            print("Moves already separated into their own files. Please delete 'game_moves' folder first then run again")
            
    #task 3.4: create a tuple that contains two dataframes that counts the first moves for white and black separately
    def first_move_counts(self):
        
        try:
            #intitialize dictionaries to count moves for white and black
            w_firsts = {}
            b_firsts = {}
            
            #iterate over moves files in folder created in task 3.3
            for f in os.listdir("game_moves/"):
                #open file
                with open(f"game_moves/{f}", "r") as file:
                    #read the moves line
                    file_read = file.readline()                                    
                #split the moves and insert in a list
                file_split = file_read.split()                
                #check if a player of any game made no moves and that game file is therefore empty
                if len(file_split) != 0:                    
                    #obtain first move from the game
                    move = file_split[0]                    
                    #if "w" is in the file name, then it is a white move, if "b" is in the file name, then it is a black move
                    if "w" in f:                        
                        #if the move is already in the dictionary, increase the count by 1. If not, create the move as an item
                        #and assign count to be 1
                        if move in w_firsts:
                            w_firsts[move] += 1
                        else:
                            w_firsts[move] = 1                                        
                    elif "b" in f:
                        if move in b_firsts:
                            b_firsts[move] += 1
                        else:
                            b_firsts[move] = 1   

            #the dictionaries created are:
            #white: {'e4': 828,'Nf3': 186,'d4': 906,'c4': 179,'e3': 3,'d3': 1,'Nc3': 1,'g3': 3,'b3': 2}
            #black: {'e5': 246,'c5': 504,'d5': 287,'Nf6': 786,'e6': 113,'g6': 57,'d6': 30,'f5': 19,'c6': 56,'Nc6': 6,'b6': 3,'b5': 1}
            
            #using the dictionaries created, create a list of the moves, and another list of the counts for each move, for both white and black.
            #these lists will be used to create the dataframes
            w_first_moves = list(w_firsts.keys())
            w_counts = list(w_firsts.values())
            b_first_moves = list(b_firsts.keys())
            b_counts = list(b_firsts.values())
            
            #create two dataframes: one for white moves and one for black moves      
            w_df = pd.DataFrame({"Moves": w_first_moves, "Counts": w_counts, "Color": "White"}, index = list(range(1,len(w_first_moves)+1)))
            b_df = pd.DataFrame({"Moves": b_first_moves, "Counts": b_counts, "Color": "Black"}, index = list(range(1,len(b_first_moves)+1)))
            
            #insert dataframes into a tuple
            self.df_tuple = (w_df, b_df)
            
            #print and return tuple
            print(self.df_tuple[0], "\n", self.df_tuple[1])
            return self.df_tuple
        
        except:
            print("Please run separate_moves method first")
    
    #task 3.5 plot the top ten most common moves and specify whether it's by white or black
    def top_moves_plot(self):
        
        try:
            #concactenate both data frames into one data frame
            df_full = pd.concat([self.df_tuple[0], self.df_tuple[1]])
            #sort the data frame by counts in descending order
            df_full_sorted = df_full.sort_values(by = "Counts", ascending = False)
            #retrieve top ten moves only
            top_ten = df_full_sorted.head(10)

            #plot graph
            plt.bar(x = "Moves", height = "Counts", data = top_ten, color = "Color")
            plt.title("Most Common First Moves")            
            #change background colour
            #inspiration from https://stackoverflow.com/questions/14088687/how-to-change-plot-background-color
            ax = plt.gca()
            ax.set(facecolor = "grey")            
            #manually create legend
            #inspiration from https://stackoverflow.com/questions/39500265/manually-add-legend-items-python-matplotlib
            white_patch = mpatches.Patch(color = "white", label = "White moves")
            black_patch = mpatches.Patch(color = "black", label = "Black moves")
            plt.legend(handles=[white_patch, black_patch])            
            plt.show()

            #print my understanding of the graph
            print("The graph shows that white only plays a pawn to d4 or e4 as a first move the overwhelming majority of the time, while black in fact plays a knight to f6 a great majority of the time")
            
        except:
            print("Please run first_move_counts method first")

#create instance of ChessGame (try to pass incorrect file name)
demo = ChessGame()

#illustrate error handling
demo.top_moves_plot()

#illustrate error handling
demo.first_move_counts()

#illustrate error handling
demo.separate_moves()

#call filter_games method
demo.filter_games()

#call separate_moves method
demo.separate_moves()

#illustrate error handling
demo.separate_moves()

#call first_move_counts method
demo.first_move_counts()

#call top_moves_plot method
demo.top_moves_plot()