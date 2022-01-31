from wzk.ds import D

asciis = " \n\t\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~`·!@#$%^&*()！@#￥%……&*（）_+——[]\;',./{}|:\"<>?？》《”：」「、。，‘；】【"
char2num_raw = {}
code = "1"
for asc in asciis:
    char2num_raw[asc] = code
    code = "0" + code

dic = D(char2num_raw)


def encode(s: str):
    ans = ""
    for ch in s:
        if ch not in dic.keys():
            raise KeyError("unknown character: '" + ch + "'")
        ans += dic[ch]
    return ans


def decode(s: str):
    ans = ""
    sep = s.split("1")
    if sep[-1] != "":
        raise ValueError("unexpected end of string")
    for wd in sep:
        if wd + "1" not in dic.inv().keys():
            raise KeyError("expected '00...0', got: " + wd)
        ans += dic.inv()[wd + "1"]
    return ans


if __name__ == '__main__':
    raw = "Hello world"
    print(encode(raw))
    print(decode(encode(raw)))