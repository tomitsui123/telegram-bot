def contains_meal_info(s):
    substrings = ["是日", "是靚"]
    return any(substring in s for substring in substrings)

