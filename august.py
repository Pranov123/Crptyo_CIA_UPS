import hashlib

# ---------------- HASH ----------------
def generate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


# ---------------- PRE-TRANSFORMATION ----------------
def pre_transform(text):
    text = text[::-1]  # reverse

    text_list = list(text)
    for i in range(0, len(text_list) - 1, 2):
        text_list[i], text_list[i+1] = text_list[i+1], text_list[i]

    return ''.join(text_list)


def reverse_pre_transform(text):
    text_list = list(text)
    for i in range(0, len(text_list) - 1, 2):
        text_list[i], text_list[i+1] = text_list[i+1], text_list[i]

    return ''.join(text_list)[::-1]


# ---------------- BLOCK PROCESSING ----------------
def block_process(text, key):
    b = (len(key) % 4) + 2
    blocks = [text[i:i+b] for i in range(0, len(text), b)]

    result = ""
    for i, block in enumerate(blocks):
        if i % 2 == 0:
            result += block[::-1]
        else:
            result += block

    return result


def reverse_block_process(text, key):
    b = (len(key) % 4) + 2
    blocks = [text[i:i+b] for i in range(0, len(text), b)]

    result = ""
    for i, block in enumerate(blocks):
        if i % 2 == 0:
            result += block[::-1]
        else:
            result += block

    return result


# ---------------- HASH INTERLEAVING ----------------
def interleave_hash(text, hash_val, key):
    r = (len(key) % 3) + 2

    result = ""
    j = 0

    for i in range(len(text)):
        result += text[i]

        if (i + 1) % r == 0 and j < len(hash_val):
            result += hash_val[j]
            j += 1

    return result


def extract_hash(text, key):
    r = (len(key) % 3) + 2

    original = ""
    extracted_hash = ""

    i = 0
    while i < len(text):
        # take r original chars
        for _ in range(r):
            if i < len(text):
                original += text[i]
                i += 1

        # next char is hash
        if i < len(text):
            extracted_hash += text[i]
            i += 1

    return original, extracted_hash


# ---------------- AUGUST CIPHER ----------------
def august_encrypt(text, rounds):
    for _ in range(rounds):
        result = ""
        for ch in text:
            if ch.isalpha():
                base = ord('a') if ch.islower() else ord('A')
                result += chr((ord(ch) - base + 1) % 26 + base)
            else:
                result += ch
        text = result
    return text


def august_decrypt(text, rounds):
    for _ in range(rounds):
        result = ""
        for ch in text:
            if ch.isalpha():
                base = ord('a') if ch.islower() else ord('A')
                result += chr((ord(ch) - base - 1) % 26 + base)
            else:
                result += ch
        text = result
    return text


# ---------------- ENCRYPT ----------------
def encrypt_message(plaintext, key):
    p1 = pre_transform(plaintext)
    p2 = block_process(p1, key)

    H = generate_hash(p2)

    p3 = interleave_hash(p2, H, key)

    rounds = (len(key) % 5) + 1
    cipher = august_encrypt(p3, rounds)

    return cipher


# ---------------- DECRYPT ----------------
def decrypt_message(ciphertext, key):
    rounds = (len(key) % 5) + 1

    p3 = august_decrypt(ciphertext, rounds)

    p2, extracted_hash = extract_hash(p3, key)

    computed_hash = generate_hash(p2)

    if not computed_hash.startswith(extracted_hash):
        return " Message Tampered!"

    p1 = reverse_block_process(p2, key)
    original = reverse_pre_transform(p1)

    return f" Decrypted Message: {original}"


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    print("=== August Cipher + Hash System ===")

    while True:
        print("\n1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            key = input("Enter key: ").strip()
            plaintext = input("Enter plaintext: ").strip()

            if not key or not plaintext:
                print(" Key and plaintext cannot be empty!")
                continue

            encrypted = encrypt_message(plaintext, key)
            print("\n Encrypted Text:", encrypted)

        elif choice == "2":
            key = input("Enter key: ").strip()
            ciphertext = input("Enter ciphertext: ").strip()

            if not key or not ciphertext:
                print("Key and ciphertext cannot be empty!")
                continue

            result = decrypt_message(ciphertext, key)
            print("\n Result:", result)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")