filename = 'W1'
with open(filename) as file:
    lines = file.readlines()

word_stat = dict()

# print (word_stat)
for line in lines:
    # print(line.strip())

    row = (line.strip()
           .replace("!", " ")
           .replace("?", " ")
           .replace(".", " ")
           .replace(",", " ")
           .strip())
    # print(row)
    words = row.split(" ")
    # print(words)
    for word in words:
            if word in word_stat:
                word_stat[word] += 1
            else:
                word_stat [word] = 1

# print(word_stat)
#
word_stat = (dict(sorted(word_stat.items(), reverse=True, key=lambda item: item[1])))

# print (word_stat)

with open('RHW1', 'w') as result:
    for key, value in word_stat.items():
        result.write (key + ':' + str (value) + '\n')
