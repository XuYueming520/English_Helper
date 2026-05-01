# This py file is for data structure of English helper by Xu Yueming.
"""@By 徐跃鸣@"""

class Stack(object):
    """栈"""
    def __init__(self):
        """初始化,建立一个空栈"""
        self.items = []  # 新建列表作为栈
    
    def Is_Empty(self):
        """判断是否为空栈"""
        return self.items == []
    
    def push(self, item):
        """往栈底加入新元素
            item -> Every_Type : 加入栈的元素"""
        self.items.append(item)
    
    def pop(self):
        """取出栈底元素"""
        return self.items.pop()
    
    def peek(self):
        """获取栈底元素"""
        return self.items[-1]
    
    def size(self):
        """获取栈的大小"""
        return len(self.items)

class Queqe(object):
    """队列"""
    def __init__(self):
        """创建新队列"""
        self.items = []
        self.head_pointer = 0
        self.tail_pointer = 0
    
    def Is_Empty(self):
        """判断队列是否为空"""
        return self.head_pointer == self.tail_pointer
    
    def add(self, item):
        """将元素加入队尾
            item -> Every_Type : 加入队尾的元素"""
        self.items[self.tail_pointer]
        self.tail_pointer += 1
    
    def pop(self):
        """取出队首元素"""
        value = self.items[self.head_pointer]
        del self.items[self.head_pointer]
        self.head_pointer += 1
        return value
    
    def peek(self):
        """获取队尾元素"""
        return self.items[self.head_pointer]
    
    def size(self):
        """获取队列大小"""
        return self.tail_pointer - self.head_pointer