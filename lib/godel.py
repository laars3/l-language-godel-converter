from .primes import nth_prime


# builds 2^e1 * 3^e2 * ... - 1, skipping zero exponents (trailing zeros just vanish)
def encode_to_string(instruction_codes):
    terms = []

    for i, exp in enumerate(instruction_codes):
        if exp == 0:
            continue
        prime = nth_prime(i + 1)
        terms.append(f"{prime}^{exp}")

    if not terms:
        return "empty program, #(P) = 0"
    return " * ".join(terms) + " - 1"


# turns prime factors back into the exponent list, padding zeros for skipped primes
def factorization_to_exponents(factors):
    if not factors:
        return []

    max_prime = max((f["prime"] for f in factors), default=2)

    exponents = []
    i = 1

    while True:
        p = nth_prime(i)
        if p > max_prime:
            break
        found = next((f for f in factors if f["prime"] == p), None)
        exponents.append(found["exp"] if found else 0)
        i += 1

    return exponents
