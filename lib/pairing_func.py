# <x, y> = 2^x * (2y + 1) - 1, a bijection from pairs of naturals to naturals
def pairing_function(x, y):
    return (2 ** x) * (2 * y + 1) - 1


# reverse: peel powers of 2 off n+1 to get x back, whatever's left gives y
def reverse_pairing_function(n):
    m = n + 1
    x = 0
    while m % 2 == 0:
        m //= 2
        x += 1
    y = (m - 1) // 2
    return {"x": x, "y": y}
