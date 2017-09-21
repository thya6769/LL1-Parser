import sys
import common
import re
import string
import random
from collections import defaultdict
from collections import OrderedDict


def main():
    common.load_grammar(sys.argv[1])

    prev_grammar_len = sum([len(v) for v in common.grammars.values()])
    convert_to_bnf()
    current_grammar_len = sum([len(v) for v in common.grammars.values()])

    # loop until theres no change in length
    while prev_grammar_len != current_grammar_len:
        prev_grammar_len = sum([len(v) for v in common.grammars.values()])
        convert_to_bnf()
        current_grammar_len = sum([len(v) for v in common.grammars.values()])

    # print the new BNF form grammars
    for grammar in common.grammars.values():
        for g in grammar:
            print(g.lhs + " ::=", end="")
            for symbol in g.rhs:
                print(" " + symbol, end="")
            print()


def find_string_in_brackets(string, starting_index, left_bracket, right_bracket):
    i = starting_index
    count = 1

    while i < len(string):
        if string[i] == left_bracket:
            count += 1
        elif string[i] == right_bracket:
            if count == 1:
                return i
            count -= 1
        i += 1

def convert_to_bnf():
    new_terminals = OrderedDict()
    new_grammars = defaultdict(set)
    for non_terminal in common.non_terminals:
        for grammar in common.grammars[non_terminal]:

            rhs = " ".join(grammar.rhs)

            m_curly = re.match(".*\{.*\}.*", rhs)
            m_square = re.match(".*\[.*\].*", rhs)
            m_or = re.match(".*\|.*", rhs)
            # match {}
            if m_curly or m_square:
                # only up till combination of two alphabetic characters
                new_terminal_symbol = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
                while new_terminal_symbol in common.non_terminals \
                        or new_terminal_symbol in common.terminals:
                    new_terminal_symbol = random.choice(string.ascii_letters)

                new_non_terminal = common.NonTerminal(new_terminal_symbol)
                new_terminals[new_terminal_symbol] = new_non_terminal

                new_grammar = common.Grammar(new_terminal_symbol)

                starting_index = 0
                closing_index = 0

                if m_square:
                    starting_index = rhs.index("[") + 1
                    closing_index = find_string_in_brackets(rhs, starting_index, "[", "]")
                if m_curly:
                    starting_index = rhs.index("{") + 1
                    closing_index = find_string_in_brackets(rhs, starting_index, "{", "}")

                    # if its curly append the non_terminal symbol at the front
                    new_grammar.rhs.append(new_terminal_symbol)

                result = rhs[0: starting_index - 1] + new_terminal_symbol + rhs[closing_index + 1: len(rhs)]
                grammar.rhs = result.split()
                symbols_in_brackets = rhs[starting_index: closing_index].split()

                new_grammar.rhs.extend(symbols_in_brackets)
                new_grammars[new_grammar.lhs].append(new_grammar)

                # add transition to epsilon
                new_grammar = common.Grammar(new_terminal_symbol)
                new_grammar.rhs.append("epsilon")
                new_grammars[new_grammar.lhs].append(new_grammar)

            elif m_or:
                index_of_or_symbol = rhs.index("|")

                new_grammar = common.Grammar(grammar.lhs)
                new_grammar.rhs = rhs[0:index_of_or_symbol - 1].split()

                new_grammars[new_grammar.lhs].add(new_grammar)

                new_grammar = common.Grammar(grammar.lhs)
                new_grammar.rhs = rhs[index_of_or_symbol+1:len(rhs)].split()

                new_grammars[new_grammar.lhs].add(new_grammar)

    # print(common.grammars)
    # for k,v in new_grammars:
    #     if v not in common.grammars[k]:
    #         common.grammars[k].append(v)
    common.grammars.update(new_grammars)
    common.non_terminals.update(new_terminals)


if __name__ == '__main__':
    main()