_prime_cache = [2]


def _is_prime(x):
    for y in _prime_cache:
        if y * y > x:
            break
        if x % y == 0:
            return False
    return True


def nth_prime(n):
    while len(_prime_cache) < n:
        x = _prime_cache[-1] + 1
        while not _is_prime(x):
            x += 1
        _prime_cache.append(x)
    return _prime_cache[n - 1]


# trial-divides by primes up to sqrt(remaining), whatever's left over is itself prime
def factorize_number(n):
    factors = []
    remaining = n
    i = 1

    while True:
        x = nth_prime(i)
        if x * x > remaining:
            break

        exp = 0
        while remaining % x == 0:
            remaining //= x
            exp += 1

        if exp > 0:
            factors.append({"prime": x, "exp": exp})
        i += 1

    if remaining > 1:
        factors.append({"prime": remaining, "exp": 1})

    return factors
