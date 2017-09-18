import sys
import common
import re
import string
import random
from collections import defaultdict
from collections import OrderedDict
from collections import Counter

def main():
    common.load_grammar(sys.argv[1])
    convert_to_bnf()


def convert_to_bnf():
    new_terminals = OrderedDict()
    new_grammars = defaultdict(list)
    for non_terminal in common.non_terminals:
        for grammar in common.grammars[non_terminal]:

            rhs = " ".join(grammar.rhs)

            m_curly = re.match(".*\{.*\}.*", rhs)
            m_square = re.match("\[.*\]", rhs)
            m_or = re.match(".*|.*", rhs)


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
                symbols_in_brackets = rhs[rhs.find("[") + 1:rhs.find("]")].split()
                # use regex pattern matching
                result = re.sub("\[.*\]", new_terminal_symbol, rhs)

                if m_curly:
                    symbols_in_brackets = rhs[rhs.find("{") + 1:rhs.find("}")].split()
                    result = re.sub("\{.*\}", new_terminal_symbol, rhs)

                    # if its curly append the non_terminal symbol at the front
                    new_grammar.rhs.append(new_terminal_symbol)

                grammar.rhs = result.split()

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
                new_grammars[new_grammar.lhs].append(new_grammar)

                new_grammar = common.Grammar(grammar.lhs)
                new_grammar.rhs = rhs[index_of_or_symbol+1:len(rhs)].split()
                # update old grammar
                new_grammars[new_grammar.lhs].append(new_grammar)

    common.grammars.update(new_grammars)
    common.non_terminals.update(new_terminals)

    for grammar in common.grammars.values():
        for g in grammar:
            print(g.lhs + " ::=", end="")
            for symbol in g.rhs:
                print(" " + symbol, end="")
            print()


if __name__ == '__main__':
    main()