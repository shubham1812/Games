#!/usr/bin/python
import sys
import numpy as np

#1. We needed to search the state space for the best possible move for the game based on the valid moves i.e. dropping a pebble in the column or rotate a column if N > 1. So, for this we defined a successor function which gives us all the valid possible moves for a given state, goal function which will tell us of if we have won the game for a state and a evaluation function which will give us a value based on the conditions of a current state.
#2. State space: It consists of all the possible states with an array of length N. It should only contain pebble (o), (x) and (.) such that the number of pebbles is atmost n(n+3)/2 in any given board.
#3. Successor: This function will return all the valid moves for a given state i.e. it will add a pebble of the current player in each column and rotate each column if N > 1.
#4. Evaluation function: It returns an integer which is the most favorable to the current player i.e it checks top N rows and columns to find if pebble (x) has a strong hold or pebble (o). It also add value if 2 pebbles of same kind are adjacent in a row or column as [x,x,x,x,o] is better for player with pebble (x) than [x,o,x,o,x]. We also tried to make the board like a circular list this way it would be easy to find out a good value for rotation moves.
#5. This program works in the same way Iterative deepening search works. The reason we choose this approach is because of the time constraint specified.

#successor function
def successor(state,chance):
    generated_successors = []
    if generate_drop_pebble_successors:
        for i in range(N):
            if state[0][i] != ".":
                continue
            for j in range(N+3):
                if state[j][i] != ".":
                    new_state = np.copy(state)
                    new_state[j-1][i] = chance
                    generated_successors.append((new_state,i+1))
                    break
                if j == N+2:
                    new_state = np.copy(state)
                    new_state[j][i] = chance
                    generated_successors.append((new_state,i+1))
                    break
    for i in range(N):
        new_state = state[:,i]
        #print(np.count_nonzero(new_state == "x") + np.count_nonzero(new_state == "o"), new_state)
        temp_count = np.count_nonzero(new_state == "x") + np.count_nonzero(new_state == "o")
        if  temp_count > 1:
            j = 0
            while(j < N+3):
                if new_state[j] != ".":
                    temp = new_state[j:]
                    temp = np.roll(temp,1)
                    temp = np.insert(temp,0,["."]*j)
                    new_state = np.copy(temp)
                    break
                j +=1
            new_state = np.insert(state,i,new_state,axis=1)
            new_state = np.delete(new_state,i+1,axis=1)
            generated_successors.append((new_state,-(i+1)))
    return generated_successors

#Goal function
def goal_state(state,chance):
    find_diagonal = state[0:N]
    diagonal = find_diagonal.diagonal()
    #print(diagonal)
    anti_diagonal = find_diagonal[:,::-1].diagonal()
    #print(anti_diagonal)
    if np.count_nonzero(diagonal == chance) == N or np.count_nonzero(anti_diagonal == chance) == N:
        #print("diagonal")
        return 1
    for i in range(N):
        if np.count_nonzero(state[i] == chance) == N :
            #print("row")
            return 1
    for i in range(N):
        if np.count_nonzero(state[:N,i] == chance) == N:
            #print("column",np.count_nonzero(state[:N,i] == chance),state[:N,i])
            return 1
    return 0

#evaluation function
def heuristic_isitial(state, chance):
    if chance == "x":
        new_chance = "o"
    else:
        new_chance = "x"
    X = 0
    O = 0
    find_diagonal = state[0:N]

    x_count_diagonal_chance = np.count_nonzero(find_diagonal.diagonal() == chance)
    x_count_antidiagonal_chance = np.count_nonzero(find_diagonal[:, ::-1].diagonal() == chance)
    o_count_diagonal = np.count_nonzero(find_diagonal[:, ::-1].diagonal() == new_chance)
    o_count_antidiagonal = np.count_nonzero(find_diagonal.diagonal() == new_chance)
    if np.count_nonzero(find_diagonal.diagonal() == ".") == N:
        X += 1*10
        O += 1*10
    elif(x_count_diagonal_chance + np.count_nonzero(find_diagonal.diagonal() == ".") == N):
        X += x_count_diagonal_chance*10
    elif(o_count_diagonal + np.count_nonzero(find_diagonal.diagonal() == ".") == N):
        O += o_count_diagonal * 10
    else:
        (x,o) = countPebbles(find_diagonal.diagonal())
        X += x*10
        O += o*10
    if np.count_nonzero(find_diagonal[:,::-1].diagonal() == ".") == N:
        X += 10
        O += 10
    elif(x_count_antidiagonal_chance + np.count_nonzero(find_diagonal[:,::-1].diagonal() == ".") == N):
        X += x_count_antidiagonal_chance*10
    elif(o_count_antidiagonal + np.count_nonzero(find_diagonal[:, ::-1].diagonal() == ".") == N):
        O += o_count_antidiagonal*10
    else:
        (x,o) = countPebbles(find_diagonal[:, ::-1].diagonal())
        X += x
        O += o
    #print("diagonal ",X,O)
    for i in range(N+3):
        #print("rows",count_rows_x,count_rows_o, N)
        x_row = np.count_nonzero(state[i] == chance)
        o_row = np.count_nonzero(state[i] == new_chance)
        if np.count_nonzero(state[i] == ".") == N:
            X += 10
            O += 10
        elif x_row + np.count_nonzero(state[i] == ".") == N:
            X += x_row*10
        elif o_row + np.count_nonzero(state[i] == ".") == N:
            O += o_row*10
        else:
            (x,o) = countPebbles(state[i])
            X += x*10
            O += o*10
    #print("row", X, O)
    for i in range(N):
        x_col = np.count_nonzero(state[:, i][:N+3] == chance)
        o_col = np.count_nonzero(state[:, i][:N+3] == new_chance)
        if np.count_nonzero(state[:,i][:N+3] == ".") == N+3:
            X += 10
            O += 10
        elif(x_col + np.count_nonzero(state[:,i][:N+3] == ".")) == N+3:
            X += x_col*10
        elif(o_col + np.count_nonzero(state[:,i][:N+3] == ".")) == N+3:
            O += o_col*10
        else:
            (x,o) = countPebbles(state[:,i][:N])
            X += x*10
            O += o*10
    (x,o) = countPebbles(state[N-2:,i][:N])
    X += x * 10
    O += o * 10
    #print("col",X,O)
    return X-O

#A part of evaluation function used to count same adjacent pebbles in a given list.
def countPebbles(state):
    #print(state)
    pebble_dict = {'x':0,'o':0,'.':1}
    for i in range(len(state)-1):
        if state[i] == state[i+1]:
            pebble_dict[state[i]] += 1
    return ((pebble_dict['x'],pebble_dict['x']))

#Min node
def min_node(state, chance, alpha, beta, terminal):
    #print(terminal,"min")
    if chance == "x":
        new_chance = "o"
    else:
        new_chance = "x"
    if goal_state(state,new_chance):
        return 999
    if goal_state(state,chance):
        return -999
    if terminal == 0:
        #print("min terminal", terminal, list(state), chance, "heuristic", heuristic_isitial(state, chance))
        return heuristic_isitial(state,new_chance)
    terminal -= 1
    for (s,move) in successor(state, chance):
        #print(s,move)
        beta = min(beta, max_node(s, new_chance, alpha, beta, terminal))
        if alpha >= beta:
            #print("min",beta, s)
            return beta
    #print("min", beta, state)
    return beta

#max node
def max_node(state, chance, alpha, beta, terminal):
    #print(terminal,"max")
    new_chance = ""
    if chance == "x":
        new_chance = "o"
    else:
        new_chance = "x"
    if goal_state(state,chance):
        return 999
    if goal_state(state, new_chance):
        return -999
    if terminal == 0:
        #print("max terminal",terminal,state,chance,"heuristic", heuristic_isitial(state,chance))
        return heuristic_isitial(state,chance)
    terminal -= 1
    for (s,move) in successor(state, chance):
        alpha = max(alpha,min_node(s, new_chance, alpha, beta, terminal))
        '''else:
            alpha = 999'''
        if alpha >= beta:
            #print("max",alpha,s)
            return alpha
    #print("max", alpha, state)
    return alpha

#main solve function
def solve(state,chance):
    max_val = []
    new_chance = ""
    if chance == "x":
        new_chance = "o"
    else:
        new_chance = "x"
    threshold = 2                   #initial cutoff value
    while True:
        max_val = []
        for (s, move) in successor(state, chance):
            if goal_state(s, chance):
                print(str(move)+" "+ "".join(s.flatten()))
                return 1
            max_val.append((min_node(s, new_chance, -999999999, +999999999, threshold), s, move))    
        #print(max_val)
        resultant_state = max(max_val,key=lambda item:item[0])
        if goal_state(resultant_state[1],chance):
            print("I win", resultant_state[2])
            print(resultant_state[0])
            print(resultant_state[1])
            return 1
        #print(str(resultant_state[0]),"Max val")
        #print(resultant_state[1])
        if resultant_state[2] <1:
            print(resultant_state)
            print("Rotate column "+str( abs(resultant_state[2])))
            print(str( resultant_state[2])+" "+ "".join(resultant_state[1].flatten()))
        else:
            print(resultant_state)
            print("Drop pebble in "+str(resultant_state[2])+" column ")
            print(str(abs(resultant_state[2])) + " " + "".join(resultant_state[1].flatten()))
        threshold += 2


N = int(sys.argv[1])
chance = sys.argv[2]
given_state = []
current_state = sys.argv[3]
for i in current_state:
    given_state.append(i)
current_state = np.array(given_state)
current_state = current_state.reshape((N+3,N))  #Convert the given board format into a N*N+3 format
print(current_state)
generate_drop_pebble_successors = False
max_pebble_count = (N*(N+3))/2
pebble_count = np.count_nonzero(current_state == chance)
if pebble_count < max_pebble_count:            #Calculate the max pebble count to stop the successor from adding extra pebbles
    generate_drop_pebble_successors = True
#print(generate_drop_pebble_successors,max_pebble_count,pebble_count)
#print(heuristic_isitial(current_state,chance))
solve(current_state,chance) #3,
