# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 18:58:21 2023

@author: 91892
"""

import numpy as np

def lorenz(x, y, z, s, r, b):
    """
    Implementation of the Lorenz system, which is a chaotic system.
    """
    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z
    return x_dot, y_dot, z_dot

def generate_key(key_length):
    """
    Generates a pseudo-random key of the specified length using the Lorenz system with random parameter values.
    """
    x, y, z = 0, 1, 1.05  # initial values for the Lorenz system
    s, r, b = np.random.uniform(0, 50), np.random.uniform(10, 50), np.random.uniform(0, 10/3) # random values for s, r, and b
    key = np.zeros(key_length)
    for i in range(key_length):
        x_dot, y_dot, z_dot = lorenz(x, y, z, s, r, b)
        x, y, z = x + x_dot * 0.01, y + y_dot * 0.01, z + z_dot * 0.01
        key[i] = abs(int(255 * (x - np.floor(x))))  # converts chaotic values to integers between 0 and 255
    return key.astype(int)



def encrypt_message(plaintext, key):
    """
    Encrypts the plaintext message using the generated key.
    """
    encrypted = ""
    for i in range(len(plaintext)):
        encrypted += chr(ord(plaintext[i]) ^ key[i % len(key)])
    return encrypted

def decrypt_message(encryptedtext, key):
    """
    Encrypts the encryptedtext message using the generated key.
    """
    encrypted = ""
    for i in range(len(encryptedtext)):
        encrypted += chr(ord(encryptedtext[i]) ^ key[i % len(key)])
    return encrypted

# example usage
plaintext = "Hello"
key_length = len(plaintext)
key = generate_key(key_length)
encrypted = encrypt_message(plaintext, key)

print(f"Plaintext: {plaintext}")
print(f"Key: {key}")
print(f"Encrypted message: {encrypted}")
