
def print_dict(d: dict):
    for k, v in d.items():
        print(k, v, sep=' = ')
        print('---------------------------')

def print_sets(sets: list):
    for s in sets:
        print_dict(s)

def print_list(sets: list):
    for s in sets:
        print(s)
        print('----------------------')