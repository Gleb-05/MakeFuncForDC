import random


# raw data
#   function "z" : its "c" terms
raw_z_data = {
    "4": "5 6 7 8 9 10 11 12".split(),
    "3": "1 2 3 4 9 10 11 12".split(),
    "2": "0 3 4 7 8 11 12 15".split(),
    "1": "2 4 7 9 10 14".split(),
    }

def random_z(DC_c_cap):
    z = [i for i in range(DC_c_cap)]
    for c in range(DC_c_cap // 2):
        z.pop(random.randint(0,len(z)-1))
    return z

# Test the limits
for z in raw_z_data:
    raw_z_data[z] = random_z(120)

print("functions z and terms c that define them")
for z in raw_z_data:
    print(raw_z_data[z])
print()


def cleaned(table):
    return {key: val for key, val in table.items() if len(val) > 1}


# greedy info
#   term "c" : functions "z" it covers
def prepare(raw_z_data):
    data = {}
    for z in raw_z_data:
        for c in raw_z_data[z]:
            if c not in data:
                data[c] = [z]
            else:
                data[c].append(z)
    return data


data = cleaned(prepare(raw_z_data))
print("terms c and functions z where they are used\n", data, "\n")

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
        covered_z = data[c]
        for mask in make_mask(len(covered_z)):
            mz = ' '.join(use_mask(covered_z, mask))
            if mz not in table:
                table[mz] = [c]
                continue
            table[mz].append(c)
    return cleaned(table)


# L-ogical E-lement n-umber - count of LE needed to cover n terms
def LEn(terms_n):
    return 1 + (terms_n - 2) // 2

# greedy property
#   density - how many terms are covered across functions at expense of how many LE
def density(z_intersectn, bundle):
    return len(z_intersectn.split()) * len(bundle) / LEn(len(bundle))

# greedy selection
def make_density_table(table):
    return {key: density(key, val) for key, val in table.items()}


z_bundles = {"4": [], "3": [], "2": [], "1": []}

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
        covered_z = data[c]
        residue_z = [z for z in covered_z if z not in uz]
        if len(residue_z) < 2:
            del data[c]
        else:
            data[c] = residue_z
    data = cleaned(data)

bundled_count = 0
bundled_LEn = 0

debug = False
# greedy loop
while True:
    if len(data) < 2:
        print("---one or no z remains, nothing to pair with, exit\n")
        break
    table = make_z_intersection_table(data)
    if len(table) < 1:
        print("---c no longer repeat across z, no possible pairs, exit\n")
        break
    ro_table = make_density_table(table)
    used_z = random_max_z_from(ro_table)
    bundle = table[used_z]
    
    bundled_count += 1
    bundled_LEn += LEn(len(bundle))
    for z in used_z.split():
        z_bundles[z].append(bundle)
    
    update_data(data, used_z, bundle)
    if (debug):
        print("z_intersection_table: \n", table)
        print("density_table: \n", ro_table)
        print("===\nbundle", bundle, "for", used_z, "\n===")
        print("updated data:\n", data)
        print("===Bundles", bundled_count)
        print("===UsedLE", bundled_LEn)
        print()


for z in z_bundles:
    print("> function", z, "used bundles:", z_bundles[z])
print("With", bundled_count, "bundles and", bundled_LEn, "logical elements used\n")

for z in z_bundles:
    common_c = [c for bundle in z_bundles[z] for c in bundle]
    uncommon_c = [c for c in raw_z_data[z] if c not in common_c]
    print ("> function", z, "uncommon terms, outside the bundles:\n", uncommon_c)
print()

def plainLEn(raw_z_data):
    total = 0
    for z in raw_z_data:
        terms = raw_z_data[z]
        total += LEn(len(terms))
    return total

def totalLEn(raw_z_data, z_bundles, bundled_LEn):
    total = bundled_LEn
    for z in raw_z_data:
        terms = raw_z_data[z]
        for bundle in z_bundles[z]:
            terms = [c for c in terms if c not in bundle]
        total += LEn(len(terms) + len(z_bundles[z]))
    return total

print("Total LE solution cost:", totalLEn(raw_z_data, z_bundles, bundled_LEn),
      "\nOriginal cost:", plainLEn(raw_z_data), "\n")
