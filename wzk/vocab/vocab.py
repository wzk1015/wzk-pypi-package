vocab = None


class WordNotFoundError(Exception):
    def __init__(self, wd):
        self.wd = wd

    def __str__(self):
        return "word '%s' not found in vocabulary"%self.wd


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
    # global vocab
    # vocab_path = pkg_resources.resource_filename("wzk", "vocab/vocabulary.txt")
    # with open(vocab_path) as f:
    #     vocab = eval(f.read().strip())
    global vocab
    from wzk.vocab.vocabulary import v
    vocab = v


def lookup(string, verbose=True, non_alpha=False):
    if vocab is None:
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


def translate(string):
    return lookup(string, verbose=False, non_alpha=True).replace("\n", "")


if __name__ == '__main__':
    print(translate("I love you!"))