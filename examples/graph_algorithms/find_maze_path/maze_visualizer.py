import gradio as gr
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image
import imageio  # Still useful for reading images if needed, but we'll use Pillow for saving GIFs
import tempfile
import os


def find_path_iterative_dfs(start_r, start_c, grid, total_xs):
    rows, cols = len(grid), len(grid[0])
    stack = [(start_r, start_c, [(start_r, start_c)])]

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


def solve_maze_for_gradio(grid_str, loop_animation):
    """
    解析文字輸入，尋找路徑，並根據使用者選擇回傳動態 GIF 或靜態 PNG。
    """
    # 1. 解析輸入的文字網格
    try:
        grid = [list(row.strip().replace(' ', '')) for row in grid_str.strip().split('\n')]
        rows = len(grid)
        cols = len(grid[0])
        if not all(len(row) == cols for row in grid):
            raise ValueError("所有行必須有相同的長度。")
    except Exception as e:
        return None, f"網格格式錯誤: {e}"

    total_xs = sum(row.count('x') for row in grid)
    if total_xs == 0:
        return None, "網格中沒有 'x'。"

    # 2. 尋找路徑
    solution_path = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'x':
                solution_path = find_path_iterative_dfs(r, c, grid, total_xs)
                if solution_path:
                    break
        if solution_path:
            break

    if not solution_path:
        return None, "未找到解決方案。"

    # 3. 產生 GIF 動畫
    images = []
    for i in range(len(solution_path)):
        # 在迴圈內為每一幀建立新的圖表
        fig, ax = plt.subplots(figsize=(cols, rows))

        # **關鍵修正：手動設定座標軸範圍以保持大小一致**
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)

        # 繪製靜態元素 (網格, 障礙物)
        ax.set_xticks(np.arange(cols + 1) - 0.5, minor=True)
        ax.set_yticks(np.arange(rows + 1) - 0.5, minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
        ax.tick_params(which="minor", size=0)
        ax.set_xticks([])
        ax.set_yticks([])

        for r_idx in range(rows):
            for c_idx in range(cols):
                if grid[r_idx][c_idx] == 'o':
                    ax.add_patch(plt.Rectangle((c_idx - 0.5, r_idx - 0.5), 1, 1, facecolor='black'))

        # 繪製當前進度的路徑
        path_x = [c for r, c in solution_path[:i+1]]
        path_y = [r for r, c in solution_path[:i+1]]
        ax.plot(path_x, path_y, color='red', linewidth=3, marker='o', markersize=8)

        # 標示起點和終點
        if i >= 0:  # 起點從一開始就標示
            ax.text(solution_path[0][1], solution_path[0][0], 'S', ha='center', va='center', color='white', fontsize=12, weight='bold')
        if i == len(solution_path) - 1:  # 終點只在最後一幀標示
            ax.text(path_x[-1], path_y[-1], 'E', ha='center', va='center', color='white', fontsize=12, weight='bold')

        ax.invert_yaxis()
        plt.tight_layout()

        # 將當前圖表儲存為圖片
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)  # 關閉圖表以釋放資源
        buf.seek(0)
        images.append(Image.open(buf))

    # 4. **關鍵修正：使用 Pillow 直接控制 GIF 儲存行為**
    with tempfile.NamedTemporaryFile(delete=False, suffix=".gif") as tmpfile:
        if loop_animation:
            # 如果要循環，儲存時加入 loop=0 參數
            images[0].save(
                tmpfile.name,
                format='GIF',
                save_all=True,
                append_images=images[1:],
                duration=0.5,
                loop=0  # 0 表示無限循環
            )
        else:
            # 如果不循環，則完全不提供 loop 參數，使其播放一次後停止
            images[0].save(
                tmpfile.name,
                format='GIF',
                save_all=True,
                append_images=images[1:],
                duration=0.5
            )
        gif_path = tmpfile.name

    return gif_path, f"成功找到路徑！共 {len(solution_path)} 步。"


# --- Gradio 介面設定 ---
default_maze = """
x x x x x
x o x x x
x o x x x
x x x x x
x x x x x
"""

iface = gr.Interface(
    fn=solve_maze_for_gradio,
    inputs=[
        gr.Textbox(lines=7, label="輸入迷宮", value=default_maze),
        gr.Checkbox(label="循環播放動畫", value=True)
    ],
    outputs=[
        gr.Image(type="filepath", label="路徑視覺化"),
        gr.Textbox(label="狀態訊息")
    ],
    title="迷宮路徑尋找器 (動畫版)",
    description="輸入一個迷宮 ('x' 代表路徑, 'o' 代表障礙物)，程式會使用 DFS 尋找一條走完所有 'x' 的路徑並以動畫顯示。",
    allow_flagging="never"
)


if __name__ == "__main__":
    iface.launch()
