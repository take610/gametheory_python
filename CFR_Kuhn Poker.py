
# coding: utf-8

# In[91]:

import random 
import numpy as np
import pandas as pd
get_ipython().run_line_magic('precision', '3')
np.set_printoptions(suppress=True)

class KuhnPoker:
    def __init__(self):
        #ゲームの構成
        self.act_list = ["p","b"] #各ノードで取りうる行動
        self.cards = [0,1,2] #p1とp2に配られるカード(重複なし)
        self.score_list = np.array([[2,-2],[-2,2],[1,-1],[-1,1]]) #ゲームの利得
        self.hist_list = [[],["b"],["p"],["p","b"],["b","p"],["b","b"],["p","b","p"],["p","b","b"],["p","p"]] #行動履歴のリスト
        self.term_list = [["b","p"],["b","b"],["p","b","p"],["p","b","b"],["p","p"]] #終点の行動履歴リスト
        self.nonterm_list = [[],["b"],["p"],["p","b"]] #終点でないノードの行動履歴リスト
        #P1,2の戦略セット[Passする確率,Betする確率]
        self.strategy_set = np.array([
            [[1/2,1/2],[1/2,1/2],[1/2,1/2],[1/2,1/2]],#カードが0の時[はじめ,b,p,pb]で手番が回ってきた時の戦略
            [[1/2,1/2],[1/2,1/2],[1/2,1/2],[1/2,1/2]],#カードが1の時
            [[1/2,1/2],[1/2,1/2],[1/2,1/2],[1/2,1/2]] #カードが2の時
        ])
        #ゲームの利得(カードの数値が高い方が利得を得る)
    def utility(self,hands,term):
        if term == self.term_list[0]: #bp
            return self.score_list[2]
        if term == self.term_list[1]: #bb
            if hands[0] > hands[1]:
                return self.score_list[0]
            else:
                return self.score_list[1]
        if term == self.term_list[2]: #pbp
            return self.score_list[3]
        if term == self.term_list[3]: #pbb
            if hands[0] > hands[1]:
                return self.score_list[0]
            else:
                return self.score_list[1]
        if term == self.term_list[4]: #pp
            if hands[0] > hands[1]:
                return self.score_list[2]
            else:
                return self.score_list[3]

    #各状態におけるプレイヤーの戦略(戦略セットの確率に応じて戦略を選択)
    def strategy(self,hand,hist):
        return(self.strategy_set[hand][self.hist_list.index(hist)])

    #各ノードの期待利得((P1のカード,P2のカード),行動履歴)
    def exut(self,hands,hist):
        if hist in self.term_list:
            return self.utility(hands,hist)
        if hist == self.nonterm_list[0]:#はじめ
            return self.utility(hands,self.term_list[0])*self.strategy(hands[0],hist)[1]*self.strategy(hands[1],["b"])[0]\
            	  +self.utility(hands,self.term_list[1])*self.strategy(hands[0],hist)[1]*self.strategy(hands[1],["b"])[1]\
            	  +self.utility(hands,self.term_list[2])*self.strategy(hands[0],hist)[0]*self.strategy(hands[1],["p"])[1]*self.strategy(hands[0],["p","b"])[0]\
            	  +self.utility(hands,self.term_list[3])*self.strategy(hands[0],hist)[0]*self.strategy(hands[1],["p"])[1]*self.strategy(hands[0],["p","b"])[1]\
            	  +self.utility(hands,self.term_list[4])*self.strategy(hands[0],hist)[0]*self.strategy(hands[1],["p"])[0]
        if hist == self.nonterm_list[1]:#b
            return self.utility(hands,self.term_list[0])*self.strategy(hands[1],hist)[0]\
            	  +self.utility(hands,self.term_list[1])*self.strategy(hands[1],hist)[1]
        if hist == self.nonterm_list[2]:#p
            return self.utility(hands,self.term_list[2])*self.strategy(hands[1],hist)[1]*self.strategy(hands[0],["p","b"])[0]\
        		  +self.utility(hands,self.term_list[3])*self.strategy(hands[1],hist)[1]*self.strategy(hands[0],["p","b"])[1]\
        		  +self.utility(hands,self.term_list[4])*self.strategy(hands[1],hist)[0]
        if hist == self.nonterm_list[3]:#pb
            return self.utility(hands,self.term_list[2])*self.strategy(hands[0],hist)[0]\
            	  +self.utility(hands,self.term_list[3])*self.strategy(hands[0],hist)[1]

    #終点でない各ノードのcounterfactual value
    def cfv(self,hands,hist):
        if hist == self.nonterm_list[0]:#はじめ
            return self.exut(hands,hist)
        if hist == self.nonterm_list[1]:#b
            return self.strategy(hands[0],self.hist_list[0])[1]*self.exut(hands,hist)
        if hist == self.nonterm_list[2]:#p
            return self.strategy(hands[0],self.hist_list[0])[0]*self.exut(hands,hist)
        if hist == self.nonterm_list[3]:#pb
            return self.strategy(hands[1],self.hist_list[2])[1]*self.exut(hands,hist)

    #各ノードで特定の行動を選択した時のcounterfactual value
    def act_cfv(self,hands,hist,act):
        hist_next = hist + [act]
        if hist == self.nonterm_list[0]:#はじめ
            return self.exut(hands,hist_next)
        if hist == self.nonterm_list[1]:#b
            return self.strategy(hands[0],self.hist_list[0])[1]*self.exut(hands,hist_next)
        if hist == self.nonterm_list[2]:#p
            return self.strategy(hands[0],self.hist_list[0])[0]*self.exut(hands,hist_next)
        if hist == self.nonterm_list[3]:#pb
            return self.strategy(hands[1],self.hist_list[2])[1]*self.exut(hands,hist_next)

    #regretの計算
    def regret(self,hand,hist,act):
        regret_value = 0
        i = 0
        if len(hist)%2 == 0:#p1のregretを計算
            for i in self.cards:
                if i == hand:
                    regret_value += 0
                else:
                    regret_value += (self.act_cfv([hand,i],hist,act)-self.cfv([hand,i],hist))[0]
        else:               #p2のregretを計算
            for i in self.cards:
                if i == hand:
                    regret_value += 0
                else:
                    regret_value += (self.act_cfv([i,hand],hist,act)-self.cfv([i,hand],hist))[1]
        return(regret_value)

    #戦略の改善
    def compute_nash(self,iteration):
       #P1,2の累計regret[Pass,Bet]
        regret_sum = np.zeros((3,4,2),dtype="float64")

        #相手の戦略を除いた各ノードへの到達確率(平均戦略計算用)
        node_prb = np.array([
                [[1,1],[1,1],[1,1],[self.strategy_set[0][0][0],self.strategy_set[0][0][0]]],
                [[1,1],[1,1],[1,1],[self.strategy_set[1][0][0],self.strategy_set[1][0][0]]],
                [[1,1],[1,1],[1,1],[self.strategy_set[2][0][0],self.strategy_set[2][0][0]]]
        ],dtype="float64")

        #相手の戦略を除いた各ノードへの累積到達確率(平均戦略計算用)
        node_prb_sum = np.zeros((3,4,2),dtype="float64")

        #累計戦略(平均戦略計算用)
        strategy_sum = self.strategy_set*node_prb
        #累計到達確率(平均戦略計算用)
        node_prb_sum = node_prb
        i = 0
        for i in range(iteration):
            #regretの値をregret_sumに加算(累計が負になる場合は0とする)
            [i0,i1,i2] = [0,0,0]
            for i0 in range(len(self.cards)):
                for i1 in range(len(self.nonterm_list)):
                    for i2 in range(len(self.act_list)):
                        regret_sum[i0][i1][i2] = max(regret_sum[i0][i1][i2]+self.regret(self.cards[i0],self.nonterm_list[i1],self.act_list[i2]),0)

            #累積regretの大きさに応じて以後の選択確率を重み付けする
            [j0,j1] = [0,0]
            for j0 in range(np.shape(regret_sum)[0]):
                for j1 in range(np.shape(regret_sum)[1]):
                    if np.sum(regret_sum[j0][j1])!=0:
                            self.strategy_set[j0][j1] = regret_sum[j0][j1]/np.sum(regret_sum[j0][j1])
                    else:
                            self.strategy_set[j0][j1] = [1/2,1/2]
            node_prb = np.array([
                [[1,1],[1,1],[1,1],[self.strategy_set[0][0][0],self.strategy_set[0][0][0]]],
                [[1,1],[1,1],[1,1],[self.strategy_set[1][0][0],self.strategy_set[1][0][0]]],
                [[1,1],[1,1],[1,1],[self.strategy_set[2][0][0],self.strategy_set[2][0][0]]]
            ],dtype="float64")
            strategy_sum += self.strategy_set*node_prb
            node_prb_sum += node_prb

        #最終的な戦略を到達確率で平均化する
        average_straegy = strategy_sum/node_prb_sum
        print("average_straegy\n",average_straegy)
        
    def play(self,n_play):
        #自己対戦をしてスコアを計算
        score_sum=0
        score_ave=0
        i = 0
        for i in range(n_play):
            game_hand = np.random.choice(self.cards,2,replace=False) #[P1のカード,P2のカード]
            game_hist = []
            while True:
                action1 = np.random.choice(self.act_list,p=self.strategy(game_hand[0],game_hist))
                game_hist.append(action1)
                if game_hist in self.term_list:
                    break
                action2 = np.random.choice(self.act_list,p=self.strategy(game_hand[1],game_hist))
                game_hist.append(action2)
                if game_hist in self.term_list:
                    break
            score_sum += self.utility(game_hand,game_hist)
        score_ave = score_sum/n_play
        print("累積スコア:",score_sum)
        print("平均スコア:",score_ave)
