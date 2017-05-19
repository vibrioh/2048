from time import clock
from BaseAI_3 import BaseAI
import math


class PlayerAI(BaseAI):
    def getMove(self, grid):
        def alpha_beta_max(grid, alpha, beta, depth):
            best_move = None
            moves = grid.getAvailableMoves()
            if depth == 0:
                return score(grid), best_move
            max_eval = -inf
            for move in moves:
                state = grid.clone()
                state.move(move)
                min_eval = alpha_beta_min(state, alpha, beta, depth - 1)
                if max_eval < min_eval:
                    best_move = move
                max_eval = max(max_eval, min_eval)
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break
            return max_eval, best_move

        def alpha_beta_min(grid, alpha, beta, depth):
            if depth == 0:
                return score(grid)
            cells = grid.getAvailableCells()
            min_eval = inf
            for i in [4, 2]:
                for cell in cells:
                    state = grid.clone()
                    state.setCellValue(cell, i)
                    min_eval = min(min_eval, alpha_beta_max(state, alpha, beta, depth - 1)[0])
                    beta = min(beta, min_eval)
                    if alpha >= beta:
                        break
            return min_eval

        def score(grid):
            h1 = mono(grid)
            h2 = smooth(grid)
            score = h1 + h2
            return score

        def lg(x):
            return math.log2(x)

        def mono(grid):
            monoScore = 0
            maxCell = grid.getMaxTile()
            freeCells = len(grid.getAvailableCells())
            occupiedCells = 16 - freeCells
            blankGrid = [[0] * 4 for i in range(4)]

            def neighbor(i, j, z):
                if i in range(4) and j in range(4) and grid.map[i][j] == z and blankGrid[i][j] == 0:
                    blankGrid[i][j] = 1
                    neighbor(i - 1, j, z)
                    neighbor(i + 1, j, z)
                    neighbor(i, j - 1, z)
                    neighbor(i, j + 1, z)

            for i in range(4):
                for j in range(4):
                    if grid.map[i][j] > 0:
                        if blankGrid[i][j] == 0:
                            monoScore -= 30
                            neighbor(i, j, grid.map[i][j])
                        monoScore += lg(grid.map[i][j]) * (8 - i - j) / occupiedCells
                        for i in [0, 3]:
                            for j in [0, 3]:
                                if maxCell == grid.map[i][j]:
                                    monoScore += lg(maxCell) * (8 - i - j) / occupiedCells
                        k = j + 1
                        while k < 4 and grid.map[i][k] == 0:
                            k += 1
                        if k < 4:
                            monoScore -= abs(lg(grid.map[i][j] / grid.map[i][k]))
                        l = i + 1
                        while l < 4 and grid.map[i][k] == 0:
                            l += 1
                        if l < 4 and grid.map[l][j] > 0:
                            monoScore -= abs(lg(grid.map[i][j] / grid.map[l][j]))
            return monoScore

        def smooth(grid):
            r1 = r2 = c1 = c2 = 0
            def row(i, j):
                if grid.map[i + 1][j] > 0:
                    return lg(grid.map[i][j] / (grid.map[i + 1][j]))
                else:
                    return lg(grid.map[i][j])
            def col(i, j):
                if grid.map[i][j + 1] > 0:
                    return lg(grid.map[i][j] / (grid.map[i][j + 1]))
                else:
                    return lg(grid.map[i][j])

            for i in range(4):
                for j in range(4):
                    if grid.map[i][j] == 0:
                        continue
                    if i < 3:
                        if grid.map[i][j] > grid.map[i + 1][j]:
                            c2 -= row(i, j)
                        else:
                            c1 += row(i, j)
                    if j < 3:
                        if grid.map[i][j] > grid.map[i][j + 1]:
                            r2 -= col(i, j)
                        else:
                            r1 += col(i, j)
            return (max(r1, r2) + max(c1, c2)) * 15

        start = clock()
        inf = float('inf')
        best_move = None
        depth = 0
        while clock() - start < 0.015 and depth < 5:
            max_eval, move = alpha_beta_max(grid, -inf, inf, depth)
            if move != None:
                best_move = move
            depth += 1
        return best_move

