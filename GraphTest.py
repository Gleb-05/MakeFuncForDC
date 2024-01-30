from MakeFuncForDC import *

DC_c = 16

plainlen = plainLEn({str(n): ['0' for m in range(DC_c // 2)] for n in reversed(range(4))})

def makefunc(raw_z_data):
    data = cleaned(prepare(raw_z_data))
    z_bundles = {str(n): [] for n in range(len(raw_z_data), 0, -1)}
    bundled_count = 0
    bundled_LEn = 0
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

    print("Total LE solution cost:", totalLEn(raw_z_data, z_bundles, bundled_LEn))

