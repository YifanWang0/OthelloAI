#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Yifan Wang yw3486
"""

import random
import sys
import time
import math

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    (p1_score,p2_score) = get_score(board)
    if color == 1:
        return p1_score - p2_score
    if color == 2:
        return p2_score - p1_score

############ MINIMAX ###############################

def minimax_min_node(board, color, level):
    opp_color = 1 if color==2 else 2
    
    if len(get_possible_moves(board,opp_color)) == 0 or level > 2:
        return compute_utility(board, color)
    else:
        lst = []
        for c in get_possible_moves(board,opp_color):
            lst.append(minimax_max_node(play_move(board,opp_color,c[0],c[1]),color, level+1))
        return min(lst)

def minimax_max_node(board, color, level):
    if len(get_possible_moves(board,color)) == 0 or level > 2:
        return compute_utility(board, color)
    else:
        lst = []
        for c in get_possible_moves(board,color):
            lst.append(minimax_min_node(play_move(board,color,c[0],c[1]),color, level+1))
        return max(lst)
    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    opp_color = 1 if color==2 else 2
    
    length = len(board)
    lst = []
    list_of_corners = [(0,0), (length-1,0), (0,length-1), (length-1,length-1)]
    list_of_nextToCorners = [(0,1),(1,0),(0,length-2),(1,length-1),(length-2,0),(length-1,1),(length-2,length-1),(length-1,length-2)]
    nextMoves = get_possible_moves(board,color)
    for c in nextMoves:  
        if c in list_of_corners:
            return c       
        if c not in list_of_nextToCorners or set(nextMoves).issubset(set(list_of_nextToCorners)):
            new_board = play_move(board,color,c[0],c[1])
            value = minimax_min_node(new_board,color,0)        
            lst.append((value,c))
    value, move = max(lst)
    return move

############ ALPHA-BETA PRUNING #####################
    
#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level): 
    opp_color = 1 if color==2 else 2
    
    if len(get_possible_moves(board,opp_color)) == 0 or level > 3:
        return compute_utility(board, color)   
    else:        
        for c in get_possible_moves(board,opp_color):
            new_board = play_move(board,opp_color,c[0],c[1])
            value = alphabeta_max_node(new_board,color,-math.inf,beta,level+1)
            if value < beta: 
                beta = value
            if alpha > beta:
                return beta
        return beta


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level):
    if len(get_possible_moves(board,color)) == 0 or level > 3:
        return compute_utility(board, color) 
    else: 
        for c in get_possible_moves(board,color):
            new_board = play_move(board,color,c[0],c[1])
            value = alphabeta_min_node(new_board,color,alpha,math.inf,level+1)
            if value > alpha:
                alpha = value   
            if beta > alpha:
                return alpha
        return alpha
        
def select_move_alphabeta(board, color):     
    
    lst = []
    for c in get_possible_moves(board,color):                   
        new_board = play_move(board,color,c[0],c[1])
        value = alphabeta_min_node(new_board,color,-math.inf,math.inf,0)        
        lst.append((value,c))
    value, move = max(lst)
    return move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Better Than Randy AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej = select_move_minimax(board, color)
            #movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
