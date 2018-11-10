# -*- coding: utf-8 -*-
"""
Created on Mon Jul 06 13:48:34 2015

@author: losj

see ticTacToe_leaner.py for infos
"""
import ticTacToe_learner as reinforcementLearning
import matplotlib.pylab as plt


#train default opponent
#noGamesDefaultOpponent = 2000000
noGamesDefaultOpponent = 10000
#oppName = "opponent2"
oppName = "player10"
#reinforcementLearning.playGame(noGamesDefaultOpponent, "opponent1","opponent2", True)

# Testsettings
result = []
# no of games to play against opponent
simulated_games= 10000


#Train & Play
#train a player with number of games 
#games = [1,10,20,40,60,80,100,120,140,160,180,200, 400, 600, 800, 1000, 2000, 4000, 6000, 100000, 200000, 300000, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000]
games = [10000]

result_games = []
result_won = []
result_lost = []
result_draw = []
unkown_statets_p = []
unkown_statets_opp = []

for noGames in games:
    #train a player by playing noGames
    #muss ja nicht jedes mal gemacht werden
   # reinforcementLearning.playGame(noGames, "player1","player2", True)
    
    #simulate game vs default opponent
    
    result = reinforcementLearning.playGame(simulated_games, "player1_"+str(noGames),oppName+"_"+str(noGamesDefaultOpponent), False)
    print "player1_"+str(noGames),":",oppName+"_"+str(noGamesDefaultOpponent), result
    result_games.append(result[0])
    result_won.append(result[1])
    result_lost.append(result[2])
    result_draw.append(result[3])
    unkown_statets_p.append(result[4])
    unkown_statets_opp.append(result[5])


plt.ion()
line_won, = plt.plot(games,result_won, label ='won')
line_lost, = plt.plot(games,result_lost, label ='lost')
line_draw, = plt.plot(games,result_draw, label ='draw')
plt.legend([line_won, line_lost, line_draw], ['won', 'lost','draw'], loc=4)
plt.xlabel('# trained Games')
plt.ylabel('% won/lost/draw games')
plt.title('played against '+str(oppName))
plt.show()

plt.ion()
line_draw, = plt.plot(games,unkown_statets_p, label ='draw')
line_draw, = plt.plot(games,unkown_statets_opp, label ='draw')
plt.legend([line_won, line_lost, line_draw], ['unkown states P1', 'unkown states Opp'], loc=1)
plt.xlabel('# trained Games')
plt.ylabel('# unkown states')
plt.show()

