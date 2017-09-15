
import common

def main():
    common.load_file()
    # recursively construct first sets
    for v in common.non_terminals.values():
        if len(v.first_set) == 0:
            common.find_first_sets(v)

    common.find_follow_sets()

    sort_sets()

    # for grammar in common.grammars.values():
    #     for g in grammar:
    #         print(g.lhs + " ", end="")
    #         print(g.first_set)

    # print
    print_sets("First")
    print_sets("Follow")


# reorder the first_set and follow_set in alphabetical order and epsilon at the end
def sort_sets():
    for non_terminal in common.non_terminals.values():
        non_terminal.first_set = sorted(non_terminal.first_set)
        non_terminal.follow_set = sorted(non_terminal.follow_set)
        # add epsilon to end if it contains one
        if "epsilon" in non_terminal.first_set:
            non_terminal.first_set.remove("epsilon")
            non_terminal.first_set.append("epsilon")
        if "$" in non_terminal.follow_set:
            non_terminal.follow_set.remove("$")
            non_terminal.follow_set.append("$")


def print_sets(command):
    print(command + ":")
    for key in sorted(common.non_terminals):
        non_terminal = common.non_terminals[key]
        print(" " + non_terminal.value + " ->", end="")

        if command == "First":

            for val in non_terminal.first_set:
                print(" " + val, end="")
        else:
            for val in non_terminal.follow_set:
                print(" " + val, end="")
        print("")



if __name__ == '__main__':
    main()
