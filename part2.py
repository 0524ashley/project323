"""
CPSC 323 – Project 2: LL(1) Predictive Parser
Author: Ashley Park
Date: April 2025
Filename: part2.py

Description:
-------------
This program implements a predictive parser for a simplified arithmetic expression grammar 
based on a given context-free grammar (CFG) and a predictive parsing table. It accepts input 
strings composed of symbols from the set { a, +, -, *, /, (, ), $ }, processes them using a 
stack-based LL(1) parsing technique, and determines if the input is valid according to the grammar.

The program also prints a detailed trace of the parsing process, including stack state, remaining 
input, and actions taken at each step (such as matching terminals or applying production rules).

GNU General Public License:
----------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
""" 


# predictive parsing_table
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

