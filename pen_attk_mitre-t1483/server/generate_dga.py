import random
import string

def generate_domain():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + ".com"

print("Generated DGA Domains:")
for _ in range(5):
    print(generate_domain())
