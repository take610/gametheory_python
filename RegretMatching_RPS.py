
# coding: utf-8

# In[1]:


import random 
import numpy as np
import pandas as pd
get_ipython().run_line_magic('precision', '3')
class RockPaperSissors:
    player = 2
    hand = ["Rock","Paper","Scissors"]
    utility = pd.DataFrame([[0,-1,1],[1,0,-1],[-1,1,0]],
                    index=["Rock","Paper","Scissors"],
                  columns=["Rock","Paper","Scissors"]) #勝ち1点,引き分け0点,負け-1点

    def __init__(self):
        self.strategy_set = np.array([[1,0,0],            #プレイヤー1の混合戦略(Rock,Paper,Scissors)
                                 [0,0,1]],dtype="float64")#プレイヤー2の混合戦略(Rock,Paper,Scissors)

        self.regret = np.array([[0,0,0],        #プレイヤー1の後悔の値
                                [0,0,0]])       #プレイヤー2の後悔の値

        self.regret_sum = np.array([[0,0,0],   #プレイヤー1の後悔の累計
                                    [0,0,0]])  #プレイヤー2の後悔の累計

        self.strategy_sum = np.array([[0,0,0],                 #プレイヤー1の戦略の累計
                                     [0,0,0]],dtype="float64") #プレイヤー2の戦略の累計 
        
        self.regret = np.array([[0,0,0],        #プレイヤー1の後悔の値
                                [0,0,0]])       #プレイヤー1の後悔の値

        self.regret_sum = np.array([[0,0,0],   #プレイヤー1の後悔の累計
                                    [0,0,0]])  #プレイヤー2の後悔の累計
        
    def compute_nash(self,iteration):
        i = 0
        for i in range(iteration):
            game_hand = np.array([np.random.choice(hand,p=self.strategy_set[0]),  #プレイヤー1の出す手
                                  np.random.choice(hand,p=self.strategy_set[1])]) #プレイヤー2の出す手

            game_utility = np.array([utility[game_hand[1]][game_hand[0]],  #プレイヤー1の利得
                                     utility[game_hand[0]][game_hand[1]]]) #プレイヤー2の利得

        #別の手を出すことによって得られていたはずの利得
            j = 0
            for j in range(np.shape(self.regret)[1]):
                self.regret[0][j] = utility[game_hand[1]][hand[j]]-game_utility[0]
                self.regret[1][j] = utility[game_hand[0]][hand[j]]-game_utility[1]

        #regretの累計
            k0 = 0
            for k0 in range(np.shape(self.regret_sum)[0]):
                k1 = 0
                for k1 in range(np.shape(self.regret_sum)[1]):
                    self.regret_sum[k0][k1] = max(self.regret_sum[k0][k1]+self.regret[k0][k1],0)

        #regretの累計を戦略に反映
            l0 = 0
            for l0 in range(np.shape(self.strategy_set)[0]):
                l1 = 0
                if sum(self.regret_sum[l0]) != 0:
                       for l1 in range(np.shape(self.strategy_set)[1]):
                            strategy_set[l0][l1] = regret_sum[l0][l1]/sum(regret_sum[l0])
            strategy_sum += strategy_set
        #平均戦略を求める
        strategy_ave = strategy_sum/iteratio
        print("平均戦略\n",strategy_ave)

