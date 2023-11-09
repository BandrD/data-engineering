filename = 'W2'
with open(filename) as file:
    lines = file.readlines()

sum_lines = list()

for line in lines:
    # print (line.strip())
    nums = line.split(';')
    # print(nums)
    sum_line = 0
    for num in nums:
        sum_line += int(num)

    sum_lines.append(sum_line)

with open('RHW2', 'w') as result:
    for value in sum_lines:
        result.write(str(value)+ '\n')
