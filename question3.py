import sys
import common
import string

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

    if isll1:  # if its LL1 calculate follow sets and print
        common.find_follow_sets()

        if common.fill_parse_table():
            input_file = open(sys.argv[2], "r")

            for line in input_file:
                is_sentence_in_language(line.strip())
        else:
            print("Grammar is not LL(1)!")
    else:
        print("Grammar is not LL(1)!")


def is_sentence_in_language(line):
    stack = []
    stack.insert(0, '$')
    stack.insert(0, list(common.non_terminals.items())[0][0])
    i = 0
    a = line[i]

    while len(stack) != 0:
        x = stack[0].split()[0]
        # if x is a non_terminal
        # print(str(stack) + " " + a)

        if x in common.non_terminals.keys():
            if (x, a) in common.parse_table:
                stack.pop(0)
                if common.parse_table[x,a] != "epsilon":
                    for val in reversed(common.parse_table[x,a]):
                        # somehow there is a problem with character 'E' on input3_4
                        # it does not recognise it as E and has weird value, maybe due to encoding issue
                        # print(val + " " + str(ord(val[0])))
                        if len(val) == 1 and ord(val) == 917:
                            val = 'E'
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