#!/usr/bin/env python3
import os

secret_key = os.urandom(32).hex()
jwt_secret_key = os.urandom(32).hex()

print(secret_key)
print(jwt_secret_key)