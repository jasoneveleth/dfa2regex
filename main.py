FA = """
q0
# arrows
q0:0>q1
q0:1>q0
q1:0>q1
q1:1>q2
q2:0>q3
q2:1>q0
q3:0>q3
q3:1>q3
# accepting states
q0
q1
q2
"""
ORDER_OF_REMOVAL = ["q2", "q1", "q0"]

e = "\u03B5" # epsilon

def fa2str(transition, end_states=["end"]):
    """converts finite automata to graphviz dot commands"""

    ret = ""
    ret += "digraph g {\n"
    ret += "rankdir=LR;\n"
    ret += f'node [ shape = "doublecircle"];'
    for s in end_states:
        ret += ' ' + s
    ret += '\n'

    ret += 'node [ shape = "circle"];\n'
    for s in transition:
        ret += f'"{s}" [ label = "{s}"]\n'
    for s in transition:
        for o in transition[s]:
            ret += f'"{s}" -> {o} [label = "{transition[s][o]}"]\n'
    ret += "}\n"
    return ret

def has_top_lvl_u(s):
    """checks if there's a top level union"""
    lvl = 0
    for i in s:
        if i == '(':
            lvl += 1
        elif i == ')':
            lvl -= 1
        elif i == 'U' and lvl == 0:
            return True
    return False

def concat(*args):
    """returns a string of the concatenation of input regex's (input as strings)"""
    ret = ""
    for r in args:
        if r == e: # skip empty string
            continue

        if has_top_lvl_u(r):
            ret += f'({r})'
        else:
            ret += r
    return ret

def union(*args):
    """returns a string of the union of input regex's (input as strings)"""
    on_our_first = True
    ret = ""
    for r in args:
        if r == "":
            continue

        if not on_our_first and len(r) >= 2:
            ret += f'({r})'
        else:
            ret += r

        on_our_first = False

        if ret != "": # only want to union if there's something there
            ret += 'U'
    return ret[:-1] # cut off last U

def star(r):
    """returns a string of the start of a regex (inptu as a string)"""
    if r == "" or r == e:
        return r

    if has_top_lvl_u(r) or len(r) >= 2:
        return f'({r})*'
    else:
        return f'{r}*'

def construct_dfa(fa):
    """turn input string into dfa"""
    i = 0
    lines = fa.split('\n')

    start_state = lines[i]
    i += 2 # skip over next line too

    transition = {"start": {start_state: e}, "end": {}}

    # handle all the arrows and break at the next comment
    while i < len(lines):
        if lines[i][0] == '#':
            i += 1
            break
        line = lines[i]
        src, tmp = line.split(':')
        regex, dst = tmp.split('>')
        if src not in transition:
            transition[src] = {dst: regex}
        else:
            if dst in transition[src]:
                transition[src][dst] = union(regex, transition[src][dst])
            else:
                transition[src][dst] = regex
        i += 1

    # handle all accept states
    while i < len(lines):
        if lines[i] not in transition:
            transition[lines[i]] = {"end": e}
        else:
            transition[lines[i]]["end"] = e
        i += 1
    return transition

def main():
    fa = construct_dfa(FA[1:-1]) # cut off first and last newline

    # we remove state r at each step
    for r in ORDER_OF_REMOVAL:
        print(fa2str(fa))
        print()

        # i -> r -> f     ===>    i ------> f
        for i in fa: # initial part of path
            if i == r or (r not in fa[i]): # skip r self-loops, and nodes that don't point to r
                continue

            for f in fa[r]: # final part of path
                if f == r: # skip r self-loops
                    continue

                old_if = '' if f not in fa[i] else fa[i][f]
                ir = '' if fa[i][r] == e else fa[i][r]
                rr = '' if r not in fa[r] else fa[r][r]
                rf = '' if fa[r][f] == e else fa[r][f]

                fa[i][f] = union(old_if, concat(ir, star(rr), rf))

            fa[i].pop(r)
        fa.pop(r)
    print(fa2str(fa))

if __name__ == "__main__":
    main()
