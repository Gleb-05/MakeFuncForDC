from itertools import combinations_with_replacement
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

template_debug = False

def substitute_values(nested_list, values):
    index = 0

    def substitute_recursively(lst):
        nonlocal index
        result = []
        for item in lst:
            if isinstance(item, list):
                result.append(substitute_recursively(item))
            else:
                result.append(values[index])
                index += 1
        return result

    return substitute_recursively(nested_list)

def define_LE_positions_for_(one_config_permutation, z_func):
    permutation = [x+1 for x in one_config_permutation]
    if template_debug:
        print("selected permutation of k configuration")
        print(permutation)

    init_k = permutation[0]
    func_covers = [[z_func[:init_k]] + z_func[init_k:]]

    for ki in range(1,len(permutation)):
        k = permutation[ki]
    
        at = 1
        i_at = (len(func_covers) + 1) // 2
    
        for i in range(len(func_covers)):
            cover = func_covers[i]
        
            if ki == len(permutation) - 1:
                if len(cover) != k:
                    print("UNEXPECTED number of terms in", cover)
                break
        
            # 'stay' is 0
            func_covers[i] = [cover[:k]] + cover[k:]
            # 'stay' is 1
            if (i == i_at):
                i_at += (i_at + 1) // 2
                at += 1
            # ignore cover if k implies terms out of bounds
            if (at+k <= len(cover)):
                func_covers.append(cover[:at] + [cover[at:at+k]] + cover[at+k:])

    if template_debug:
        print("all possible LE positions for selected permutation of one configuration")
        for cover in func_covers:
            print(cover)
        print()
    return func_covers


k = 3


def define_template_covers(m):
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

    template_covers = []
    
    for leN_group in LEk_configs:
        for k_config in LEk_configs[leN_group]:
            k_config_permutations = unique_permutations(k_config)
            
            if template_debug:
                print(f"permutations for configuration with {leN_group} LEs:")
                for config in k_config_permutations:
                    print(config)
                print()
         
            for one_config_permutation in k_config_permutations:
                covers_for_permutation = define_LE_positions_for_(one_config_permutation, [c for c in range(m)])
                template_covers.extend(covers_for_permutation)
    
    return template_covers


def define_func_covers(raw_z_func):
    print(f"Definition for ALL covers for {raw_z_func} function STARTED")
    m = len(raw_z_func)
    print("Expected", math.factorial(m), "to be done")
    template_covers = define_template_covers(m)
    
    func_covers = []

    active_counter = 0
    # for all unique permutations, substitute values in template covers
    for constituent_permutation in unique_permutations(raw_z_func):
        active_counter += 1
        if active_counter%1000 == 0:
            print("Done", active_counter)
        func_covers.extend([substitute_values(template, constituent_permutation) for template in template_covers])
    
    print("Actual", active_counter, "done")
    return func_covers
    
        
raw_z_func = "5 6 7 8 9 10 11 12".split()
define_func_covers(raw_z_func)
