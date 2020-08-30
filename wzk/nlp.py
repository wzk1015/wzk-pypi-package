import math


def bleu(pred, gt, k=4):
    def sub_seqs(tokens, length):
        for j in range(len(tokens) - length + 1):
            yield tokens[j: j+length]

    pred_tokens, gt_tokens = pred.split(), gt.split()
    pred_len, gt_len = len(pred_tokens), len(gt_tokens)
    k = min(k, pred_len, gt_len)
    score = math.exp(min(0, 1 - gt_len / pred_len))
    for i in range(1, k+1):
        p = 0
        pred_seqs = list(sub_seqs(pred_tokens, i))
        gt_seqs = list(sub_seqs(gt_tokens, i))
        print(pred_seqs, gt_seqs)
        for idx1 in range(len(pred_seqs)):
            for idx2 in range(len(gt_seqs)):
                if pred_seqs[idx1] == gt_seqs[idx2]:
                    p += 1
        print(p, i)
        score *= (p / len(pred_seqs)) ** (0.5 ** i)
    return score


if __name__ == '__main__':
    print(bleu("they are good", "they are not good", k=2))
