
def closer_to_than(x, y, dest):
    for a in all_assigns:
        for b1 in all_assigns:
            if evaluate(x, b1) == evaluate(x, a):
                found = any((evaluate(y, a) == evaluate(y, b2)) and (evaluate(dest, b1) == evaluate(dest, b2)) for b2 in all_assigns)
                if not found:
                    return False
    return True
