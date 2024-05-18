# This py file is for making and solving crossword puzzle of English helper by Xu Yueming.
"""@By 徐跃鸣@"""
import writer, Data_structure
from random import shuffle
# 导包
from time import time  # DeBug

class English_crossword_puzzle(object):
    """英语字谜 徐跃鸣制作"""
    def __init__(self, row=13, col=13):
        """初始化
            row -> int : 制作字谜的行数
            col -> int : 制作字谜的列数"""
        self.list = []  # 此列表存放原始的单词,句子
        self.row = row  # 行数
        self.col = col  # 列数
        self.No = False  # 空白单元格的值
        self.hide = None  # 单词中隐藏的字母的值
        self.puzzle = [[self.No for _ in range(self.row)] for _ in range(self.col)]  # 一个大小为输入行列的2维数组,初始值全为空白,此列表单词均显示(即为答案)
        self.end_puzzle = [[self.No for _ in range(self.row)] for _ in range(self.col)]  # 同上,只不过把单词中的部分字母隐藏掉了
        self.prompt = [{}, {}]  # 用来存放句子,[0]为横,[1]为竖
        self.words = []  # 单词
        self.start_time = None  # 开始时间
        
        self.stack = Data_structure.Stack()  # 用于深度优先搜索循环的栈
        self.queue = Data_structure.Queqe()  # 用于深度优先搜索循环的队列
        
        self.docx = writer.Docx_writer()  # 读写
    
    def get_word_sentence(self, words=None, sentences=None):
        """获取列表
            words -> list : 提前输入好的单词
            sentences- > list : 提前输入好的句子"""
        self.list = []  # 清空
        if words is None or sentences is None:  # 两个都为空,即没有提前输入
            while 1:  # 一直循环
                temp = input('input word and sentence>>>').split(' ')  # 输入单词句子,以空格拆分
                if temp[0] == '':  # 第一个单词就是空,那么说明输入完毕
                    break  # 跳出循环
                if len(temp) < 2:  # 输入数量少于2(即为1),报错少输入
                    print('You muse input word and sentence. e.g.word The word is really long!')  # 报错
                elif temp[0] in list(map(lambda n: n[0], self.list)):  # 输入的单词有重复
                    print('Please input a different word and sentence!')  # 有重复
                else:  # 否则输入没问题
                    self.list.append((temp[0], ' '.join(temp[1:])))  # 加入列表
        else:  # 提前输入好了
            for i in range(len(words)):  # 遍历
                self.list.append((words[i], sentences[i]))  # 加入
    
    def make_puzzle(self, must_cross=True, max_left_out=0, algorithm="DFS"):
        """制作字谜
            must_cross -> bool : 单词之间一定要有交叉
            max_left_out -> int : 单词如果放不下,最多舍去几个
            algorithm -> str("DFS" or "BFS") : 生成算法"""
        self.start_time = time()  # 开始时间
        
        word_prompt_copy_list = self.list[:]  # 保存原始的单词提示
        self.puzzle = [[self.No for _ in range(self.row)] for _ in range(self.col)]  # 一个大小为输入行列的2维数组,初始值全为空白,此列表单词均显示(即为答案)
        self.end_puzzle = [[self.No for _ in range(self.row)] for _ in range(self.col)]  # 同上,只不过把单词中的部分字母隐藏掉了
        self.prompt = [{}, {}]  # 用来存放句子,[0]为竖,[1]为横
        self.words = []  # 单词
        
        if algorithm == "DFS":  # 深度优先递归
            res = self.make_puzzle_DFS(must_cross, max_left_out, True)  # 调用递归函数
        elif algorithm == "BFS":  # 广度优先递归
            res = self.make_puzzle_BFS(must_cross, max_left_out, True)  # 调用递归函数
        elif algorithm == "DFS_LOOP":  # 深度优先循环
            res = self.make_puzzle_DFS_LOOP(must_cross, max_left_out, True)  # 调用循环函数
        elif algorithm == "BFS_LOOP":  # 广度优先循环
            res = self.make_puzzle_BFS_LOOP(must_cross, max_left_out, True)  # 调用循环函数
        else:  # 不是"DFS"或“BFS”或"DFS_LOOP"或"BFS_LOOP"
            return -1  # 输入错误
        
        if res == -1:  # 不能生成字谜
            return -1  # 生成错误
        
        self.get_prompt(self.words, word_prompt_copy_list)  # 获取提示
        return self.puzzle, self.end_puzzle, self.prompt, len(self.list)  # 返回
    
    def make_puzzle_DFS(self, must_cross=True, max_left_out=0, first=False):
        """使用DFS(深度优先)算法制作字谜
            must_cross -> bool : 单词之间一定要有交叉
            max_left_out -> int : 单词如果放不下,最多舍去几个
            first -> bool : 是否为第一次调用"""
        # print('\r%6.2fs' % (time() - self.start_time), end='')  # DeBug
        if len(self.list) <= max_left_out:  # 当剩下单词数量符合要求的时候就不必继续递归了
            return 1  # 完成生成
        
        for i in range(len(self.list)):  # 遍历剩下所有单词,这里千万不能直接取值,防止回溯时候添加元素造成BUG
            for start_c in range(self.col):
                for start_r in range(self.row):  # 遍历字谜内每个位置
                    for r_v in range(2):  # 横放还是竖放
                        if self.can_putup(self.list[i][0], r_v, (start_c, start_r), False if first else must_cross):  # 可以放置,第一次运行,字谜中没有任何单词,所以不能有交叉
                            word, sentence = self.list[i]
                            if r_v:  # 竖
                                temp1 = self.puzzle[start_c][start_r:start_r + len(word)]  # 用来回溯,存放之前这个单词所在位置原来的数据
                                temp2 = self.end_puzzle[start_c][start_r:start_r + len(word)]  # 用来回溯,存放之前这个单词所在位置原来的数据
                            else:  # 横
                                temp1 = list(map(lambda u: u[start_r], self.puzzle[start_c:start_c + len(word)]))  # 用来回溯,存放之前这个单词所在位置原来的数据
                                temp2 = list(map(lambda u: u[start_r], self.end_puzzle[start_c:start_c + len(word)]))  # 用来回溯,存放之前这个单词所在位置原来的数据
                            
                            self.putup(word, sentence, r_v, (start_c, start_r))  # 放置单词
                            flag = self.make_puzzle_DFS(must_cross, max_left_out)  # 递归
                            
                            if flag == 1:  # 制作完成
                                return 1  # 制作完成向前退出
                            # 回溯
                            # print(f'│Get│{word}', end='')
                            # print(' ' * (15 - len(f'│Get│{word}')), end='')
                            # print(f'│on│{(start_c, start_r)}', end='')
                            # print(' ' * (15 - len(f'│on│{(start_c, start_r)}')), end='')
                            # print(f'│{r_v}', end='')
                            # print(' ' * 3, end='│\n')  # DeBug
                            
                            self.list.insert(i, (word, sentence))  # 重新将单词句子插入原来的位置,注意不是简单的append
                            if r_v:  # 竖
                                u = start_r
                                for o in temp1:
                                    self.puzzle[start_c][u] = o
                                    u += 1
                                u = start_r
                                for o in temp2:
                                    self.end_puzzle[start_c][u] = o
                                    u += 1
                            else:  # 横
                                u = start_c
                                for o in temp1:
                                    self.puzzle[u][start_r] = o
                                    u += 1
                                u = start_c
                                for o in temp2:
                                    self.end_puzzle[u][start_r] = o
                                    u += 1
                            del self.words[self.words.index(((start_c, start_r), word, r_v))], temp1, temp2
        return -1  # 不能生成
    
    def make_puzzle_BFS(self, must_cross=True, max_left_out=0, first=False):
        """使用BFS(广度优先)算法制作字谜
            must_cross -> bool : 单词之间一定要有交叉
            max_left_out -> int : 单词如果放不下,最多舍去几个
            first -> bool : 是否为第一次调用"""
        pass
    
    def make_puzzle_DFS_LOOP(self, must_cross=True, max_left_out=0, first=False):
        """使用DFS(深度优先)循环算法制作字谜
            must_cross -> bool : 单词之间一定要有交叉
            max_left_out -> int : 单词如果放不下,最多舍去几个
            first -> bool : 是否为第一次调用"""
        pass
    
    def make_puzzle_BFS_LOOP(self, must_cross=True, max_left_out=0, first=False):
        """使用BFS(广度优先)循环算法制作字谜
            must_cross -> bool : 单词之间一定要有交叉
            max_left_out -> int : 单词如果放不下,最多舍去几个
            first -> bool : 是否为第一次调用"""
        pass
    
    def solve_puzzle(self, puzzle, list):
        """解决puzzle
            puzzle -> list : 待解决的字谜
            list -> list : 单词句子"""
        pass
    
    def save_puzzle(self, puzzle, prompt, path, **kwargs):
        """保存puzzle
            puzzle -> list : 字谜(可以是答案)
            prompt -> list : 句子
            path -> str : 保存路径
            kwargs -> dict : 其他保存时的参数"""
        self.docx.write_cross_puzzle(puzzle, prompt, **kwargs)  # 写入
        self.docx.save(file_path=path)  # 保存
    
    def can_putup(self, word, ross_or_vertical, start_number, must_cross=True):
        """可以放置?
            word -> str : 要放置的单词
            ross_or_vertical -> int(0,1) : 方向(0横1竖)
            start_number -> tuple : 单词开始的位置
            must_cross -> bool : 一定要有交叉"""
        has_cross = False  # 拥有交叉
        if ross_or_vertical:  # 竖
            if start_number[1] + len(word) >= self.row:
                return False  # 出界
            
            if start_number[1] + len(word) != self.row and self.puzzle[start_number[0]][start_number[1] + len(word) + 1 - 1] != self.No:  # 单词结尾不是最后一个并且单词后面的单元格不为空
                return False  # 下面有单词
            if start_number[1] != 0 and self.puzzle[start_number[0]][start_number[1] - 1] != self.No:  # 单词不是开头并且前面的单元格不为空
                return False  # 上面有单词
            
            for (s, w, r_v) in self.words:  # 遍历(s:开始的坐标,w:单词,r_v:方向)
                if r_v == ross_or_vertical and s[0] == start_number[0] and \
                        (start_number[1] < s[1] < start_number[1] + len(word)) and \
                        (start_number[1] < s[1] + len(w) < start_number[1] + len(word)):  # 同向,并且在本单词范围内
                    return False  # 单词中覆盖
            
            i = 0  # 循环变量
            for x in range(start_number[1], start_number[1] + len(word)):  # 遍历
                if self.puzzle[start_number[0]][x] != self.No:  # 位置不为空
                    has_cross = True  # 拥有交叉
                    if self.puzzle[start_number[0]][x].upper() != word[i].upper():  # 但是如果不是同一个字母
                        return False  # 与原单词有交涉
                
                for (s, w, r_v) in self.words:  # 遍历所有单词
                    if r_v == ross_or_vertical:  # 方向相同
                        if start_number[0] - 1 == s[0] and (start_number[1] <= s[1] + len(w) or s[1] <= start_number[1] + len(word)):  # 检查单词列数比本单词列数少1(即在左边),并且有碰到
                            return False  # 左边有同向单词
                        if start_number[0] + 1 == s[0] and (start_number[1] <= s[1] + len(w) or s[1] <= start_number[1] + len(word)):  # 检查单词列数比本单词列数多1(即在右边),并且有碰到
                            return False  # 右边有同向单词
                    else:  # 方向不同
                        if start_number[0] - 1 == s[0] + len(w) - 1 and s[1] == x:  # 在列数少1列处有单词的结尾
                            return False  # 左边有异向单词
                        if start_number[0] + 1 == s[0] and s[1] == x:  # 在列数多1列处有单词的开头
                            return False  # 右边有异向单词
                i += 1  # 自增
        else:  # 横
            if start_number[0] + len(word) >= self.col:
                return False  # 出界
            
            if start_number[0] + len(word) != self.col and self.puzzle[start_number[0] + len(word) + 1 - 1][start_number[1]] != self.No:  # 单词结尾不是最后一个并且单词后面的单元格不为空
                return False  # 右面有单词
            if start_number[0] != 0 and self.puzzle[start_number[0] - 1][start_number[1]] != self.No:  # 单词不是开头并且前面的单元格不为空
                return False  # 左面有单词
            
            for (s, w, r_v) in self.words:  # 遍历(s:开始的坐标,w:单词,r_v:方向)
                if r_v == ross_or_vertical and s[1] == start_number[1] and \
                        (start_number[0] < s[0] < start_number[0] + len(word)) and \
                        (start_number[0] < s[0] + len(w) < start_number[0] + len(word)):  # 同向,并且在本单词范围内
                    return False  # 单词中覆盖
            
            i = 0  # 循环变量
            for y in range(start_number[0], start_number[0] + len(word)):  # 遍历
                if self.puzzle[y][start_number[1]] != self.No:  # 位置不为空
                    has_cross = True  # 拥有交叉
                    if self.puzzle[y][start_number[1]].upper() != word[i].upper():  # 但是如果不是同一个字母
                        return False  # 与原单词有交涉
                
                for (s, w, r_v) in self.words:  # 遍历所有单词
                    if r_v == ross_or_vertical:  # 方向相同
                        if start_number[1] - 1 == s[1] and (start_number[0] <= s[0] + len(w) or s[0] <= start_number[0] + len(word)):  # 检查单词列数比本单词列数少1(即在左边),并且有碰到
                            return False  # 上边有同向单词
                        if start_number[1] + 1 == s[1] and (
                                start_number[0] <= s[0] + len(w) or s[0] <= start_number[0] + len(word)):  # 检查单词列数比本单词列数多1(即在左边),并且有碰到
                            return False  # 下边有同向单词
                    else:
                        if start_number[1] - 1 == s[1] + len(w) - 1 and s[0] == y:  # 在列数少1列处有单词的结尾
                            return False  # 上边有异向单词
                        if start_number[1] + 1 == s[1] and s[0] == y:  # 在列数多1列处有单词的结尾
                            return False  # 下边有异向单词
                i += 1  # 自增
        
        if must_cross and not has_cross:  # 如果必须要交叉但是没有交叉
            return False  # 没有交叉
        
        return True  # 可以放置
    
    def putup(self, word, prompt, ross_or_vertical, start_number):
        """放置单词和提示
            word -> str : 要放置的单词
            prompt -> str : 单词提示
            ross_or_vertical -> int(0,1) : 方向
            start_number -> tuple : 单词起始位置"""
        
        if ross_or_vertical:  # 竖
            n = 0  # 循环变量
            for x in range(start_number[1], start_number[1] + len(word)):  # 遍历
                if self.end_puzzle[start_number[0]][x] != self.No:  # 原本单词位置就有字母
                    if self.puzzle[start_number[0]][x] != word[n]:  # 不相等(即为大写小写)
                        self.end_puzzle[start_number[0]][x] = f'{word[n].lower()}/{word[n].upper()}'  # 大写小写
                    else:  # 相等
                        self.end_puzzle[start_number[0]][x] = word[n]  # 放入字母
                else:  # 没字母就不是交叉点
                    self.end_puzzle[start_number[0]][x] = self.hide  # 需要填空,单词中隐藏的字母
                
                if self.puzzle[start_number[0]][x] not in [word[n], self.No]:  # 不等于单词(即为大写小写)
                    self.puzzle[start_number[0]][x] = f'{word[n].lower()}/{word[n].upper()}'  # 大写小写
                else:  # 相等
                    self.puzzle[start_number[0]][x] = word[n]  # 放入字母
                n += 1  # 自增
            self.words.append((start_number, word, ross_or_vertical))  # 将单词加入到已经存放好的单词中
        else:  # 横
            n = 0  # 循环变量
            for y in range(start_number[0], start_number[0] + len(word)):  # 遍历
                if self.end_puzzle[y][start_number[1]] != self.No:  # 原本单词位置就有字母
                    if self.puzzle[y][start_number[1]] != word[n]:  # 不相等(即为大写小写)
                        self.end_puzzle[y][start_number[1]] = f'{word[n].lower()}/{word[n].upper()}'  # 大写小写
                    else:  # 相等
                        self.end_puzzle[y][start_number[1]] = word[n]  # 放入字母
                else:  # 没字母就不是交叉点
                    self.end_puzzle[y][start_number[1]] = self.hide  # 需要填空,单词中隐藏的字母
                
                if self.puzzle[y][start_number[1]] not in [word[n], self.No]:  # 不等于单词(即为大写小写)
                    self.puzzle[y][start_number[1]] = f'{word[n].lower()}/{word[n].upper()}'  # 大写小写
                else:  # 相等
                    self.puzzle[y][start_number[1]] = word[n]  # 放入字母
                n += 1  # 自增
            self.words.append((start_number, word, ross_or_vertical))  # 将单词加入到已经存放好的单词中
        del self.list[self.list.index((word, prompt))]  # 将添加好的单词从列表中删除
        
        # print(f'│Put│{word}', end='')
        # print(' ' * (15 - len(f'│Put│{word}')), end='')
        # print(f'│on│{start_number}', end='')
        # print(' ' * (15 - len(f'│on│{start_number}')), end='')
        # print(f'│{ross_or_vertical}', end='')
        # print(' ' * 3, end='│\n')  # DeBug
    
    def get_prompt(self, words, word_prompt_list):
        """获取字谜的提示
            words -> list : 每个单词
            word_prompt_list -> list : 存放每个单词和提示的句子"""
        for ((start_c, start_r), word, r_v) in words:
            for w,p in word_prompt_list:
                if word == w:
                    temp = list(p.upper().replace(word.upper(), '_' * len(word)).lower())  # 将句子中单词替换成等长的下划线
                    for s in range(len(p)):  # 遍历原句
                        if p[s].isupper():  # 如果原句中的字母大写
                            temp[s] = temp[s].upper()  # 大写
                    self.prompt[r_v][start_c + 1 if r_v else start_r + 1] = ''.join(temp)  # 添加到提示
                    # 将句子中单词替换成下划线
                    break
    
    def shuffle_list(self, list=None):
        """打乱列表
            list -> list : 用来打乱的列表,默认为self.list"""
        shuffle(list if list is not None else self.list)  # 打乱列表
    
    def print_puzzle(self, puzzle, prompt):
        """输出字谜
            puzzle -> list : 输出的列表
            prompt -> list : 提示句子"""
        print('\n---the crossword puzzle---\n')  # 标题
        for r in range(self.row):
            for c in range(self.col):  # 遍历
                if puzzle[c][r] == self.No:  # 为空
                    print('\033[41;1m \033[0m', end='\033[41;1m \033[0m')  # 输出红颜色的空格
                elif puzzle[c][r] == self.hide:  # 为隐藏字母
                    print('\033[44;1m \033[0m', end='\033[41;1m \033[0m')  # 输出黄颜色的空格
                else:  # 正常字母
                    print('\033[41;44;1m' + puzzle[c][r] + '\033[0m', end='\033[41;1m \033[0m')  # 输出
            print()
        
        print(prompt)  # 提示句子


if __name__ == '__main__':  # DeBug
    # 检测是否能放置
    # crossword_puzzle = English_crossword_puzzle(20, 20)
    # crossword_puzzle.list = [('book', 'fuck books'), ('language', 'fuck languages')]
    # crossword_puzzle.putup('language', 'fuck languages', 0, (0, 4))
    # crossword_puzzle.print_puzzle(crossword_puzzle.puzzle, crossword_puzzle.prompt)
    # if crossword_puzzle.can_putup(word='book', ross_or_vertical=1, start_number=(7, 0), must_cross=False):
    #     print('fuck you!')
    #     crossword_puzzle.putup('book', 'fuck books', 1, (7, 0))
    #     crossword_puzzle.print_puzzle(crossword_puzzle.puzzle, crossword_puzzle.prompt)
    # else:
    #     print('what fuck?')
    #     crossword_puzzle.putup('book', 'fuck books', 1, (7, 0))
    #     crossword_puzzle.print_puzzle(crossword_puzzle.puzzle, crossword_puzzle.prompt)
    
    # 输入单词,句子,输出单个字谜
    crossword_puzzle = English_crossword_puzzle(35, 35)
    crossword_puzzle.get_word_sentence()

    # ------对输入的单词、句子以单词拼写在字母表的顺序排序------ #
    sorted_list = []
    for x in sorted(list(map(lambda x: x[0].lower(), crossword_puzzle.list))):
        for y in crossword_puzzle.list:
            if y[0].lower() == x:
                sorted_list.append(y)
                break

    for x, y in sorted_list:
        print(x, y)
    # ------对输入的单词、句子以单词拼写在字母表的顺序排序------ #

    # crossword_puzzle.shuffle_list()
    print(crossword_puzzle.list)

    print('┌' + '-' * 16 + 'Start' + '-' * 17 + '┐')
    s_t = time()
    puzzle, end_puzzle, prompt, left_out = crossword_puzzle.make_puzzle(algorithm="DFS")
    e_t = time()
    print('└' + '-' * 17 + 'End' + '-' * 18 + '┘')
    print(crossword_puzzle.list)
    print(len(crossword_puzzle.list))

    crossword_puzzle.print_puzzle(puzzle, prompt)
    crossword_puzzle.print_puzzle(end_puzzle, prompt)

    print()
    print(e_t - s_t)

    if input('是否保存(Y/N)>>>') == 'Y':
        model = (puzzle, end_puzzle, prompt, left_out)
        writer.easy_save(model)
        w = writer.Docx_writer()
        w.write_cross_puzzle(puzzle, prompt)
        w.save(r'.\a.docx')
        w.write_cross_puzzle(end_puzzle, prompt)
        w.save(r'.\b.docx')
    
    # 测试算法生成速度
    # crossword_puzzle = English_crossword_puzzle(20, 20)
    # lists = []
    # while 1:
    #     temp = input('input word and sentence>>>').split(' ')
    #     if temp[0] == '':
    #         break
    #     lists += [(temp[0], ' '.join(temp[1:]))]
    # print(lists)
    # times = []
    # for x in range(1, len(lists)+1):
    #     print(x)
    #     crossword_puzzle.list = lists[:x]
    #     crossword_puzzle.shuffle_list()
    #     s_t = time()
    #     puzzle, end_puzzle, prompt, left_out = crossword_puzzle.make_puzzle()
    #     e_t = time()
    #     crossword_puzzle.print_puzzle(puzzle, prompt)
    #     times.append(e_t - s_t)
    #     print(times[-1])
    #     print('-------------------------------------')
    # print(times)
    # crossword_puzzle.print_puzzle(puzzle, prompt)

r"""
baby I have a baby brother.
book I read lots of books yesterday.
bring But bring an umbrella with you, it is rainy outside.
build Look! There are some buildings.
calm Calm down!Don't be angry!
capital Beijing is the capital of China.
celebrate He cannot return home to celebrate her birthday.
conversion These are good ways to start a conversion.
dear I love you! My dear!
die You are going to die!
do I'm doing homework.
especially It is especially famous for its university.
excellent Excellent!I agree with you.
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
sorry Sorry?Can you say that again?
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


"""