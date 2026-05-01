# This py file is the main file of English helper by Xu Yueming.
"""@By 徐跃鸣@"""
import tkinter as tk
import tkinter.messagebox
import ttkbootstrap as ttk
from tkinter.colorchooser import askcolor
from ttkbootstrap.constants import *
from os import getcwd

from Word_search import English_word_search
from Flop import English_flop
from Crossword_puzzle import English_crossword_puzzle
from Bingo import English_bingo
from Word_challenge import English_word_challenge
# 导包

class GUI(object):
    """图形用户界面"""
    def __init__(self, main_window_size=(420, 400)):
        """初始化
            main_window_size -> tuple : 主窗口大小"""
        self.main_window_size = main_window_size  # 主窗口大小
        self.helps = [('括号里面字母什么意思', '某些菜单栏末尾的口号里面的字母是它的快捷键.如"帮助(H)"您可以先按下ALT键,会发现所有括号内的字母加上了下划线(这是为了区分有无按下),然后按下快捷键"H".亦可直接按下ALT+H.'),
                      ('打乱单词句子有什么用', '在长时间未加载出来时点击它,然后再重新生成,可能会增加生成效率,并且生成一个全新的字谜.')]  # 帮助中的信息
        
        self.window = ttk.Window(themename='morph')  # 主窗口
        self.window.title("Python English Helper By 徐跃鸣")  # 窗口标题
        self.window.geometry(f'{self.main_window_size[0]}x{self.main_window_size[1]}+{int((self.window.winfo_screenwidth() - self.main_window_size[0]) / 2)}+{int((self.window.winfo_screenheight() - self.main_window_size[1]) / 2)}')  # 窗口大小,出现在屏幕中央
        self.window.resizable(False, False)  # 不可以调节大小
        self.window.iconbitmap(r'.\icon.ico')  # 图标
        self.window.protocol("WM_DELETE_WINDOW", self.exit)  # 按下窗口右上角'×'
        self.font_names = sorted(list(tk.font.families()))  # 所有可用字体
        
        self.menubar = tk.Menu(self.window)  # 菜单栏
        self.helper_menu = tk.Menu(self.menubar, tearoff=0)  # 帮助菜单项
        for (x, y) in self.helps:  # 遍历帮助
            self.helper_menu.add_command(label=x, command=lambda: tk.messagebox.showinfo('帮助', y))  # 显示帮助
        self.helper_menu.add_separator()  # 分割线
        self.helper_menu.add_command(label='关于作者', command=lambda: tk.messagebox.showinfo('关于作者', '乐清市 乐成一中 七(13)班 徐跃鸣'))  # 关于作者
        self.helper_menu.add_command(label='关于程序', command=lambda: tk.messagebox.showinfo('关于程序', '本程序为英语帮助程序\n版本号:1.0.0\n主窗口大小:' + str(self.main_window_size) +
                                                                                          '\n使用python3.7.9编写\n声明:本程序仅为学习目的,不得运用于商业目的.如因违法使用本程序造成的损失,作者不承担责任!'))  # 关于程序
        self.menubar.add_cascade(label="帮助(H)", menu=self.helper_menu, underline=3)  # 帮助,快捷键ALT+H
        self.menubar.add_command(label='退出(Q)', command=self.exit, underline=3)  # 退出
        # self.menubar.add_command(label='DeBug', command=lambda: tk.messagebox.showinfo('DeBug', self.crossword_puzzle_words_color.get()+self.crossword_puzzle_NO_color.get()))  # DeBug
        self.window.config(menu=self.menubar)  # 添加菜单栏
        
        self.tab_main = ttk.Notebook(self.window)  # 主标签栏
        self.tab_crossword_puzzle = tk.Frame(width=self.main_window_size[1], height=self.main_window_size[0] - 80)
        self.tab_word_search = tk.Frame()
        self.tab_bingo = tk.Frame()
        self.tab_flop = tk.Frame()
        self.tab_word_challenge = tk.Frame()
        self.tab_crossword_puzzle.pack()
        self.tab_word_search.pack()
        self.tab_bingo.pack()
        self.tab_flop.pack()
        self.tab_word_challenge.pack()
        self.tab_main.add(self.tab_crossword_puzzle, text='Crossword Puzzle')
        self.tab_main.add(self.tab_word_search, text='Word Search')
        self.tab_main.add(self.tab_bingo, text='Bingo')
        self.tab_main.add(self.tab_flop, text='Flop')
        self.tab_main.add(self.tab_word_challenge, text='Word Challenge')
        self.tab_main.pack()
        
        self.crossword_puzzle = English_crossword_puzzle()  # 初始化纵横字谜
        self.crossword_puzzle_col_init = 20
        self.crossword_puzzle_row_init = 20
        self.crossword_puzzle_max_left_init = 0
        self.crossword_puzzle_lenth_init = 15
        self.crossword_puzzle_col = tk.StringVar(value=self.crossword_puzzle_col_init)
        self.crossword_puzzle_row = tk.StringVar(value=self.crossword_puzzle_row_init)
        self.crossword_puzzle_max_left = tk.StringVar(value=self.crossword_puzzle_max_left_init)
        self.crossword_puzzle_must_cross = tk.BooleanVar(value=True)
        self.crossword_puzzle_name = tk.StringVar(value='徐跃鸣')
        self.crossword_puzzle_from_module = tk.StringVar(value='Module 5201314')
        self.crossword_puzzle_title = tk.StringVar(value='Crossword puzzle')
        self.crossword_puzzle_NO_color = tk.StringVar(value='(255, 128, 128)')
        self.crossword_puzzle_words_color = tk.StringVar(value='(0, 0, 0)')
        self.crossword_puzzle_Chinese_font = tk.StringVar(value='宋体')
        self.crossword_puzzle_English_font = tk.StringVar(value='Arial')
        self.crossword_puzzle_lenth = tk.IntVar(value=self.crossword_puzzle_lenth_init)
        self.crossword_puzzle_made_puzzle = None
        self.crossword_puzzle_made_end_puzzle = None
        self.crossword_puzzle_made_prompt = None
        self.crossword_puzzle_made_left_out = None
        self.crossword_puzzle_path = tk.StringVar(value=fr'{getcwd()}\Crossword Puzzle.docx')
        self.crossword_puzzle_preview_NO_color = None
        self.crossword_puzzle_preview_words_color = None
        self.crossword_puzzle_preview_Chinese_font = None
        self.crossword_puzzle_preview_English_font = None
        self.crossword_puzzle_col_Spinbox = None
        self.crossword_puzzle_row_Spinbox = None
        
        self.word_search = English_word_search()  # 初始化单词查找
        pass
        
        self.bingo = English_bingo()  # 初始化Bingo
        pass
        
        self.flop = English_flop()  # 初始化翻牌游戏
        pass
        
        self.word_challenge = English_word_challenge()  # 初始化单词比赛
        pass
        
        self.crossword_puzzle_monty_settings = ttk.LabelFrame(self.tab_crossword_puzzle, text='Crossword Puzzle 设置', width=self.main_window_size[1], height=168, bootstyle=DANGER)
        self.crossword_puzzle_monty_preview = ttk.LabelFrame(self.crossword_puzzle_monty_settings, text='预览', width=50, height=50, labelanchor=N, bootstyle=SUCCESS)
        self.crossword_puzzle_monty_input = ttk.LabelFrame(self.tab_crossword_puzzle, text='输入单词句子', width=self.main_window_size[1], height=150, bootstyle=DANGER)
        self.crossword_puzzle_monty_make = ttk.LabelFrame(self.tab_crossword_puzzle, text='Crossword Puzzle 生成')
        self.crossword_puzzle_monty_solve = ttk.LabelFrame(self.tab_crossword_puzzle, text='Crossword Puzzle 解决')
        self.crossword_puzzle_monty_settings.grid(column=0, row=0)
        self.crossword_puzzle_monty_preview.place(x=300, y=80, width=90, height=65)
        self.crossword_puzzle_monty_input.grid(column=0, row=1)
        self.crossword_puzzle_monty_make.grid(column=0, row=2)
        self.crossword_puzzle_monty_solve.grid(column=0, row=3)
        
        ttk.Label(self.crossword_puzzle_monty_settings, text='列数:', bootstyle=INFO, font=('宋体', '11')).place(x=0, y=3, width=40)
        self.crossword_puzzle_col_Spinbox = ttk.Spinbox(self.crossword_puzzle_monty_settings, from_=15, to=40,
                                                        textvariable=self.crossword_puzzle_col, font=('Arial', '10'), validate="focusout",  # 焦点被移出
                                                        validatecommand=(lambda: self.number_validate(self.crossword_puzzle_col_Spinbox, self.crossword_puzzle_col, self.crossword_puzzle_col_init)))
        self.crossword_puzzle_col_Spinbox.place(x=45, y=0, width=63, height=25)
        ttk.Label(self.crossword_puzzle_monty_settings, text='行数:', bootstyle=INFO, font=('宋体', '11')).place(x=113, y=3, width=40)
        self.crossword_puzzle_row_Spinbox = ttk.Spinbox(self.crossword_puzzle_monty_settings, from_=15, to=40,
                                                        textvariable=self.crossword_puzzle_row, font=('Arial', '10'), validate="focusout",  # 焦点被移出
                                                        validatecommand=(lambda: self.number_validate(self.crossword_puzzle_row_Spinbox, self.crossword_puzzle_row, self.crossword_puzzle_row_init)))
        self.crossword_puzzle_row_Spinbox.place(x=158, y=0, width=63, height=25)
        self.crossword_puzzle_must_cross_button = ttk.Checkbutton(self.crossword_puzzle_monty_settings, variable=self.crossword_puzzle_must_cross, onvalue=True, offvalue=False, bootstyle='round-toggle')
        self.crossword_puzzle_must_cross_button.selection_own()
        self.crossword_puzzle_must_cross_button.place(x=236, y=-5, width=25, height=35)
        ttk.Label(self.crossword_puzzle_monty_settings, text='必须有交叉', bootstyle=INFO, font=('宋体', '11')).place(x=261, y=3, width=80)
        
        ttk.Label(self.crossword_puzzle_monty_settings, text='姓名:', bootstyle=INFO, font=('宋体', '11')).place(x=0, y=33, width=40)
        ttk.Entry(self.crossword_puzzle_monty_settings, textvariable=self.crossword_puzzle_name).place(x=45, y=30, width=50, height=25)
        ttk.Label(self.crossword_puzzle_monty_settings, text='来自模块:', bootstyle=INFO, font=('宋体', '11')).place(x=100, y=31, width=85, height=25)
        ttk.Entry(self.crossword_puzzle_monty_settings, textvariable=self.crossword_puzzle_from_module).place(x=175, y=30, width=113, height=25)
        
        ttk.Label(self.crossword_puzzle_monty_settings, text='标题:', bootstyle=INFO, font=('宋体', '11')).place(x=0, y=63, width=45)
        ttk.Entry(self.crossword_puzzle_monty_settings, textvariable=self.crossword_puzzle_title).place(x=50, y=60, width=120, height=25)
        ttk.Label(self.crossword_puzzle_monty_settings, text='最多舍去个数:', bootstyle=INFO, font=('宋体', '11')).place(x=170, y=63, width=100)
        self.crossword_puzzle_max_left_out_Spinbox = ttk.Spinbox(self.crossword_puzzle_monty_settings, from_=0, to=5,
                                                                 textvariable=self.crossword_puzzle_max_left, font=('Arial', '10'), validate="focusout",  # 焦点被移出
                                                                 validatecommand=(lambda: self.number_validate(self.crossword_puzzle_max_left_out_Spinbox, self.crossword_puzzle_max_left, self.crossword_puzzle_max_left_init)))
        self.crossword_puzzle_max_left_out_Spinbox.place(x=275, y=60, width=43, height=25)
        
        self.crossword_puzzle_preview_Chinese_font = tk.Label(self.crossword_puzzle_monty_preview, text='我喜', font=(self.crossword_puzzle_Chinese_font, '11', 'bold'))
        self.crossword_puzzle_preview_Chinese_font.config(fg='#E52527')
        self.crossword_puzzle_preview_Chinese_font.place(x=0, y=-3, width=45, height=20)
        ttk.Label(self.crossword_puzzle_monty_settings, text='中文字体:', bootstyle=INFO, font=('宋体', '11')).place(x=0, y=91, width=75)
        self.crossword_puzzle_Chinese_font_combobox = ttk.Combobox(self.crossword_puzzle_monty_settings, textvariable=self.crossword_puzzle_Chinese_font, values=self.font_names, state='readonly')
        self.crossword_puzzle_Chinese_font_combobox.bind('<<ComboboxSelected>>', lambda event: self.crossword_puzzle_preview_Chinese_font.config(font=(self.crossword_puzzle_Chinese_font.get(),)))  # 绑定虚拟事件,使选择后更改预览区的字体
        self.crossword_puzzle_Chinese_font_combobox.place(x=75, y=88, width=50, height=25)
        
        self.crossword_puzzle_preview_English_font = tk.Label(self.crossword_puzzle_monty_preview, text='LIKE', font=(self.crossword_puzzle_English_font, '13', 'bold'))
        self.crossword_puzzle_preview_English_font.config(fg='#FFC14F')
        self.crossword_puzzle_preview_English_font.place(x=38, y=-5, width=50, height=20)
        ttk.Label(self.crossword_puzzle_monty_settings, text='英文字体:', bootstyle=INFO, font=('宋体', '11')).place(x=125, y=91, width=75)
        self.crossword_puzzle_English_font_combobox = ttk.Combobox(self.crossword_puzzle_monty_settings, textvariable=self.crossword_puzzle_English_font, values=self.font_names, state='readonly')
        self.crossword_puzzle_English_font_combobox.bind('<<ComboboxSelected>>', lambda event: self.crossword_puzzle_preview_English_font.config(font=(self.crossword_puzzle_English_font.get(),)))
        self.crossword_puzzle_English_font_combobox.place(x=200, y=88, width=95, height=25)
        
        self.crossword_puzzle_preview_NO_color = tk.Label(self.crossword_puzzle_monty_preview, text='欢我', font=(self.crossword_puzzle_Chinese_font, '11', 'bold'))
        self.crossword_puzzle_preview_NO_color.config(fg=self.RGB_color_to_HEX_color(self.crossword_puzzle_NO_color.get()))
        self.crossword_puzzle_preview_NO_color.place(x=0, y=20, width=45, height=20)
        ttk.Label(self.crossword_puzzle_monty_settings, text='空白单元格颜色:', bootstyle=INFO, font=('宋体', '11')).place(x=0, y=120, width=115)
        ttk.Button(self.crossword_puzzle_monty_settings, text='选择', bootstyle=(PRIMARY, "outline-toolbutton"), command=self.crossword_puzzle_choose_NO_color).place(x=120, y=118, width=50, height=25)
        
        self.crossword_puzzle_preview_words_color = tk.Label(self.crossword_puzzle_monty_preview, text='ME', font=(self.crossword_puzzle_English_font, '13', 'bold'))
        self.crossword_puzzle_preview_words_color.config(fg=self.RGB_color_to_HEX_color(self.crossword_puzzle_words_color.get()))
        self.crossword_puzzle_preview_words_color.place(x=43, y=18, width=45, height=20)
        ttk.Label(self.crossword_puzzle_monty_settings, text='文字颜色:', bootstyle=INFO, font=('宋体', '11')).place(x=170, y=120, width=100)
        ttk.Button(self.crossword_puzzle_monty_settings, text='选择', bootstyle=(PRIMARY, "outline-toolbutton"), command=self.crossword_puzzle_choose_words_color).place(x=245, y=118, width=50, height=25)

        ttk.Label(self.crossword_puzzle_monty_input, text='个数:', bootstyle=SUCCESS, font=('宋体', '11')).place(x=4, y=0, width=50, height=25)
        self.crossword_puzzle_lenth_Spinbox = ttk.Spinbox(self.crossword_puzzle_monty_input, from_=1, to=20,
                                                          textvariable=self.crossword_puzzle_lenth, font=('Arial', '10'), validate="focusout",  # 焦点被移出
                                                          validatecommand=(lambda: self.number_validate(self.crossword_puzzle_lenth_Spinbox, self.crossword_puzzle_lenth, self.crossword_puzzle_lenth_init)))
        self.crossword_puzzle_lenth_Spinbox.place(x=0, y=25, width=50, height=25)
        
        ttk.Button(self.crossword_puzzle_monty_input, text='导出', bootstyle=SUCCESS, command=self.crossword_puzzle_word_sentence_export).place(x=0, y=55, width=50, height=25)
        ttk.Button(self.crossword_puzzle_monty_input, text='导入', bootstyle=SUCCESS, command=self.crossword_puzzle_word_sentence_import).place(x=0, y=81, width=50, height=25)
        
        # ttk.Label(self.crossword_puzzle_monty_settings, text='保存路径:', bootstyle=INFO, font=('宋体', '11')).place(x=165, y=60, width=85, height=25)
        # ttk.Entry(self.crossword_puzzle_monty_settings, textvariable=self.crossword_puzzle_path).place(x=240, y=60, width=100, height=25)
        # ttk.Button(self.crossword_puzzle_monty_settings, text='选择', command=self.crossword_puzzle_ask_save_path).place(x=340, y=60, width=50, height=25)
        
        tk.Label(self.tab_word_search, text='努力研发中……').pack()
        tk.Label(self.tab_bingo, text='努力研发中……').pack()
        tk.Label(self.tab_flop, text='努力研发中……').pack()
        tk.Label(self.tab_word_challenge, text='努力研发中……')
        tk.Label(self.tab_word_challenge, text='努力研发中……')
    
    def crossword_puzzle_choose_NO_color(self):
        """选择空白单元格颜色"""
        color = self.choose_color()  # 选择一个颜色
        if color[0] is not None:  # 选择了了一个眼色
            self.crossword_puzzle_NO_color.set(str(color[0]))  # 赋值颜色
            self.crossword_puzzle_preview_NO_color.config(fg=self.RGB_color_to_HEX_color(tuple(map(int, color[0]))))  # 更改预览区颜色
    
    def crossword_puzzle_choose_words_color(self):
        """选择单词颜色"""
        color = self.choose_color()  # 选择一个颜色
        if color[0] is not None:  # 选择了了一个眼色
            self.crossword_puzzle_words_color.set(str(color[0]))  # 赋值颜色
            self.crossword_puzzle_preview_words_color.config(fg=self.RGB_color_to_HEX_color(tuple(map(int, color[0]))))  # 更改预览区颜色
    
    def crossword_puzzle_ask_save_path(self):
        """询问保存路径"""
        # lambda: self.file_path.set(abspath(asksaveasfilename(initialdir=getcwd(), title='选择保存路径',
        #                                                      defaultextension='*.docx', filetypes=[('Documentx File', '*.docx'), ('Document File', '*.doc'), ('All Files', '*.*')])))
    
    def crossword_puzzle_word_sentence_export(self):
        """导出单词句子"""
        pass
    
    def crossword_puzzle_word_sentence_import(self):
        """导入单词句子"""
        pass
    
    def number_validate(self, entry, intvar, init_value):
        """验证输入框输入的是否为数字
            entry -> tkinter.Entry : 需要判断的输入框
            intvar -> tk.IntVar : 与输入框绑定的数值
            init_value -> int : 默认值"""
        if (not entry.get().isdigit()) or (int(entry.get()) < 0):  # 不是纯正整数
            tk.messagebox.showwarning('提示', f'请输入纯正整数!而不是"{entry.get()}"')  # 提示
            intvar.set(init_value)  # 更改成默认值
            entry.focus_set()  # 焦点移回
            return False
        return True
    
    def choose_color(self):
        """选择一种颜色并返回"""
        return askcolor(title='选择颜色')  # 返回选择的颜色
    
    def RGB_color_to_HEX_color(self, rgb_color):
        """将RGB颜色转化为十六进制颜色
            rgb_color -> str或tuple : 待转化的RGB颜色"""
        if type(rgb_color) == str:
            rgb_color = rgb_color[1:-1].split(', ')  # 去除左右括号并分割
        strs = '#'  # 结果
        for i in rgb_color:  # 遍历
            strs += str(hex(int(i)))[-2:].replace('x', '0')  # 每一位
        return strs  # 返回
    
    def exit(self):
        """退出程序"""
        # if tk.messagebox.askyesno(title='警告', message='真的要退出本程序吗?'):  # 询问是否真的要退出,而不是不小心点到了
        self.window.destroy()  # 消除主程序窗口
    
    def start(self):
        """开始"""
        self.window.mainloop()  # 循环

def main():
    """主程序"""
    gui = GUI()  # 初始化
    gui.start()  # 主循环

if __name__ == '__main__':  # 直接运行本程序
    main()  # 主函数