# Author: Acer Zhang
# Datetime:2021/10/8 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import threading
import traceback
import gc

import tkinter
import tkinter.font
from tkinter import ttk
from tkinter.messagebox import showerror


class ProgressbarFrame:
    def __init__(self,
                 bind_fuc,
                 max_step: int,
                 default_text: str = "正在准备",
                 title: str = "初始化程序 - QPT",
                 icon=None):
        from ttkbootstrap import Style

        self.scale = 1. / (max_step + 1)
        self.count = 0
        # 窗体构建
        self.root = tkinter.Tk()
        self.root.geometry("666x25")
        self.root.style = Style("lumen")
        self.root.title(title)
        self.root.wm_resizable(False, False)
        self.root.iconbitmap(icon)
        default_font = tkinter.font.nametofont("TkDefaultFont")
        # ToDo 此处需考虑字体在不同操作系统兼容性
        default_font.configure(family="等线", size=10)
        self.root.option_add("*Font", "TkDefaultFont")

        self.progressbar_var = tkinter.IntVar(self.root, value=0)
        self.label_var = tkinter.StringVar(self.root, value=default_text)
        self.value_var = tkinter.StringVar(self.root, value="进度" + f"{0:.2f} %".rjust(10, " "))
        self.progressbar_var.trace("w", self.progressbar_var_trace)

        label = ttk.Label(self.root,
                          textvariable=self.label_var,
                          style="TLabel",
                          width=20)
        label.pack(side="left", padx=5)

        progressbar = ttk.Progressbar(self.root,
                                      variable=self.progressbar_var,
                                      style="Striped.Horizontal.TProgressbar")
        progressbar.pack(side="left", fill="x", expand="yes", padx=5, pady=2)

        value = ttk.Label(self.root,
                          textvariable=self.value_var,
                          style="TLabel",
                          width=12)
        value.pack(side="left", fill="x", padx=1)

        self.thread = None

        def render():
            def func(self):
                try:
                    bind_fuc(self)
                    self.step("加载完毕")
                except Exception as e:
                    msg = traceback.format_exc()
                    showerror(title="发生异常 - QPT提示", message=f"简略异常说明:\n{e}\n\n完整报错信息如下：\n{msg}")
                finally:
                    self.close()
                    gc.collect()
                return func

            self.thread = threading.Thread(target=func, args=(self,))
            self.thread.setDaemon(True)
            self.thread.start()

        self.root.after(ms=32, func=render)

        self.root.mainloop()

    def progressbar_var_trace(self, *args):
        v = self.progressbar_var.get()
        self.value_var.set(f"进度 {v:.2f} %")

    def close(self):
        self.root.destroy()
        # self.root.quit()

    def step(self, text: str = None):
        if text:
            self.label_var.set(text)
        self.progressbar_var.set(self.scale * (self.count + 1) * 100)
        self.count += 1


if __name__ == '__main__':
    import time


    def foo(self):
        for i in range(10):
            print(2)
            time.sleep(0.2)
            self.step()
        self.close()


    ProgressbarFrame(foo, 10)
