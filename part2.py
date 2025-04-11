# CPSC 323 Project 2 - LL(1) Predictive Parser
# Author: Ashley Park

parsing_table = {
    'E': {'a': ['T', 'Q'], '(': ['T', 'Q']},
    'Q': {'+': ['+', 'T', 'Q'], '-': ['-', 'T', 'Q'], ')': ['ε'], '$': ['ε']},
    'T': {'a': ['F', 'R'], '(': ['F', 'R']},
    'R': {'+': ['ε'], '-': ['ε'], '*': ['*', 'F', 'R'], '/': ['/', 'F', 'R'], ')': ['ε'], '$': ['ε']},
    'F': {'a': ['a'], '(': ['(', 'E', ')']}
}

terminals = ['a', '+', '-', '*', '/', '(', ')', '$']
non_terminals = ['E', 'Q', 'T', 'R', 'F']

def trace_parse(input_string):
    stack = ['$', 'E']
    input_string = input_string.strip()
    if not input_string.endswith('$'):
        input_string += '$'

    index = 0
    step = 1 
    success = True

    print(f"\nInput: {input_string}")
    print(f"{'Step':<5} {'Stack':<30} {'Remaining Input':<20} {'Action'}")

    while stack:
        top = stack[-1]
        current_input = input_string[index:]

        if index >= len(input_string):
            break

        current_char = input_string[index]

        if top == current_char:
            print(f"{step:<5} {str(stack):<30} {current_input:<20} Match '{top}'")
            stack.pop()
            index += 1
        elif top in terminals:
            print(f"{step:<5} {str(stack):<30} {current_input:<20} Error: Unexpected terminal '{top}'")
            success = False
            break
        elif top in non_terminals:
            production = parsing_table.get(top, {}).get(current_char)
            if production:
                rule = f"{top} -> {' '.join(production)}"
                print(f"{step:<5} {str(stack):<30} {current_input:<20} Apply {rule}")
                stack.pop()
                if production[0] != 'ε':
                    for symbol in reversed(production):
                        stack.append(symbol)
            else:
                print(f"{step:<5} {str(stack):<30} {current_input:<20} Error: No rule for {top} with '{current_char}'")
                success = False
                break
        else:
            print(f"{step:<5} {str(stack):<30} {current_input:<20} Error: Invalid symbol '{top}'")
            success = False
            break

        step += 1

    print(f"\nFinal Stack: {stack}")
    if success and index == len(input_string):
        print("Output: String is accepted/ valid.\n")
    else:
        print("Output: String is not accepted/ In valid.\n")

# === Test all 3 required input strings ===
test_inputs = [
    "(a+a)*a$",
    "a*(a/a)$",
    "a(a+a)$" 
]

for test in test_inputs:
    trace_parse(test)
