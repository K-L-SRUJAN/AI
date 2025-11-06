# CNF Conversion for First-Order Logic
# Supports: ∧, ∨, ¬, →, ↔, ∀, ∃

import re
 
def remove_implications(expr):
    expr = expr.replace('↔', '<->').replace('→', '->')
 
    expr = re.sub(r'([A-Za-z0-9_()]+)\s*->\s*([A-Za-z0-9_()]+)',
                  r'(~\1 ∨ \2)', expr)
 
    expr = re.sub(r'([A-Za-z0-9_()]+)\s*<->\s*([A-Za-z0-9_()]+)',
                  r'((\1 -> \2) ∧ (\2 -> \1))', expr)
    return expr

 
def move_negation(expr):
    expr = expr.replace("¬", "~")
 
    expr = expr.replace("~(A ∧ B)", "(~A ∨ ~B)")
    expr = expr.replace("~(A ∨ B)", "(~A ∧ ~B)")
 
    expr = expr.replace("~∀", "∃~")
    expr = expr.replace("~∃", "∀~")
    return expr
 
def standardize_variables(expr):
    var_map = {}
    new_expr = ""
    counter = 0

    for ch in expr:
        if ch.islower():
            if ch not in var_map:
                var_map[ch] = f"v{counter}"
                counter += 1
            new_expr += var_map[ch]
        else:
            new_expr += ch

    return new_expr

 
def skolemize(expr):
 
    expr = re.sub(r'∃([a-z][0-9]*)', '', expr)
    expr = re.sub(r'([a-z][0-9]*)', r'c_\1', expr)
    return expr
 
def distribute(expr):
    expr = expr.replace("∨", " OR ").replace("∧", " AND ")
    expr = expr.replace("(", " ( ").replace(")", " ) ")
    return expr
 
def to_cnf(expr):
    print("\n--- Original Expression ---")
    print(expr)

    expr = remove_implications(expr)
    print("\nStep 1: Remove implications")
    print(expr)

    expr = move_negation(expr)
    print("\nStep 2: Move negation inward (NNF)")
    print(expr)

    expr = standardize_variables(expr)
    print("\nStep 3: Standardize variables")
    print(expr)

    expr = skolemize(expr)
    print("\nStep 4: Skolemization")
    print(expr)

    expr = distribute(expr)
    print("\nStep 5: Distribute OR over AND (CNF form)")
    print(expr)

    print("\nFinal CNF:")
    return expr

 
statement = "∀x (P(x) → ∃y Q(x, y))"
cnf_output = to_cnf(statement)
print(cnf_output)
