# CPSC 323 Project 2 - LL(1) Predictive Parser
# Author: Ashley Park

# --- Predictive Parsing Table ---
# Each non-terminal maps to a dictionary of terminals and their corresponding productions
parsing_table = {
    'E': {'a': ['T', 'Q'], '(': ['T', 'Q']},
    'Q': {'+': ['+', 'T', 'Q'], '-': ['-', 'T', 'Q'], ')': ['ε'], '$': ['ε']},
    'T': {'a': ['F', 'R'], '(': ['F', 'R']},
    'R': {'+': ['ε'], '-': ['ε'], '*': ['*', 'F', 'R'], '/': ['/', 'F', 'R'], ')': ['ε'], '$': ['ε']},
    'F': {'a': ['a'], '(': ['(', 'E', ')']}
}

# Terminals and non-terminals used for validation
terminals = ['a', '+', '-', '*', '/', '(', ')', '$']
non_terminals = ['E', 'Q', 'T', 'R', 'F']

def trace_parse(input_string):
    # Initialize parsing stack with end symbol and start symbol
    stack = ['$', 'E']
    
    # Sanitize input: ensure it ends with $
    input_string = input_string.strip()
    if not input_string.endswith('$'):
        input_string += '$'

    index = 0  # Pointer to current character in input
    step = 1   # Step counter for display
    success = True  # Track acceptance

    # Print header for tracing
    print(f"\nInput: {input_string}")
    print(f"{'Step':<5} {'Stack':<30} {'Remaining Input':<20} {'Action'}")

    # Main parsing loop
    while stack:
        top = stack[-1]                 # Symbol on top of the stack
        current_input = input_string[index:]  # Remaining input

        if index >= len(input_string):
            break

        current_char = input_string[index]  # Current input symbol

        # If top of stack matches current input character, pop and advance
        if top == current_char:
            print(f"{step:<5} {str(stack):<30} {current_input:<20} Match '{top}'")
            stack.pop()
            index += 1

        # If top of stack is terminal but doesn't match input → error
        elif top in terminals:
            print(f"{step:<5} {str(stack):<30} {current_input:<20} Error: Unexpected terminal '{top}'")
            success = False
            break

        # If top is non-terminal, look up production rule
        elif top in non_terminals:
            production = parsing_table.get(top, {}).get(current_char)
            if production:
                rule = f"{top} -> {' '.join(production)}"
                print(f"{step:<5} {str(stack):<30} {current_input:<20} Apply {rule}")
                stack.pop()
                if production[0] != 'ε':  # empty production
                    for symbol in reversed(production):
                        stack.append(symbol)
            else:
                print(f"{step:<5} {str(stack):<30} {current_input:<20} Error: No rule for {top} with '{current_char}'")
                success = False
                break

        # Invalid character in stack (not terminal or non-terminal)
        else:
            print(f"{step:<5} {str(stack):<30} {current_input:<20} Error: Invalid symbol '{top}'")
            success = False
            break

        step += 1

    # Final result reporting
    print(f"\nFinal Stack: {stack}")
    if success and index == len(input_string):
        print("Output: String is accepted/ valid.\n")
    else:
        print("Output: String is not accepted/ In valid.\n")


# === Required test strings ===
test_inputs = [
    "(a+a)*a$",   # Valid
    "a*(a/a)$",   # Valid
    "a(a+a)$"     # Invalid
]

# Run parser on each test input
for test in test_inputs:
    trace_parse(test)

