import sys
from collections import defaultdict

non_terminals = {} # dictionary of string as key and value as NonTerminal class
grammars = defaultdict(list) # multimap of grammars
#
#
# class NonTerminal:
#
#     def __init__(self, val):
#         self.value = val
#         self.first_set = []
#         self.follow_set = []
#
#     def __hash__(self):
#         return hash(self.value)
#
#     def __eq__(self, other):
#         return self.value == other.value


class Grammar:
    def __init__(self, left):
        self.lhs = left
        self.rhs = []
        self.first_set = []
        self.follow_set = []


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

    # fill in the initial first_set from the grammar
    order_first_set()
    find_first_set()


    #
    # # recursively find first set for any grammar with first symbol being non_terminal
    # for non_terminal in non_terminals.values():
    #     for grammar in grammars[non_terminal.value]:
    #         if grammar.rhs[0] in non_terminals:
    #             # print grammar.lhs + " " + grammar.rhs[0]
    #             # concatenate sets
    #             non_terminal.first_set |= find_first_recursive(non_terminal)

    # print
    print "First:"
    for non_terminal in non_terminals.values():
        print " " + non_terminal.value + " ->",

        for val in non_terminal.first_set:
            print " " + val,
        print ""


def initial_first_set():
    for non_terminal in non_terminals.values():
        for grammar in grammars[non_terminal.value]:
            for symbol in grammar.rhs:
                non_terminal.first_set.append(symbol)
                if symbol not in non_terminals:
                    break


def find_first_set():

    needs_first_set = []  # list of non_terminals that needs computations of first set
    for non_terminal in non_terminals.values():
        needs_first_set.append(non_terminal)

    # use a stack and continue until empty
    while len(needs_first_set) != 0:

        current = needs_first_set.pop()

        first_set = []
        first_set.append(current.first_set)
        for symbol in first_set:
            if symbol in non_terminals:
                current.first_set.remove(symbol)
                current.first_set.insert(non_terminals[symbol].first_set, 0)


        # check if it contains non_terminals
        for value in current.first_set:
            if value in non_terminals:
                needs_first_set.append(current)
                break



# def find_first_base():
#     for grammar in grammars.values():
#         for val in grammar:
#             symbol = val.rhs[0]  # first symbol on rhs
#             if symbol not in non_terminals.keys():
#                 non_terminals[val.lhs].first_set.add(symbol)
#
#
# def find_first_recursive(non_terminal):
#
#     for grammar in grammars[non_terminal.value]:
#         if grammar.rhs[0] not in non_terminals:
#             # print grammar.lhs + " " + grammar.rhs[0]
#             # print non_terminal.first_set
#             return non_terminal.first_set
#
#         else: # non-terminal
#             symbols = set()
#             contains_epsilon = False
#             for symbol in grammar.rhs:
#                 if symbol in non_terminals and symbol != non_terminal.value:
#                     symbols |= find_first_recursive(non_terminals[symbol])
#                     # continue until you reach symbols without epsilon
#                     if "epsilon" not in symbols:
#                         return symbols
#                     else:
#                         symbols.remove("epsilon")
#                         contains_epsilon = True
#                 else: # symbol is a terminal so add it
#                     if contains_epsilon:
#                         symbols.add(symbol)
#                         return symbols



if __name__ == '__main__':
    main()
