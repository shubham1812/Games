#1. We needed to search the state space for the best possible move for the game based on the valid moves i.e. dropping a pebble in the column or rotate a column if N > 1. So, for this we defined a successor function which gives us all the valid possible moves for a given state, goal function which will tell us of if we have won the game for a state and a evaluation function which will give us a value based on the conditions of a current state.

#2. State space: It consists of all the possible states with an array of length N. It should only contain pebble (o), (x) and (.) such that the number of pebbles is atmost n(n+3)/2 in any given board.

#3. Successor: This function will return all the valid moves for a given state i.e. it will add a pebble of the current player in each column and rotate each column if N > 1.

#4. Evaluation function: It returns an integer which is the most favorable to the current player i.e it checks top N rows and columns to find if pebble (x) has a strong hold or pebble (o). It also add value if 2 pebbles of same kind are adjacent in a row or column as [x,x,x,x,o] is better for player with pebble (x) than [x,o,x,o,x]. We also tried to make the board like a circular list this way it would be easy to find out a good value for rotation moves.

#5. This program works in the same way Iterative deepening search works. The reason we choose this approach is because of the time constraint specified.
