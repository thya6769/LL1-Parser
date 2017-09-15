import  common
from collections import OrderedDict
# key as pair of (non_terminal, terminal) value as list
parse_table = OrderedDict()
rules = [] # pair of rules to keep count

def main():
    common.load_file()
    # recursively construct first sets
    for v in common.non_terminals.values():
        if len(v.first_set) == 0:
            common.find_first_sets(v)

    common.find_follow_sets()
    fill_parse_table()

    for k1,k2 in parse_table:
        print("R[" + k1 + ","+ k2 + "] = " + str(rules.index((k1, parse_table[k1,k2]))))



def fill_parse_table():
    for grammar in common.grammars.values():
        for g in grammar:
            for terminal in g.first_set:
                if terminal != "epsilon":
                    parse_table[g.lhs, terminal] = g.rhs
                    if (g.lhs, g.rhs) not in rules:
                        rules.append((g.lhs, g.rhs))

            if "epsilon" in g.first_set:
                for terminal in common.non_terminals[g.lhs].follow_set:
                    parse_table[g.lhs, terminal] = "epsilon"
                    if (g.lhs, "epsilon") not in rules:
                        rules.append((g.lhs, "epsilon"))



if __name__ == '__main__':
    main()