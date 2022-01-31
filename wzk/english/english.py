import http.client
import hashlib
import urllib.parse
import random
import re
import json
from time import sleep

vocab = {}
wordle = []


class WordNotFoundError(Exception):
    def __init__(self, wd):
        self.wd = wd

    def __str__(self):
        return "word '%s' not found in vocabulary" % self.wd


def make_csv():
    import csv
    with open('../../words.csv') as f:
        reader = csv.reader(f)
        lines = list(reader)
        word_dict = {}
        for line in lines:
            word_dict[line[0]] = line[1]

    with open('vocabulary.txt', 'w') as out:
        print(word_dict, file=out)


def load_vocab():
    # global english
    # vocab_path = pkg_resources.resource_filename("wzk", "english/vocabulary.txt")
    # with open(vocab_path) as f:
    #     english = eval(f.read().strip())
    global vocab
    from wzk.english.vocabulary import v
    vocab = v
    for word in vocab.keys():
        if len(word) == 5 and word.isalpha():
            wordle.append(word.lower())
    wordle.sort()


def lookup(string, verbose=True, non_alpha=False):
    if not vocab:
        load_vocab()
    words = string.split()
    result = ""

    for word in words:
        wd, prefix, suffix = word, "", ""
        if non_alpha and not word[0].isalpha():
            wd, prefix = wd[1:], wd[0]
        if non_alpha and not word[-1].isalpha():
            wd, suffix = wd[:-1], wd[-1]

        try:
            value = vocab[wd.lower()]
            part_of_speech = ["n", "v", "vt", "vi", "adj", "adv", "conj", "prep",
                              "abbr", "vbl", "aux", "int", "pron", "num", "art"]
            for ps in part_of_speech:
                value = value.replace(ps + ".", "\n" + ps + ".")
            value = value.strip()

            if verbose:
                result += prefix + value + suffix + "\n\n"
            else:
                result += prefix + value.split(".")[1].split()[0].split(",")[0] + suffix + "\n\n"

        except KeyError:
            raise WordNotFoundError(wd)

    return result.strip()


def direct_translate(string):
    return lookup(string, verbose=False, non_alpha=True).replace("\n", "")


def translate(query, from_lang="en", to_lang="zh"):
    app_id = '20200902000557415'  #你的appid(这里是必填的, 从百度 开发者信息一览获取)
    secret_key = 'HbwHva24hVgTBvM5sZ9e'  #你的密钥(这里是必填的, 从百度 开发者信息一览获取)

    http_client = None
    myurl = '/api/trans/vip/translate'

    while True:
        salt = random.randint(32768, 65536)
        sign = app_id + query + str(salt) + secret_key
        m1 = hashlib.md5()
        m1.update(sign.encode())
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + app_id + '&q=' + urllib.parse.quote(query) + '&from=' \
                + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign
        result = ""
        try:
            http_client = http.client.HTTPConnection('api.fanyi.baidu.com')
            http_client.request('GET', myurl)
            #response是HTTPResponse对象
            response = http_client.getresponse()
            result = response.read()
        except Exception as e:
            print(e)
        finally:
            if http_client:
                http_client.close()
        try:
            return json.loads(result)['trans_result'][0]['dst']
        except:
            sleep(1)


def funny_translate(query, times=20):
    languages = {"en" : "英语", "jp": "日语", "kor": "韩语", "spa": "西班牙语",
                 "fra": "法语", "th": "泰语", "ara": "阿拉伯语", "ru": "俄语",
                 "pt" : "葡萄牙语", "yue": "粤语", "wyw": "文言文", "de": "德语",
                 "it": "意大利语"}
    print("Original:", query)
    for i in range(1, times + 1):
        lang = random.choice(list(languages.keys()))
        query = translate(query, from_lang="zh", to_lang=lang)
        print(languages[lang].ljust(7), query)
        sleep(1)
        query = translate(query, from_lang=lang, to_lang="zh")
        print((str(i)+" times:").ljust(6), query)
        sleep(1)


def words_like(query):
    if not vocab:
        load_vocab()
    assert len(query) == 5
    condition = [0, 0, 0, 0, 0]
    for i, ch in enumerate(query):
        if ch.isalpha():
            condition[i] = ch.lower()

    ans = []
    for word in wordle:
        flag = False
        for i, cond in enumerate(condition):
            if cond != 0 and cond != word[i]:
                flag = True
                break
        if not flag:
            ans.append(word)
    return ans


def solve_wordle(yellows=(), greens=()):
    '''
    yellows/greens: ["Y1", "C2", ...]
    '''
    if not yellows and not greens:
        raise ValueError("no requirement specified")

    for i, green in enumerate(greens):
        greens[i] = (green[0].lower(), int(green[1])-1)
    for i, yellow in enumerate(yellows):
        yellows[i] = (yellow[0].lower(), int(yellow[1])-1)

    query = ["-"] * 5
    for ch, pos in greens:
        query[pos] = ch

    possible_words = words_like(query)
    ans = []
    for word in possible_words:
        flag = False
        for ch, pos in yellows:
            if ch not in word or word[pos] == ch:
                flag = True
                break
        if not flag:
            ans.append(word)
    return ans


def solve_wordle_simple(trials, colors):
    '''
    trials: ["OPERA", "LEMON", "EIGHT"]
    colors: ["YBYBB", "BYBYB", "YBBYY"]
    '''
    yellows = []
    greens = []
    for i, color in enumerate(colors):
        for j, ch in enumerate(color):
            if ch.upper() == "Y":
                yellows.append((trials[i][j], j+1))
            elif ch.upper() == "G":
                greens.append((trials[i][j], j+1))
    return solve_wordle(yellows, greens)




if __name__ == '__main__':
    # funny_translate("二臣贼子，你枉活七十有六，一生未立寸功，只会摇唇鼓舌，助曹为虐！")
    # print(words_like("SEA__"))
    print(solve_wordle(
        yellows=["O1", "E3", "E2", "O4", "E1", "H4"],
        greens=["T1"]
    ))
    print(solve_wordle_simple(
        trials=["OPERA", "LEMON", "EIGHT"],
        colors=["YBYBB", "BYBYB", "YBBYY"]
    ))