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
    12: "4 3 2",
    # 10: "1",
    # 11: "2",
    # 12: "2",
    # mask is smart enough to ignore residue elements
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
    z = data[c].split()
    for mask in make_mask(len(z)):
        mz = ' '.join(use_mask(z, mask))
        if mz not in table:
            table[mz] = [c]
            continue
        table[mz].append(c)

print(table)


def cleaned(table):
    return {key: val for key, val in table.items() if len(val) > 1}

table = cleaned(table)
print(table)


def LEn(terms_n):
    return 1 + (terms_n - 2) // 2

ro_table = {}

for z_intersectn in table:
    ro_table[z_intersectn] = len(z_intersectn.split()) * len(table[z_intersectn]) / LEn(len(table[z_intersectn]))
    
print(ro_table)


answer = {1: [],2: [], 3: [], 4: []}

