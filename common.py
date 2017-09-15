from collections import defaultdict
from collections import OrderedDict
from collections import Counter

import sys

non_terminals = OrderedDict() # dictionary of string as key and value as NonTerminal class
terminals = set()
grammars = defaultdict(list) # multimap of grammars


class NonTerminal:

    def __init__(self, val):
        self.value = val
        self.first_set = set()
        self.follow_set = set()


class Grammar:
    def __init__(self, left):
        self.lhs = left
        self.rhs = []

        # for parsing table purpose
        self.first_set = set()


def load_file():
    input_file = open(sys.argv[1], "r")

    for line in input_file:
        line = line.split(" ::= ")
        left = line[0]
        right = line[1].split()

        non_terminal = NonTerminal(left)  # create non_terminal for left symbol
        non_terminals[non_terminal.value] = non_terminal

        grammar = Grammar(left)

        for value in right:
            grammar.rhs.append(value)

        grammars[left].append(grammar)

    # add all terminals
    for grammar in grammars.values():
        for g in grammar:
            for symbol in g.rhs:
                if symbol not in non_terminals and symbol != "epsilon":
                    terminals.add(symbol)


def find_first_sets(non_terminal):

    for grammar in grammars[non_terminal.value]:
        symbols = set()
        for symbol in grammar.rhs:
            if symbol == non_terminal.value: # skip this to avoid infinite recursion
                break
            elif symbol in non_terminals:

                if len(non_terminals[symbol].first_set) == 0:
                    find_first_sets(non_terminals[symbol])
                symbols |= non_terminals[symbol].first_set

                if "epsilon" not in symbols:
                    break
            else: # symbol is a terminal
                symbols.add(symbol)
                break

        # store first_set for each grammar
        if non_terminal == list(non_terminals.items())[0][1] and "epsilon" in symbols:
            symbols.remove("epsilon")
        grammar.first_set = symbols

    for grammar in grammars[non_terminal.value]:
        non_terminal.first_set |= grammar.first_set



def find_follow_sets():
    # add $ to follow set of start symbol
    list(non_terminals.items())[0][1].follow_set.add("$")
    while True:
        # store the sets before finding the follow set
        before = []
        for non_terminal in non_terminals.values():
            before.append(set(non_terminal.follow_set))

        # find follow_sets
        for v in non_terminals.values():
            helper_find_follow_sets(v)

        # compare the follow set after the execution
        i = 0
        for non_terminal in non_terminals.values():
            if Counter(before[i]) != Counter(non_terminal.follow_set):
                break
            i += 1
        if i >= len(before):
            break

def helper_find_follow_sets(non_terminal):

    for grammar in grammars[non_terminal.value]:
        for i in range(0, len(grammar.rhs)):
            symbols = set()

            # S -> X Y
            symbol_x = grammar.rhs[i]

            # if its a terminal no need to find follow set
            if symbol_x not in non_terminals:
                continue
            # if the index is at the end
            # or non_terminal -> non_terminal e.g. T ::= F
            elif i == len(grammar.rhs) - 1:
                symbols |= non_terminal.follow_set
            else:
                need_to_add_follow = True
                for j in range(i+1, len(grammar.rhs)):
                    symbol_y = grammar.rhs[j]

                    if symbol_y in non_terminals:
                        symbols |= non_terminals[symbol_y].first_set

                        if "epsilon" in symbols:
                            symbols.remove("epsilon")
                        else:
                            need_to_add_follow = False
                            break
                    else:
                        need_to_add_follow = False
                        if symbol_y != "epsilon":
                            symbols.add(symbol_y)
                        break

                if need_to_add_follow:
                    symbols |= non_terminal.follow_set

            non_terminals[symbol_x].follow_set |= symbols
