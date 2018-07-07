## Description
* RegretMatching_RPS\
  RegretMatchingというメカニズムを用いてじゃんけんゲームのナッシュ均衡を求めるコードです。RegretMatchingとは、各プレイヤーが特定の確率(戦略)に基づいて実行した行動に対する後悔の度合いを定式化し、戦略の改善を繰り返すことで最適な戦略に近づいていくというメカニズムです。じゃんけんのような二人ゼロ和ゲームの場合、お互いの戦略が相手の戦略に対して最適となっているナッシュ均衡に収束することが知られています。
* CFR_KuhnPoker\
  Counterfactual Regret Minimization(CFR)という手法を用いて上記のRegretMarchingを行い、KuhnPokerと呼ばれるルールを単純化したポーカーにおけるナッシュ均衡を求めるコードです。2017年にAlberta大学が開発したポーカーAI "DeepStack"はこのCFRアルゴリズムを応用しており、プロのポーカープレイヤーを上回る戦績をあげることに成功しています。
## Examples
* RegretMatching_RPS\
  二人のプレイヤーが勝ちを利得1、負けを利得-1、引き分けを利得0としてじゃんけんを行います。例えばプレイヤー2がチョキ(Sissors)で負けた場合、仮にチョキではなくパーを出していれば利得を2だけ改善でき、グーを出していれば利得を1だけ改善できるため、次回の混合戦略は(グー、パー、チョキ)=(1/3,2/3,0)となります。このように改善できる利得をregretと定義し、各ゲームごとに累積されたリグレットに応じて各行動の選択確率を重み付けします。近似的ナッシュ均衡はRockPaperSissorsクラスのcompute_nashメソッドによって求めることができ、はじめは純粋戦略(グー,チョキ)をとっていたプレイヤーの戦略がゲームを複数回繰り返すことで（1/3,1/3,1/3）に近づくことがわかります。\
![RPS](https://i.imgur.com/TsgXdKl.png)
* CFR_KuhnPoker\
  二人のプレイヤーに0,1,2のカードから1枚ずつ配られ、相手のカードを非公開情報として各々の手番でベットかパスを選択します。お互いがベットまたはパスを選択した場合は数字の大きい方がベットなら利得2、パスなら利得1を得ます。相手のベットに対してパスを選択した場合はベットを行ったプレイヤーが利得1を得ます。RegretMatchingを用いるために、各手番におけるCounterfactual Valueと呼ばれる利得の期待値を計算しそのノードで特定の行動を行った際の利得の改善値をregretとします。例えば自分のカードが1であり相手がパスを選択してきた場合、現在の戦略によって得られる利得の期待値が1、この手番において必ずベットを選択することで得られる利得の期待値が2であるならば、ベットに対するregretの値は1となり、次回この手番でベットを選択する確率は高くなります。十分多くのゲームを行いregretの値を最小化した後で、これまでの戦略を特定の確率で重み付けし平均化した戦略がナッシュ均衡に近づくことがわかります。このように自己対戦を繰り返すことで、例えばプレイヤー1の手札が0(最弱)であっても25%の確率でブラフベットをしたり、手札が2(最強)であってもむやみにベットせずパスを選択して相手のベットを誘ったりする方が良いことをAIが学習するといったことが示唆されます。\
![Kuhn](https://i.imgur.com/LPT3Rnh.png)\
(wikipediaに記載されているナッシュ均衡に近い値を取っていることが確認できます)

## References
* Martin Zinkevich et al.(2008)Regret Minimization in Games with Incomplete Information(http://poker.cs.ualberta.ca/publications/NIPS07-cfr.pdf)
* Todd W. Neller,Marc Lanctot(2013)An Introduction to Counterfactual Regret Minimization(http://modelai.gettysburg.edu/2013/cfr/cfr.pdf)
* Wikipedia「クーンポーカー」(https://ja.wikipedia.org/wiki/クーン・ポーカー)
* Jun Okumura(2017)「ポーカーAIの最新動向」(SlideShare)https://www.slideshare.net/juneokumura/ai-20171031
