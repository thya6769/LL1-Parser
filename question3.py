import sys
import common

def main():
    common.load_grammar(sys.argv[1])

    # recursively construct first sets
    for v in common.non_terminals.values():
        if len(v.first_set) == 0:
            common.find_first_sets(v)

    common.find_follow_sets()
    common.fill_parse_table()

    input_file = open(sys.argv[2], "r")
    for line in input_file:
        is_sentence_in_language(line.strip())


def is_sentence_in_language(line):
    stack = []
    stack.insert(0, "$")
    stack.insert(0, list(common.non_terminals.items())[0][0])
    i = 0
    a = line[i]
    while len(stack) != 0:
        x = stack[0]
        if x in common.non_terminals:
            if (x, a) in common.parse_table:
                stack.pop(0)
                if common.parse_table[x,a] != "epsilon":
                    for val in reversed(common.parse_table[x,a]):
                        stack.insert(0, val)
            else:
                print("reject")
                return
        else:
            if x == a:
                stack.pop(0)
                if i == len(line) - 1:
                    a = "$"
                else:
                    i += 1
                    a = line[i]

            else:
                print("reject")
                return

    if a != "$":
        print("reject")
    else:
        print("accept")


if __name__ == '__main__':
    main()