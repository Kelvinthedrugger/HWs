# AUTOGENERATED! DO NOT EDIT! File to edit: 04_DNAA.ipynb (unless otherwise specified).

__all__ = ['people', 'data', 'frags', 'checkppl']

# Cell
people = {}

# Cell
with open('databases\small.csv', 'r', newline='') as f1:
    reader = csv.DictReader(f1)
    for row in reader:
        #print(row['name'])
        people[row['name']] = row

# Cell
data = ""
with open('sequences\\1.txt', 'r') as f1:
    data = f1.read()
f1.close()
#print(data, type(data))

# Cell
frags = [] # name of dna fragments
# get the first name to get the list of name of dna fragments
for pplname in people:
    break
# below would print: # for small.csv
# name <class 'str'>
# AGATC <class 'str'>
# AATG <class 'str'>
# TATC <class 'str'>
for ele in list(people[pplname]):
    #print(ele, type(ele))
    frags.append(ele)
frags.pop(0) # get rid of the 'name'
#print(frags)
#['AGATC', 'AATG', 'TATC']

# Cell
# Succeeded, stupid str() to int() conversion

def checkppl(people, pplname, dnas, data):
    for ele in dnas:
        # cache the key instead of convert it every time
        key = str(longest_match(data,ele))
        if people[pplname][ele] != key:
            return False
    return True

for pplname in people:
    if checkppl(people, pplname, frags, data):
        print(pplname)
        break # since there would be only one match as the problem suggested