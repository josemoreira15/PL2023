def get_number(string):
    list = []
    for i in range(0,len(string)):
        if string[i].isdigit():
            list.append(int(string[i]))
        else:
            return i,list
    
    return i+1,list


def nr_in_list(list):
    acc = 0
    size = len(list)
    for i in range(0,size):
        acc += (list[i] * 10**(size-i-1))

    return acc


def process(list,flag,sum):
    it = 0
    while it < len(list):
        if flag == 0:
            if it < len(list)-1 and (list[it] == 'O' or list[it] == 'o') and (list[it+1] == 'N' or list[it+1] == 'n'):
                flag = 1
                it += 1
                print('>>> The counter is ON! <<<')
            elif list[it] == '=':
                print(f'[>>> The sum is {sum}! <<<]')
                it += 1
            else:
                it += 1
        if flag == 1:
            if it < len(list)-2 and (list[it] == 'O' or list[it] == 'o') and (list[it+1] == 'F' or list[it+1] == 'f') and (list[it+2] == 'F' or list[it+2] == 'f'):
                flag = 0
                it += 3
                print('>>> The counter is OFF! <<<')
            elif list[it].isdigit():
                result = get_number(list[it:])
                it += result[0]
                sum += nr_in_list(result[1])
            elif list[it] == '=':
                print(f'[>>> The sum is {sum}! <<<]')
                it += 1
            else:
                it += 1
    
    return sum,flag


def main():
    sum, flag = 0,1
    print('>>> The counter is ON! <<<')
    while(1):
        s = input('>>> Type your string: ')

        sum,flag = process(s,flag,sum)

if __name__ == "__main__":
    main()
