# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 21:20:32 2023

@author: 91892
"""
import numpy as np
import random

original_text = "chaos system"
r = 3.99
xe1 = random.random()
xe2 = random.random()
print(xe1)
print(xe2)
ciphertext3 = []
ciphertext2 = []
map2 = []
for i in range(len(original_text)):
    xe1 = r*xe1*(1-xe1)
    str1 = format(int(xe1*(2**32)), '032b')
    a = np.bitwise_xor(ord(original_text[i]), int(100*xe1))
    ciphertext3.append(chr(a))
    xe2 = r*xe2*(1-xe2)
    b = np.bitwise_xor(a, int(100*xe2))
    ciphertext2.append(chr(b))

ciphertext3 = ''.join(ciphertext3)
ciphertext2 = ''.join(ciphertext2)

print(ciphertext2)
print(ciphertext3)