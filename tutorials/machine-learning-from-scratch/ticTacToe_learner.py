# -*- coding: utf-8 -*-

from random import seed, randint
from numpy import add, invert, sign, multiply
import pickle


"""

-- http://www-ekp.physik.uni-karlsruhe.de/~tkuhr/Hauptseminar/Hermann_handout.pdf
-- http://www.ke.tu-darmstadt.de/lehre/archiv/ss07/ki/reinforcement-learning.pdf

-- Author: losj 02.07.2015

Es gibt 2 Files:

Erstes File: tic-tac-toe_learner.py
Dieses hat die Methode playGame(max_game, pickleFileP1, pickleFileP2, trainMode)

Ist trainMode auf true werden zwei Spieler trainiert, welche max_game mal gegeneinander spielen. 
Dabei wird immer abgewechselt, wer beginnen darf. Alle gespielten Situationen werden mit den 
jeweiligen Wahrscheinlichkeiten in die Pickle-Files geschrieben.
Das manuelles Training erfolgt mit…. playGame(10000, "player1", "player2", True)

Ist trainMode auf false wird ein Spiel zwischen zwei Spieler simuliert, welche max_game mal 
gegeneinander spielen. Dabei wird immer abgewechselt, wer beginnen darf.  
Das manuelle Spielen erfolgt mit… playGame(10000, p1, p2, False)

Es existieren weitere Funktionen, die alle durch playGame ausgeführt werden. Die sollten 
selbsterklärend sein. Die Funktion isGameOver könnte man noch leicht „schöner“ machen und die 
Anzahl gespielter Züge mitberücksichtigen.

Zweites File: tic-tac-toe_simulation.py
Dieses Skript führt dient für die Veranschaulichung. Dabei wird ein DefaultGegner definiert, welcher eine 
festgelegtes Training kriegt. Dieser DefaultGegner spielt dann gegen beliebig trainierte Spieler. Diese 
kann man im Array games =[] festlegen.  

"""

#für eine unbekannte Situation die Wahrscheinlichkeiten erstellen
def addStateToStateTable(state, state_table):
# all position where state is 1 a player is allowed to do the next turn on it
# sign(2,1,1,0,0) --> (1,1,1,0,0) 
# invert(1,1,1,0,0) --> (-2,-2,-2,-1,-1)
# add(-2,-2,-2,-1,-1) --> [0,0,0,1,1]
    state_table[state]= multiply(add(invert(sign(state)),2), 1)

# returns index of choosen field
def chooseAction(state, state_table):
#print state," ",state_table[state]
    selection = randint(1, sum(state_table[state]))
    for i in range(1,10):
        if sum(state_table[state][0:i]) >= selection:
            return i-1
    return -1

# führt einen Spielzug aus
def executeTurn(current_player, choosenField, state):
    calc_next_state = list(state)
    calc_next_state[choosenField] = current_player
    return tuple(calc_next_state)

#überprüft ob das Spiel beendet ist (1 --> Spieler 1 gewonnen, 2 --> Spieler 2 gewonnen
# 0 --> remis oder Spiel noch nicht vorbei)
def isGameOver(next_state):
    current_state = list(next_state)
    win_condition = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
        )
    for each in win_condition:
        if current_state[each[0]] == current_state[each[1]] and current_state[each[1]] == current_state[each[2]] and current_state[each[0]] != 0:
            return current_state[each[0]]
    return 0

# ändert für alle gespielten Situationen die Wahrscheinlichkeiten
def changeProbabilities(turns, winner, state_table_player1, state_table_player2):
    change_weight_won = 2
    change_weight_lost = -1
    change_weight_draw = 0
                        
#    print winner ,"nach", len(turns)
    
    for state in turns:
        # change probabilities player1
        if turns[state][0] == 1:
#            print "p1", turns[state][0],state_table_player1[state][turns[state][1]] 
            if winner == 1 and state_table_player1[state][turns[state][1]] + change_weight_won > 0:
                state_table_player1[state][turns[state][1]] += change_weight_won
            if winner == 2 and state_table_player1[state][turns[state][1]] + change_weight_lost > 0:
                state_table_player1[state][turns[state][1]] += change_weight_lost
            if winner == 0 and state_table_player1[state][turns[state][1]] + change_weight_draw > 0:
                state_table_player1[state][turns[state][1]] += change_weight_draw
#            print "p1", turns[state][0], state_table_player1[state][turns[state][1]] 
                
        # change probabilities player2
        if turns[state][0] == 2:
#            print "p2",turns[state][0], state_table_player2[state][turns[state][1]] 
            if winner == 2 and state_table_player2[state][turns[state][1]] + change_weight_won > 0:
                state_table_player2[state][turns[state][1]] += change_weight_won
            if winner == 1 and state_table_player2[state][turns[state][1]] + change_weight_lost > 0:
                state_table_player2[state][turns[state][1]] += change_weight_lost
            if winner == 0 and state_table_player2[state][turns[state][1]] + change_weight_draw > 0:
                state_table_player2[state][turns[state][1]] += change_weight_draw
#            print "p2",turns[state][0], state_table_player2[state][turns[state][1]] 
    return

    
def playGame(max_game, pickleFileP1, pickleFileP2, trainMode):    

    if trainMode:
        state_table_player1 = {}
        state_table_player2 = {}
    else:
        # Dictionary including all states
        pkl_file1 = open(pickleFileP1+".pkl", 'rb')
        state_table_player1 = pickle.load(pkl_file1)
        pkl_file1.close()
    
        # Dictionary including all states
        pkl_file2 = open(pickleFileP2+".pkl", 'rb')
        state_table_player2 = pickle.load(pkl_file2)
        pkl_file2.close()
        
    # init Game
    current_game_number = 1
    state = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    current_turn = 1
    start_player = randint(1,2)
    current_player = start_player
    turns = {}
    
    #statistics from the perspective of player 1
    draw = 0
    won = 0 
    lost = 0
    totTurns = 0
    unkownStatePlayer1 = 0
    unkownStatePlayer2 = 0
    
    #print
    show = 0
    show_result = 0

    while current_game_number <= max_game:
        
        if current_player == 1 and state not in state_table_player1:
            # add new state to state_table
            addStateToStateTable(state, state_table_player1)
            unkownStatePlayer1 += 1
                

        if current_player == 2 and state not in state_table_player2:
            # add new state to state_table
            addStateToStateTable(state, state_table_player2)
            unkownStatePlayer2 += 1
#
        # choose next Action
        if current_player == 1:
            choosen_field = chooseAction(state, state_table_player1)
            
        if current_player == 2:
            choosen_field = chooseAction(state, state_table_player2)
            

        # execute next Turn
        next_state = executeTurn(current_player, choosen_field, state)
    
#        print next_state
        #store current Turn
        turns[state] = [current_player, choosen_field]

        # print next_state
#        print "player", current_player,"turn", current_turn, "field",choosen_field

       # if show:
     #   print "turn", current_turn,"player", current_player, "field",choosen_field
   #     print next_state

        winner = isGameOver(next_state)
        if winner or current_turn == 9:
            if trainMode:   
                changeProbabilities(turns, winner, state_table_player1, state_table_player2);            
            #update statistics
            if winner == 1:
                won += 1
#                print "winner 1"
            elif winner == 2:
                lost += 1
#                print "winner 2"
            elif winner == 0:
                draw += 1
#                print "Draw"

            # init next Game
            current_game_number += 1
            state = (0, 0, 0, 0, 0, 0, 0, 0, 0)
            #switch start player
            start_player = start_player % 2 + 1
#            current_player = randint(1,2)
            current_player = start_player
            totTurns += current_turn
            current_turn = 1
            turns = {}
#            print "start playing game number", current_game_number, current_player
            if show:
                print "start playing game number", current_game_number, current_player
        else:
            state = next_state
            current_turn += 1
            #switch player
            current_player = current_player % 2 + 1
           
    if show_result == 1:
        print "played games", max_game
        print "wins player_1", won, won*1.0/max_game
        print "losts player_1", lost, lost*1.0/max_game
        print "draws", draw, draw*1.0/max_game
    

    if trainMode:   
        output1 = open(pickleFileP1+"_"+str(max_game)+".pkl", 'wb')
        pickle.dump(state_table_player1, output1)
        output1.close()
    
        output2 = open(pickleFileP2+"_"+str(max_game)+".pkl", 'wb')
        pickle.dump(state_table_player2, output2)
        output2.close()
    
    return [max_game,  won*1.0/max_game, lost*1.0/max_game, draw*1.0/max_game,unkownStatePlayer1, unkownStatePlayer2, totTurns*1.0/max_game]
            

if __name__ == "__main__":
    
    
    
    
 #Einzelne Tests


    print "training"
    
    print playGame(10000, "player1", "player2", True)
    print playGame(10000, "player3", "player4", True)
    print playGame(10000, "player5", "player6", True)
    print playGame(10000, "player7", "player8", True)
    print playGame(10000, "player9", "player10", True)

    p1 = "player1_10000"
    p2 = "player2_10000"
    p3 = "player3_10000"
    p4 = "player4_10000"
    p5 = "player5_10000"
    p6 = "player6_10000"
    p7 = "player7_10000"
    p8 = "player8_10000"
    p9 = "player9_10000"
    p10 = "player10_10000"

    print "playing"
#
    print playGame(10000, p1, p1, False)
    print playGame(10000, p1, p2, False)
    print playGame(10000, p1, p3, False)
    print playGame(10000, p1, p4, False)
    print playGame(10000, p1, p5, False)
    print playGame(10000, p1, p6, False)
    print playGame(10000, p1, p7, False)
    print playGame(10000, p1, p8, False)
    print playGame(10000, p1, p9, False)
    print playGame(10000, p1, p10, False)

#    print "----1:1"
#    print playGame(10000, p1, p1, False)
#    print playGame(10000, p1, p1, False)
#    print playGame(10000, p1, p1, False)
#    print "----1:2"
#    print playGame(10000, p1, p2, False)
#    print playGame(10000, p1, p2, False)
#    print playGame(10000, p1, p2, False)
#    print "----2:1"
#    print playGame(10000, p2, p1, False)
#    print playGame(10000, p2, p1, False)
#    print playGame(10000, p2, p1, False)
#    print "----2:2"
#    print playGame(10000, p2, p2, False)
#    print playGame(10000, p2, p2, False)
#    print playGame(10000, p2, p2, False)
    

