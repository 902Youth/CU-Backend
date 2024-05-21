# function for checking the strength 
import string


def get_password_strength(password):
    upper_case = sum([1 if c in string.ascii_uppercase else 0 for c in password])
    lower_case = sum([1 if c in string.ascii_lowercase else 0 for c in password])
    special = sum([1 if c in string.punctuation else 0 for c in password])
    digits = sum([1 if c in string.digits else 0 for c in password])

    with open('common.txt', 'r') as f:
        common = f.read().splitlines()

    if password in common:
        return "Password was found in a common list. Please use a different password."
    

    return upper_case, lower_case, special, digits
    
# test method call
print(get_password_strength(''))
