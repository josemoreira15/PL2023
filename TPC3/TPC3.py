import re
import json

def read_file(path):
    f = open(path)
    ds = []

    for line in f:
        got = re.search(r'(?P<id>\d+)::(?P<date>\d{4}-\d{2}-\d{2})(?P<content>::.+)[::::|.::]', line)
        if got != None:
            dic = got.groupdict()
            ds.append(dic)
    
    return ds


def proc_per_year(ds):
    res = {}
    procs = {}

    for dic in ds:
        proc_got = re.findall(r'Proc.(\d+).',dic.get('content'))
        date = dic.get('date')
        for proc in proc_got:
            conc = proc + ' : ' + date
            if conc not in procs:
                procs[conc] = 1
                year = date[:4]
                if year not in res:
                    res[year] = 0
                res[year] += 1

    keys = sorted(res)
    sorted_res = {k : res[k] for k in keys}
    return sorted_res
        

def find_sec(year):
    if year[2:] == '00':
        return int(year[:2])
    return (int(year[:2]) + 1)

def most_common_names(ds):
    res = []
    np = {}
    na = {}
    for dic in ds:
        sec = find_sec(dic.get('date')[:4])
        if sec not in np:
            np[sec] = {}
        if sec not in na:
            na[sec] = {}


        namesP = re.findall(r'::([A-Z][a-z]+)\s',dic.get('content'))
             
        for nameP in namesP:
            if nameP not in np[sec]:
                np[sec][nameP] = 0
            np[sec][nameP] += 1

        namesP2 = re.findall(r'\s\s+([A-Z][a-z]{2}[a-z]+)\s',dic.get('content'))
        for nameP2 in namesP2:
            if nameP2 not in np[sec]:
                np[sec][nameP2] = 0
            np[sec][nameP2] += 1
        
        namesA = re.findall(r'\s([A-Z][a-z]{2}[a-z]+)[,|::]',dic.get('content'))
        for nameA in namesA:
            if nameA not in na[sec]:
                na[sec][nameA] = 0
            na[sec][nameA] += 1
        
        namesA2 = re.findall(r'\s([A-Z][a-z]{2}[a-z]+)::',dic.get('content'))
        for nameA2 in namesA2:
            if nameA2 not in na[sec]:
                na[sec][nameA2] = 0
            na[sec][nameA2] += 1
    
    res.append(np)
    res.append(na)

    return res


def relation_freq(ds):
    res = {}
    for dic in ds:
        rels = re.findall(r'[a-z],([A-Z][a-zA-Z]*\s*[a-zA-Z]*?)\.\s[a-zA-Z]',dic.get('content'))
        for rel in rels:
            if rel not in res:
                res[rel] = 0
            res[rel] += 1

    sorted_res = {k : res[k] for k in sorted(res, key = res.get)}
    return sorted_res


def create_json(ds):
    output = open("output.json","w")
    var = "[\n"
    for i in range(0,20):
        keys = list(ds[i].keys())
        var += "    {\n"
        for j in range (0,3):
            if j < 2:
                var += f'        "{keys[j]}": "{ds[i].get(keys[j])}",\n'
            else:
                var += f'        "{keys[j]}": "{ds[i].get(keys[j])}"'
        if i<19:
            var += "\n    },\n"
        else:
            var += "\n    }\n"
    var += "]"
    
    output.write(var)
    output.close()


def print_proc_per_year(res):
    print('|----------------------------------------------|')
    print('|       DISTRIBUIÇÃO DE PROCESSOS POR ANO      |')
    print('|                                              |')
    print('|      (apenas se encontram representados      |')
    print('|       os anos com processos registados)      |')
    print('|----------------------------------------------|')
    print('|----------------------------------------------|')
    print('|       Ano       |     Número de processos    |')
    print('|----------------------------------------------|')
    print('|----------------------------------------------|')
    for key in res:
        print('|    {:^9}    |          {:^9}         |'.format(key,res[key]))
        print('|----------------------------------------------|')


def print_names_per_sec(res):
    print('|-------------------------------------------------------------------------|')
    print('|                 FREQUÊNCIA DE NOMES PRÓPRIOS E APELIDOS                 |')
    print('|                                POR SÉCULO                               |')
    print('|-------------------------------------------------------------------------|')
    print('|-------------------------------------------------------------------------|')
    print('|      Século     |    NOME PRÓRIO [número]   |      APELIDO [número]     |')
    print('|-------------------------------------------------------------------------|')
    print('|-------------------------------------------------------------------------|')

    ks = list(res[0].keys())
    ks.sort()
    
    for k in ks:
        np = res[0].get(k)
        sorted_np = {k : np[k] for k in sorted(np, key = np.get, reverse = True)[:5]}
        k_list = list(sorted_np.keys())
        
        na = res[1].get(k)
        sorted_na = {k : na[k] for k in sorted(na, key = na.get, reverse = True)[:5]}
        k2_list = list(sorted_na.keys())
        
        for i in range(0,5):
            if i == 0:
                print('|    {:^9}    |   {:^9} [{:^9}]   |   {:^9} [{:^9}]   |'.format(k,k_list[i],sorted_np[k_list[i]],k2_list[i],sorted_na[k2_list[i]]))
            else:
                print('|                 |   {:^9} [{:^9}]   |   {:^9} [{:^9}]   |'.format(k_list[i],sorted_np[k_list[i]],k2_list[i],sorted_na[k2_list[i]]))
        
        print('|-------------------------------------------------------------------------|')

    
def print_relation_freq(res):
    print('|------------------------------------------|')
    print('|          Frequência de Relações          |')
    print('|------------------------------------------|')
    print('|------------------------------------------|')
    print('|       Relação       |     Frequência     |')
    print('|------------------------------------------|')
    print('|------------------------------------------|')
    for key in res:
        print('| {:^20}|      {:^9}     |'.format(key,res[key]))
        print('|------------------------------------------|')


def main():
    ds = read_file("processos.txt")

    res1 = proc_per_year(ds)
    print_proc_per_year(res1)
    res2 = most_common_names(ds)
    print_names_per_sec(res2)
    res3 = relation_freq(ds)
    print_relation_freq(res3)
    create_json(ds)


if __name__ == "__main__":
    main()   