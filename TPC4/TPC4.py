import re

def read_file(csv_path):
    lines = []

    file = open(csv_path, "r")
    for line in file:
        lines.append(line.rstrip().split(',', 3))

    file.close()
    return lines 


def lines_to_dicts(lines):
    main_dicts = []
    main_line = lines.pop(0)
    
    for line in lines:
        dict = {}
        for i in range(0,len(main_line)):
            if i < 3:
                dict[main_line[i]] = line[i]
            else:
                if re.search(r'{\d}',main_line[3]):
                    dict[main_line[i][:5]] = line[3].split(',')

                elif re.search(r'{\d,\d},',main_line[3]):    
                    dict[main_line[i][:5]] = list(filter(None, line[3].split(',')))

                elif re.search(r'{\d,\d}::',main_line[3]): 
                    operation = main_line[i][12:].split(",")[0]
                    key = main_line[i][:5] + "_" + operation
                    if operation == 'sum':
                        dict[key] = sum(map(int,list(filter(None, line[3].split(',')))))
                    elif operation == 'media':
                        i_list = list(filter(None, line[3].split(',')))
                        dict[key] = sum(map(int,i_list))/len(i_list)
                    else:
                        print('Operação não suportada!')
                else:
                    break
        main_dicts.append(dict)
    
    return main_dicts


def json_convert(json_path,main_dicts):
    file = open(json_path, "w")

    s_wr = "["
    list_size = len(main_dicts)
    for i in range(0,list_size):
        dict = main_dicts[i]
        s_wr += "\n  {"
        size = len(dict)
        counter = 0
        for key in dict:
            p_value = ""
            value = dict[key]
            if type(value) is list:
                p_value += "["
                for i in range(0,len(value)):
                    p_value += str(value[i])
                    if i < len(value)-1:
                        p_value += ","
                p_value += "]"
            elif type(value) is str:
                p_value += f'"{value}"'
            else:
                p_value += f'{str(value)}'
            s_wr += f'\n    "{key}": {p_value}'
            if counter < size-1:
                s_wr += ","
            counter += 1
        s_wr += "\n  }"
        if i < list_size - 1:
            s_wr += ","
    s_wr += "\n]"
    
    file.write(s_wr)
    file.close()


def main():
    lines = read_file('csv/alunos.csv')
    dicts = lines_to_dicts(lines)
    json_convert('json/alunos.json',dicts)

if __name__ == "__main__":
    main()
