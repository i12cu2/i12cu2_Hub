import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from pathlib import Path

# 当前 py 脚本所在目录
BASE_DIR = Path(__file__).resolve().parent

# ==================== 文件路径 ====================
MARKDOWN_FILE_PATH = BASE_DIR / "badline.md"
GOODFRIEND_FILE_PATH = BASE_DIR / "goodfriend.md"
BADFRIEND_FILE_PATH = BASE_DIR / "badfriend.md"

def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        messagebox.showerror("错误", f"读取文件失败：{e}")
        return None

# ==================== 数据解析 ====================
def parse_markdown_tables(md_text):
    counters_of = {}   # hero -> [克星列表]
    hero_position = {}
    pos_map = {"射": "发育路", "边": "对抗路", "野": "打野", "中": "中路", "辅": "游走"}
    table_positions = ["发育路", "对抗路", "打野", "中路", "游走"]
    table_idx = 0

    lines = md_text.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|') and '所选英雄' in line:
            current_first_col_pos = table_positions[table_idx] if table_idx < len(table_positions) else "未知"
            # 解析表头，保留空单元格
            header_cells = line.split('|')[1:-1]  # 去掉首尾空
            header_cells = [c.strip() for c in header_cells]
            if len(header_cells) < 6:
                i += 1
                continue
            # 位置列名（射、边、野、中、辅）
            pos_cols = header_cells[1:6]  # 第2~6列
            i += 1
            # 跳过分隔线
            while i < len(lines) and re.match(r'^\|[\s\-|]+\|$', lines[i].strip()):
                i += 1
            # 读取数据行
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = lines[i].strip()
                cells = row.split('|')[1:-1]   # 保留空单元格
                if len(cells) < 6:
                    i += 1
                    continue
                hero = cells[0].strip()
                if not hero:
                    i += 1
                    continue
                if hero not in hero_position:
                    hero_position[hero] = current_first_col_pos

                # 遍历每个位置列
                for idx, col_name in enumerate(pos_cols):
                    cell = cells[idx + 1].strip()
                    if not cell:
                        continue
                    for c_hero in re.split(r'[/、]', cell):
                        c_hero = c_hero.strip()
                        if not c_hero:
                            continue
                        counters_of.setdefault(hero, []).append(c_hero)
                        pos = pos_map.get(col_name)
                        if pos and c_hero not in hero_position:
                            hero_position[c_hero] = pos
                i += 1
            table_idx += 1
        else:
            i += 1

    # 去重
    for hero in counters_of:
        counters_of[hero] = list(set(counters_of[hero]))

    # 反向映射
    counter_to = {}
    for hero, counters in counters_of.items():
        for c in counters:
            counter_to.setdefault(c, []).append(hero)

    return counters_of, counter_to, hero_position

def parse_synergy_table(file_path, is_good):
    """
    解析配合表（goodfriend.md 或 badfriend.md）
    返回 dict: hero -> [list of synergy heroes]
    is_good: True 表示加分配合，False 表示减分配合（仅用于提示）
    """
    if not os.path.exists(file_path):
        print(f"警告：文件 {file_path} 不存在，跳过")
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    synergy = {}
    lines = text.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|') and '所选英雄' in line:
            # 表头行，解析列索引
            header_cells = line.split('|')[1:-1]
            header_cells = [c.strip() for c in header_cells]
            # 期望第一列为英雄名，后面5列为位置
            if len(header_cells) < 6:
                i += 1
                continue
            # 位置列名（射、边、野、中、辅）
            pos_cols = header_cells[1:6]
            i += 1
            # 跳过分隔线
            while i < len(lines) and re.match(r'^\|[\s\-|]+\|$', lines[i].strip()):
                i += 1
            # 读取数据行
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = lines[i].strip()
                cells = row.split('|')[1:-1]
                if len(cells) < 6:
                    i += 1
                    continue
                hero = cells[0].strip()
                if not hero:
                    i += 1
                    continue
                # 收集所有位置中的英雄
                for idx in range(5):  # 5个位置
                    cell = cells[idx + 1].strip()
                    if not cell:
                        continue
                    for h in re.split(r'[/、]', cell):
                        h = h.strip()
                        if h:
                            synergy.setdefault(hero, []).append(h)
                i += 1
            break  # 只处理第一个匹配的表
        else:
            i += 1
    # 去重
    for hero in synergy:
        synergy[hero] = list(set(synergy[hero]))
    return synergy

# ==================== 全局数据 ====================
COUNTERS_OF = {}
COUNTER_TO = {}
HERO_POSITION = {}
GOODFRIEND = {}   # 英雄 -> 配合队友列表
BADFRIEND = {}    # 英雄 -> 冲突队友列表

def load_data():
    global COUNTERS_OF, COUNTER_TO, HERO_POSITION, GOODFRIEND, BADFRIEND
    # 加载克制表
    md_text = read_markdown_file(MARKDOWN_FILE_PATH)
    if md_text is None:
        return False
    COUNTERS_OF, COUNTER_TO, HERO_POSITION = parse_markdown_tables(md_text)
    if not COUNTERS_OF:
        messagebox.showerror("错误", "未能从文件中解析出有效的克制关系，请检查文件格式")
        return False

    # 加载配合表
    GOODFRIEND = parse_synergy_table(GOODFRIEND_FILE_PATH, is_good=True)
    BADFRIEND = parse_synergy_table(BADFRIEND_FILE_PATH, is_good=False)

    return True

# ==================== 推荐算法 ====================
POSITION_WEIGHTS = {
    "对抗路": {"对抗路": 0.6, "打野": 0.8, "中路": 0.5, "发育路": 0.4, "游走": 0.5},
    "打野": {"对抗路": 0.5, "打野": 0.7, "中路": 0.6, "发育路": 0.4, "游走": 0.6},
    "中路": {"对抗路": 0.5, "打野": 0.8, "中路": 0.7, "发育路": 0.4, "游走": 0.6},
    "发育路": {"对抗路": 0.4, "打野": 1.0, "中路": 0.8, "发育路": 0.3, "游走": 0.7},
    "游走": {"对抗路": 0.4, "打野": 0.6, "中路": 0.5, "发育路": 0.4, "游走": 0.6},
}

def recommend_heroes(my_position, ally_heroes, enemy_heroes, show_all=False):
    all_heroes = set(HERO_POSITION.keys())
    selected = set(h["name"] for h in ally_heroes) | set(h["name"] for h in enemy_heroes)
    candidates = [h for h in all_heroes if HERO_POSITION.get(h) == my_position and h not in selected]

    if not candidates:
        return []

    scores = []
    for hero in candidates:
        score = 0.0
        counter_enemies = []
        be_countered = []
        good_ally = []
        bad_ally = []

        # 1. 克制对方
        for enemy in enemy_heroes:
            if enemy["name"] in COUNTER_TO.get(hero, []):
                w = POSITION_WEIGHTS.get(enemy["position"], {}).get(my_position, 0.5)
                score += 10 * w
                counter_enemies.append(enemy["name"])

        # 2. 被对方克制
        for enemy in enemy_heroes:
            if enemy["name"] in COUNTERS_OF.get(hero, []):
                w = POSITION_WEIGHTS.get(my_position, {}).get(enemy["position"], 0.5)
                score -= 10 * w
                be_countered.append(enemy["name"])

        # 3. 队友配合（加分）
        for ally in ally_heroes:
            if ally["name"] in GOODFRIEND.get(hero, []):
                # 队友配合加分 5 分
                score += 5
                good_ally.append(ally["name"])

        # 4. 队友冲突（减分）
        for ally in ally_heroes:
            if ally["name"] in BADFRIEND.get(hero, []):
                score -= 5
                bad_ally.append(ally["name"])

        # 构造详情字符串
        if not enemy_heroes:
            total_counters = len(COUNTERS_OF.get(hero, []))
            score = max(0, 100 - total_counters * 5)
            detail = f"(抗性分：被{total_counters}个英雄克制)"
        else:
            detail_parts = []
            if counter_enemies:
                detail_parts.append(f"克制 {', '.join(counter_enemies)}")
            if be_countered:
                detail_parts.append(f"被 {', '.join(be_countered)} 克制")
            if good_ally:
                detail_parts.append(f"适配 {', '.join(good_ally)}")
            if bad_ally:
                detail_parts.append(f"不适配 {', '.join(bad_ally)}")
            detail = "(" + ", ".join(detail_parts) + ")" if detail_parts else "(无克制关系)"

        scores.append((hero, score, detail))

    scores.sort(key=lambda x: x[1], reverse=True)
    if show_all:
        return scores
    else:
        return scores[:5]

# ==================== GUI ====================
class BPApp:
    def __init__(self, root):
        self.root = root
        root.title("王者荣耀 BP 推荐系统")
        root.geometry("850x750")

        if not load_data():
            root.destroy()
            return

        # 配置分组（你的位置 + 选人阶段）
        config_frame = ttk.LabelFrame(root, text="配置", padding=5)
        config_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(config_frame, text="你的位置：").pack(side="left", padx=5)
        self.pos_var = tk.StringVar(value="打野")
        pos_combo = ttk.Combobox(config_frame, textvariable=self.pos_var,
                                 values=["对抗路", "打野", "中路", "发育路", "游走"],
                                 state="readonly", width=10)
        pos_combo.pack(side="left", padx=5)

        ttk.Label(config_frame, text="选人阶段：").pack(side="left", padx=20)
        self.stage_var = tk.StringVar(value="红方一楼二楼")
        stage_combo = ttk.Combobox(config_frame, textvariable=self.stage_var,
                                   values=["蓝方一楼", "红方一楼二楼", "蓝方二三楼", "红方三四楼", "蓝方四五楼", "红方五楼"],
                                   state="readonly", width=15)
        stage_combo.pack(side="left", padx=5)
        self.stage_var.trace_add("write", self.on_stage_change)

        # 已选英雄区域
        self.heroes_frame = ttk.Frame(root)
        self.heroes_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.entries = []
        self.create_inputs()

        # 推荐按钮
        ttk.Button(root, text="推荐", command=self.do_recommend).pack(pady=10)

        # 结果展示
        self.result_text = tk.Text(root, height=15, width=90)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=5)

    def on_stage_change(self, *args):
        self.create_inputs()

    def create_inputs(self):
        for widget in self.heroes_frame.winfo_children():
            widget.destroy()

        stage = self.stage_var.get()
        stage_order = {
            "蓝方一楼": [],
            "红方一楼二楼": [("蓝方1楼", "蓝")],
            "蓝方二三楼": [("蓝方1楼", "蓝"), ("红方1楼", "红"), ("红方2楼", "红")],
            "红方三四楼": [("蓝方1楼", "蓝"), ("红方1楼", "红"), ("红方2楼", "红"), ("蓝方2楼", "蓝"), ("蓝方3楼", "蓝")],
            "蓝方四五楼": [("蓝方1楼", "蓝"), ("红方1楼", "红"), ("红方2楼", "红"), ("蓝方2楼", "蓝"), ("蓝方3楼", "蓝"),
                           ("红方3楼", "红"), ("红方4楼", "红")],
            "红方五楼": [("蓝方1楼", "蓝"), ("红方1楼", "红"), ("红方2楼", "红"), ("蓝方2楼", "蓝"), ("蓝方3楼", "蓝"),
                         ("红方3楼", "红"), ("红方4楼", "红"), ("蓝方4楼", "蓝"), ("蓝方5楼", "蓝")],
        }
        order = stage_order.get(stage, [])
        if not order:
            ttk.Label(self.heroes_frame, text="当前为蓝方一楼，无已选英雄").pack()
            self.entries = []
            return

        left_frame = ttk.LabelFrame(self.heroes_frame, text="蓝方已选英雄")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        right_frame = ttk.LabelFrame(self.heroes_frame, text="红方已选英雄")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        my_side = "蓝" if stage.startswith("蓝方") else "红"
        self.entries = []
        for desc, side in order:
            parent = left_frame if side == "蓝" else right_frame
            frame = ttk.Frame(parent)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text=f"{desc}：").pack(side="left", padx=5)
            entry = ttk.Entry(frame, width=20)
            entry.pack(side="left", padx=5)
            is_ally = (side == my_side)
            self.entries.append((entry, is_ally, desc))

    def get_selected_heroes(self):
        ally = []
        enemy = []
        for entry, is_ally, desc in self.entries:
            name = entry.get().strip()
            if not name:
                continue
            pos = HERO_POSITION.get(name)
            if pos is None:
                messagebox.showerror("错误", f"英雄「{name}」的位置未知，请检查输入或补充数据")
                return None, None
            hero_info = {"name": name, "position": pos}
            if is_ally:
                ally.append(hero_info)
            else:
                enemy.append(hero_info)
        return ally, enemy

    def do_recommend(self):
        my_pos = self.pos_var.get()
        ally, enemy = self.get_selected_heroes()
        if ally is None:
            return

        recs = recommend_heroes(my_pos, ally, enemy, show_all=True)

        self.result_text.delete(1.0, tk.END)
        if not recs:
            self.result_text.insert(tk.END, "没有可推荐的英雄（可能所有英雄都已选或数据不全）")
        else:
            for i, (hero, score, detail) in enumerate(recs, 1):
                self.result_text.insert(tk.END, f"{i}. {hero} - 推荐指数 {score:.1f} {detail}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BPApp(root)
    root.mainloop()