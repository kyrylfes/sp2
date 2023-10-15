def load_fa(file_path):
    fa = {}

    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

        num_states, num_transitions = map(int, lines[0].split())
        start_state = int(lines[1])

        final_states = set(map(int, lines[2].split()[1:]))

        for line in lines[3:]:
            s, a, s_prime = line.split()
            s = int(s)
            s_prime = int(s_prime)

            if s not in fa:
                fa[s] = {}

            if a not in fa[s]:
                fa[s][a] = s_prime

    return num_states, start_state, final_states, fa


def find_reachable_states(fa, start_state):
    reachable_states = set()
    stack = [start_state]

    while stack:
        current_state = stack.pop()

        if current_state not in reachable_states:
            reachable_states.add(current_state)

            if current_state in fa.keys():
                for a in fa[current_state].values():
                    stack.append(a)

    return reachable_states


def find_unreachable_states(fa, reachable_states):
    all_states = set()

    for state in fa:
        all_states.add(state)

    unreachable_states = all_states - reachable_states

    return unreachable_states if unreachable_states else {}


def find_deadend_states(fa, final_states):
    deadend_states = set()
    visited_states = set()

    for state in fa.keys():
        if state not in visited_states:
            find_deadend_states_recursive(fa, state, visited_states, final_states, deadend_states)

    return deadend_states if deadend_states else {}


def find_deadend_states_recursive(fa, current_state, visited_states, final_states, deadend_states):
    visited_states.add(current_state)

    if current_state not in fa:
        if current_state in final_states:
            return

        deadend_states.add(current_state)
        return

    for next_state in fa[current_state].values():
        if next_state not in visited_states:
            find_deadend_states_recursive(fa, next_state, visited_states, final_states, deadend_states)


def main():
    num_states, start_state, final_states, fa = load_fa("automaton.txt")
    reachable_states = find_reachable_states(fa, start_state)
    unreachable_states = find_unreachable_states(fa, reachable_states)
    deadend_states = find_deadend_states(fa, final_states)

    print("Досяжні стани:", reachable_states)
    print("Недосяжні стани:", unreachable_states)
    print("Тупикові стани:", deadend_states)


if __name__ == '__main__':
    main()
