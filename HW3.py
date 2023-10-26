import math

filename = 'W3'
with open(filename) as file:
    lines = file.readlines()

matrix = list()

for line in lines:
    # print(line.strip())
    nums = line.strip().split(",")
    for i in range(len(nums)):
        if nums[i] == 'NA':
            nums[i] = str((int(nums[i-1])+int(nums[i+1])) / 2)


    filtered = list()
    for item in nums:
        num = float(item)
        if num > 0 and math.sqrt(num) > 77:
            filtered.append(num)

    matrix.append(filtered)

    # print(filtered)

with open('RHW3', 'w') as result:
    for row in matrix:
        for num in row:
            result.write(str(num) + ',')
        result.write("\n")
