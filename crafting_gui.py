import tkinter as tk
from tkinter import PhotoImage
from configs import BACKGROUND_IMAGE, ITEM_IMAGES, GRID_POSITIONS, ITEM_START_POSITIONS, SCREEN_HEIGHT, SCREEN_WIDTH


class DraggableItem(tk.Label):
    """可拖拽物品"""
    def __init__(self, parent, image_path, x, y):
        self.parent = parent
        self.image = PhotoImage(file=image_path)
        super().__init__(parent, image=self.image, bd=0)
        self.x, self.y = x, y
        self.place(x=x, y=y)
        self.start_x, self.start_y = x, y  # 初始位置
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.lift()

    def on_drag(self, event):
        new_x = self.winfo_x() + event.x - self.image.width() // 2
        new_y = self.winfo_y() + event.y - self.image.height() // 2
        self.place(x=new_x, y=new_y)

    def on_release(self, event):
        """松开鼠标，检查是否放入合成网格"""
        x, y = self.winfo_x(), self.winfo_y()
        for grid_x, grid_y in GRID_POSITIONS:
            if abs(x - grid_x) < 30 and abs(y - grid_y) < 30:
                self.place(x=grid_x, y=grid_y)
                return
        self.place(x=self.start_x, y=self.start_y)  # 返回原位置


class CraftingGUI(tk.Tk):
    """合成台 GUI"""
    def __init__(self):
        super().__init__()
        self.title("Minecraft 合成台")
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.resizable(False, False)

        # 背景图片
        self.bg_image = PhotoImage(file=BACKGROUND_IMAGE)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 物品
        self.items = []
        for i, img in enumerate(ITEM_IMAGES):
            item = DraggableItem(self, img, *ITEM_START_POSITIONS[i])
            self.items.append(item)
