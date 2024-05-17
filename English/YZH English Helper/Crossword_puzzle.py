# This py file is for making and solving crossword puzzle of English helper by Xu Yueming.
"""@ By 徐跃鸣 @"""
from random import shuffle
from time import time, sleep
from enum import Enum
from IO import print, input, Fore, Back, debug, Style
from random import shuffle

class Crossword_puzzle_saver:
    pass

class Crossword_puzzle_maker:
    """
    英语字谜生成器
    """
    
    class Word:
        """
        单元格
        """
        
        class Type(Enum):
            """
            单元格类型
            """
            WHITE = 1
            HIDE = 2
            WORD = 3
        
        def __init__(self, tp: Type, word: str = ' ', dirc: int = -1, ptd: int = 0, multi: bool = False) -> None:
            """
            初始化

            Args:
                word (str): 这个单元格的字母
                tp (Type): 这个单元格的类型
                dirc (int): 这个单元格的方向 0b10 表示横向 0b01 表示纵向 0b00 表示不确定
                ptd (int): 这个单元格是否是某个单词的一端，方向 0b0001 向左 0b0010 向右 0b0100 向上 0b1000 向下
                multi (bool): 这个单元格是否同时存在大小写
            """
            if tp == self.Type.WHITE:
                self.type: Crossword_puzzle_maker.Word.Type = self.Type.WHITE
                self.word: str = word
                self.dirc: int = 0b00
                self.ptd: int = 0
                self.multi: bool = False
            elif tp == self.Type.HIDE:
                self.type: Crossword_puzzle_maker.Word.Type = self.Type.HIDE
                self.word: str = word
                self.dirc: int = 0b00
                self.ptd: int = 0
                self.multi: bool = False
            else:
                self.type: Crossword_puzzle_maker.Word.Type = self.Type.WORD
                self.word: str = str(word)
                self.dirc: int = dirc
                self.ptd: int = ptd
                self.multi: bool = multi
        
        def __str__(self) -> str:
            """
            转换成字符串
            """
            return self.word
        
        def inrow(self) -> bool:
            """
            是否有一个横向的单词使用这个单元格
            """
            return bool(self.dirc & 0b10)
        
        def incol(self) -> bool:
            """
            是否有一个纵向的单词使用这个单元格
            """
            return bool(self.dirc & 0b01)
        
        def faceleft(self) -> bool:
            """
            是否端点朝向左边
            """
            return bool(self.ptd & 0b0001)
        
        def faceright(self) -> bool:
            """
            是否端点朝向右边
            """
            return bool(self.ptd & 0b0010)
        
        def faceup(self) -> bool:
            """
            是否端点朝向上边
            """
            return bool(self.ptd & 0b0100)
        
        def facedown(self) -> bool:
            """
            是否端点朝向下边
            """
            return bool(self.ptd & 0b1000)
    
    def __init__(self, row: int = 13, col: int = 13) -> None:
        """
        初始化

        Args:
            row (int, optional): 字谜行数. Defaults to 13.
            col (int, optional): 字谜列数. Defaults to 13.
        """
        self.row: int = row
        self.col: int = col
        self.list: list[tuple[str, str]] = []  # 单词、句子
        self.puzzle: list[list[Crossword_puzzle_maker.Word]] = [[self.Word(self.Word.Type.WHITE) for _ in range(col)] for _ in range(row)]  # 字谜
        self.prompt: list[dict[int, list[str]]] = [{}, {}]  # 提示 [0] 为行的提示，[1] 为列的提示
        self.writer: Crossword_puzzle_saver = Crossword_puzzle_saver()  # 保存器
    
    def input_words_and_sentences(self) -> None:
        """
        输入单词和句子
        """
        self.list = []
        print('Please input words and sentences for making a crossword puzzle.', fore = Fore.BLUE)
        print('Example: ', fore = Fore.BLUE, end = '')
        print('apple I like apple pie.', fore = Fore.RED)
        print('╔════════════════════════════════════════════════════════╗', fore = Fore.LIGHTBLUE_EX)
        print('║                         Tips:                          ║', fore = Fore.LIGHTBLUE_EX)
        print('║', fore = Fore.LIGHTBLUE_EX, end = '')
        print('The word in the sentence will be replaced by underlines.', fore = Fore.BLUE, end = '')
        print('║\n║', fore = Fore.LIGHTBLUE_EX, end = '')
        print('           Or you can replace them by yourself.         ', fore = Fore.BLUE, end = '')
        print('║\n║', fore = Fore.LIGHTBLUE_EX, end = '')
        print('              End inputing by an empty line.            ', fore = Fore.BLUE, end = '')
        print('║', fore = Fore.LIGHTBLUE_EX)
        print('╚════════════════════════════════════════════════════════╝', fore = Fore.LIGHTBLUE_EX)
        
        while True:
            res: str = input(">>> ", fore = Fore.BLUE).strip()
            if res == '':  ## 没有输入
                break  # 结束输入
            l: list[str] = res.split(' ')
            if len(l) < 2:  # 输入个事不合法
                print('ERROR: The input is not valid.', fore = Fore.WHITE, back = Back.RED)
                print('Please input a word and a sentence.', fore = Fore.RED)
                print('Example: apple I like apple pie.', fore = Fore.RED)
                continue
            if l[0] in list(map(lambda x: x[0], self.list)):  # 重复单词
                print('ERROR: The input is not valid.', fore = Fore.WHITE, back = Back.RED)
                print('This word has already been input!', fore = Fore.RED)
                continue
            if len(l[0]) == 1:  # 单词长度为 1
                print('ERROR: The input is not valid.', fore = Fore.WHITE, back = Back.RED)
                print('The word should not be only one letter!', fore = Fore.RED)
                continue
            
            word: str = l[0]
            sentence: str = ' '.join(l[1:])
            
            replaced_sentence: list[str] = list(sentence.upper().replace(word.upper(), '_' * len(word)).lower())  # 替换句子中的单词为下划线
            
            # 但是句子中如果是大写，有些单词会变成小写，这时要转换回去
            for i in range(len(replaced_sentence)):
                if sentence[i].isupper():
                    replaced_sentence[i] = replaced_sentence[i].upper()
            
            self.list.append((word, ''.join(replaced_sentence)))  # 添加到列表中
        
        print('Input complete.', fore = Fore.BLUE)
    
    def make_puzzle(self, must_cross: bool = True, max_remain: int = 0) -> list[tuple[str, str]]:
        """
        生成字谜

        Args:
            must_cross (bool, optional): 单词之间是否必须有交叉. Defaults to True.
            max_remain (int, optional): 最多舍去几个单词. Defaults to 0.
        
        Returns:
            list[tuple[str, str]]: 剩余的单词句子
        """
        print(f'Start generating the crossword puzzle ({len(self.list)} words).', fore = Fore.BLUE)
        
        start_time = time()
        
        def can_putup(word: str, dirc: int, pos: tuple[int, int], must_cross: bool) -> bool:
            """
            判断放置单词的合法性

            Args:
                word (str): 要放置的单词
                dirc (int): 方向 0 为横向 1 为纵向
                pos (tuple[int, int]): 开始放的位置，（行，列）
                must_cross (bool): 单词之间是否必须有交叉

            Returns:
                bool: 是否合法
            """
            
            # 考虑以下几种情况：
            #     1. 出界
            #     2. 单词后一个位置和前一个位置有单词
            #     3. 和原先同向单词相交
            #     4. 和原先异向单词有交叉，且不是同一个字母
            #     5. 两侧有没有原先异向的单词的一端
            #     6. 两侧有没有同向单词
            
            cross: bool = False  # 如果放置是否有交叉
            
            if dirc == 1:  # 纵向放置
                if pos[0] + len(word) - 1 >= self.row:  # 超出行数
                    return False
                
                if pos[0] + len(word) != self.row and self.puzzle[pos[0] + len(word)][pos[1]].type != self.Word.Type.WHITE:  # 后面有单词
                    return False
                if pos[0] != 0 and self.puzzle[pos[0] - 1][pos[1]].type != self.Word.Type.WHITE:  # 前面有单词
                    return False
                
                for i in range(len(word)):
                    if self.puzzle[pos[0] + i][pos[1]].type != self.Word.Type.WHITE:
                        if self.puzzle[pos[0] + i][pos[1]].incol():  # 同向单词相交
                            return False
                        if self.puzzle[pos[0] + i][pos[1]].word.lower() != word[i].lower():  # 不相同相交
                            return False
                        cross = True
                    if pos[1] != 0:  # 看看左边
                        if self.puzzle[pos[0] + i][pos[1] - 1].type != self.Word.Type.WHITE:
                            if self.puzzle[pos[0] + i][pos[1] - 1].incol():  # 同向
                                return False
                            if self.puzzle[pos[0] + i][pos[1] - 1].faceleft():
                                return False
                    if pos[1] != self.col - 1:  # 看看右边
                        if self.puzzle[pos[0] + i][pos[1] + 1].type != self.Word.Type.WHITE:
                            if self.puzzle[pos[0] + i][pos[1] + 1].incol():  # 同向
                                return False
                            if self.puzzle[pos[0] + i][pos[1] + 1].faceright():
                                return False
            else:  # 横向放置
                if pos[1] + len(word) - 1 >= self.col:  # 超出列数
                    return False
                
                if pos[1] + len(word) != self.col and self.puzzle[pos[0]][pos[1] + len(word)].type != self.Word.Type.WHITE:  # 后面有单词
                    return False
                if pos[1] != 0 and self.puzzle[pos[0]][pos[1] - 1].type != self.Word.Type.WHITE:  # 前面有单词
                    return False
                
                for i in range(len(word)):
                    if self.puzzle[pos[0]][pos[1] + i].type != self.Word.Type.WHITE:
                        if self.puzzle[pos[0]][pos[1] + i].inrow():  # 同向单词相交
                            return False
                        if self.puzzle[pos[0]][pos[1] + i].word.lower() != word[i].lower():  # 不相同相交
                            return False
                        cross = True
                    if pos[0] != 0:  # 看看上边
                        if self.puzzle[pos[0] - 1][pos[1] + i].type != self.Word.Type.WHITE:
                            if self.puzzle[pos[0] - 1][pos[1] + i].inrow():  # 同向
                                return False
                            if self.puzzle[pos[0] - 1][pos[1] + i].faceup():
                                return False
                    if pos[0] != self.row - 1:  # 看看下边
                        if self.puzzle[pos[0] + 1][pos[1] + i].type != self.Word.Type.WHITE:
                            if self.puzzle[pos[0] + 1][pos[1] + i].inrow():  # 同向
                                return False
                            if self.puzzle[pos[0] + 1][pos[1] + i].facedown():
                                return False
            
            if must_cross and not cross:  # 如果必须有交叉，但是没有交叉，则不合法
                return False
            return True  # 否则合法
        
        def putup(word: str, idx: int, dirc: int, pos: tuple[int, int]) -> None:
            """
            放置单词

            Args:
                word (str): 要放置的单词
                idx (int): 在原序列的索引
                dirc (int): 方向 0 为横向 1 为纵向
                pos (tuple[int, int]): 开始放的位置，（行，列）
            """
            if dirc == 1:  # 纵向放置
                self.puzzle[pos[0]][pos[1]].ptd |= 0b1000  # 标记上端点
                self.puzzle[pos[0] + len(word) - 1][pos[1]].ptd |= 0b0100  # 标记下端点
                if pos[1] in self.prompt[1].keys():
                    self.prompt[1][pos[1]].append(self.list[idx][1])
                else:
                    self.prompt[1][pos[1]] = [self.list[idx][1]]
                
                for i in range(len(word)):
                    if self.puzzle[pos[0] + i][pos[1]].type == self.Word.Type.WHITE:  # 原本位置没有字母就需要填空
                        self.puzzle[pos[0] + i][pos[1]].type = self.Word.Type.HIDE
                        self.puzzle[pos[0] + i][pos[1]].word = word[i]
                    else:
                        self.puzzle[pos[0] + i][pos[1]].type = self.Word.Type.WORD
                        if self.puzzle[pos[0] + i][pos[1]].word != word[i]:  # 大写小写
                            self.puzzle[pos[0] + i][pos[1]].multi = True
                            self.puzzle[pos[0] + i][pos[1]].word = f"{word[i].upper()}/{word[i].lower()}"
                        else:
                            self.puzzle[pos[0] + i][pos[1]].word = word[i]
                    self.puzzle[pos[0] + i][pos[1]].dirc |= 0b01
            else:  # 横向放置
                self.puzzle[pos[0]][pos[1]].ptd |= 0b0010  # 标记左端点
                self.puzzle[pos[0]][pos[1] + len(word) - 1].ptd |= 0b0001  # 标记右端点
                if pos[0] in self.prompt[0].keys():
                    self.prompt[0][pos[0]].append(self.list[idx][1])
                else:
                    self.prompt[0][pos[0]] = [self.list[idx][1]]
                
                for i in range(len(word)):
                    if self.puzzle[pos[0]][pos[1] + i].type == self.Word.Type.WHITE:  # 原本位置没有字母就需要填空
                        self.puzzle[pos[0]][pos[1] + i].type = self.Word.Type.HIDE
                        self.puzzle[pos[0]][pos[1] + i].word = word[i]
                    else:
                        self.puzzle[pos[0]][pos[1] + i].type = self.Word.Type.WORD
                        if self.puzzle[pos[0]][pos[1] + i].word != word[i]:  # 大写小写
                            self.puzzle[pos[0]][pos[1] + i].multi = True
                            self.puzzle[pos[0]][pos[1] + i].word = f"{word[i].upper()}/{word[i].lower()}"
                        else:
                            self.puzzle[pos[0]][pos[1] + i].word = word[i]
                    self.puzzle[pos[0]][pos[1] + i].dirc |= 0b10
        
        def copyWord(w: Crossword_puzzle_maker.Word) -> Crossword_puzzle_maker.Word:
            """
            复制单元格

            Args:
                w (Crossword_puzzle_maker.Word): 要复制的单元格
            """
            return self.Word(w.type, w.word, w.dirc, w.ptd, w.multi)
        
        def copy(l: list[Crossword_puzzle_maker.Word]) -> list[Crossword_puzzle_maker.Word]:
            """
            深度复制单元格列表

            Args:
                l (list[Crossword_puzzle_maker.Word]): 单元格列表
            """
            res: list[Crossword_puzzle_maker.Word] = []
            for x in l:
                res.append(copyWord(x))
            return res
        
        def generate_puzzle(first_run: bool = True) -> bool:
            """
            使用深度优先搜索生成字谜

            Args:
                first_run (bool, optional): 是否为第一次运行. Defaults to True.
            
            Returns:
                bool: 是否生成完毕
            """
            
            if len(self.list) <= max_remain:  # 生成完毕
                return True
            
            for now in range(len(self.list)):
                for i in range(self.row):
                    for j in range(self.col):  # 尝试放置在每一个位置
                        for d in range(2):  # 尝试放置横向和纵向
                            if can_putup(self.list[now][0], d, (i, j), False if first_run else must_cross):
                                if d == 1:
                                    saver: list[Crossword_puzzle_maker.Word] = copy(list(map(lambda x: x[j], self.puzzle[i: i + len(self.list[now][0])])))
                                else:
                                    saver: list[Crossword_puzzle_maker.Word] = copy(self.puzzle[i][j: j + len(self.list[now][0])])
                                
                                putup(self.list[now][0], now, d, (i, j))  # 放置单词
                                
                                tmp: tuple[str, str] = self.list[now]
                                del self.list[now]
                                if generate_puzzle(False):  # 递归生成
                                    return True  # 生成成功
                                
                                # 回溯
                                self.list.insert(now, tmp)  # 重新将单词句子插入原来的位置，注意不是简单的 append
                                
                                if d == 1:
                                    del self.prompt[1][j][-1]
                                    if len(self.prompt[1][j]) == 0:
                                        del self.prompt[1][j]
                                    for t in range(len(saver)):
                                        self.puzzle[i + t][j] = copyWord(saver[t])
                                else:
                                    del self.prompt[0][i][-1]
                                    if len(self.prompt[0][i]) == 0:
                                        del self.prompt[0][i]
                                    for t in range(len(saver)):
                                        self.puzzle[i][j + t] = copyWord(saver[t])
                                
            return False  # 生成失败
        
        if not generate_puzzle():  # 生成字谜
            print('ERROR: The puzzle is not generated.', fore = Fore.WHITE, back = Back.RED)
            exit(-1)
            return self.list
        
        # 按照行数 / 列数排序
        self.prompt[0] = dict(sorted(self.prompt[0].items(), key = lambda x: x[0]))
        self.prompt[1] = dict(sorted(self.prompt[1].items(), key = lambda x: x[0]))
        
        end_time = time()
        
        print('The crossword puzzle has been generated.', fore = Fore.BLUE)
        print("Time used: ", fore = Fore.BLUE, end = '')
        print(str(1000.0 * (end_time - start_time)), fore = Fore.RED, end = '')
        print(" ms.", fore = Fore.BLUE)
        
        return self.list
    
    def print_puzzle(self) -> None:
        """
        输出字谜
        """
        print('\nThe generated crossword puzzle is:\n', fore = Fore.BLUE, end = '')
        for i in range(self.row):
            for j in range(self.col):
                if self.puzzle[i][j].type == self.Word.Type.WORD:
                    if self.puzzle[i][j].multi:
                        print(self.puzzle[i][j].word, fore = Fore.BLACK, back = Back.BLUE, end = '')
                    else:
                        print(' ', back = Back.RED, end = '')
                        print(self.puzzle[i][j].word, fore = Fore.BLACK, back = Back.BLUE, end = '')
                        print(' ', back = Back.RED, end = '')
                elif self.puzzle[i][j].type == self.Word.Type.WHITE:
                    print(' ', back = Back.RED, end = '')
                    print(' ', back = Back.RED, end = '')
                    print(' ', back = Back.RED, end = '')
                elif self.puzzle[i][j].type == self.Word.Type.HIDE:
                    print(' ', back = Back.RED, end = '')
                    print(' ', back = Back.BLUE, end = '')
                    print(' ', back = Back.RED, end = '')
            print()
        print('The prompt is:', fore = Fore.BLUE)
        print('\n'.join([Fore.RED + f"Row #{r + 1}: " + Style.RESET_ALL + f"{(Fore.RED + ' | ' + Style.RESET_ALL).join(p)}" for r, p in self.prompt[0].items()]), fore = Fore.GREEN)
        print('\n'.join([Fore.RED + f"Col #{c + 1}: " + Style.RESET_ALL + f"{(Fore.RED + ' | ' + Style.RESET_ALL).join(p)}" for c, p in self.prompt[1].items()]), fore = Fore.GREEN)
    
    def print_answer(self) -> None:
        """
        输出答案
        """
        print('\nThe answer of the generated crossword puzzle is:\n', fore = Fore.BLUE, end = '')
        for i in range(self.row):
            for j in range(self.col):
                if self.puzzle[i][j].type == self.Word.Type.WORD:
                    if self.puzzle[i][j].multi:
                        print(self.puzzle[i][j].word, fore = Fore.BLACK, back = Back.BLUE, end = '')
                    else:
                        print(' ', back = Back.RED, end = '')
                        print(self.puzzle[i][j].word, fore = Fore.BLACK, back = Back.BLUE, end = '')
                        print(' ', back = Back.RED, end = '')
                elif self.puzzle[i][j].type == self.Word.Type.WHITE:
                    print(' ', back = Back.RED, end = '')
                    print(' ', back = Back.RED, end = '')
                    print(' ', back = Back.RED, end = '')
                elif self.puzzle[i][j].type == self.Word.Type.HIDE:
                    print(' ', back = Back.RED, end = '')
                    print(self.puzzle[i][j].word, fore = Fore.BLACK, back = Back.GREEN, end = '')
                    print(' ', back = Back.RED, end = '')
            print()

if __name__ == '__main__':
    tester = Crossword_puzzle_maker(row = 30, col = 30)
    tester.input_words_and_sentences()
    tester.make_puzzle()
    tester.print_puzzle()
    tester.print_answer()

"""
baby I have a baby brother.
book I read lots of books yesterday.
bring But bring an umbrella with you, it is rainy outside.
build Look! There are some buildings.
calm Calm down! Don't be angry!
capital Beijing is the capital of China.
celebrate He cannot return home to celebrate her birthday.
conversion These are good ways to start a conversion.
dear I love you! My dear!
die You are going to die!
do I'm doing homework.
especially It is especially famous for its university.
excellent Excellent! I agree with you.
favorite My favorite color is white.
feast It's a big feast of rock and pop music.
fever You are having a fever!
fire Fire is very dangerous!
forty There are forty students in my class.
has He has two eyes.
hello Hello world!
island He found the boat near the island.
language English and Esperanto are languages.
lesson Try to do something they didn't do before the lesson.
let She let students think.
love I always love you!
lover We're lovers.
March Today is March 1st!
monitor I want to run for the class monitor.
most You will need it most days.
motorcycle Look! A man is riding a motorcycle behind you!
natural It is natural to forget new words.
newspaper I'm going to buy a newspaper.
photo There's a photo.
popular Do you know the popular song?
population That is larger than the population of many other cities in China.
prefer I prefer slow music because I think it's good for my study.
promise I promise to help you!
sorry Sorry? Can you say that again?
successful He was very successful.
suggest I suggest you should do homework right now.
telephone What's your telephone number?
theater He's the manager of a theater.
through I get to know a lot about the world through reading.
unreal Computer games are unreal!
used I used to study hard.
vocabulary The third question is about vocabulary.
Wednesday Today is Wednesday.
well I can get on well with everyone.
work My favorite writer is Mark Twain for his well-known work The Prince and The Pauper.
writer Mark Twain was a famous writer in America.
young He was the class monitor in class when he was young.
XuYueming My name is XuYueming
YZH YZH is so cute!
are Are you OK?!
beach Little Pig Beach is a very famous cartoon.
crossword This a generator of crossword puzzle.
China We are in China.
fall I'm falling love with you.
flower I love flowers.
good Good job! You did well.
happy Happy birthday!
help I need your help.
house I live in a small house.
man Man and woman are friends.
music I like listening to music.

"""