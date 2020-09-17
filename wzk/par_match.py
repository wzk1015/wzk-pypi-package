bg_color_dict = {1: "41",  #red
                 2: "42",  #green
                 3: "43",  #yellow
                 4: "44",  #blue
                 5: "45",  #purple
                 6: "46"  #lignt blue
                 }  #

match_dict = {
    ")": "(",
    "]": "[",
    # "'" : "'",
    # '"' : '"',
    "}": "{",
    ">": "<"
}


def match(s):
    colors = [0 for i in range(len(s))]
    myStack = []
    idx = 0
    #try:
    ch = s[idx]
    try:
        while not ch == '\n':
            if ch in match_dict.values():
                myStack.append((idx, ch))
                colors[idx] = bg_color_dict[len(myStack)]
            elif ch in match_dict.keys():
                id, x = myStack.pop()
                if not x == match_dict[ch]:
                    print("括号不匹配:", ch)
                    return False
                colors[idx] = colors[id]
            idx += 1
            if not idx >= len(s):
                ch = s[idx]
            else:
                break
        for i in range(len(s)):
            print("\033[5;30;{0}m{1}\033[0m".format(colors[i], s[i]), end="")
        print()
    except IndexError:
        print("括号不匹配:", "index error")
        raise
    if len(myStack) != 0:
        print("括号不匹配:", "栈非空")
        return False
    return True


if __name__ == '__main__':
    s = input("括号匹配，支持六层嵌套\n注：由于颜色显示原因，请使用Pycharm或Jupyter打开\n请输入字符串：\n")
    match(s)
