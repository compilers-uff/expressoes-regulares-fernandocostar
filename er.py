import re
import State

def from_epsilon():
    #sigma = aceitos pela linguagem
    #q = estados do automato
    #delta = função de transicao como sendo {estado de partida: [(simbolo1, estado alcançavel1)...(simbolon, estado alcançaveln)]}
    #inicial = estado inicial do automato
    #finais = estados finais do automato
    #A = {sigma, Q, delta, inicial, finais}
    A = {"sigma": [], "q": ["q0", "q1"], "delta": {"q0": [tuple(("epsilon", "q1"))]}, "inicial": "q0", "finais": ["q1"]}
    return A

def from_symbol(symbol):
    #sigma = aceitos pela linguagem
    #q = estados do automato
    #delta = função de transicao como sendo {estado de partida: [(simbolo1, estado alcançavel1)...(simbolon, estado alcançaveln)]}
    #inicial = estado inicial do automato
    #finais = estados finais do automato
    #A = {sigma, Q, delta, inicial, finais}
    A = {"sigma": [symbol], "q": ["q0", "q1"], "delta": {"q0": [tuple((symbol, "q1"))]}, "inicial": "q0", "finais": ["q1"]}
    return A

def sum_to_name(name, n):
    return "q" + str(int(name[1:]) + n)

def get_struct(postfix):
    keys = list(set(re.sub('[^A-Za-z0-9]+', '', postfix)+'e'))
    return keys

def rename(len_a, B):

    n = len_a

    #rename states
    for i in range(len(B["q"])):
        B["q"][i] = sum_to_name(B["q"][i], n)

    new = {}

    #rename delta
    for each in B["delta"]:
        new[sum_to_name(each, n)] = []
        for i in range(len(B["delta"][each])):
            new[sum_to_name(each, n)].append(tuple((B["delta"][each][i][0], sum_to_name(B["delta"][each][i][1], n))))
    B["delta"] = new

    #rename initial state
    B["inicial"] = sum_to_name(B["inicial"], n)

    #rename final states
    for i in range(len(B["finais"])):
        B["finais"][i] = sum_to_name(B["finais"][i], n)

    return B

def add_epsilon_transition(A, B):

    #starts final A, connects starts B
    res = {"sigma": [], "q": [], "delta": {}, "inicial": None, "finais": []}

    #rename B
    B = rename(len(A["q"]), B)

    #update res sigma
    [res["sigma"].append(symbol) for symbol in A["sigma"] if symbol not in res["sigma"]]
    [res["sigma"].append(symbol) for symbol in B["sigma"] if symbol not in res["sigma"]]

    #update res states, once theres no intersection between those
    res["q"] = A["q"].copy() + B["q"].copy()

    #update delta
    for key in A["delta"]:
        res["delta"][key] = A["delta"][key].copy()
    for key in B["delta"]:
        res["delta"][key] = B["delta"][key].copy()

    #add epsilon transition
    if A["finais"][0] not in res["delta"]:
        res["delta"][A["finais"][0]] = [tuple(("epsilon", B["inicial"]))]
    else:
        res["delta"][A["finais"][0]].append(tuple(("epsilon", B["inicial"])))

    res["inicial"] = A["inicial"]
    res["finais"] = B["finais"].copy()
    return res

def add_symbol_transition(A, B, symbol):

    #starts final A, connects starts B
    res = {"sigma": [], "q": [], "delta": {}, "inicial": None, "finais": []}

    #rename B
    B = rename(len(A["q"]), B)

    #update res sigma
    [res["sigma"].append(symbol) for symbol in A["sigma"] if symbol not in res["sigma"]]
    [res["sigma"].append(symbol) for symbol in B["sigma"] if symbol not in res["sigma"]]

    #update res states, once theres no intersection between those
    res["q"] = A["q"].copy() + B["q"].copy()

    #update delta
    for key in A["delta"]:
        res["delta"][key] = A["delta"][key].copy()
    for key in B["delta"]:
        res["delta"][key] = B["delta"][key].copy()

    #add epsilon transition
    if A["finais"][0] not in res["delta"]:
        res["delta"][A["finais"][0]] = [tuple((symbol, B["inicial"]))]
    else:
        res["delta"][A["finais"][0]].append(tuple((symbol, B["inicial"])))

    if symbol not in res["sigma"]:
        res["sigma"].append(symbol)

    #initial and final states copied
    res["inicial"] = A["inicial"]
    res["finais"] = B["finais"].copy()
    return res


def concat(A, B):

    #starts final A, connects starts B
    res = {"sigma": [], "q": [], "delta": {}, "inicial": None, "finais": []}

    #rename B
    B = rename(len(A["q"])-1, B)

    #update res sigma
    [res["sigma"].append(symbol) for symbol in A["sigma"] if symbol not in res["sigma"]]
    [res["sigma"].append(symbol) for symbol in B["sigma"] if symbol not in res["sigma"]]

    #update res states, once theres no intersection between those
    res["q"] = A["q"].copy() + [each for each in B["q"].copy() if each not in A["q"].copy()]

    #update delta
    for key in A["delta"]:
        res["delta"][key] = A["delta"][key].copy()
    for key in B["delta"]:
        if key not in res["delta"]:
            res["delta"][key] = B["delta"][key].copy()
        else:
             res["delta"][key] += B["delta"][key].copy()

    res["inicial"] = A["inicial"]
    res["finais"] = B["finais"].copy()
    return res


def union(A, B):

        #starts final A, connects starts B
        res = {"sigma": [], "q": [], "delta": {}, "inicial": 'q0', "finais": []}

        #renames
        A = rename(1, A)
        B = rename(len(A["q"])+1, B)

        #update res sigma
        [res["sigma"].append(symbol) for symbol in A["sigma"] if symbol not in res["sigma"]]
        [res["sigma"].append(symbol) for symbol in B["sigma"] if symbol not in res["sigma"]]

        #update res states, once theres no intersection between those
        res["q"] = A["q"].copy() + B["q"].copy() + ["q0"] + ["q" + str(len(A["q"]) + len(B["q"]) + 1)]
        res["q"].sort()

        #update final states
        res["finais"] = ["q" + str(len(A["q"]) + len(B["q"]) + 1)].copy()

        #update delta
        for key in A["delta"]:
            res["delta"][key] = A["delta"][key].copy()
        for key in B["delta"]:
            res["delta"][key] = B["delta"][key].copy()

        #add epsilon transitions
        res["delta"][res["inicial"]] = [ tuple(("epsilon", A["inicial"])), tuple(("epsilon", B["inicial"])) ]
        res["delta"][A["finais"][0]] = [ tuple(("epsilon", res["finais"][0])) ]
        res["delta"][B["finais"][0]] = [ tuple(("epsilon", res["finais"][0])) ]
        return res


def closure(A):

    old_initial = sum_to_name(A["inicial"], 1)
    new_initial = "q0"

    old_final = sum_to_name(A["finais"][0], 1)
    new_final = sum_to_name(old_final, 1)

    A = rename(1, A)

    A["inicial"] = new_initial

    A["q"] += [new_initial, new_final]
    A["q"].sort()

    A["finais"] = [new_final]

    A["delta"][new_initial] = [ tuple(("epsilon", old_initial)), tuple(("epsilon", new_final)) ]
    A["delta"][old_final] = [ tuple(("epsilon", new_final)) ]
    A["delta"][old_final] += [tuple(("epsilon", old_initial))]

    return A

#transforms infix to posfix
def prefix2posfix(expression):

    print("initial exp:", expression)
    expression = expression.replace(",", "")
    expression = expression.replace(" ", "")

    print("replaced exp:", expression)

    s = expression

    stack = []

    s = s[::-1]

    for i in s:

        if i == '+' or i == '|' or i == '.':
            a = stack.pop()
            b = stack.pop()
            temp = a+b+i
            stack.append(temp)

        else:
            stack.append(i)

    print("postfix exp:", "".join(stack))
    return "".join(stack)

def erToAFNe(regex):

    #sigma = aceitos pela linguagem
    #q = estados do automato
    #delta = função de transicao como sendo {estado de partida: [(simbolo1, estado alcançavel1)...(simbolon, estado alcançaveln)]}
    #inicial = estado inicial do automato
    #finais = estados finais do automato
    #A = {sigma, Q, delta, inicial, finais}
    A = {"sigma": [], "q": [], "delta": {}, "inicial": None, "finais": []}

    if regex == "":
        return from_epsilon()

    stack = []

    for token in regex:

        if token == "*":
            print("closure")
            A = stack.pop()
            print("\n")
            stack.append(closure(A))
        elif token == "+":
            print("union")
            r = stack.pop()
            l = stack.pop()
            stack.append(union(r, l))
        elif token == ".":
            print("concat")
            r = stack.pop()
            l = stack.pop()
            stack.append(concat(l, r))
        else:
            print("add ", token)
            stack.append(from_symbol(token))
    return stack.pop()


def verify_epsilon_to_final(A):

    for state in A["delta"]:
        for pair in A["delta"][state]:
            if pair[0] == "epsilon" and pair[1] in A["finais"]:
                return False
    return True


def afneToAFN(A):

    temp_finals = []

    #mark new finals
    while(not verify_epsilon_to_final(A)): #keep until there are no states going with epsilon to final states
        #add all symbols transitions from states that have epsilon to final (careful to do not duplicate transitions)
        for state in A["delta"]:
            aux = []
            for pair in A["delta"][state]:
                if pair[0] == "epsilon":

                    if pair[1] in A["finais"]: A["finais"].append(state)

                    for symbol in A["sigma"]:
                        tmp_tuple = tuple( (symbol, pair[1]) )
                        if tmp_tuple not in aux:
                            aux.append(tmp_tuple)
                else:
                    aux.append(pair)
            A["delta"][state] = aux.copy()

    #remove epsilon transitions that goes finals
    for state in A["delta"]:
        for pair in A["delta"][state]:
            if not (pair[0] == "epsilon") and (pair not in A["delta"][state]):
                aux.append(pair)

    #update finals with the ones temp saved above
    A["finais"] += temp_finals
    print(A)
    return A



def main():

    postfix = prefix2posfix("*(.(a,b))")
    print(postfix)
    A = erToAFNe(postfix)
    A = afneToAFN(A)
    print("\n\n\n\n\n")
    print(A)
    for each in A:
        if each == "delta":
            for item in A[each]:
                print("     ", item, A[each][item])
        else:
            print(each, A[each])


main()
