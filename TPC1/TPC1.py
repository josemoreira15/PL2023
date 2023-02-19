def read_file(path):
    f = open(path)
    lines = []

    for line in f:
        lines.append(line.rstrip().split(","))

    lines.pop(0)

    return lines


def sickness_per_sex(lines):
    men = 0
    women = 0
    mSick = 0
    wSick = 0
    result = []
    menL = []
    womenL = []

    for line in lines:
        if line[1] == 'F':
            women +=1
            if line[5] == '1':
                wSick += 1
        else:
            men += 1
            if line[5] == '1':
                mSick += 1
    
    menL.append(mSick)
    menL.append(men)
    womenL.append(wSick)
    womenL.append(women)

    result.append(menL)
    result.append(womenL)

    return result


def max_age_max_min_cholesterol(lines):
    maxA = 0
    maxC = 0
    minC = 999
    result = []

    for line in lines:
        value = int(line[0])
        if value > maxA:
            maxA = value
        
        col = int(line[3])
        if col > maxC:
            maxC = col 
        elif col < minC:
            if col != 0:
                minC = col
        
    
    result.append(maxA)
    result.append(maxC)
    result.append(minC)

    return result


def escaloes(maxAge, maxChol, minChol):
    minA = 30
    excx = []

    excA = dict()
    excC = dict()

    while minA <= maxAge:
        excA[minA] = [0,0]
        minA += 5

    excC[0] = [0,0]
    while minChol <= maxChol:
        excC[minChol] = [0,0]
        minChol += 10
    
    excx.append(excA)
    excx.append(excC)

    return excx


def insert_escaloes_age(excA, age, flag):
    if flag == 0:
        for key in excA:
            if age >= key and age <= (key + 4):
                excA[key][0] += 1
                excA[key][1] += 1
                break
    
    else:
        for key in excA:
            if age >= key and age <= (key + 4):
                excA[key][1] += 1
                break


def sickness_per_age(lines, excA):
    for line in lines:
        if line[5] == '1':
            insert_escaloes_age(excA,int(line[0]),0)

        else:
            insert_escaloes_age(excA,int(line[0]),1)
    
    return excA


def insert_escaloes_cholesterol(excC,chol,flag):
    if flag == 0:
        for key in excC:
            if chol >= key and chol <= (key + 9):
                excC[key][0] += 1
                excC[key][1] += 1
                break
    
    else:
        for key in excC:
            if chol >= key and chol <= (key + 9):
                excC[key][1] += 1
                break


def sickness_per_cholesterol(lines, excC):
    for line in lines:
        if line[5] == '1':
            insert_escaloes_cholesterol(excC,int(line[3]),0)
        else:
            insert_escaloes_cholesterol(excC,int(line[3]),1)
    
    return excC


def print_sex(list):
    print(f'Há {list[0][0]} homens doentes num total de {list[0][1]}!')
    print(f'Há {list[1][0]} mulheres doentes num total de {list[1][1]}')


def print_age(result):
    for key in result[0]:
        print(f'Idade: {key}-{key + 4} -> Número de doentes: {result[0][key]}')


def print_cholesterol(result):
    for key in result[0]:
        print(f'Colesterol: {key}-{key + 9} -> Número de doentes: {result[0][key]}')


def print_table_sex(list):
    print('|----------------------------------------|')
    print('|     Distribuição da doença por sexo    |')
    print('|----------------------------------------|')
    print('|     Sexo     |   Doentes   |   Total   |')
    print('|----------------------------------------|')

    for index in range(0,2):
        if index == 0: 
            print('|       M      |  {:^9}  | {:^9} |'.format(*list[index]))
        else:
            print('|       F      |  {:^9}  | {:^9} |'.format(*list[index]))
        print('|----------------------------------------|')


def print_table_age(excA):
    print('|----------------------------------------|')
    print('|    Distribuição da doença por idade    |')
    print('|----------------------------------------|')
    print('|     Idade    |   Doentes   |   Total   |')
    print('|----------------------------------------|')

    for key in excA:
        print("|     {}-{}    |  {:^9}  | {:^9} |".format(key,key+4,excA[key][0],excA[key][1]))
        print('|----------------------------------------|')


def print_table_cholesterol(excC):
    print('|----------------------------------------|')
    print('|  Distribuição da doença por colesterol |')
    print('|----------------------------------------|')
    print('|  Colesterol  |   Doentes   |   Total   |')
    print('|----------------------------------------|')

    for key in excC:
        if key == 0:
            print("|    [ND]/0    |  {:^9}  | {:^9} |".format(excC[key][0],excC[key][1]))
        
        elif key < 100:
            print("|     {}-{}    |  {:^9}  | {:^9} |".format(key,key+4,excC[key][0],excC[key][1]))

        else:
            print("|    {}-{}   |  {:^9}  | {:^9} |".format(key,key+4,excC[key][0],excC[key][1]))
        
        print('|----------------------------------------|')

def main():
    lines = read_file("myheart.csv")
    values = max_age_max_min_cholesterol(lines)
    excx = escaloes(values[0],values[1],values[2])

    result1 = sickness_per_sex(lines)
    print_table_sex(result1)
    result2 = sickness_per_age(lines, excx[0])
    print_table_age(result2)
    result3 = sickness_per_cholesterol(lines, excx[1])
    print_table_cholesterol(result3)


if __name__ == "__main__":
    main()
