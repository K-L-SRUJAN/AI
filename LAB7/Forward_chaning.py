 
facts = {

    "Man(Marcus)",

    "Pompeian(Marcus)"

}
 

rules = [

    ("Pompeian(x)", "Roman(x)"),  

    ("Roman(x)", "Loyal(x)"),     

    ("Man(x)", "Person(x)"),        

    ("Person(x)", "Mortal(x)")       

]
 

query = "Mortal(Marcus)"

 
def match(statement, fact):

    """

    Match a statement pattern like 'Pompeian(x)' to a fact like 'Pompeian(Marcus)'.

    Returns the substitution (x -> Marcus) if they match.

    """

    if "(" not in statement or "(" not in fact:

        return None

    pred1, arg1 = statement[:-1].split("(")

    pred2, arg2 = fact[:-1].split("(")

    if pred1.strip() != pred2.strip():

        return None

    if arg1.strip().islower():   

        return {arg1.strip(): arg2.strip()}

    elif arg1.strip() == arg2.strip():

        return {}

    else:

        return None

def substitute(statement, subs):

    """

    Replace variable (like x) with its value (like Marcus).

    """

    for var, val in subs.items():

        statement = statement.replace(var, val)

    return statement

 
def forward_chain(facts, rules, query):

    inferred = set()

    while True:

        new_facts = set(facts)

        for antecedent, consequent in rules:

            for fact in facts:

                subs = match(antecedent, fact)

                if subs is not None:

                    new_fact = substitute(consequent, subs)

                    if new_fact not in facts:

                        print(f"Inferred: {new_fact} (from {fact} using rule {antecedent} → {consequent})")

                        new_facts.add(new_fact)

    
        if new_facts == facts:

            break

        facts = new_facts

    return query in facts, facts



result, all_facts = forward_chain(facts, rules, query)

print("\n--- Final Facts ---")

for f in sorted(all_facts):

    print(f)

print("\n--- Result ---")

if result:

    print(f"✅ The query '{query}' is TRUE based on forward reasoning.")

else:

    print(f"❌ The query '{query}' cannot be proven from the given knowledge base.")


