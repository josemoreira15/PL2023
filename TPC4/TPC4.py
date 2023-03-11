import re

def read_file(csv_path):
    lines = []

    file = open(csv_path, "r")
    for line in file:
        lines.append(line.rstrip().split(','))

    file.close()
    return lines 


def lines_to_dicts(lines):
    main_dicts = []
    main_line = lines.pop(0)

    counter = 0
    while(counter < len(main_line)):
        if '}' in main_line[counter] and main_line[counter-1][-1].isdigit():
            main_line[counter-1] += ',' + main_line[counter]
            main_line.pop(counter)
        counter += 1
    
    for line in lines:
        dict = {}
        for i in range(0,len(main_line)):
            if main_line[i] != '':
                list_type = re.search(r'(\w+){(\d+),*(\d*)}', main_line[i])
                
                if list_type:
                    key = list_type.group(1)
                    max = int(list_type.group(2))
                    if list_type.group(3):
                        max = int(list_type.group(3))
                    aux = []
                    for index in range(i,i+max):
                        if line[index] != '':
                            aux.append(line[index])
                        else:
                            break
                    value = aux

                    function_type = re.search(r'(\w+){(\d+),*(\d*)}::(\w+)', main_line[i])
                    if function_type:
                        function = function_type.group(3)
                        if function_type.group(4):
                            function = function_type.group(4)
                        key = list_type.group(1) + "_" + function
                        value = sum(map(int,aux))
                        if (function == 'media'):
                            value = float(sum(map(int,aux))) / float(len(aux))

                    dict[key] = value
                    
                    
                else: 
                    dict[main_line[i]] = line[i]

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
