import sys
from collections import defaultdict

non_terminals = {} # dictionary of string as key and value as NonTerminal class
grammars = defaultdict(list) # multimap of grammars


class NonTerminal:

    def __init__(self, val):
        self.value = val
        self.first_set = set()
        self.follow_set = set()

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Grammar:
    def __init__(self, left):
        self.lhs = left
        self.rhs = []


def main():
    input_file = open(sys.argv[1], "r")

    for line in input_file:
        line = line.split(" ::= ")
        left = line[0]
        right = line[1].split()

        non_terminal = NonTerminal(left) # create non_terminal for left symbol
        non_terminals[non_terminal.value] = non_terminal

        grammar = Grammar(left)

        for value in right:
            grammar.rhs.append(value)

        grammars[left].append(grammar)

    # for grammar in grammars.values():
    #     print grammar


    find_first_base() # find first set for base case

    # recursively find first set
    for non_terminal in non_terminals.values():
        if len(non_terminal.first_set) == 0:
            # concatenate sets
            non_terminal.first_set |= find_first_recursive(non_terminal)

    # print
    for non_terminal in non_terminals.values():
        print non_terminal.value + " ",
        print non_terminal.first_set


def find_first_base():
    for grammar in grammars.values():
        for val in grammar:
            symbol = val.rhs[0]  # first symbol on rhs
            if symbol not in non_terminals.keys():
                non_terminals[val.lhs].first_set.add(symbol)


def find_first_recursive(non_terminal):
    for grammar in grammars[non_terminal.value]:
        symbols = set()

        for symbol in grammar.rhs:
            if symbol in non_terminals and symbol != non_terminal.value: # symbol is a non_terminal

                symbols |= find_first_recursive(non_terminals[symbol])
                # continue until you reach symbols without epsilon
                if "epsilon" not in symbols:
                    return symbols
                else:
                    symbols.remove("epsilon")


    # we reached the base case thus return the first_set
    return non_terminal.first_set


if __name__ == '__main__':
    main()
