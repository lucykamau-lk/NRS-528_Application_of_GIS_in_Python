list_a = ['dog', 'cat', 'rabbit', 'hamster', 'gerbil']
list_b = ['dog', 'hamster', 'snake']

common_items = set(list_a) & set(list_b)

print("common_items:", common_items)

non_overlapping_items = set(list_a) ^ set(list_b)

print("Non-overlapping items:", non_overlapping_items)
