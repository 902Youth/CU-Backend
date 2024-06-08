# function for checking the strength 
import string
import os



def get_password_strength(password):
    upper_case = sum([1 if c in string.ascii_uppercase else 0 for c in password])
    lower_case = sum([1 if c in string.ascii_lowercase else 0 for c in password])
    special = sum([1 if c in string.punctuation else 0 for c in password])
    digits = sum([1 if c in string.digits else 0 for c in password])

    current_directory = os.path.dirname(__file__)
    common_file_path = os.path.join(current_directory, 'common.txt')
    try:
        with open(common_file_path, 'r') as f:
            common = f.read().splitlines()
    except FileNotFoundError as e:
        return upper_case, lower_case, special, digits, False


    if password in common:
        return upper_case, lower_case, special, digits, True

    

    return upper_case, lower_case, special, digits, False
    
# test method call
# print(get_password_strength(''))
