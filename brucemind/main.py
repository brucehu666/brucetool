import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from yaml import safe_load, dump

class MindMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BruceMind - 思维导图工具")
        self.root.geometry("800x600")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建树状视图
        self.create_treeview()
        
        # 初始化数据结构
        self.mind_map_data = {}
    
    def create_toolbar(self):
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # 添加按钮
        ttk.Button(toolbar, text="新建节点", command=self.add_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="删除节点", command=self.delete_node).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="保存到YAML", command=self.save_to_yaml).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="从YAML加载", command=self.load_from_yaml).pack(side=tk.LEFT, padx=2)
    
    def create_treeview(self):
        # 创建包含树状视图和滚动条的框架
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建树状视图，设置为从左到右的显示方式
        self.tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 设置自定义样式
        style = ttk.Style()
        style.configure("Custom.Treeview", indent=40)  # 增加缩进以使节点间距更大
        
        # 绑定双击事件用于编辑节点
        self.tree.bind('<Double-1>', self.edit_node)
        
        # 添加水平滚动条
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 添加垂直滚动条
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置树状视图的滚动
        self.tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
    
    def add_node(self):
        selected = self.tree.selection()
        parent = "" if not selected else selected[0]
        new_node = self.tree.insert(parent, 'end', text="新节点")
        self.tree.see(new_node)
    
    def delete_node(self):
        selected = self.tree.selection()
        if selected:
            if messagebox.askyesno("确认", "确定要删除选中的节点吗？"):
                for item in selected:
                    self.tree.delete(item)
    
    def edit_node(self, event):
        item = self.tree.selection()[0]
        if item:
            x, y, w, h = self.tree.bbox(item)
            
            # 创建编辑框
            entry = ttk.Entry(self.tree)
            entry.insert(0, self.tree.item(item, 'text'))
            entry.select_range(0, tk.END)
            
            def save_edit():
                if entry.winfo_exists():
                    self.tree.item(item, text=entry.get())
                    entry.destroy()
            
            def handle_return(event):
                save_edit()
                # 创建同级节点
                parent = self.tree.parent(item)
                new_node = self.tree.insert(parent, 'end', text="新节点")
                self.tree.see(new_node)
                self.edit_node(None)  # 立即编辑新节点
            
            def handle_tab(event):
                save_edit()
                # 创建子节点
                new_node = self.tree.insert(item, 'end', text="新节点")
                self.tree.see(new_node)
                self.edit_node(None)  # 立即编辑新节点
                return 'break'  # 阻止默认的Tab行为
            
            entry.bind('<Return>', handle_return)
            entry.bind('<Tab>', handle_tab)
            entry.bind('<FocusOut>', lambda e: save_edit())
            entry.place(x=x, y=y, width=w, height=h)
            entry.focus_set()
            
            # 绑定树视图的点击事件，当点击空白处时保存编辑
            def handle_tree_click(event):
                if entry.winfo_exists():
                    clicked_item = self.tree.identify('item', event.x, event.y)
                    if not clicked_item:  # 点击了空白处
                        save_edit()
            
            self.tree.bind('<Button-1>', handle_tree_click)
            entry.bind('<Destroy>', lambda e: self.tree.bind('<Button-1>', self.edit_node))  # 恢复原始绑定
    
    def save_to_yaml(self):
        try:
            data = self._tree_to_dict("")
            with open("mindmap.yaml", "w", encoding="utf-8") as f:
                dump(data, f, allow_unicode=True)
            messagebox.showinfo("成功", "数据已保存到mindmap.yaml")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{str(e)}")
    
    def load_from_yaml(self):
        try:
            with open("mindmap.yaml", "r", encoding="utf-8") as f:
                data = safe_load(f)
            self.tree.delete(*self.tree.get_children())
            self._dict_to_tree(data, "")
            messagebox.showinfo("成功", "数据已从mindmap.yaml加载")
        except Exception as e:
            messagebox.showerror("错误", f"加载失败：{str(e)}")
    
    def _tree_to_dict(self, node):
        result = {}
        children = self.tree.get_children(node)
        
        if not node:  # 根节点
            if children:
                result = {self.tree.item(child, 'text'): 
                         self._tree_to_dict(child) for child in children}
        else:
            for child in children:
                result[self.tree.item(child, 'text')] = self._tree_to_dict(child)
        
        return result
    
    def _dict_to_tree(self, data, parent):
        for key, value in data.items():
            node = self.tree.insert(parent, 'end', text=key)
            if isinstance(value, dict):
                self._dict_to_tree(value, node)

def main():
    root = tk.Tk()
    app = MindMapApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()