from .primes import factorize_number
from .godel import factorization_to_exponents
from .pairing_func import reverse_pairing_function
from .labels import ordinal_to_label
from .variables import c_to_variable


# unpairs twice to recover a, then b and c, then rebuilds the instruction from those
def decode_instruction_code(code, index):
    ab = reverse_pairing_function(code)
    a, pair_bc = ab["x"], ab["y"]
    bc = reverse_pairing_function(pair_bc)
    b, c = bc["x"], bc["y"]

    label = ordinal_to_label(a) if a != 0 else None
    variable = c_to_variable(c)

    if b == 0:
        instruction = {"label": label, "variable": variable, "statementType": "dummy", "targetLabel": None}
    elif b == 1:
        instruction = {"label": label, "variable": variable, "statementType": "increment", "targetLabel": None}
    elif b == 2:
        instruction = {"label": label, "variable": variable, "statementType": "decrement", "targetLabel": None}
    else:
        target_label = ordinal_to_label(b - 2)
        instruction = {"label": label, "variable": variable, "statementType": "Goto", "targetLabel": target_label}

    return {
        "instructionIndex": index,
        "code": code,
        "a": a,
        "b": b,
        "c": c,
        "pairBC": pair_bc,
        "instruction": instruction,
    }


# q+1 factored into primes gives the instruction codes back, one exponent per prime slot
def decode_q(q):
    n = q + 1
    factorization = factorize_number(n)
    instruction_codes = factorization_to_exponents(factorization)
    steps = [decode_instruction_code(code, index + 1) for index, code in enumerate(instruction_codes)]

    return {
        "q": q,
        "n": n,
        "factorization": factorization,
        "instructionCodes": instruction_codes,
        "steps": steps,
        "instructions": [s["instruction"] for s in steps],
    }
