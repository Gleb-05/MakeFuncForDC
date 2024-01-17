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
        
#print("check, unique permutations of 2,3,3:", unique_permutations([2,3,3]))

raw_z_func = "5 6 7 8 9 10 11 12".split()

m = len(raw_z_func)
k = 3

# def LEn_k(terms_n, k):
#     return 1 + (terms_n - 2) // (k - 1)


# https://stackoverflow.com/questions/26812803/find-all-possible-combinations-partitions-of-2-numbers-for-a-given-number
from itertools import combinations_with_replacement

LEk_configs = {}
# range from best(k'=k) to worst(k'=2) possible number of LE, LE used to cover function
for leN in range(4,7+1):
    LEk_configs[leN] = [list(x) for x in combinations_with_replacement(range(1,k), leN) if sum(x) == m-1]

print("number of used up LEs and corresponding configurations for their inputs: ", LEk_configs)

# for leN_group in LEk_configs:
#     for k_config in leN_group:
k_config = LEk_configs[4][0]
k_config_permutations = unique_permutations(k_config)
print("permutations for most efficient configuration:")
for config in k_config_permutations:
    print(config)
    
# for one_config_permutation in k_config_permutations:
#     permutation = [x+1 for x in one_config_permutation]
permutation = [x+1 for x in k_config_permutations[3]]
print("selected permutation of k configuration")
print(permutation)

init_k = permutation[0]
func_covers = [[raw_z_func[:init_k]] + raw_z_func[init_k:]]

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


print("all possible LE positions for selected permutation of one configuration")
for cover in func_covers:
    print(cover)
print()
