from itertools import combinations_with_replacement, product
import math

# https://stackoverflow.com/questions/12836385/how-can-i-interleave-or-create-unique-permutations-of-two-strings-without-recur/12837695#12837695
def unique_permutations(seq):
    i_indices = list(range(len(seq) - 1, -1, -1))
    k_indices = i_indices[1:]

    seq = sorted(seq)
    ans = []
    
    while True:
        ans.append(seq[:])

        for k in k_indices:
            if seq[k] < seq[k + 1]:
                break
        else:
            return ans

        k_val = seq[k]

        for i in i_indices:
            if k_val < seq[i]:
                break

        (seq[k], seq[i]) = (seq[i], seq[k])
        seq[k + 1:] = seq[-1:k:-1]

k = 3
signatures_debug = False


def signatures_for(permutation, m):
    if signatures_debug:
        print("selected permutation of k configuration")
        print(permutation)

    init_k = permutation[0]
    signatures = [[init_k]]
    term_counts = [m - init_k]

    for ki in range(1,len(permutation)):
        k = permutation[ki]
    
        at = 1
        i_at = (len(signatures) + 1) // 2
    
        for i in range(len(signatures)):
            signature = signatures[i]
            termCount = term_counts[i]
        
            if ki == len(permutation) - 1:
                signatures[i] = signature + ["j", k]
                continue
        
            # 'jump' is 1 ('stay' is 0)
            if (i == i_at):
                i_at += (i_at + 1) // 2
                at += 1   
            term_counts[i] = termCount + at - k

            signatures[i] = signature + ["j", k]
             
            # 'jump' is 0
            # ignore cover if k implies terms out of bounds
            if (termCount - k >= 0):
                signatures.append(signature + [k])
                term_counts.append(termCount - k)

    if signatures_debug:
        print("all possible signatures for selected permutation of one configuration")
        for signature in signatures:
            print(signature)
        print()    
        
    return signatures


def get_cover_by(signature, values):
    groups = []
    weights = [int(x) for x in values]
    at = 0
    
    for ki in range(len(signature)):
        k = signature[ki]
        
        if ki == len(signature) - 1:
            if len(values) != k:
                print("UNEXPECTED number of terms in", values)
                return
            if signatures_debug:
                values = tuple(rearrange_based_on_weights(values, weights))
                print(values)
            return tuple(groups)
        if k == 'j':
            at = 0
        else:
            weight_subpart = weights[at:at+k]
            value_subpart = values[at:at+k]
            ordered_values = tuple(rearrange_based_on_weights(value_subpart, weight_subpart))
            
            values = values[:at] + [ordered_values] + values[at+k:]
            weights = weights[:at] + [min(weight_subpart)] + weights[at+k:]
            groups.append(ordered_values)
            at += 1


def rearrange_based_on_weights(values, weights):
    # https://stackoverflow.com/questions/6618515/sorting-list-according-to-corresponding-values-from-a-parallel-list
    return [v for _,v in sorted(zip(weights,values))]
#TEST
# for signature in signatures_for([3,3,3,2], 8):
#     print(signature)
#     print(get_cover_by(signature, [6,5,4,3,2,1,7,8]))
#     print()
    

def define_cover_signatures(m):
    def LEn_k(terms_n, k):
        return 1 + (terms_n - 2) // (k - 1)

    LEk_configs = {}

    # https://stackoverflow.com/questions/26812803/find-all-possible-combinations-partitions-of-2-numbers-for-a-given-number
    # possible number of LE ranges from best(k'=k) to worst(k'=2), LE are used up to cover function
    for leN in range(LEn_k(m,k), LEn_k(m,2)+1):
        LEk_configs[leN] = [list(x) for x in combinations_with_replacement(range(1,k), leN) if sum(x) == m-1]

    print(f"For k={k} and m={m}, see number of used up LEs, and corresponding configurations showing 'input_N - 1' for them")
    for leN_group in LEk_configs:
        print(leN_group, ":", LEk_configs[leN_group])
    print()

    cover_signatures = []

    for leN_group in LEk_configs:
        for k_config in LEk_configs[leN_group]:
            k_config_permutations = unique_permutations(k_config)
            
            if signatures_debug:
                print(f"permutations for configuration with {leN_group} LEs:")
                for config in k_config_permutations:
                    print(config)
                print()
         
            for one_config_permutation in k_config_permutations:
                permutation = [x+1 for x in one_config_permutation]
                cover_signatures.extend(signatures_for(permutation, m))
                # Possible? Check for duplicate signatures (very few, hardly worth the while)
                # Like 2 3 3 j 3, 3 2 3 j 3, 3 3 2 j 3.
                # While 3 j 3 2 j 3 and 3 j 2 3 j 3 are different
    
    return cover_signatures

# for cover in define_cover_signatures(8):
#     print(cover)
    

def define_func_covers(raw_z_func):
    print(f"Definition for ALL covers for {raw_z_func} function STARTED")
    m = len(raw_z_func)
    cover_signatures = define_cover_signatures(m)

    func_covers = set()

    active_counter = 0
    # for all unique permutations, construct covers by signatures
    for constituent_permutation in unique_permutations(raw_z_func):
        active_counter += 1
        if active_counter%100 == 0:
            print("grain done", active_counter)
        if active_counter%1000 == 0:
            print("Done", active_counter)
            
        for signature in cover_signatures:
            cover = get_cover_by(signature, constituent_permutation)
            # if isinstance(cover, list)
            func_covers.add(cover)
        break
    
    print("Done", active_counter, "with", math.factorial(m), "expected")
    print()
    return func_covers
    

raw_z_data = {
    "4": "5 6 7 8 9 10 11 12".split(),
    "3": "1 2 3 4 9 10 11 12".split(),
    "2": "0 3 4 7 8 11 12 15".split(),
    "1": "2 4 7 9 10 14".split(),
    }


z_covers = []
total_combinations = 1

for z in raw_z_data:
    z_cover = define_func_covers(raw_z_data[z])
    cover_count = math.log10(len(z_cover))
    print(f"LogCount of z{z} cover:", cover_count, "\n")
    total_combinations += cover_count
    z_covers.append(z_cover)
print()
    

min_cost = 1000
min_configuration = tuple()
z_count = len(raw_z_data)

active_count = 0
for func_configuration in product(*z_covers):
    active_count += 1
    group_config = set(group for func in func_configuration for group in func)
    # print(func_configuration)
    # print(group_config)
    if active_count%1000000 == 0:
        print("Done", "{:.2f}".format(math.log10(active_count)), "out of", "{:.2f}".format(total_combinations))
    LE_cost = z_count + len(group_config)
    if LE_cost < min_cost:
        min_cost = LE_cost
        min_configuration = func_configuration
        print("Current best cost:", LE_cost)
        

print("min LE cost:", min_cost)
print("Used groups:")
for group in min_configuration:
    print(group)