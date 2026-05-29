n = int(input("Enter series length: "))

assert(n >= 1)

past_item, current_item = 1, 0

for i in range(n):
    print(current_item)
    past_item, current_item = current_item, past_item + current_item
