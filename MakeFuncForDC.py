#===something to form (z) and (bundle)

import random

# greedy data
data = {
    "2": "3 1",
    "3": "3 2",
    "4": "3 2 1",
    "7": "4 2 1",
    "8": "4 2",
    "9": "4 3 1",
    "10": "4 3 1",
    "11": "4 3 2",
    "12": "4 3 2",
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
    
def make_z_intersection_table(data):
    table = {}
    for c in data:
        z = data[c].split()
        for mask in make_mask(len(z)):
            mz = ' '.join(use_mask(z, mask))
            if mz not in table:
                table[mz] = [c]
                continue
            table[mz].append(c)
    return table

def cleaned(table):
    return {key: val for key, val in table.items() if len(val) > 1}


def LEn(terms_n):
    return 1 + (terms_n - 2) // 2

# greedy property
def density(z_intersectn, bundle):
    return len(z_intersectn.split()) * len(bundle) / LEn(len(bundle))

# greedy selection
def make_density_table(table):
    return {key: density(key, val) for key, val in table.items()}


answer = {"4": [], "3": [], "2": [], "1": []}

# greedy pick
def random_max_z_from(ro_table):
    high_density_z = []
    max_density = 0
    for z in ro_table:
        ro = ro_table[z]
        if ro > max_density:
            max_density = ro
            high_density_z = [z]
        elif ro == max_density:
            high_density_z.append(z)
    return high_density_z[random.randint(0, len(high_density_z) - 1)]

def update_data(data, used_z, bundle):
    uz = used_z.split()
    for c in bundle:
        cz = data[c].split()
        residue_z = [z for z in cz if z not in uz]
        if len(residue_z) < 2:
            del data[c]
        else:
            data[c] = " ".join(residue_z)
    
optimisedLEn = 0

# greedy loop
while True:
    if len(data) < 2:
        break
    table = make_z_intersection_table(data)
    table = cleaned(table)
    if len(table) < 1:
        break
    ro_table = make_density_table(table)
    used_z = random_max_z_from(ro_table)
    bundle = table[used_z]
    
    optimisedLEn += 1
    for z in used_z.split():
        answer[z].append(" ".join(bundle))
    
    update_data(data, used_z, bundle)


for func in answer:
    print("  function", func, "used bundles:", answer[func])

print("All at a cost of", optimisedLEn, "logical elements")    
    