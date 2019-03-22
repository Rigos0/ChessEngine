import sys, select

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
       time = 2
       nodes = 2000
       nps = 5000
       bestmove = str('e4')

       while True:
        interrupt, o, e = select.select([sys.stdin], [], [], 0.2)
        if interrupt:
            message = str(sys.stdin.readline().strip())
            if message == 'stop':
                break
            elif message == 'quit':
                stop = True
                break

        else:
            print('info depth', (depth), 'score cp ',(score), 'time', (time), 'nodes', (nodes), 'nps', (nps), 'pv', (bestmove))

   else:
       pass




