import re

monkeys = {}
curr_monkey_num = 0

monkey_prod = 1

with open("day11.txt") as file:
    for line in file.readlines():
        curr = line.strip()

        if curr.startswith("Monkey"):
            match = re.search("Monkey (\d*)", curr)
            monkey_num = match.group(1)

            curr_monkey_num = monkey_num
            monkeys[curr_monkey_num] = {}
            monkeys[curr_monkey_num]["inspects"] = 0

        elif curr.startswith("Starting"):
            match = re.search("Starting items: (.*)", curr)
            monkey_items = match.group(1)
            monkey_items = monkey_items.split(", ")
            monkey_items = [int(item) for item in monkey_items]

            monkeys[curr_monkey_num]["items"] = monkey_items

        elif curr.startswith("Operation"):
            match = re.search("Operation: new = old (.) (\d*|old)", curr)
            monkey_op = match.group(1)
            monkey_op_num = match.group(2)

            if monkey_op_num:
                monkey_op_num = int(monkey_op_num)

            monkeys[curr_monkey_num]["op"] = monkey_op
            monkeys[curr_monkey_num]["op_num"] = "old" if not monkey_op_num else monkey_op_num

        elif curr.startswith("Test"):
            match = re.search("Test: divisible by (\d*)", curr)
            monkey_test_num = int(match.group(1))

            monkeys[curr_monkey_num]["test_num"] = monkey_test_num
            monkey_prod *= monkey_test_num

        elif curr.startswith("If true"):
            match = re.search("If true: throw to monkey (\d*)", curr)
            monkey_throw_true = match.group(1)

            monkeys[curr_monkey_num]["throw_true"] = monkey_throw_true

        elif curr.startswith("If false"):
            match = re.search("If false: throw to monkey (\d*)", curr)
            monkey_throw_false = match.group(1)

            monkeys[curr_monkey_num]["throw_false"] = monkey_throw_false

# print(monkeys)


for i in range(10000):
    for monkey in monkeys:
        curr = monkeys[monkey]
        # print(curr)

        to_del = []

        for j, _ in enumerate(curr["items"]):
            curr["inspects"] += 1
            if curr["op"] == "+":
                if curr["op_num"] == "old":
                    curr["items"][j] = (curr["items"][j] + curr["items"][j]) % monkey_prod
                else:
                    curr["items"][j] = (curr["items"][j] + curr["op_num"]) % monkey_prod
            else:
                # mult
                if curr["op_num"] == "old":
                    curr["items"][j] = (curr["items"][j] * curr["items"][j]) % monkey_prod
                else:
                    curr["items"][j] = (curr["items"][j] * curr["op_num"]) % monkey_prod
                

            # curr["items"][j] = curr["items"][j] // 3

            to_del.append(j)
            throw_to = curr["throw_true"] if curr["items"][j] % curr["test_num"] == 0 else curr["throw_false"]
            # print(throw_to)
            arr = monkeys[throw_to]["items"]
            arr.append(curr["items"][j])
            monkeys[throw_to]["items"] = arr

        # print(to_del)
        diff = 0
        for index in to_del:
            del curr["items"][index - diff]
            diff += 1

        # print(monkeys[monkey]["items"])

final = []

for monkey in monkeys:
    final.append(monkeys[monkey]["inspects"])

first = max(final)
index1 = final.index(first)
final.pop(index1)

second = max(final)

print(f"PART 2: {first * second}")