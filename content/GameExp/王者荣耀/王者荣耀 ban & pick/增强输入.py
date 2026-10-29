import tkinter as tk
from tkinter import ttk

# 尝试导入拼音库，若未安装则给出提示并回退到仅汉字匹配
try:
    from pypinyin import lazy_pinyin
    PINYIN_AVAILABLE = True
except ImportError:
    PINYIN_AVAILABLE = False
    print("提示：未安装 pypinyin，拼音匹配不可用。可运行 'pip install pypinyin' 安装。")

class AutocompleteDemo:
    def __init__(self, root):
        self.root = root
        root.title("英雄名自动补全（支持拼音）")
        root.geometry("400x300")

        # 示例英雄数据
        self.all_heroes = [
            "安琪拉", "李白", "李信", "韩信", "孙悟空", "鲁班七号",
            "后羿", "妲己", "王昭君", "貂蝉", "吕布",
            "诸葛亮", "赵云", "典韦", "夏侯惇", "花木兰"
        ]

        # 预计算拼音（若无拼音库则使用空列表）
        if PINYIN_AVAILABLE:
            self.pinyin_map = {hero: ''.join(lazy_pinyin(hero)) for hero in self.all_heroes}
        else:
            self.pinyin_map = {}

        # 输入框
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(root, textvariable=self.entry_var, width=30)
        self.entry.pack(pady=10)

        # 列表框
        self.listbox = tk.Listbox(root, height=8, width=30)
        self.listbox.pack(pady=5)

        # 绑定事件
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<Up>", self.on_up)
        self.entry.bind("<Down>", self.on_down)
        self.entry.bind("<Return>", self.on_enter)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # 保存当前匹配列表
        self.current_matches = self.all_heroes[:]
        self.update_listbox("")

    def matches_keyword(self, hero, keyword):
        """判断英雄是否匹配关键字（支持汉字和拼音）"""
        kw = keyword.lower()
        if kw in hero.lower():
            return True
        if PINYIN_AVAILABLE and kw in self.pinyin_map.get(hero, ''):
            return True
        return False

    def update_listbox(self, keyword):
        """根据关键字更新列表框"""
        self.listbox.delete(0, tk.END)
        matches = []
        for hero in self.all_heroes:
            if self.matches_keyword(hero, keyword):
                matches.append(hero)
        self.current_matches = matches
        for hero in matches:
            self.listbox.insert(tk.END, hero)
        if matches:
            self.listbox.selection_set(0)
            self.listbox.activate(0)

    def on_key_release(self, event):
        """输入框按键释放时更新候选列表（忽略上下键和回车）"""
        if event.keysym in ('Up', 'Down', 'Return'):
            return
        keyword = self.entry_var.get()
        self.update_listbox(keyword)

    def on_up(self, event):
        """按上键：列表框选中上一项"""
        if self.listbox.size() == 0:
            return "break"
        current = self.listbox.curselection()
        if current:
            idx = current[0]
            if idx > 0:
                new_idx = idx - 1
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(new_idx)
                self.listbox.activate(new_idx)
                self.listbox.see(new_idx)
        else:
            last = self.listbox.size() - 1
            self.listbox.selection_set(last)
            self.listbox.activate(last)
            self.listbox.see(last)
        return "break"

    def on_down(self, event):
        """按下键：列表框选中下一项"""
        if self.listbox.size() == 0:
            return "break"
        current = self.listbox.curselection()
        if current:
            idx = current[0]
            if idx < self.listbox.size() - 1:
                new_idx = idx + 1
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(new_idx)
                self.listbox.activate(new_idx)
                self.listbox.see(new_idx)
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.see(0)
        return "break"

    def on_enter(self, event):
        """按回车：将当前选中的英雄填入输入框并清空列表"""
        selected = self.listbox.curselection()
        if selected:
            hero = self.listbox.get(selected[0])
            self.entry_var.set(hero)
        elif self.listbox.size() > 0:
            hero = self.listbox.get(0)
            self.entry_var.set(hero)
        self.update_listbox("")  # 清空列表（也可以保留，按需）
        return "break"

    def on_listbox_select(self, event):
        """点击列表框项时自动填入输入框并清空列表"""
        selected = self.listbox.curselection()
        if selected:
            hero = self.listbox.get(selected[0])
            self.entry_var.set(hero)
            self.update_listbox("")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutocompleteDemo(root)
    root.mainloop()