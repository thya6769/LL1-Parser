import common
import sys


def main():
    common.load_grammar(sys.argv[1])

    isll1 = True
    # recursively construct first sets
    try:
        # recursively construct first sets
        for v in common.non_terminals.values():
            if len(v.first_set) == 0:
                common.find_first_sets(v)
    except RuntimeError:
        isll1 = False

    if isll1: # if its LL1 calculate follow sets and print
        common.find_follow_sets()

        if common.fill_parse_table():
            for k1,k2 in common.parse_table:
                print("R[" + k1 + ","+ k2 + "] = " + str(common.rules.index((k1, common.parse_table[k1,k2]))))
        else:
            print("Grammar is not LL(1)!")
    else:
        print("Grammar is not LL(1)!")

if __name__ == '__main__':
    main()