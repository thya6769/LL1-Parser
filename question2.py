import common
import sys


def main():
    common.load_grammar(sys.argv[1])

    # recursively construct first sets
    for v in common.non_terminals.values():
        if len(v.first_set) == 0:
            common.find_first_sets(v)

    common.find_follow_sets()
    common.fill_parse_table()

    for k1,k2 in common.parse_table:
        print("R[" + k1 + ","+ k2 + "] = " + str(common.rules.index((k1, common.parse_table[k1,k2]))))


if __name__ == '__main__':
    main()