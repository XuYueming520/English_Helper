#This py file is the main file of Endlish helper by Xu Yueming.
'''@By 徐跃鸣@'''
from random import randint,shuffle
from os.path import isfile,abspath
from os import popen,getcwd
from threading import Thread

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter.filedialog import asksaveasfilename,askopenfile
from tkinter.simpledialog import askstring
from tkinter.colorchooser import askcolor
# from sys import exit

import Crossword_puzzle,Word_search
#导包

class GUI(object):
    '''GUI'''
    def __init__(self,size=(410,280)):
        '''初始化
            size -> tuple : 窗口大小'''
        self.helps = [('打乱单词句子有什么用','在长时间未加载出来时点击它,然后再重新生成,可能会增加生成效率,并且生成一个全新的字谜')] #帮助中的信息
        
        self.crossword_puzzle = Crossword_puzzle.English_crossword_puzzle()
        self.word_search = Word_search.English_word_search() #初始化
        self.window = tk.Tk() #主窗口
        self.window.title("Python Endlish Helper By 徐跃鸣") #窗口标题
        self.window.geometry(f'{size[0]}x{size[1]}+{int((self.window.winfo_screenwidth()-size[0])/2)}+{int((self.window.winfo_screenheight()-size[1])/2)}') #窗口大小,出现在屏幕中央
        self.window.resizable(0,0) #不可以调节大小
        self.window.iconbitmap(r'.\icon.ico') #图标
        
        self.menubar = tk.Menu(self.window) #菜单栏
        self.helper_menu = tk.Menu(self.menubar, tearoff=0) #帮助菜单项
        for (x,y) in self.helps: #遍历帮助
            self.helper_menu.add_command(label=x,command=lambda:tk.messagebox.showinfo('帮助',y)) #显示帮助
        self.helper_menu.add_separator() #分割线
        self.helper_menu.add_command(label='关于作者',command=
                                     lambda:tk.messagebox.showinfo('关于作者','乐清市 乐成一中 七(13)班 徐跃鸣')) #关于作者
        self.helper_menu.add_command(label='关于程序',command=
                                     lambda:tk.messagebox.showinfo('关于程序','本程序为英语帮助程序\nvision:1.0.0\nmain window size:'+str(size)+\
                                     '\n使用python3.7.9编写\n声明:本程序仅为学习目的,不得运用于商业目的.如因违法使用本程序造成的损失,作者不承担责任!')) #关于程序
        self.menubar.add_cascade(label="帮助(H)",menu=self.helper_menu,underline=3) #帮助
        self.menubar.add_command(label='退出(Q)',command=self.window.destroy,underline=3) #退出
#         self.menubar.add_command(label='DeBug',command=lambda:tk.messagebox.showinfo('DeBug',' '.join(self.words)+'\n'+' '.join(self.sentences))) #DeBug
        self.window.config(menu=self.menubar) #添加菜单栏
        
        self.tab_main = ttk.Notebook(self.window) #主标签栏
        self.tab_crossword_puzzle = tk.Frame() #Crossword Puzzle
        self.tab_find_word = tk.Frame() #Find Word
        
        self.puzzle = None #字谜答案
        self.end_puzzle = None #字谜
        self.prompt = None #句子
        self.left_out = None #舍去个数
        
        self.monty0 = ttk.LabelFrame(self.tab_crossword_puzzle,text='puzzle设置')
        self.monty0.grid(column=0,row=0)
        
        self.col = tk.IntVar(value=20)
        tk.Label(self.monty0,text='列数:').grid(column=0,row=0)
        tk.Entry(self.monty0,bd=2,textvariable=self.col,width=8).grid(column=1,row=0)
        
        self.row = tk.IntVar(value=20)
        tk.Label(self.monty0,text='行数:').grid(column=2,row=0)
        tk.Entry(self.monty0,bd=2,textvariable=self.row,width=8).grid(column=3,row=0)
        
        self.must_cross = tk.StringVar(value='True')
        self.cross = ttk.Checkbutton(self.monty0,width=12,text='必须有交叉',variable=self.must_cross,onvalue='True',offvalue='False')
        self.cross.selection_own()
        self.cross.grid(column=4,row=0,sticky='w')
        
        self.name = tk.StringVar(value='徐跃鸣')
        tk.Label(self.monty0,text='姓名:').grid(column=0,row=1)
        tk.Entry(self.monty0,bd=2,textvariable=self.name,width=8).grid(column=1,row=1)
        
        self.from_model = tk.StringVar(value='Module 5201314')
        tk.Label(self.monty0,text='来自模块:').grid(column=2,row=1)
        tk.Entry(self.monty0,bd=2,textvariable=self.from_model,width=28).grid(column=3,row=1,columnspan=3)
        
        self.No_color = tk.StringVar(value='ff8080')
        tk.Label(self.monty0,text='空白颜色:').grid(column=0,row=2)
        tk.Entry(self.monty0,bd=2,textvariable=self.No_color,width=8).grid(column=1,row=2)
        tk.Button(self.monty0,text='选择',width=9,command=self.choose_color).grid(column=2,row=2)
        
        self.file_path = tk.StringVar(value=fr"{getcwd()}\Crossword puzzle.docx")
        tk.Label(self.monty0,text='word路径:').grid(column=3,row=2)
        tk.Entry(self.monty0,bd=2,textvariable=self.file_path,width=14).grid(column=4,row=2)
        tk.Button(self.monty0,text='选择',width=3,command=
                  lambda:self.file_path.set(abspath(asksaveasfilename(initialdir=getcwd(),title='选择保存路径',
                  defaultextension='*.docx',filetypes=[('Documentx File','*.docx'),('Document File', '*.doc'),('All Files','*.*')])))).grid(column=5,row=2)
        
        self.monty1 = ttk.LabelFrame(self.tab_crossword_puzzle,text='puzzle输入单词句子')
        self.monty1.grid(column=0,row=1,pady=10)
        
        self.num = tk.IntVar(value=10)
        tk.Label(self.monty1,text='个数:').grid(column=0,row=0)
        tk.Entry(self.monty1,bd=2,textvariable=self.num,width=2).grid(column=1,row=0)
        
        self.words = []
        self.sentences = []
        tk.Button(self.monty1,text='输入',width=3,command=self.input_word_sentence).grid(column=2,row=0)
        
        tk.Button(self.monty1,text='查看',width=3,command=
                  lambda:tk.messagebox.showinfo(title='单词句子',message='\n'.join([f'{self.words[i]} {self.sentences[i]}' for i in range(len(self.words))]))).grid(column=3,row=0)
        
        tk.Button(self.monty1,text='导入',width=3,command=self.load_word_sentence).grid(column=4,row=0)
        
        tk.Button(self.monty1,text='打乱',width=3,
                  command=self.shuffle).grid(column=5,row=0)
        
        self.monty2 = ttk.LabelFrame(self.tab_crossword_puzzle,text='puzzle')
        self.monty2.grid(column=0,row=2)
        
        tk.Button(self.monty2,text='生成puzzle',command=self.make_puzzle).grid(column=0,row=0)
        
        tk.Button(self.monty2,text='查看puzzle',command=self.show_puzzle).grid(column=1,row=0)
        
        tk.Button(self.monty2,text='保存puzzle',command=lambda:self.crossword_puzzle.save_puzzle(self.end_puzzle,self.prompt,path=self.file_path.get(),name=self.name.get(),where_from=self.from_model.get(),NOcolor=self.No_color.get()) if self.end_puzzle != None else tk.messagebox.showerror(title='错误',message='请先输入单词 句子!')).grid(column=2,row=0)
        
        tk.Button(self.monty2,text='打开puzzle',command=lambda:Thread(target=lambda:popen(self.file_path.get()).read()).start()).grid(column=3,row=0)
        
        tk.Label(self.tab_find_word,text='努力研发中……').pack()
        
        self.tab_crossword_puzzle.place()
        self.tab_find_word.place()
        self.tab_main.add(self.tab_crossword_puzzle,text='Crossword Puzzle')
        self.tab_main.add(self.tab_find_word,text='Find Word')
        self.tab_main.pack()
        ###待注释###
#         self.first = True #是否第一次运行
    
    def shuffle(self):
        '''打乱单词句子'''
        self.crossword_puzzle.shuffle_list()
        self.words = []
        self.sentences = []
        for (w,s) in self.crossword_puzzle.list:
            self.words.append(w)
            self.sentences.append(s)
    
    def load_word_sentence(self):
        '''从文件导入单词句子'''
        i = 0
        f = askopenfile(initialdir=getcwd(),title='选择导入路径',
                  defaultextension='*.txt',filetypes=[('Txt File','*.txt'),('All Files','*.*')])
        if f is None:
            return
        self.words = []
        self.sentences = []
        for l in f.read().split('\n'):
            self.words.append(l.split(' ')[0])
            self.sentences.append(' '.join(l.split(' ')[1:]))
            i += 1
        self.num.set(i)
        for x in range(len(self.words)):
            self.crossword_puzzle.list.append((self.words[x],self.sentences[x]))
    
    def choose_color(self):
        '''选择颜色'''
        c = askcolor(title='选择颜色')
        if c[1] != None:
            self.No_color.set(c[1][1:])
    
    def show_puzzle(self,sizex=40,sizey=40):
        '''查看puzzle'''
        if self.puzzle == None:
            tk.messagebox.showerror('错误','请先输入单词,句子!')
        else:
            self.new_window = tk.Toplevel() #在新窗口查看
            self.new_window.title('Python Crossword Puzzle By 徐跃鸣')
            size = (self.col.get()*sizex,self.row.get()*sizey)
            self.new_window.geometry(fr"{size[0]}x{size[1]+40}+{int((self.window.winfo_screenwidth()-size[0])/2)}+{int((self.window.winfo_screenheight()-size[1]-40)/2)}")
            self.new_window.resizable(0,0)
            
            c = tk.Canvas(self.new_window,bg='#'+self.No_color.get())
            c.config(width=size[0],height=size[1])
            
            for col in range(len(self.crossword_puzzle.puzzle)):
                for row in range(len(self.crossword_puzzle.puzzle[0])):
                    self.draw_cell(c=row,r=col,sizex=sizex,sizey=sizey,canvas=c)
            
            c.grid(column=0,row=0)
            self.crossword_puzzle.print_puzzle(self.end_puzzle,self.prompt)
            self.crossword_puzzle.print_puzzle(self.puzzle,self.prompt)
            tk.Button(self.new_window,text='查看句子',command=self.see_sentences).grid(column=0,row=1)
    
    def draw_cell(self,c,r,sizex,sizey,canvas):
        '''画一个单元格'''
        start_x = r * sizex
        start_y = c * sizey
        end_x = start_x + sizex
        end_y = start_y + sizey
        #方框四角坐标
        
        if c == 0: #第一列左上角
            x = ''
            for s in str(r): #避免多位数
                x += self.crossword_puzzle.docx.dict[int(s)]
            canvas.create_text((start_x+3,start_y+3),font=('微软雅黑',5,'bold'),text=x)
        elif r == 0: #第一行左上角,但不是第一列
            x = ''
            for s in str(c): #避免多位数
                x += self.crossword_puzzle.docx.dict[int(s)]
            canvas.create_text((start_x+3,start_y+3),font=('微软雅黑',5,'bold'),text=x)
        
        if self.crossword_puzzle.end_puzzle[c][r] == None: #单词隐藏的字母
            canvas.create_rectangle((start_x,start_y,end_x,end_y),fill='white',outline='white',width=1)
        elif self.crossword_puzzle.end_puzzle[c][r] == self.crossword_puzzle.No: #空的
            canvas.create_rectangle((start_x,start_y,end_x,end_y),fill='#'+self.No_color.get(),outline='white',width=1)
        else: #字母
            canvas.create_rectangle((start_x,start_y,end_x,end_y),fill='white',outline='white',width=1)
            canvas.create_text((start_x+int(sizex/2),start_y+int(sizey/2)),font=('微软雅黑',15,'bold'),text=self.crossword_puzzle.end_puzzle[c][r])
    
    def see_sentences(self):
        '''查看句子'''
        s = 'Cross:\n'
        for (k,v) in self.crossword_puzzle.prompt[1].items():
            s += str(k) + ':' + v + '\n'
        tk.messagebox.showinfo(title='Cross',message=s)
        
        s = 'Down:\n'
        for (k,v) in self.crossword_puzzle.prompt[0].items():
            s += str(k) + ':' + v + '\n'
        tk.messagebox.showinfo(title='Down',message=s)
    
    def make_puzzle(self):
        '''生成puzzle'''
        if self.words == []:
            tk.messagebox.showerror(title='错误',message='请先输入单词 句子!')
        else:
            self.crossword_puzzle.col = self.col.get()
            self.crossword_puzzle.row = self.row.get()
            self.crossword_puzzle.puzzle = [[self.crossword_puzzle.No for _ in range(self.crossword_puzzle.row)] for _ in range(self.crossword_puzzle.col)]
            self.crossword_puzzle.end_puzzle = [[self.crossword_puzzle.No for _ in range(self.crossword_puzzle.row)] for _ in range(self.crossword_puzzle.col)]
            self.crossword_puzzle.prompt = {0:{},1:{}}
            self.crossword_puzzle.words = []
            self.crossword_puzzle.get_word_sentence(words=self.words,sentences=self.sentences)
            self.puzzle,self.end_puzzle,self.prompt,self.left_out = self.crossword_puzzle.make_puzzle(bool(self.must_cross.get()))
            print('\rdone.')
    
    def input_word_sentence(self):
        '''输入'''
        self.words = []
        self.sentences = []
        self.crossword_puzzle.list = []
        self.crossword_puzzle.words = []
        for i in range(self.num.get()):
            result = askstring(title=f'输入数据{i+1}个',prompt='请输入单词 句子：',initialvalue='word sentence')
            if result == None:
                return
            result = result.split(' ')
            while result[0] in self.words or result[1] in self.sentences:
                tk.messagebox.showwarning(title='警告',message='请输入不同的单词or句子!')
                result = askstring(title=f'输入数据{i}',prompt='请输入单词 句子：',initialvalue='word sentence')
            self.words.append(result[0])
            self.sentences.append(' '.join(result[1:]))
        for x in range(len(self.words)):
            self.crossword_puzzle.list.append((self.words[x],self.sentences[x]))
    
    def start(self):
        '''开始'''
        self.window.mainloop()

def main():
    '''主程序'''
    gui = GUI() #初始化
    gui.start() #主循环

if __name__ == '__main__': #直接运行本程序
    main() #主函数