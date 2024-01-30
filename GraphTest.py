from MakeFuncForDC import *
import matplotlib.pyplot as plt
import time

DC_c = 16
iterations = 1000

plainlen = plainLEn({str(n): ['0' for m in range(DC_c // 2)] for n in reversed(range(4))})
print("Plainlen is", plainlen)
total_time = 0

def test_makefunc(raw_z_data):
    start_time = time.time()
    data = cleaned(prepare(raw_z_data))
    z_bundles = {str(n): [] for n in range(len(raw_z_data), 0, -1)}
    bundled_count = 0
    bundled_LEn = 0
    while True:
        if len(data) < 2:
            break
        table = make_z_intersection_table(data)
        if len(table) < 1:
            break
        ro_table = make_density_table(table)
        used_z = random_max_z_from(ro_table)
        bundle = table[used_z]
    
        bundled_count += 1
        bundled_LEn += LEn(len(bundle))
        for z in used_z.split():
            z_bundles[z].append(bundle)
    
        update_data(data, used_z, bundle)
    end_time = time.time()
    
    global total_time
    total_time += end_time - start_time
    return totalLEn(raw_z_data, z_bundles, bundled_LEn)

raw_z_data = {'4': [], '3': [], '2': [], '1': []}
tlen_list = []

for i in range(iterations):
    for z in raw_z_data:
        raw_z_data[z] = random_z(DC_c)
    
    total_len = test_makefunc(raw_z_data)
    tlen_list.append(total_len)
    
    if i%100 == 0: print("i:", i)

counts, bins, _ = plt.hist(tlen_list, bins=range(min(tlen_list), max(tlen_list) + 1), align='left', rwidth=0.8)

# Set labels and title
plt.xlabel('LE cost')
plt.ylabel('Frequency')
plt.title('Implementation of four eight-term functions')

for count, bin_edge in zip(counts, bins[:-1]):
    plt.text(bin_edge, count + 0.1, str(int(count)), color='black', fontweight='bold')
    
print("\nMean time: {:.4f} seconds".format(total_time / iterations))

# Display the plot
plt.show()
