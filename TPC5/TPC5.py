import re

def value_to_str(balance):
    b_str = str(balance)
    sep = b_str.split('.')
    result = sep[0] + 'e' + sep[1]
    if (len(sep[1]) == 1):
        result += '0'
    result += 'c'

    return result

def value(money, balance):
    qt = 0
    coins = money.split(', ')
    for coin in coins:
        if re.match(r"[125]0?c",coin) or re.match(r"[12]e",coin):
            if coin[-1] == 'c':
                qt += float(coin[:-1]) / 100
            else:
                qt += float(coin[:-1])
        else:
            print(f'maq: "Moeda inválida: {coin}"')
    
    print(f'maq: Saldo = {value_to_str(qt + balance)}')
    
    return qt + balance


def phone_call(number, balance):
    if re.match(r"601|641",number):
        print('maq: "Chamada bloqueada!"')
    
    else:
        if re.match(r"00",number):
            if (balance - 1.5 >= 0):
                balance -= 1.5
            else:
                print('maq: "Saldo insuficiente!"')

        elif re.match(r"2",number):
            if (balance - 0.25 >= 0):
                balance -= 0.25
            else:
                print('maq: "Saldo insuficiente!"')

        elif re.match(r"800",number):
            return balance

        elif re.match(r"808",number):
            if (balance - 0.1 >= 0):
                balance -= 0.1
            else:
                print('maq: "Saldo insuficiente!"')
    
        else:
            print('maq: "Número inválido!"')

        print(f'maq: Saldo = {value_to_str(balance)}')

    return balance


def process(state, balance):
    if re.match(r"LEVANTAR$", state):
        print('maq: "Operação inválida... A máquina já se encontra funcional!"')
        return balance

    elif re.match(r"POUSAR$", state) or re.match(r"ABORTAR$", state):
        return balance

    elif re.match(r"MOEDA ([0-9]+c, |[0-9]+e, )*([0-9]+c|[0-9]+e)$", state):
        return value(state.split("MOEDA ")[1], balance)
    
    elif re.match(r"T=([1-9][0-9]{8})$", state) or re.match(r"T=([0-9][1-9][0-9]{7})$", state) or re.match(r"T=(00[0-9]{9})$", state):
        return phone_call(state.split("T=")[1], balance)

    else:
        print('maq: "Opção inválida!"')
        return balance

    
def main():
    state = ""
    balance = 0
    while(state != "LEVANTAR"):
        state = input('maq: "Digite "LEVANTAR" para iniciar a cabine telefónica!"\n')

    print('maq: "Introduza moedas."')
    while (state != "ABORTAR" and state != "POUSAR"):
        state = input()
        balance = process(state, balance)

    print(f'maq: "troco={value_to_str(balance)}e; Volte sempre!"')

        
if __name__ == "__main__":
    main()