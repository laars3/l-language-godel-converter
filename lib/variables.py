# Y=1, X_i=2i (even), Z_i=2i+1 (odd), so kind+index maps to one ordinal
def variable_to_ordinal(variable):
    if variable["kind"] == "Y":
        return 1

    if variable["kind"] == "X":
        return 2 * variable["index"]

    if variable["kind"] == "Z":
        return 2 * variable["index"] + 1

    return 1


# reverse of variable_to_ordinal: even -> X, odd -> Z, 1 -> Y
def ordinal_to_variable(k):
    if k == 1:
        return {"kind": "Y"}

    if k % 2 == 0:
        return {"kind": "X", "index": k // 2}

    return {"kind": "Z", "index": (k - 1) // 2}


def variable_to_c(variable):
    return variable_to_ordinal(variable) - 1


def c_to_variable(c):
    return ordinal_to_variable(c + 1)


def variable_to_string(variable):
    if variable["kind"] == "Y":
        return "Y"
    if variable["kind"] == "X":
        return f"X{variable['index']}"
    return f"Z{variable['index']}"
