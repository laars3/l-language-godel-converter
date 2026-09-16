from .labels import label_to_ordinal
from .variables import variable_to_c
from .pairing_func import pairing_function
from .godel import encode_to_string


# a=label ordinal, b=statement type (0/1/2, or goto target+2), c=variable, then paired twice
def encode_instruction(instruction):
    a = label_to_ordinal(instruction["label"]) if instruction.get("label") else 0
    c = variable_to_c(instruction["variable"])

    statement_type = instruction["statementType"]
    if statement_type == "dummy":
        b = 0
    elif statement_type == "increment":
        b = 1
    elif statement_type == "decrement":
        b = 2
    else:
        b = label_to_ordinal(instruction["targetLabel"]) + 2

    inner_func = pairing_function(b, c)
    instruction_code = pairing_function(a, inner_func)

    return {"a": a, "b": b, "c": c, "innerFunc": inner_func, "instructionCode": instruction_code}


# encodes every instruction, then combines the codes into the final godel number string
def encode_program(instructions):
    steps = []
    for index, instruction in enumerate(instructions):
        step = {"instructionIndex": index + 1}
        step.update(encode_instruction(instruction))
        step["instruction"] = instruction
        steps.append(step)

    instruction_code = [s["instructionCode"] for s in steps]
    q_prime_power_string = encode_to_string(instruction_code)

    return {"steps": steps, "instructionCode": instruction_code, "qPrimePowerString": q_prime_power_string}
