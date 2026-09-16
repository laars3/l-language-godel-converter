# L-Program Coder / Decoder

A web app that encodes and decodes programs written in the theoretical language 'L'.

Built for Professor Fechter's Theory of Computation course, implements the formal coding and decoding functions covered in class.

## Background

A Gödel number is a way to encode a piece of formal syntax, a formula, a proof, a program, as a single natural number, built so the encoding can always be reversed. Gödel introduced the technique for the incompleteness theorems: once a formal system can refer to its own formulas as numbers, it can make statements about its own provability.

The same idea underlies computability theory. Assigning every program a unique number makes "the set of all programs" a countable, enumerable set, which is exactly what diagonalization arguments need, including the proof that the halting problem is undecidable. 'L' is a small register-machine language used to make this concrete: a handful of instruction types (increment, decrement, conditional goto), each reducible to three integers `a`, `b`, `c`, which get folded together with a pairing function and then combined into one number via prime factorization.

## What It Does

**Encode:** takes an L-program (a list of instructions) and computes its Gödel number `#(P)`, shown in prime power form.

**Decode:** takes a number and recovers the original L-program, showing every intermediate step.

## How It Works

- each instruction is broken down into values `a`, `b`, `c`
- paired using the pairing function `<x, y> = 2^x * (2y + 1) - 1`
- the list of instruction codes is encoded as a Gödel number `2^e1 * 3^e2 * 5^e3 * ... - 1`
- decoding reverses all of these steps

## Example

```
[A1] X1 <- X1 + 1
     IF X1 != 0 GOTO A1
```

| instruction | a | b | c | `<b,c>` | `#(I)` |
|---|---|---|---|---|---|
| I1 | 1 | 1 | 1 | 5 | 21 |
| I2 | 0 | 3 | 1 | 23 | 46 |

`#(P) = 2^21 * 3^46 - 1`

## Notes

- large numbers can take a while to decode, especially if q+1 turns out to be prime
- a trailing no-op instruction (`Y <- Y`, no label) won't survive a round trip since its code is 0 and drops out of the prime factorization entirely, that's the encoding scheme working as intended, not a bug

## Built With

- Python, running client-side in the browser via [PyScript](https://pyscript.net) (Pyodide/WebAssembly)
- rewritten from an earlier TypeScript/React version, this time keeping the whole app, math included, in Python
- no external libraries, all math implemented from scratch using native arbitrary-precision `int`
- no build step, static HTML/CSS/Python served as-is

## Project Layout

- `lib/`, the math: primes, pairing function, Gödel encoding, labels, variables, encode/decode
- `main.py`, UI wiring and DOM handling via PyScript
- `index.html` / `style.css`, page shell

## Running Locally

```
python3 -m http.server
```

then open `http://localhost:8000`.

## Live

deployed on GitHub Pages

---

Built by: Lars Ponikvar  
For: Professor Ronald W. Fechter  
Inspired by: Ronald W. Fechter and Dr. Martin Davis
