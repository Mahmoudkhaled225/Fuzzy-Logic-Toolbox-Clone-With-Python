#Names&Id:-
#Mahmoud Khaled Helmy       20188045
#Gamal Hanafi Khalil        20198021
#Mohamed Ramadan Mohamed    20198071
#Aya Khalid Mohamed         20198016

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

variable = {}
f = open("enter the path", "r")
n = f.readline()
for line in range(int(n)):
    name = f.readline().split()
    l = name[1:4]
    variable[name[0]] = l

VariableKeys = list(variable.keys())
f.readline()
NumofSets = f.readline()

for i in range(int(NumofSets)):
    varName = f.readline().strip()
    if varName in VariableKeys:
        numOfProj = f.readline()
        for line in range(int(numOfProj)):
            name = f.readline().split()
            if name[1] == "TRAP":
                set = name[0]
                l = name[1:6]
                var = {}
                var[set] = l
                variable[varName].append(var)
            else:
                set = name[0]
                l = name[1:5]
                var = {}
                var[set] = l
                variable[varName].append(var)
        f.readline()

def MapingTrap(var):
    trpozdoa = [0, 1, 1, 0]
    result = tuple(map(list, zip(var, trpozdoa)))
    return result

def MapingTri(var):
    tri = [0, 1, 0]
    result = tuple(map(list, zip(var, tri)))
    return result

def fuzzification():

    projNum = int(f.readline())
    mylist = []
    for k in VariableKeys:
        if variable[k][0] == "IN":
            for n in range(3, len(variable[k])):
                z = list(variable[k][n].keys())[0]
                if variable[k][n][z][0] == "TRAP":
                    projArr1 = list(variable[k][n][z][1:5])
                    for i in range(0, len(projArr1)):
                        projArr1[i] = int(projArr1[i])
                    proj = int(projNum)
                    if proj >= MapingTrap(projArr1)[0][0] and proj < MapingTrap(projArr1)[3][0]:
                        LiProg = MapingTrap(projArr1)  # li->list
                        for i in range(len(LiProg)):
                            if proj >= LiProg[i][0] and proj < LiProg[i + 1][0]:
                                slope = (LiProg[i + 1][1] - LiProg[i][1]) / (LiProg[i + 1][0] - LiProg[i][0])
                                X = LiProg[i][0]
                                Y = LiProg[i][1]
                                C = Y - (slope * X)
                                membership = (slope * proj) + C
                                Small_List = [k, list(variable[k][n].keys())[0], membership]
                                mylist.append(Small_List)
                else:
                    exeArr1 = list(variable[k][n][z][1:4])
                    for i in range(0, len(exeArr1)):
                        exeArr1[i] = int(exeArr1[i])
                    proj = int(projNum)
                    if proj >= MapingTri(exeArr1)[0][0] and proj < MapingTri(exeArr1)[2][0]:
                        liExe = MapingTri(exeArr1)
                        for i in range(len(liExe)):
                            if proj >= liExe[i][0] and proj < liExe[i + 1][0]:
                                slope = (liExe[i + 1][1] - liExe[i][1]) / (liExe[i + 1][0] - liExe[i][0])
                                X = liExe[i][0]
                                Y = liExe[i][1]
                                C = Y - (slope * X)
                                membership = (slope * proj) + C
                                Small_List = [k, list(variable[k][n].keys())[0], membership]
                                mylist.append(Small_List)
            projNum = f.readline()
    return (mylist)

fuzzy_value = fuzzification()

def rules(val):
    final = []
    n_rules = f.readline()
    for n in range(int(n_rules) + 1):
        Num1 = 0
        Num2 = 0
        result = 0
        line = f.readline().split()
        for i in range(len(val)):
            if line[0:2] == val[i][0:2]:
                Num1 = val[i][2]
            if line[3:5] == val[i][0:2]:
                Num2 = val[i][2]
        if line[2] == "and":
            result = min(Num1, Num2)
        if line[2] == "or":
            result = max(Num1, Num2)
        if line[2] == "and_not":
            result = min(Num1, (1 - Num2))
        final.append([line[7], result])
    return final

ans = rules(fuzzy_value)

def makeSetUniqe(ans):
    setUniqe = []
    for i in range(len(ans)):
        temp = ans[i]
        for j in range(i + 1, len(ans)):
            if (temp[0] == ans[j][0]):
                setUniqe.append([ans[j][0], (max(temp[1], ans[j][1]))])
    for x in ans:
        if x not in setUniqe and x[0] not in setUniqe[0]:
            setUniqe.append(x)
    return setUniqe

def check(ans, vall):
    li = []
    member = []
    for i in range(len(ans)):
        if vall >= min(ans[i][0]) and vall <= max(ans[i][0]):
            li.append(ans[i])
    if len(li[0][0]) == 3:
        for i in range(len(li)):
            # print(li[i])
            liTri = MapingTri(li[i][0])
            for j in range(len(liTri)):
                if vall > liTri[j][0] and vall <= liTri[j + 1][0]:
                    slope = (liTri[j + 1][1] - liTri[i][1]) / (liTri[j + 1][0] - liTri[i][0])
                    X = liTri[j][0]
                    Y = liTri[j][1]
                    C = Y - (slope * X)
                    membership = (slope * vall) + C
                    member.append((membership, li[j][1]))
            break
    else:
        for i in range(len(li)):
            # print(li[i])
            liTri = MapingTrap(li[i][0])
            for j in range(len(liTri)):
                if vall > liTri[j][0] and vall <= liTri[j + 1][0]:
                    slope = (liTri[j + 1][1] - liTri[i][1]) / (liTri[j + 1][0] - liTri[i][0])
                    X = liTri[j][0]
                    Y = liTri[j][1]
                    C = Y - (slope * X)
                    membership = (slope * vall) + C
                    member.append((membership, li[j][1]))
            break

    return member[0]

def defuzzyfication(ans):
    uniqeSet = makeSetUniqe(ans)
    ans = []
    for k in VariableKeys:
        if variable[k][0] == "OUT":
            for n in range(3, len(variable[k])):
                z = list(variable[k][n].keys())[0]
                if variable[k][n][z][0] == "TRAP":
                    projArr1 = list(variable[k][n][z][1:5])
                    for i in range(0, len(projArr1)):
                        projArr1[i] = int(projArr1[i])
                    ans.append((projArr1, list(variable[k][n].keys())[0]))

                else:
                    exeArr1 = list(variable[k][n][z][1:4])
                    for i in range(0, len(exeArr1)):
                        exeArr1[i] = int(exeArr1[i])
                    ans.append((exeArr1, list(variable[k][n].keys())[0]))
    s2 = 0
    s3 = 0
    for i in range(len(uniqeSet)):
        s3 += uniqeSet[i][1]
    for i in range(len(ans)):
        if len(ans[i][0]) == 3:
            s = sum(ans[i][0])
            mean = s / len(ans[i][0])
            for j in range(len(uniqeSet)):
                if uniqeSet[j][0] == ans[i][1]:
                    s2 += mean * uniqeSet[j][1]
    Ans = s2 / s3
    type = check(ans, Ans)
    return (Ans, type)

king = defuzzyfication(ans)
print(f"The predicted is {king[1][1]} ({king[0]})")

def gui():
    x_prog_funding = np.arange(0, 100, 1)
    x_exelevel = np.arange(0, 60, 1)
    x_risk = np.arange(0, 100, 1)
    for i in range(3, 7):
        a0 = list(map(int, variable[VariableKeys[0]][i][list(variable[VariableKeys[0]][3].keys())[0]][1:6]))
        b0 = list(map(int, variable[VariableKeys[0]][i + 1][list(variable[VariableKeys[0]][4].keys())[0]][1:6]))
        c0 = list(map(int, variable[VariableKeys[0]][i + 2][list(variable[VariableKeys[0]][5].keys())[0]][1:6]))
        d0 = list(map(int, variable[VariableKeys[0]][i + 3][list(variable[VariableKeys[0]][6].keys())[0]][1:6]))
        break

    very_low = fuzz.trapmf(x_prog_funding, [a0[0], a0[1], a0[2], a0[3]])
    low = fuzz.trapmf(x_prog_funding, [b0[0], b0[1], b0[2], b0[3]])
    medium = fuzz.trapmf(x_prog_funding, [c0[0], c0[1], c0[2], c0[3]])
    high = fuzz.trapmf(x_prog_funding, [d0[0], d0[1], d0[2], d0[3]])
    for i in range(3, 6):
        a1 = list(map(int, variable[VariableKeys[1]][i][list(variable[VariableKeys[1]][3].keys())[0]][1:6]))
        b1 = list(map(int, variable[VariableKeys[1]][i + 1][list(variable[VariableKeys[1]][4].keys())[0]][1:6]))
        c1 = list(map(int, variable[VariableKeys[1]][i + 2][list(variable[VariableKeys[1]][5].keys())[0]][1:6]))
        break
    beginner = fuzz.trimf(x_exelevel, [a1[0], a1[1], a1[2]])
    intermediate = fuzz.trimf(x_exelevel, [b1[0], b1[1], b1[2]])
    expert = fuzz.trimf(x_exelevel, [c1[0], c1[1], c1[2]])

    for i in range(3, 6):
        a2 = list(map(int, variable[VariableKeys[2]][i][list(variable[VariableKeys[2]][3].keys())[0]][1:6]))
        b2 = list(map(int, variable[VariableKeys[2]][i + 1][list(variable[VariableKeys[2]][4].keys())[0]][1:6]))
        c2 = list(map(int, variable[VariableKeys[2]][i + 2][list(variable[VariableKeys[2]][5].keys())[0]][1:6]))
        break
    low1 = fuzz.trimf(x_risk, [a2[0], a2[1], a2[2]])
    normal = fuzz.trimf(x_risk, [b2[0], b2[1], b2[2]])
    high1 = fuzz.trimf(x_risk, [c2[0], c2[1], c2[2]])

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 10))

    ax0.plot(x_prog_funding, very_low, 'b', linewidth=2, label=list(variable[VariableKeys[0]][3].keys())[0])
    ax0.plot(x_prog_funding, low, 'g', linewidth=2, label=list(variable[VariableKeys[0]][4].keys())[0])
    ax0.plot(x_prog_funding, medium, 'r', linewidth=2, label=list(variable[VariableKeys[0]][5].keys())[0])
    ax0.plot(x_prog_funding, high, 'black', linewidth=2, label=list(variable[VariableKeys[0]][6].keys())[0])
    ax0.set_title('proj_funding_fuzzy')
    ax0.legend()
    ax0.axvline(x=0, ymin=0.05, ymax=0.96, color="b")
    ax0.axvline(x=99, ymin=0.05, ymax=0.96, color="black")

    ax1.plot(x_exelevel, beginner, 'b', linewidth=2, label=list(variable[VariableKeys[1]][3].keys())[0])
    ax1.plot(x_exelevel, intermediate, 'g', linewidth=2, label=list(variable[VariableKeys[1]][4].keys())[0])
    ax1.plot(x_exelevel, expert, 'r', linewidth=2, label=list(variable[VariableKeys[1]][5].keys())[0])
    ax1.set_title('exp_level_fuzzy')
    ax1.legend()
    ax1.axvline(x=59, ymin=0.05, ymax=0.93, color="r")

    ax2.plot(x_risk, low1, 'b', linewidth=2, label=list(variable[VariableKeys[2]][3].keys())[0])
    ax2.plot(x_risk, normal, 'g', linewidth=2, label=list(variable[VariableKeys[2]][4].keys())[0])
    ax2.plot(x_risk, high1, 'r', linewidth=2, label=list(variable[VariableKeys[2]][5].keys())[0])
    ax2.set_title('risk_fuzzy')
    ax2.legend()
    ax2.axvline(x=99, ymin=0.05, ymax=0.93, color="r")

    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.tight_layout()
    plt.show()

#gui()
