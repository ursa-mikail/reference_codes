""" permit_issuance_conditioned_by_counter.py
Generate a json permit with a counter, signed at the base, i.e. authorized signature.
This is issued by a server termed as CA, let this be a function for now.
this is issued to A and A presents to CA, and it makes a random delay (and accepts and deducts the counter, and display the json, and show count left), when it reaches zero, it rejects.

A then applies for another permit and the cycles continues. 
CA will also have an internal counter, as it reaches MAX accumulated, it halts and the program comes to an end. 

Class CA:
1. Initializes with an internal counter and a maximum accumulated permits value.
2. sign_permit method simulates signing a permit using a hash.
3. issue_permit method issues a new permit if the internal counter hasn't reached the maximum accumulated permits.
4. validate_and_use_permit method simulates validating and using the permit, reducing the counter, and adding a random delay.

apply_for_permit:
1. Function to simulate entity A applying for a permit.
2. Continuously validates and uses the permit until the counter reaches zero.
3. Re-applies for a new permit if the internal counter hasn't reached the maximum accumulated value.

This script models the permit issuance and management as described, ensuring the counters and reapplications are handled correctly.

"""
import json
import random
import time
import hashlib
import sys

class CA:
    def __init__(self, max_accumulated):
        self.internal_counter = 0
        self.max_accumulated = max_accumulated

    def sign_permit(self, permit):
        # Simulate a digital signature with a hash for simplicity
        permit_str = json.dumps(permit, sort_keys=True)
        permit_hash = hashlib.sha256(permit_str.encode()).hexdigest()
        permit['signature'] = permit_hash
        return permit

    def issue_permit(self, recipient, counter):
        if self.internal_counter >= self.max_accumulated:
            print("CA has reached its maximum accumulated permits. Halting.")
            exit()
        else:
            print(f"CA has not reached its maximum accumulated permits of {self.max_accumulated}. Current counter: {self.internal_counter}")


        permit = {
            'recipient': recipient,
            'counter': counter
        }
        signed_permit = self.sign_permit(permit)
        #self.internal_counter += 1
        return signed_permit

    def validate_and_use_permit(self, permit):
        if permit['counter'] <= 0:
            print("Permit counter has reached zero. Rejected.")
            return False

        # Simulate random delay
        time.sleep(random.uniform(1, 3))

        permit['counter'] -= 1
        self.internal_counter += 1

        signed_permit = self.sign_permit(permit)  # Re-sign the permit after modifying it
        print(f"Permit accepted. Counter left: {signed_permit['counter']}")
        print("Updated permit:", json.dumps(signed_permit, indent=4))
        return signed_permit

# Initialize CA with a maximum accumulated value of 10
ca = CA(max_accumulated=10)

# Simulate entity A applying for a permit
def apply_for_permit(entity, initial_counter):
    permit = ca.issue_permit(entity, initial_counter)
    if not permit:
        return

    while permit['counter'] > 0:
        permit = ca.validate_and_use_permit(permit)
        if not permit:
            break

    if ca.internal_counter < ca.max_accumulated:
        print("Permit counter reached zero. Applying for a new permit.")
        apply_for_permit(entity, initial_counter)
    else:
        print("CA has halted further permit issuance.")
        exit()

# Entity A applies for permits with an initial counter of 5
apply_for_permit("A", 5)

"""
CA has not reached its maximum accumulated permits of 10. Current counter: 0
Permit accepted. Counter left: 4
Updated permit: {
    "recipient": "A",
    "counter": 4,
    "signature": "ca64f888012cadecbf1d234ee367fbbf73d2322f974ad48a16553b2addde505a"
}
Permit accepted. Counter left: 3
Updated permit: {
    "recipient": "A",
    "counter": 3,
    "signature": "dc7050dc8179e9dc68e952ae29cb087e327555ce97f7ffc94be038a9ae14d55b"
}
Permit accepted. Counter left: 2
Updated permit: {
    "recipient": "A",
    "counter": 2,
    "signature": "6f427c0563ae50710a8f4252b159bce2c945529265a7b9fb82a79750ed229ca9"
}
Permit accepted. Counter left: 1
Updated permit: {
    "recipient": "A",
    "counter": 1,
    "signature": "2c0b56f9c5b022f70823a3eafb748ea66cdaef1ce33b330ed0588688524b5327"
}
Permit accepted. Counter left: 0
Updated permit: {
    "recipient": "A",
    "counter": 0,
    "signature": "3018e4ec98c40a2517f7e2350aafcddb6cc7d82f3cf30bbb0ef7bbc2a2d9b45a"
}
Permit counter reached zero. Applying for a new permit.
CA has not reached its maximum accumulated permits of 10. Current counter: 5
Permit accepted. Counter left: 4
Updated permit: {
    "recipient": "A",
    "counter": 4,
    "signature": "ca64f888012cadecbf1d234ee367fbbf73d2322f974ad48a16553b2addde505a"
}
Permit accepted. Counter left: 3
Updated permit: {
    "recipient": "A",
    "counter": 3,
    "signature": "dc7050dc8179e9dc68e952ae29cb087e327555ce97f7ffc94be038a9ae14d55b"
}
Permit accepted. Counter left: 2
Updated permit: {
    "recipient": "A",
    "counter": 2,
    "signature": "6f427c0563ae50710a8f4252b159bce2c945529265a7b9fb82a79750ed229ca9"
}
Permit accepted. Counter left: 1
Updated permit: {
    "recipient": "A",
    "counter": 1,
    "signature": "2c0b56f9c5b022f70823a3eafb748ea66cdaef1ce33b330ed0588688524b5327"
}
Permit accepted. Counter left: 0
Updated permit: {
    "recipient": "A",
    "counter": 0,
    "signature": "3018e4ec98c40a2517f7e2350aafcddb6cc7d82f3cf30bbb0ef7bbc2a2d9b45a"
}
CA has halted further permit issuance.
"""