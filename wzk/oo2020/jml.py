from random import *

instrs = ['add_person', 'add_person', 'add_relation', 'query_value', 'query_conflict',
          'query_acquaintance_sum', 'compare_age', 'compare_name', 'queury_name_rank',
          'query_people_sum', 'query_circle', 'query_circle']

name = ["limbo", "nyima", "claw", "orange"]
adj = ["beautiful", "ugly", "clever", "rubbish", "great", "bad", "excellent", "terrible"]


def hw9_generator(LENGTH, PEOPLE):
    if random() < 0.5:
        print("GENERATE ADD FIRST")
        return _hw9_generate_add_first(LENGTH, PEOPLE)
    elif random() < 0.5:
        print("GENERATE CIRCLE")
        return _hw9_generate_circle(LENGTH, PEOPLE)
    else:
        print("GENERATE RANDOM")
        return _hw9_generate_random(LENGTH, PEOPLE)


def _hw9_generate_circle(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(people_num):
        instrlist += "add_person"
        instrlist += ' '
        instrlist += str(i)
        instrlist += ' '
        instrlist += choice(adj) + "_" + choice(name)
        instrlist += ' '
        instrlist += str(randint(1000000, 10000000))
        instrlist += ' '
        instrlist += str(randint(1, 80))
        instrlist += '\n'
    relations = randint(people_num, people_num * (people_num) / 2)
    relations = min(LENGTH - 50, relations)
    for i in range(relations):
        instrlist += "add_relation"
        instrlist += ' '
        instrlist += str(randint(1, people_num))
        instrlist += ' '
        instrlist += str(randint(1, people_num))
        instrlist += ' '
        instrlist += str(111)
        instrlist += '\n'
    for i in range(LENGTH - PEOPLE - relations):
        instrlist += "query_circle"
        instrlist += ' '
        instrlist += str(randint(1, people_num))
        instrlist += ' '
        instrlist += str(randint(1, people_num))
        instrlist += '\n'
    return instrlist


def _hw9_generate_add_first(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(people_num):
        instrlist += "add_person"
        instrlist += ' '
        instrlist += str(i)
        instrlist += ' '
        instrlist += choice(adj) + "_" + choice(name)
        instrlist += ' '
        instrlist += str(randint(1000000, 10000000))
        instrlist += ' '
        instrlist += str(randint(1, 80))
        instrlist += '\n'
    for i in range(LENGTH - people_num):
        instr = choice(instrs)
        if instr == "add_person":
            continue
        instrlist += instr
        if instr == 'add_relation':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, 15))
        elif instr == 'query_value' or instr == 'query_conflict':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'query_acquaintance_sum' or instr == 'queury_name_rank':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'compare_age' or instr == 'compare_name' or instr == 'query_circle':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        instrlist += '\n'
    return instrlist


def _hw9_generate_random(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(LENGTH):
        instr = choice(instrs)
        instrlist += instr
        if instr == 'add_person':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += choice(adj) + "_" + choice(name)
            instrlist += ' '
            instrlist += str(randint(1000000, 10000000))
            instrlist += ' '
            instrlist += str(randint(1, 80))
        elif instr == 'add_relation':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, 15))
        elif instr == 'query_value' or instr == 'query_conflict':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'query_acquaintance_sum' or instr == 'queury_name_rank':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        elif instr == 'compare_age' or instr == 'compare_name' or instr == 'query_circle':
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
            instrlist += ' '
            instrlist += str(randint(1, int(people_num)))
        instrlist += '\n'
    return instrlist


instrs10 = ['ap', 'ap', 'ar', 'qv', 'qc',
          'qas', 'ca', 'cn', 'qnr',
          'qps', 'qci', 'qci', 'ag', 'atg',
          'qgs', 'qgps', 'qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs','qgrs','qgvs',
           'qgcs', 'qgam', 'qgav']

#name = ["limbo", "nyima", "claw", "orange"]
#adj = ["beautiful", "ugly", "clever", "rubbish", "great", "bad", "excellent", "terrible"]
name10 = ["l", "n", "c", "o"]
adj10 = ["beau", "ugly", "clever", "rubbish", "great", "bad", "excel", "terrible"]



limit = {
    "ap" : 5000,
    "qnr": 333,
    "qci": 333,
    "ag" : 10
}

instr_count = {
    "ap" : 0,
    "qnr": 0,
    "qci": 0,
    "ag" : 0
}


def r(people_num):
    return randint(1, people_num + 1)  # +1 allow for exception


def hw10_generator(LENGTH, PEOPLE):
    if random() < 0.7:
        print("GENERATE ADD FIRST")
        return _hw10_generate_add_first(LENGTH, PEOPLE)
    elif random() < 0.5:
        print("GENERATE N SQUARE")
        return _hw10_generate_n_square(LENGTH, PEOPLE)
    elif random() < 0.3:
        print("GENERATE CIRCLE")
        return _hw10_generate_circle(LENGTH, PEOPLE)
    else:
        print("GENERATE RANDOM")
        return _hw10_generate_random(LENGTH, PEOPLE)


def _hw10_generate_n_square(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0

    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj10) + "_" + choice(name10), randint(1000000, 10000000),
                                               randint(1, 80))
    relations = randint(people_num, people_num*(people_num)/2)
    relations = min(LENGTH - 2*people_num, relations)
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), randint(1,50))

    for i in range(LENGTH - PEOPLE - relations):
        pass

    return instrlist


def _hw10_generate_circle(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj10) + "_" + choice(name10), randint(1000000, 10000000),
                                               randint(1, 80))
    relations = randint(people_num, people_num * people_num / 2)
    relations = min(LENGTH - 50, relations)
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), 111)
    for i in range(LENGTH - PEOPLE - relations):
        instr = choice(["qgvs", "qgrs"])
        instrlist += '{} {}\n'.format(instr, randint(0, 10))
    return instrlist


def _hw10_generate_add_first(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0
    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj10) + "_" + choice(name10), randint(1000000, 10000000),
                                               randint(1, 80))
    for i in range(LENGTH - people_num):
        instr = choice(instrs10)
        if instr == "ap":
            continue
        if instr in limit.keys():
            if instr_count[instr] > limit[instr]:
                continue
            else:
                instr_count[instr] += 1
        if instr == 'ar':
            instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), 111)
        elif instr == 'qv' or instr == 'qc':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'qas' or instr == 'qnr':
            instrlist += '{} {}\n'.format(instr, r(people_num))
        elif instr == 'ca' or instr == 'cn' or instr == 'qci':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag':
            instrlist += 'ag {}\n'.format(group_num)
            group_num += 1
        elif instr == 'atg':
            instrlist += 'atg {} {}\n'.format(r(people_num), randint(1, 10))
        elif instr == 'qgps' or instr == 'qgrs' or instr == 'qgvs':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr == 'qgcs' or instr == 'qgam' or instr == 'qgav':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
    return instrlist


def _hw10_generate_random(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0
    for i in range(LENGTH):
        instr = choice(instrs10)
        if instr in limit.keys():
            if instr_count[instr] > limit[instr]:
                continue
            else:
                instr_count[instr] += 1
        if instr == 'ap':
            instrlist += "ap {} {} {} {}\n".format(i, choice(adj10) + "_" + choice(name10), randint(1000000, 10000000),
                                                   randint(1, 80))
        elif instr == 'ar':
            instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), 111)
        elif instr == 'qv' or instr == 'qc':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'qas' or instr == 'qnr':
            instrlist += '{} {}\n'.format(instr, r(people_num))
        elif instr == 'ca' or instr == 'cn' or instr == 'qci':
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag' and group_num < 10:
            instrlist += 'ag {}\n'.format(group_num)
            group_num += 1
        elif instr == 'atg':
            instrlist += 'atg {} {}\n'.format(r(people_num), randint(1, 10))
        elif instr == 'qgps' or instr == 'qgrs' or instr == 'qgvs':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr == 'qgcs' or instr == 'qgam' or instr == 'qgav':
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
    return instrlist


instrs11 = ['ap', 'ap', 'ar',
          'qci', 'qci', 'ag', 'atg', 'ag', 'atg', 'ag', 'atg',
          'qgps', 'qgrs', 'qgvs',
          'qgcs', 'qgam', 'qgav',
          'qasu', 'bf', 'qm',
          'qmp', 'qmp', 'qmp', 'qmp',
          'qsl', 'qsl',
          'dfg', 'dfg',
          'qbs', 'qbs'
          ]

name11 = ["Limbo", "Nyima", "Claw", "Orange"]
adj11 = ["fuck", "ugly", "damn", "shit", "nuts", "crap", "ass", "dick", "jerk", "cum", "cunt"]

limit11 = {
    "ap" : 800,
    "qsl": 20,
    "ag" : 10
}

instr_count11 = {
    "ap" : 0,
    "qsl": 0,
    "ag" : 0
}


def hw11_generator(LENGTH, PEOPLE):
    if random() < 0.8:
        print("GENERATE ADD FIRST")
        return _hw11_generate_add_first(LENGTH, PEOPLE)
    elif random() < 0.1:
        print("GENERATE N SQUARE")
        return _hw11_generate_n_square(LENGTH, PEOPLE)
    else:
        print("GENERATE RANDOM")
        return _hw11_generate_random(LENGTH, PEOPLE)


def _hw11_generate_n_square(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE

    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj11) + choice(name11), randint(1000000, 10000000),
                                               randint(1, 80))
    relations = randint(people_num, people_num*(people_num)/2)
    relations = min(LENGTH - 2*people_num, relations)
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), randint(1, 50))

    for i in range(LENGTH - PEOPLE - relations):
        pass

    return instrlist


def _hw11_generate_add_first(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 1
    for i in range(people_num):
        instrlist += "ap {} {} {} {}\n".format(i, choice(adj11) + choice(name11), randint(1000000, 10000000),
                                               randint(0, 80))
    relations = randint(int(people_num/2), min(people_num*10, int(LENGTH/2)))
    for i in range(relations):
        instrlist += "ar {} {} {}\n".format(r(people_num), r(people_num), randint(0, 1000))

    for i in range(LENGTH - people_num - relations):
        instr = choice(instrs11)
        if instr in limit11.keys():
            if instr_count11[instr] > limit11[instr]:
                i -= 1
                continue
            else:
                instr_count11[instr] += 1
        if instr == 'ap':
            instrlist += "ap {} {} {} {}\n".format(people_num + i, choice(adj11) + choice(name11), randint(1000000, 10000000),
                                                   randint(0, 80))
        elif instr in ['ar', 'bf']:
            instrlist += "{} {} {} {}\n".format(instr, r(people_num), r(people_num), randint(0, 1000))
        elif instr in ['qci', 'qmp', 'qsl']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag':
            instrlist += 'ag {}\n'.format(group_num + 1)
            group_num += 1
        elif instr in ['atg', 'dfg']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), randint(1, group_num))
        elif instr == 'qasu':
            instrlist += 'qasu {} {}\n'.format(randint(0, 20), randint(0, 80))
        elif instr == 'qbs':
            instrlist += 'qbs\n'
        elif instr == 'qm':
            instrlist += 'qm {}\n'.format(r(people_num))
        elif instr in ['qgps', 'qgrs', 'qgvs']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr in ['qgcs', 'qgam', 'qgav']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        else:
            print("unimplemented instruction {}".format(instr))
            exit(1)
    #print(len(instrlist.split("\n")))
    return instrlist


def _hw11_generate_random(LENGTH, PEOPLE):
    instrlist = ''
    people_num = PEOPLE
    group_num = 0
    for i in range(LENGTH):
        instr = choice(instrs11)
        if instr in limit11.keys():
            if instr_count11[instr] > limit11[instr]:
                i -= 1
                continue
            else:
                instr_count11[instr] += 1
        if instr == 'ap':
            instrlist += "ap {} {} {} {}\n".format(i, choice(adj11) + choice(name11), randint(1000000, 10000000),
                                                   randint(0, 80))
        elif instr in ['ar', 'bf']:
            instrlist += "{} {} {} {}\n".format(instr, r(people_num), r(people_num), randint(0, 1000))
        elif instr in ['qci', 'qmp', 'qsl']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), r(people_num))
        elif instr == 'ag':
            instrlist += 'ag {}\n'.format(group_num)
            group_num += 1
        elif instr in ['atg', 'dfg']:
            instrlist += '{} {} {}\n'.format(instr, r(people_num), randint(1, 10))
        elif instr == 'qasu':
            instrlist += 'qasu {} {}\n'.format(randint(0, 20), randint(0, 80))
        elif instr == 'qbs':
            instrlist += 'qbs\n'
        elif instr == 'qm':
            instrlist += 'qm {}\n'.format(r(people_num))
        elif instr in ['qgps', 'qgrs', 'qgvs']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        elif instr in ['qgcs', 'qgam', 'qgav']:
            instrlist += '{} {}\n'.format(instr, randint(0, group_num))
        else:
            print("unimplemented instruction {}".format(instr))
            exit(1)
    return instrlist