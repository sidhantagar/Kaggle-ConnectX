import random
import numpy as np

def get_heuristic(grid, mark, config):
    score = 0
    for i in range(config.inarow):
        num  = count_windows (grid,i+1,mark,config)
        score += (4**(i+1))*num
    for i in range(config.inarow):
        num_opp = count_windows (grid,i+1,mark%2+1,config)
        score-= (2**((2*i)+3))*num_opp
    return score

def count_windows(grid, num_discs, piece, config):
    num_windows = 0
    # horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[row, col:col+config.inarow])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(grid[row:row+config.inarow, col])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row+config.inarow), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    # negative diagonal
    for row in range(config.inarow-1, config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(grid[range(row, row-config.inarow, -1), range(col, col+config.inarow)])
            if check_window(window, num_discs, piece, config):
                num_windows += 1
    return num_windows

def drop_piece(grid, col, mark, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = mark
    return next_grid

def check_window(window, num_discs, piece, config):
    return (window.count(piece) == num_discs and window.count(0) == config.inarow-num_discs)

def score_move_a(grid, col, mark, config,n_steps=1):
    next_grid = drop_piece(grid, col, mark, config)
    valid_moves = [col for col in range (config.columns) if next_grid[0][col]==0]
    if len(valid_moves)==0 or n_steps ==0:
        score = get_heuristic3(next_grid, mark, config)
        return score
    else :
        scores = [score_move_b(next_grid,col,mark,config,n_steps-1) for col in valid_moves]
        score = min(scores)
    return score

def score_move_b(grid, col, mark, config,n_steps):
    next_grid = drop_piece(grid,col,(mark%2)+1,config)
    valid_moves = [col for col in range (config.columns) if next_grid[0][col]==0]
    if len(valid_moves)==0 or n_steps ==0:
        score = get_heuristic(next_grid, mark, config)
        return score
    else :
        scores = [score_move_a(next_grid,col,mark,config,n_steps-1) for col in valid_moves]
        score = max(scores)
    return score

def agent(obs, config):
    valid_moves = [c for c in range(config.columns) if obs.board[c] == 0]
    grid = np.asarray(obs.board).reshape(config.rows, config.columns)
    scores = dict(zip(valid_moves, [score_move_a(grid, col, obs.mark, config,1) for col in valid_moves]))
    max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
    return random.choice(max_cols)