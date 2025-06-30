import sys

# 增加遞迴深度限制，以應對深度搜尋
sys.setrecursionlimit(2000)


def print_solution(path, grid):
    """
    將找到的路徑以網格形式印出。

    Args:
        path (list): 包含路徑座標的列表。
        grid (list): 迷宮的網格。
    """
    print("找到路徑：")
    rows, cols = len(grid), len(grid[0])
    path_grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    for i, (pr, pc) in enumerate(path):
        path_grid[pr][pc] = str(i % 10)

    for r_idx, row in enumerate(path_grid):
        for c_idx, cell in enumerate(row):
            if grid[r_idx][c_idx] == 'o':
                print('o', end=' ')
            else:
                print(cell, end=' ')
        print()
    print("\n路徑座標 (row, col):")
    print(path)


def find_path_recursive_dfs(r, c, path, visited, grid, total_xs):
    """
    【方法一：遞迴 DFS】透過遞迴尋找哈密頓路徑。

    Args:
        r (int): 目前的 row。
        c (int): 目前的 column。
        path (list): 目前的路徑。
        visited (list): 記錄已訪問格子的二維列表。
        grid (list): 迷宮網格。
        total_xs (int): 需要訪問的 'x' 總數。

    Returns:
        bool: 如果找到完整路徑則回傳 True，否則回傳 False。
    """
    path.append((r, c))
    visited[r][c] = True

    if len(path) == total_xs:
        return True

    rows, cols = len(grid), len(grid[0])
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dr, dc in moves:
        next_r, next_c = r + dr, c + dc
        if 0 <= next_r < rows and 0 <= next_c < cols and \
           grid[next_r][next_c] == 'x' and not visited[next_r][next_c]:
            if find_path_recursive_dfs(next_r, next_c, path, visited, grid, total_xs):
                return True

    # --- 回溯 (Backtracking) ---
    # 如果執行到這裡，代表從 (r, c) 這個點出發的所有可能路徑都已經嘗試過，
    # 但都無法找到一條完整的哈密頓路徑。
    # 因此，我們需要「撤銷」上一步的選擇，退回到上一個狀態，去嘗試其他的可能性。

    # 1. 將目前節點從路徑中移除。
    #    就像在迷宮中走到了死路，我們需要從路徑記錄中擦掉這一步。
    path.pop()

    # 2. 將目前節點標記為「未訪問」。
    #    這樣一來，其他的路徑在未來探索時，依然可以考慮經過這個節點。
    #    如果沒有這一步，這個節點就會被永久排除，導致我們錯過可能的解。
    visited[r][c] = False

    # 3. 回傳 False，告訴上一層的呼叫：從我這裡走不通。
    return False


def find_path_iterative_dfs(start_r, start_c, grid, total_xs):
    """
    【方法二：迭代 DFS】透過堆疊（stack）模擬遞迴來尋找哈密頓路徑。

    Args:
        start_r (int): 起始的 row。
        start_c (int): 起始的 column。
        grid (list): 迷宮網格。
        total_xs (int): 需要訪問的 'x' 總數。

    Returns:
        list or None: 如果找到路徑，回傳路徑列表；否則回傳 None。
    """
    rows, cols = len(grid), len(grid[0])
    stack = [(start_r, start_c, [(start_r, start_c)])]  # (r, c, current_path)

    while stack:
        r, c, path = stack.pop()

        if len(path) == total_xs:
            return path

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in moves:
            next_r, next_c = r + dr, c + dc
            if 0 <= next_r < rows and 0 <= next_c < cols and \
               grid[next_r][next_c] == 'x' and (next_r, next_c) not in path:
                new_path = path + [(next_r, next_c)]
                stack.append((next_r, next_c, new_path))
    return None


def solve_maze(grid, method='iterative'):
    """
    在給定的網格中尋找哈密頓路徑。

    Args:
        grid (list): 迷宮網格。
        method (str): 使用的方法，可為 'iterative' 或 'recursive'。
    """
    rows, cols = len(grid), len(grid[0])
    total_xs = sum(row.count('x') for row in grid)

    print(f"正在使用 {method} DFS 方法尋找路徑...")
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'x':
                solution_path = None
                if method == 'iterative':
                    solution_path = find_path_iterative_dfs(r, c, grid, total_xs)
                elif method == 'recursive':
                    path = []
                    visited = [[False for _ in range(cols)] for _ in range(rows)]
                    if find_path_recursive_dfs(r, c, path, visited, grid, total_xs):
                        solution_path = path

                if solution_path:
                    print_solution(solution_path, grid)
                    return

    print("未找到解決方案。")


if __name__ == "__main__":
    maze_grid = [
        ['x', 'x', 'x', 'x', 'x'],
        ['x', 'o', 'x', 'x', 'x'],
        ['x', 'o', 'x', 'x', 'x'],
        ['x', 'x', 'x', 'x', 'x'],
        ['x', 'x', 'x', 'x', 'x']
    ]

    # 您可以在這裡切換 'iterative' 或 'recursive' 來測試不同的方法
    solve_maze(maze_grid, method='recursive')
    solve_maze(maze_grid, method='iterative')
