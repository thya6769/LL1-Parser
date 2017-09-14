import sys
from collections import defaultdict
from collections import OrderedDict


non_terminals = OrderedDict() # dictionary of string as key and value as NonTerminal class
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


def main():
    load_file()
    # recursively construct first sets
    for v in non_terminals.values():
        if len(v.first_set) == 0:
            find_first_sets(v)




    # reorder the first_set in alphabetical order and epsilon at the end
    for non_terminal in non_terminals.values():
        non_terminal.first_set = sorted(non_terminal.first_set)

        # add epsilon to end if it contains one
        if "epsilon" in non_terminal.first_set:
            non_terminal.first_set.remove("epsilon")
            non_terminal.first_set.append("epsilon")

    # print
    print("First:")
    for key in sorted(non_terminals):
        non_terminal = non_terminals[key]
        print(" " + non_terminal.value + " ->", end="")

        for val in non_terminal.first_set:
            print(" " + val, end="")
        print("")


def find_first_sets(non_terminal):

    symbols = set()
    for grammar in grammars[non_terminal.value]:
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

    # remove epsilon if its a start symbol
    if non_terminal == list(non_terminals.items())[0][1] and "epsilon" in symbols:
        symbols.remove("epsilon")
    non_terminal.first_set = symbols

def find_follow_sets(non_terminal):


if __name__ == '__main__':
    main()
