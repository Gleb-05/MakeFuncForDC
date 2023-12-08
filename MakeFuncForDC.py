#===something to form (z) and (bundle)

data = {
    2: "3 1",
    3: "3 2",
    4: "3 2 1",
    7: "4 2 1",
    8: "4 2",
    9: "4 3 1",
    10: "4 3 1",
    11: "4 3 2",
    12: "4 3 2"
}

def make_mask(n):
    mask = []
    for i in range(2**n):
        bin_i = bin(i)[2:]
        if bin_i.count('1') < 2:
            continue
        bin_i = bin_i.zfill(n)
        mask.append(bin_i)
    return mask

def use_mask(word, mask):
    return [word[i] for i in range(len(word)) if mask[i]=='1']
    

table = {}

for c in data:
    if data[c] in table:
        table[data[c]].append(c)
        continue
    z = data[c].split()
    for mask in make_mask(len(z)):
        mz = ' '.join(use_mask(z, mask))
        if mz in table:
            table[mz].append(c)
            continue
        table[mz] = [c]

print(table)