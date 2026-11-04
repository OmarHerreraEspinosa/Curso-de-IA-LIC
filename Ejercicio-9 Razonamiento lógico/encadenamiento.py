from pathlib import Path
import sys

import yaml


def atom(text):
    name, arguments = text[:-1].split("(")
    return (name, *arguments.split(", "))


def show(atom):
    return f"{atom[0]}({', '.join(atom[1:])})"


def is_variable(term):
    return term[0].islower()


def substitute(atom, bindings):
    result = []
    for term in atom:
        while is_variable(term) and term in bindings:
            term = bindings[term]
        result.append(term)
    return tuple(result)


def unify(left, right, bindings=None):
    if left[0] != right[0] or len(left) != len(right):
        return None

    bindings = dict(bindings or {})
    for a, b in zip(left[1:], right[1:]):
        a = substitute((a,), bindings)[0]
        b = substitute((b,), bindings)[0]
        if a == b:
            continue
        if is_variable(a):
            bindings[a] = b
        elif is_variable(b):
            bindings[b] = a
        else:
            return None
    return bindings


def fresh(rule, number):
    names = {}

    def rename(atom):
        return tuple(
            names.setdefault(term, f"{term}_{number}") if is_variable(term) else term
            for term in atom
        )

    return [rename(p) for p in rule["if"]], rename(rule["then"])


def match(premises, facts, bindings):
    if not premises:
        yield bindings
        return
    for fact in facts:
        result = unify(substitute(premises[0], bindings), fact, bindings)
        if result is not None:
            yield from match(premises[1:], facts, result)


def forward(facts, rules, query):
    known, inferred, number = list(facts), [], 0
    print("\nHacia adelante:")

    while True:
        current_facts, new = list(known), []
        print("Ronda:")
        for rule in rules:
            number += 1
            premises, head = fresh(rule, number)
            for bindings in match(premises, current_facts, {}):
                result = substitute(head, bindings)
                if result not in known and result not in new:
                    new.append(result)
                    inferred.append(result)
                    print(f"  {rule['id']} -> {show(result)}")
        if not new:
            break
        known.extend(new)

    proved = any(unify(query, fact) is not None for fact in known)
    print("Átomos nuevos:", ", ".join(map(show, inferred)) or "(ninguno)")
    print("Probada:", "Sí" if proved else "No")


def backward(facts, rules, query):
    number = 0

    def prove(goal, stack):
        nonlocal number
        goal = substitute(goal, {})
        name = show(goal)
        indent = "  " * len(stack)
        if name in stack:
            print(f"{indent}Ciclo: {name}")
            return False
        print(f"{indent}Meta: {name}")

        for fact in facts:
            if unify(goal, fact) is not None:
                print(f"{indent}Hecho: {show(fact)}")
                return True

        for rule in rules:
            number += 1
            premises, head = fresh(rule, number)
            bindings = unify(goal, head)
            if bindings is None:
                continue
            print(f"{indent}Regla: {rule['id']}")
            if all(prove(substitute(p, bindings), stack + (name,)) for p in premises):
                return True

        print(f"{indent}Falla: {name}")
        return False

    print("\nHacia atrás:")
    print("Probada:", "Sí" if prove(query, ()) else "No")


def run_query(facts, rules, query):
    print(f"\nConsulta: {show(query)}")
    forward(facts, rules, query)
    backward(facts, rules, query)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    with Path(__file__).with_name("biblioteca.yaml").open(encoding="utf-8") as file:
        data = yaml.safe_load(file)

    facts = tuple(atom(text) for text in data["facts"])
    rules = [
        {
            "id": rule["id"],
            "if": [atom(text) for text in rule["if"]],
            "then": atom(rule["then"]),
        }
        for rule in data["rules"]
    ]

    for text in data["queries"]:
        run_query(facts, rules, atom(text))

    print("\nCaso adicional: se agrega TieneCredencial(Luis)")
    facts = facts + (atom("TieneCredencial(Luis)"),)
    run_query(facts, rules, atom("AccesoNoche(Luis)"))


if __name__ == "__main__":
    main()