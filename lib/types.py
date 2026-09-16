# instruction: {label, variable, statementType, targetLabel}
# statementType is one of dummy | increment | decrement | Goto
# variable is one of {kind: Y} | {kind: X, index} | {kind: Z, index}
def empty_instruction():
    return {
        "label": None,
        "variable": {"kind": "Y"},
        "statementType": "dummy",
        "targetLabel": None,
    }
