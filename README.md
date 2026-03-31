
# August Cipher + Hash-Based Secure Messaging System

A custom cryptographic system that combines:
- Structural transformations
- Hash-based integrity verification
- Multi-pass Caesar (August) cipher

This project demonstrates how **confidentiality + integrity** can be achieved using layered techniques, while strictly adhering to a **fixed shift (+1) August cipher**.

---

## Features

- Reversible transformation pipeline
- SHA-256 based integrity verification
- Hash interleaving (instead of simple appending)
- Multi-pass August cipher (shift = +1 only)
- Block-based scrambling
- Key-driven variability (deterministic, not random)

---

## System Design

The system is divided into two parts:

### 1. Encryption (Forward Pipeline)
Transforms plaintext into ciphertext using multiple reversible steps.

### 2. Decryption (Reverse Pipeline)
Reverses transformations and verifies integrity using hash comparison.

---

## Algorithm

### Encryption

**Input:**
- Plaintext `P`
- Key `K`

---

### Step 1: Pre-Transformation
- Reverse the plaintext
- Swap characters at even and odd indices

Result → `P1`

---

### Step 2: Block Processing
- Compute block size:
```

b = (len(K) % 4) + 2

```
- Split `P1` into blocks of size `b`
- Reverse blocks at even indices

Result → `P2`

---

### Step 3: Hash Generation
- Compute SHA-256 hash:
```

H = SHA256(P2)

```

---

### Step 4: Hash Interleaving
- Compute interval:
```

r = (len(K) % 3) + 2

```
- Insert characters of `H` into `P2` after every `r` characters

Result → `P3`

---

### Step 5: Multi-Pass August Cipher
- Compute number of rounds:
```

n = (len(K) % 5) + 1

```
- Apply August cipher (shift = +1) `n` times

Final Output → `C` (Ciphertext)

---

## Decryption

**Input:**
- Ciphertext `C`
- Key `K`

---

### Step 1: Reverse Cipher
- Apply August cipher with shift = -1, `n` times

Result → `P3`

---

### Step 2: Extract Hash
- Remove interleaved characters using interval `r`
- Recover:
- `P2`
- Extracted hash `H'`

---

### Step 3: Verify Integrity
- Compute:
```

H_check = SHA256(P2)

```
- Validate:
- If `H_check` starts with `H'` → valid
- Else → tampered

---

### Step 4: Reverse Block Processing
- Split into blocks of size `b`
- Reverse even-indexed blocks

Result → `P1`

---

### Step 5: Reverse Pre-Transformation
- Swap even/odd indices
- Reverse string

Final Output → Original plaintext `P`

---

## Example

```

Input:
Plaintext = HELLO
Key = KEY

Output:
Encrypted Text = (varies based on transformations)
Decrypted Text = HELLO

````

---

## Important Notes

- The August cipher uses **strict shift = +1** (no variation allowed)
- Hashing is **one-way** and used only for integrity verification
- Only part of the hash is interleaved → verification uses prefix matching
- All transformation steps are fully reversible

---

## Design Rationale

- **Reversible transformations** ensure correct decryption
- **Hash interleaving** embeds integrity within data (harder to tamper)
- **Modulo operations** ensure controlled variability:
  - Prevents extreme values
  - Keeps system deterministic
- **Multi-pass cipher** increases obfuscation while maintaining simplicity

---

mo)**
```
