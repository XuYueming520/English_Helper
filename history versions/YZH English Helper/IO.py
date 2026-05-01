# To input and output more beautifully
import colorama
from colorama import Fore, Back, Style
from typing import Any
from inspect import getframeinfo, stack, currentframe
from itertools import chain
from pickle import load as Load
from pickle import dump
from os import remove, getcwd, listdir
from os.path import split, splitext

colorama.init()

__print = print
__input = input

def input(prompt: str = '', fore: str = Fore.WHITE, back: str = Back.BLACK) -> str:
    """
    To input more beautifully

    Args:
        prompt (str): the prompt of the input. Defaults to ''.
        fore (str): the fore color of the text. Defaults to Fore.WHITE.
        back (str): the back color of the text. Defaults to Back.BLACK.

    Returns:
        str: the input string
    """
    __print(fore + back + prompt + Style.RESET_ALL, end = '')
    return __input()

def print(*text: Any, fore: str = Fore.WHITE, back: str = Back.BLACK, end: str = '\n', sep: str = ' ') -> None:
    """
    To output more beautifully

    Args:
        text (Any): text to be printed.
        fore (str): the fore color of the text. Defaults to Fore.WHITE.
        back (str): the back color of the text. Defaults to Back.BLACK.
        end (str): the end character of the text. Defaults to '\n'.
        sep (str): the separator of the text. Defaults to ' '.
    """
    __print(fore + back + sep.join([str(x) for x in list(text)]) + Style.RESET_ALL, end = end)

def debug(*text: Any, end: str = '\n', sep: str ='') -> None:
    """
    调试
    
    Args:
        text (Any): text to be printed.
        end (str): the end character of the text. Defaults to '\n'.
        sep (str): the separator of the text. Defaults to ' '.
    """
    caller = getframeinfo(stack()[1][0])
    print("Debug:", fore = Fore.YELLOW, end = ' ')
    print(caller.filename, caller.lineno, sep.join([str(x) for x in list(text)]), fore = Fore.LIGHTMAGENTA_EX, end = end)

def save(data: Any, path: str | None = None):
    """
    保存对象到文件

    Args:
        data (Any): 保存的数据
        path (str, optional): 保存路径. Defaults to None.
    """
    if path is None:
        fr = currentframe()
        if fr is None or fr.f_back is None:
            path = getcwd() + '\\' + 'Unknown.save'
        else:
            for var_name, value in chain(fr.f_back.f_locals.items(), fr.f_back.f_globals.items()):
                if value is data:
                    path = getcwd() + '\\' + var_name + '.save'
                    break
            if path is None:
                path = getcwd() + '\\' + 'Unknown.save'
    with open(path, 'wb') as fb:
        dump(data, fb)

def load(path: str | list[str] | None = None) -> dict[str, Any]:
    """
    从文件加载对象

    Args:
        path (str | list[str] | None, optional): 文件路径，可以用列表. Defaults to None.

    Returns:
        dict[str, Any]: 每个文件名和对应对象
    """
    if type(path) == str:
        path = [path]
    elif path is None:
        path = []
        for f in listdir(getcwd()):
            if f.endswith('.save'):
                path.append(getcwd() + '\\' + f)
    res = {}
    for file in path:
        with open(file, 'rb') as fb:
            info = Load(fb)
        name = splitext(split(file)[1])[0]
        res[name] = info
    return res

if __name__ == '__main__':
    debug()
    print('Hello, world!', 'I love Yzh!', [1, 1, 4, 5, 1, 4], fore = Fore.BLACK, back = Back.GREEN, end = '\n')
    print(input('Input something: ', fore = Fore.RED), fore = Fore.BLACK, back = Back.WHITE)
    
    test = []
    test.append(test)
    
    save(test)
    res = load()
    remove(getcwd() + '\\' + 'test.save')
    print(res)