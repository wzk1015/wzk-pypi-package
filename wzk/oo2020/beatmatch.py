from wzk.utils import diff_compare


def check_files(paths):
    print("checking".center(50, "-"))

    all_flag = True
    for i in range(len(paths)):
        flag = True
        for j in range(len(paths)):
            if i == j:
                continue
            with open(paths[i]) as f1:
                out_lines = f1.read()
            with open(paths[j]) as f2:
                out_lines2 = f2.read()
            if out_lines != out_lines2:
                print("DIFFERENT {} {}".format(paths[i],
                                               paths[j]).center(50, "="))
                #print(out_lines)
                #print(out_lines2)
                print(diff_compare(out_lines, out_lines2))
                print(50*"-")
                flag = False
                all_flag = False
        if flag:
            print('{} no difference'.format(paths[i]))
    if all_flag:
        print("all correct".center(50, "-"))


if __name__ == '__main__':
    check_files(["test" + str(i) + ".txt" for i in range(1, 5)])
