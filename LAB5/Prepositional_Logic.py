import itertools

# ----- Helper: evaluate propositional logic sentence -----
def pl_true(expr, model):
    if isinstance(expr, str):
        return model[expr]

    op = expr[0]

    if op == 'not':
        return not pl_true(expr[1], model)
    elif op == 'and':
        return pl_true(expr[1], model) and pl_true(expr[2], model)
    elif op == 'or':
        return pl_true(expr[1], model) or pl_true(expr[2], model)
    elif op == 'implies':
        return (not pl_true(expr[1], model)) or pl_true(expr[2], model)
    else:
        raise ValueError("Unknown operator: " + op)


# ----- Truth table entailment algorithm -----
def tt_entails(KB, query, symbols):
    for values in itertools.product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))

        # If KB is true but query is false -> Not entailed
        if all(pl_true(sentence, model) for sentence in KB):
            if not pl_true(query, model):
                print("Counterexample model:", model)
                return False

    return True


# ----- Define your KB -----
# KB: Q → P,  P → ¬Q,  Q ∨ R
KB = [
    ('implies', 'Q', 'P'),              # Q → P
    ('implies', 'P', ('not', 'Q')),     # P → ¬Q
    ('or', 'Q', 'R')                    # Q ∨ R
]

symbols = ['P', 'Q', 'R']

# ----- Define queries -----
queries = {
    "R": 'R',
    "R → P": ('implies', 'R', 'P'),
    "Q → R": ('implies', 'Q', 'R')
}

# ----- Run entailment tests -----
for name, q in queries.items():
    result = tt_entails(KB, q, symbols)
    print(f"KB entails {name}: {result}")
