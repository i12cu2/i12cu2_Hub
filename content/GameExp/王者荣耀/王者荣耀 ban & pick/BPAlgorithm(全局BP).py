import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from itertools import chain
from pathlib import Path

# 当前 py 脚本所在目录
BASE_DIR = Path(__file__).resolve().parent

# 尝试导入拼音库
try:
    from pypinyin import lazy_pinyin
    PINYIN_AVAILABLE = True
except ImportError:
    PINYIN_AVAILABLE = False
    print("提示：未安装 pypinyin，拼音匹配不可用。可运行 'pip install pypinyin' 安装。")

# ==================== 文件路径 ====================
MARKDOWN_FILE_PATH = BASE_DIR / "badline.md"
GOODFRIEND_FILE_PATH = BASE_DIR / "goodfriend.md"
BADFRIEND_FILE_PATH = BASE_DIR / "badfriend.md"

# ==================== 数据解析（两遍扫描） ====================
def read_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        messagebox.showerror("错误", f"读取文件失败：{e}")
        return None

def parse_markdown_tables(md_text):
    counters_of = {}
    hero_main_position = {}   # 英雄的主分路（作为第一列出现的位置）
    pos_map = {"射": "发育路", "边": "对抗路", "野": "打野", "中": "中路", "辅": "游走"}
    table_positions = ["发育路", "对抗路", "打野", "中路", "游走"]
    table_idx = 0
    # 每个位置的英雄列表（从所有表格对应列收集）
    position_heroes = {pos: [] for pos in table_positions}

    lines = md_text.strip().split('\n')
    n = len(lines)

    # ===== 第一遍：记录主分路（第一列英雄） =====
    i = 0
    while i < n:
        line = lines[i].strip()
        if line.startswith('|') and '所选英雄' in line:
            current_pos = table_positions[table_idx] if table_idx < len(table_positions) else "未知"
            i += 1
            # 跳过分隔行
            while i < n and re.match(r'^\|[\s\-|]+\|$', lines[i].strip()):
                i += 1
            # 处理数据行
            while i < n and lines[i].strip().startswith('|'):
                row = lines[i].strip()
                cells = row.split('|')[1:-1]
                if len(cells) >= 1:
                    hero = cells[0].strip()
                    if hero:
                        if hero not in hero_main_position:
                            hero_main_position[hero] = current_pos
                i += 1
            table_idx += 1
        else:
            i += 1

    # ===== 第二遍：收集各列英雄（按列位置归入对应位置列表），并解析克制关系 =====
    table_idx = 0
    i = 0
    while i < n:
        line = lines[i].strip()
        if line.startswith('|') and '所选英雄' in line:
            current_pos = table_positions[table_idx] if table_idx < len(table_positions) else "未知"
            header_cells = line.split('|')[1:-1]
            header_cells = [c.strip() for c in header_cells]
            if len(header_cells) < 6:
                i += 1
                continue
            col_names = header_cells[1:6]  # 列名：射、边、野、中、辅
            i += 1
            # 跳过分隔行
            while i < n and re.match(r'^\|[\s\-|]+\|$', lines[i].strip()):
                i += 1
            # 处理数据行
            while i < n and lines[i].strip().startswith('|'):
                row = lines[i].strip()
                cells = row.split('|')[1:-1]
                if len(cells) < 6:
                    i += 1
                    continue
                hero = cells[0].strip()
                if not hero:
                    i += 1
                    continue

                # 将当前行的第一列英雄加入当前表格位置列表
                if current_pos in position_heroes:
                    position_heroes[current_pos].append(hero)

                # 遍历后续5列（索引1~5）
                for col_idx in range(5):
                    col_name = col_names[col_idx]
                    col_pos = pos_map.get(col_name, None)
                    if not col_pos:
                        continue
                    cell = cells[col_idx + 1].strip()
                    if not cell:
                        continue
                    for h in re.split(r'[/、]', cell):
                        h = h.strip()
                        if not h:
                            continue
                        # 将该英雄加入对应位置列表
                        if col_pos in position_heroes:
                            position_heroes[col_pos].append(h)
                        # 如果该英雄尚未有主分路，则设置为当前列对应位置（后备）
                        if h not in hero_main_position:
                            hero_main_position[h] = col_pos

                        # 克制关系：当前行英雄（第一列）克制该英雄
                        counters_of.setdefault(hero, []).append(h)

                i += 1
            table_idx += 1
        else:
            i += 1

    # 去重
    for pos in position_heroes:
        position_heroes[pos] = list(set(position_heroes[pos]))
    for hero in counters_of:
        counters_of[hero] = list(set(counters_of[hero]))

    # 构建反向克制
    counter_to = {}
    for hero, counters in counters_of.items():
        for c in counters:
            counter_to.setdefault(c, []).append(hero)

    return counters_of, counter_to, hero_main_position, position_heroes

def parse_synergy_table(file_path, is_good):
    if not os.path.exists(file_path):
        print(f"警告：文件 {file_path} 不存在，跳过")
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"读取 {file_path} 失败: {e}")
        return {}

    synergy = {}
    lines = text.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|') and '所选英雄' in line:
            header_cells = line.split('|')[1:-1]
            header_cells = [c.strip() for c in header_cells]
            if len(header_cells) < 6:
                i += 1
                continue
            i += 1
            while i < len(lines) and re.match(r'^\|[\s\-|]+\|$', lines[i].strip()):
                i += 1
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
                related_heroes = []
                for idx in range(1, 6):
                    cell = cells[idx].strip()
                    if not cell:
                        continue
                    for h in re.split(r'[/、]', cell):
                        h = h.strip()
                        if h:
                            related_heroes.append(h)
                for r in related_heroes:
                    synergy.setdefault(hero, set()).add(r)
                    synergy.setdefault(r, set()).add(hero)
                i += 1
            break
        else:
            i += 1

    for hero in synergy:
        synergy[hero] = list(synergy[hero])
    return synergy

# ==================== 全局数据 ====================
COUNTERS_OF = {}
COUNTER_TO = {}
HERO_MAIN_POSITION = {}  # 英雄的主分路
POSITION_HEROES = {}     # 位置->英雄列表（从所有表格对应列收集）
GOODFRIEND = {}
BADFRIEND = {}

def load_data():
    global COUNTERS_OF, COUNTER_TO, HERO_MAIN_POSITION, POSITION_HEROES, GOODFRIEND, BADFRIEND
    md_text = read_markdown_file(MARKDOWN_FILE_PATH)
    if md_text is None:
        return False
    COUNTERS_OF, COUNTER_TO, HERO_MAIN_POSITION, POSITION_HEROES = parse_markdown_tables(md_text)
    if not COUNTERS_OF:
        messagebox.showerror("错误", "未能从文件中解析出有效的克制关系，请检查文件格式")
        return False

    GOODFRIEND = parse_synergy_table(GOODFRIEND_FILE_PATH, is_good=True)
    BADFRIEND = parse_synergy_table(BADFRIEND_FILE_PATH, is_good=False)
    return True

# ==================== 自动补全输入框组件（幽灵文本位置优化） ====================
class AutocompleteEntry(ttk.Frame):
    def __init__(self, parent, hero_list, **kwargs):
        super().__init__(parent)
        self.hero_list = hero_list
        self.pinyin_map = {}
        if PINYIN_AVAILABLE:
            self.pinyin_map = {hero: ''.join(lazy_pinyin(hero)) for hero in hero_list}

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.entry_var, **kwargs)
        self.entry.pack(side="left", fill="x", expand=True)

        try:
            bg_color = self.entry.cget('background')
            if not bg_color or bg_color == '':
                bg_color = 'white'
        except:
            bg_color = 'white'
        self.ghost_label = tk.Label(self, text="", foreground="gray", background=bg_color)
        self.ghost_label.place_forget()

        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<Up>", self.on_up)
        self.entry.bind("<Down>", self.on_down)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Escape>", self.on_escape)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<FocusIn>", self.on_focus_in)

        self.ghost_label.bind("<Button-1>", lambda e: self.entry.focus_set())

        self.current_matches = []
        self.selected_index = -1
        self.last_keyword = ""

    def matches_keyword(self, hero, keyword):
        kw = keyword.lower()
        if kw in hero.lower():
            return True
        if PINYIN_AVAILABLE and kw in self.pinyin_map.get(hero, ''):
            return True
        return False

    def update_ghost_text(self):
        current_text = self.entry_var.get()
        if not current_text or self.selected_index == -1 or self.selected_index >= len(self.current_matches):
            self.ghost_label.place_forget()
            return

        matched_hero = self.current_matches[self.selected_index]
        ghost_text = f" ({matched_hero})"
        self.ghost_label.config(text=ghost_text)

        try:
            bbox = self.entry.bbox("insert")
            if bbox:
                x = bbox[0] + bbox[2] + 2
                y = bbox[1]
                entry_width = self.entry.winfo_width()
                ghost_width = self.ghost_label.winfo_reqwidth()
                if x + ghost_width > entry_width:
                    x = entry_width - ghost_width - 5
                self.ghost_label.place(in_=self.entry, x=x, y=y, anchor='nw')
                self.ghost_label.lift()
                return
        except:
            pass
        self.ghost_label.place(in_=self.entry, anchor='e', relx=1.0, x=-5, y=0)
        self.ghost_label.lift()

    def update_candidates(self, keyword):
        if not keyword.strip():
            self.current_matches = []
            self.selected_index = -1
            self.ghost_label.place_forget()
            return

        matches = [h for h in self.hero_list if self.matches_keyword(h, keyword)]
        self.current_matches = matches
        if matches:
            self.selected_index = 0
            self.update_ghost_text()
        else:
            self.selected_index = -1
            self.ghost_label.place_forget()

    def on_key_release(self, event):
        if event.keysym in ('Up', 'Down', 'Return', 'Escape'):
            return
        keyword = self.entry_var.get()
        self.last_keyword = keyword
        self.update_candidates(keyword)

    def on_up(self, event):
        if not self.current_matches:
            return "break"
        if self.selected_index > 0:
            self.selected_index -= 1
            self.update_ghost_text()
        return "break"

    def on_down(self, event):
        if not self.current_matches:
            return "break"
        if self.selected_index < len(self.current_matches) - 1:
            self.selected_index += 1
            self.update_ghost_text()
        return "break"

    def on_enter(self, event):
        if self.selected_index != -1 and self.selected_index < len(self.current_matches):
            hero = self.current_matches[self.selected_index]
            self.entry_var.set(hero)
        self.ghost_label.place_forget()
        return "break"

    def on_escape(self, event):
        self.ghost_label.place_forget()
        return "break"

    def on_focus_out(self, event):
        self.ghost_label.place_forget()

    def on_focus_in(self, event):
        keyword = self.entry_var.get()
        if keyword:
            self.update_candidates(keyword)

    def get(self):
        return self.entry_var.get().strip()

    def set(self, value):
        self.entry_var.set(value)
        self.current_matches = []
        self.selected_index = -1
        self.ghost_label.place_forget()

    def delete(self, first, last=None):
        self.entry.delete(first, last)

# ==================== 推荐算法 ====================
POSITION_WEIGHTS = {
    "对抗路": {"对抗路": 0.6, "打野": 0.8, "中路": 0.5, "发育路": 0.4, "游走": 0.5},
    "打野": {"对抗路": 0.5, "打野": 0.7, "中路": 0.6, "发育路": 0.4, "游走": 0.6},
    "中路": {"对抗路": 0.5, "打野": 0.8, "中路": 0.7, "发育路": 0.4, "游走": 0.6},
    "发育路": {"对抗路": 0.4, "打野": 1.0, "中路": 0.8, "发育路": 0.3, "游走": 0.7},
    "游走": {"对抗路": 0.4, "打野": 0.6, "中路": 0.5, "发育路": 0.4, "游走": 0.6},
}

SYNERGY_WEIGHTS = {
    "对抗路": {"对抗路": 0.8, "打野": 0.7, "中路": 0.6, "发育路": 0.5, "游走": 0.7},
    "打野": {"对抗路": 0.7, "打野": 0.6, "中路": 0.8, "发育路": 0.7, "游走": 0.9},
    "中路": {"对抗路": 0.6, "打野": 0.8, "中路": 0.5, "发育路": 0.7, "游走": 0.8},
    "发育路": {"对抗路": 0.5, "打野": 0.7, "中路": 0.7, "发育路": 0.4, "游走": 1.0},
    "游走": {"对抗路": 0.7, "打野": 0.9, "中路": 0.8, "发育路": 1.0, "游走": 0.5},
}

def recommend_heroes(my_position, ally_heroes, enemy_heroes, show_all=False):
    all_position_heroes = POSITION_HEROES.get(my_position, [])
    if not all_position_heroes:
        return []
    
    selected = set(h["name"] for h in ally_heroes) | set(h["name"] for h in enemy_heroes)
    candidates = [h for h in all_position_heroes if h not in selected]

    if not candidates:
        return []

    result = []  # 每个元素为 (hero, main_pos, score, counter_list, be_countered_list, good_list, bad_list, threat_count)
    enemy_names = set(e["name"] for e in enemy_heroes)
    enemy_positions = set(e["position"] for e in enemy_heroes)

    for hero in candidates:
        main_pos = HERO_MAIN_POSITION.get(hero, None)
        score = 0.0
        counter_enemies = []
        be_countered = []
        good_ally_names = []
        bad_ally_names = []

        # 克制敌方
        for enemy in enemy_heroes:
            if enemy["name"] in COUNTER_TO.get(hero, []):
                w = POSITION_WEIGHTS.get(enemy["position"], {}).get(my_position, 0.5)
                score += 10 * w
                counter_enemies.append(enemy["name"])

        # 被敌方克制
        for enemy in enemy_heroes:
            if enemy["name"] in COUNTERS_OF.get(hero, []):
                w = POSITION_WEIGHTS.get(my_position, {}).get(enemy["position"], 0.5)
                score -= 10 * w
                be_countered.append(enemy["name"])

        # 己方适配
        for ally in ally_heroes:
            if ally["name"] in GOODFRIEND.get(hero, []):
                w = SYNERGY_WEIGHTS.get(my_position, {}).get(ally["position"], 0.5)
                score += 5 * w
                good_ally_names.append(ally["name"])

        # 己方不适配
        for ally in ally_heroes:
            if ally["name"] in BADFRIEND.get(hero, []):
                w = SYNERGY_WEIGHTS.get(my_position, {}).get(ally["position"], 0.5)
                score -= 5 * w
                bad_ally_names.append(ally["name"])

        total_counters_set = set(COUNTERS_OF.get(hero, []))
        threat_count = 0
        for c in total_counters_set:
            if c in enemy_names:
                threat_count += 1
            else:
                c_pos = HERO_MAIN_POSITION.get(c)
                if c_pos and c_pos in enemy_positions:
                    continue
                else:
                    threat_count += 1

        # 如果没有敌方英雄，简单处理
        if not enemy_heroes:
            base_score = max(0, 100 - len(total_counters_set) * 5)
            good_weighted = 0
            bad_weighted = 0
            for ally in ally_heroes:
                if ally["name"] in GOODFRIEND.get(hero, []):
                    w = SYNERGY_WEIGHTS.get(my_position, {}).get(ally["position"], 0.5)
                    good_weighted += 5 * w
                if ally["name"] in BADFRIEND.get(hero, []):
                    w = SYNERGY_WEIGHTS.get(my_position, {}).get(ally["position"], 0.5)
                    bad_weighted += 5 * w
            final_score = base_score + good_weighted - bad_weighted
        else:
            final_score = score

        result.append((hero, main_pos, final_score, counter_enemies, be_countered, good_ally_names, bad_ally_names, threat_count))

    # 排序
    result.sort(key=lambda x: (-x[2], x[7]))
    if show_all:
        return result
    else:
        return result[:5]

# ==================== GUI 主程序 ====================
class BPApp:
    def __init__(self, root):
        self.root = root
        root.title("王者荣耀 BP 推荐系统")
        root.geometry("1100x750")  # 加宽以容纳表格

        if not load_data():
            root.destroy()
            return

        self.hero_list = list(HERO_MAIN_POSITION.keys())

        config_frame = ttk.LabelFrame(root, text="配置", padding=2)
        config_frame.pack(fill="x", padx=8, pady=3)

        ttk.Label(config_frame, text="你的位置：").pack(side="left", padx=3)
        self.pos_var = tk.StringVar(value="野")
        pos_frame = ttk.Frame(config_frame)
        pos_frame.pack(side="left", padx=3)
        for key in ("射", "边", "野", "中", "辅"):
            rb = ttk.Radiobutton(pos_frame, text=key, variable=self.pos_var, value=key)
            rb.pack(side="left", padx=1)

        ttk.Label(config_frame, text="己方阵营：").pack(side="left", padx=10)
        self.side_var = tk.StringVar(value="蓝方")
        side_frame = ttk.Frame(config_frame)
        side_frame.pack(side="left", padx=3)
        for side in ("蓝方", "红方"):
            rb = ttk.Radiobutton(side_frame, text=side, variable=self.side_var, value=side)
            rb.pack(side="left", padx=1)

        heroes_frame = ttk.LabelFrame(root, text="已选英雄", padding=2)
        heroes_frame.pack(fill="x", padx=8, pady=3)

        left_frame = ttk.LabelFrame(heroes_frame, text="蓝方", padding=2)
        left_frame.pack(side="left", fill="both", expand=True, padx=3, pady=2)
        self.blue_entries = []
        for i in range(1, 6):
            frame = ttk.Frame(left_frame)
            frame.pack(fill="x", pady=1)
            ttk.Label(frame, text=f"{i}楼：", width=4).pack(side="left", padx=2)
            entry = AutocompleteEntry(frame, self.hero_list, width=20)
            entry.pack(side="left", fill="x", expand=True)
            self.blue_entries.append(entry)

        right_frame = ttk.LabelFrame(heroes_frame, text="红方", padding=2)
        right_frame.pack(side="right", fill="both", expand=True, padx=3, pady=2)
        self.red_entries = []
        for i in range(1, 5):
            frame = ttk.Frame(right_frame)
            frame.pack(fill="x", pady=1)
            ttk.Label(frame, text=f"{i}楼：", width=4).pack(side="left", padx=2)
            entry = AutocompleteEntry(frame, self.hero_list, width=20)
            entry.pack(side="left", fill="x", expand=True)
            self.red_entries.append(entry)

        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill="x", pady=3)
        clear_btn = ttk.Button(button_frame, text="清空所有输入", command=self.clear_all_entries)
        clear_btn.pack(side="left", fill="x", expand=True, padx=2)
        recommend_btn = ttk.Button(button_frame, text="推荐", command=self.do_recommend)
        recommend_btn.pack(side="right", fill="x", expand=True, padx=2)

        # 结果表格区域
        result_frame = ttk.LabelFrame(root, text="推荐结果", padding=2)
        result_frame.pack(fill="both", expand=True, padx=8, pady=3)

        # 创建 Treeview 表格
        columns = ("hero", "counter", "be_countered", "good", "bad", "threat")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=15)
        
        # 定义列标题和宽度
        self.tree.heading("hero", text="所选英雄")
        self.tree.heading("counter", text="克制英雄")
        self.tree.heading("be_countered", text="被克制英雄")
        self.tree.heading("good", text="适配英雄")
        self.tree.heading("bad", text="不适配英雄")
        self.tree.heading("threat", text="被克制数量")
        
        self.tree.column("hero", width=150, anchor="w")
        self.tree.column("counter", width=200, anchor="w")
        self.tree.column("be_countered", width=200, anchor="w")
        self.tree.column("good", width=120, anchor="w")
        self.tree.column("bad", width=120, anchor="w")
        self.tree.column("threat", width=80, anchor="center")
        
        # 滚动条
        vsb = ttk.Scrollbar(result_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(result_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        
        # 鼠标滚轮支持
        self.tree.bind("<MouseWheel>", self._on_mousewheel)
        self.tree.bind("<Button-4>", self._on_mousewheel)
        self.tree.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.tree.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.tree.yview_scroll(1, "units")
        return "break"

    def clear_all_entries(self):
        for entry in chain(self.blue_entries, self.red_entries):
            entry.set("")

    def get_selected_heroes(self):
        ally = []
        enemy = []
        my_side = self.side_var.get()

        blue_names = [entry.get() for entry in self.blue_entries if entry.get()]
        red_names = [entry.get() for entry in self.red_entries if entry.get()]

        if my_side == "蓝方":
            ally_names = blue_names
            enemy_names = red_names
        else:
            ally_names = red_names
            enemy_names = blue_names

        for name in ally_names:
            pos = HERO_MAIN_POSITION.get(name)
            if pos is None:
                messagebox.showerror("错误", f"英雄「{name}」的位置未知，请检查输入或补充数据")
                return None, None
            ally.append({"name": name, "position": pos})

        for name in enemy_names:
            pos = HERO_MAIN_POSITION.get(name)
            if pos is None:
                messagebox.showerror("错误", f"英雄「{name}」的位置未知，请检查输入或补充数据")
                return None, None
            enemy.append({"name": name, "position": pos})

        return ally, enemy

    def do_recommend(self):
        pos_code = self.pos_var.get()
        pos_map = {"射": "发育路", "边": "对抗路", "野": "打野", "中": "中路", "辅": "游走"}
        my_position = pos_map.get(pos_code, "打野")

        ally, enemy = self.get_selected_heroes()
        if ally is None:
            return

        recs = recommend_heroes(my_position, ally, enemy, show_all=True)

        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not recs:
            self.tree.insert("", "end", values=("没有可推荐的英雄", "", "", "", "", ""))
            return

        pos_to_short = {"发育路": "射", "对抗路": "边", "打野": "野", "中路": "中", "游走": "辅"}

        for hero, main_pos, score, counter_list, be_countered_list, good_list, bad_list, threat in recs:
            # 构造英雄名显示：若主分路与推荐位置不同，则添加 (短标注)
            short_main = pos_to_short.get(main_pos, "") if main_pos else ""
            if short_main and short_main != pos_code:
                hero_display = f"{hero}({short_main})"
            else:
                hero_display = hero

            counter_str = ", ".join(counter_list) if counter_list else ""
            be_countered_str = ", ".join(be_countered_list) if be_countered_list else ""
            good_str = ", ".join(good_list) if good_list else ""
            bad_str = ", ".join(bad_list) if bad_list else ""
            threat_str = str(threat) if threat >= 0 else ""

            self.tree.insert("", "end", values=(hero_display, counter_str, be_countered_str, good_str, bad_str, threat_str))

if __name__ == "__main__":
    root = tk.Tk()
    app = BPApp(root)
    root.mainloop()