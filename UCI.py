import time


stop = False
while not stop:
   token = input()

   if token == 'stop' or token =='quit':
       break

   elif token == 'uci':
       print('id name Pyfish')
       print('id author Richard Mladek')
       print('uciok')

   elif token == 'isready':
       print('readyok')
         
   elif token == 'ucinewgame':
       from zd import new_game
       new_game()

   elif token.startswith('go'):
       depth = 0
       score = 1
       timer = 2
       nodes = 2000
       nps = 5000
       bestmove = str('e4')
       for i in range(1,20):
           time.sleep(1)
           print('info depth', (depth), 'score cp ',(score), 'time', (timer), 'nodes', (nodes), 'nps', (nps), 'pv', (bestmove))
           depth += 0
           score += 1
           timer += 2
           nodes += 2000
           nps += 5000
       
                  
   else:
       pass




