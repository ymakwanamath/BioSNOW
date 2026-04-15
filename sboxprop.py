from itertools import combinations

SYMBOL_TO_BITS = {'0': '00', '1': '01', '2': '10', '3': '11'}


def decode_qary_word(word):
    """Decode a string over {0,1,2,3} where each symbol encodes 2 bits."""
    return int(''.join(SYMBOL_TO_BITS[ch] for ch in word), 2)


def decode_sbox_dict(sbox_dict):
    """Convert the user's dictionary format into a list S of integers."""
    items = []
    for k, v in sbox_dict.items():
        x = decode_qary_word(k)
        y = decode_qary_word(v)
        items.append((x, y))

    n = len(next(iter(sbox_dict.keys()))) * 2
    size = 1 << n
    S = [0] * size
    seen = set()

    for x, y in items:
        if x in seen:
            raise ValueError(f"Duplicate decoded input: {x}")
        seen.add(x)
        S[x] = y

    if len(seen) != size:
        raise ValueError(f"Expected {size} inputs, found {len(seen)}")

    return S, n


def parity(x):
    return x.bit_count() & 1


def mobius_transform(vec):
    a = vec[:]
    n = (len(a)).bit_length() - 1
    for i in range(n):
        step = 1 << i
        for mask in range(len(a)):
            if mask & step:
                a[mask] ^= a[mask ^ step]
    return a


def anf_degree_of_boolean_function(truth):
    coeffs = mobius_transform(truth)
    deg = 0
    for mask, c in enumerate(coeffs):
        if c:
            deg = max(deg, mask.bit_count())
    return deg, coeffs


def is_permutation(S):
    return len(set(S)) == len(S)


def fixed_points(S):
    return [x for x, y in enumerate(S) if x == y]


def opposite_fixed_points(S, n):
    mask = (1 << n) - 1
    return [x for x, y in enumerate(S) if y == (x ^ mask)]


def cycle_decomposition(S):
    n = len(S)
    vis = [False] * n
    cycles = []
    for i in range(n):
        if not vis[i]:
            cur = i
            cyc = []
            while not vis[cur]:
                vis[cur] = True
                cyc.append(cur)
                cur = S[cur]
            cycles.append(cyc)
    return cycles


def differential_uniformity(S):
    size = len(S)
    ddt = [[0] * size for _ in range(size)]
    du = 0
    max_pairs = []
    for a in range(1, size):
        row_max = 0
        row_bs = []
        for x in range(size):
            b = S[x] ^ S[x ^ a]
            ddt[a][b] += 1
        row_max = max(ddt[a])
        if row_max > du:
            du = row_max
            max_pairs = [(a, b) for b, v in enumerate(ddt[a]) if v == du]
        elif row_max == du:
            max_pairs.extend((a, b) for b, v in enumerate(ddt[a]) if v == du)
    dap = du / size
    return du, dap, ddt, max_pairs


def walsh_component(S, a, b):
    total = 0
    for x in range(len(S)):
        total += 1 if parity(a & x) == parity(b & S[x]) else -1
    return total


def nonlinearity_and_lat(S, n):
    size = len(S)
    max_abs = 0
    lat = [[0] * size for _ in range(size)]
    component_nl = {}
    for b in range(1, size):
        comp_max_abs = 0
        for a in range(size):
            w = walsh_component(S, a, b)
            lat[a][b] = w
            aw = abs(w)
            comp_max_abs = max(comp_max_abs, aw)
            max_abs = max(max_abs, aw)
        component_nl[b] = (size // 2) - (comp_max_abs // 2)
    sbox_nl = min(component_nl.values())
    lap = (size + max_abs) / (2 * size)
    max_bias = max_abs / (2 * size)
    return sbox_nl, max_abs, max_bias, lap, lat, component_nl


def component_algebraic_degrees(S, n):
    size = len(S)
    degrees = {}
    coeffs = {}
    for b in range(1, size):
        truth = [parity(b & S[x]) for x in range(size)]
        deg, anf = anf_degree_of_boolean_function(truth)
        degrees[b] = deg
        coeffs[b] = anf
    return min(degrees.values()), max(degrees.values()), degrees, coeffs


def coordinate_algebraic_degrees(S, n):
    size = len(S)
    degrees = {}
    coeffs = {}
    for bit in range(n):
        truth = [((S[x] >> bit) & 1) for x in range(size)]
        deg, anf = anf_degree_of_boolean_function(truth)
        degrees[bit] = deg
        coeffs[bit] = anf
    return min(degrees.values()), max(degrees.values()), degrees, coeffs


def sac_matrix(S, n):
    size = len(S)
    mat = [[0.0] * n for _ in range(n)]
    dev = [[0.0] * n for _ in range(n)]
    worst = 0.0
    for i in range(n):
        dx = 1 << i
        for j in range(n):
            flips = 0
            for x in range(size):
                flips += ((S[x] ^ S[x ^ dx]) >> j) & 1
            p = flips / size
            mat[i][j] = p
            dev[i][j] = abs(p - 0.5)
            worst = max(worst, dev[i][j])
    avg_dev = sum(sum(row) for row in dev) / (n * n)
    return mat, dev, worst, avg_dev


def bic_sac(S, n):
    size = len(S)
    results = {}
    worst = 0.0
    avg = 0.0
    count = 0
    for i in range(n):
        dx = 1 << i
        for j, k in combinations(range(n), 2):
            both = 0
            for x in range(size):
                d = S[x] ^ S[x ^ dx]
                if ((d >> j) & 1) and ((d >> k) & 1):
                    both += 1
            p = both / size
            dev = abs(p - 0.25)
            results[(i, j, k)] = (p, dev)
            worst = max(worst, dev)
            avg += dev
            count += 1
    avg /= count
    return results, worst, avg


def bic_nl(S, n):
    size = len(S)
    nls = {}
    for j, k in combinations(range(n), 2):
        truth = [((S[x] >> j) & 1) ^ ((S[x] >> k) & 1) for x in range(size)]
        max_abs = 0
        for a in range(size):
            w = 0
            for x in range(size):
                w += 1 if parity(a & x) == truth[x] else -1
            max_abs = max(max_abs, abs(w))
        nls[(j, k)] = (size // 2) - (max_abs // 2)
    return min(nls.values()), max(nls.values()), nls


def boomerang_uniformity(S):
    size = len(S)
    if len(set(S)) != size:
        return None, None
    inv = [0] * size
    for x, y in enumerate(S):
        inv[y] = x
    bct = [[0] * size for _ in range(size)]
    beta = 0
    max_pairs = []
    for a in range(1, size):
        for b in range(1, size):
            cnt = 0
            for x in range(size):
                y1 = S[x] ^ b
                y2 = S[x ^ a] ^ b
                if inv[y1] ^ inv[y2] == a:
                    cnt += 1
            bct[a][b] = cnt
            if cnt > beta:
                beta = cnt
                max_pairs = [(a, b)]
            elif cnt == beta:
                max_pairs.append((a, b))
    return beta, (bct, max_pairs)


def summary_report(S, n):
    size = len(S)
    perm = is_permutation(S)
    fp = fixed_points(S)
    ofp = opposite_fixed_points(S, n)
    cycles = cycle_decomposition(S) if perm else []
    cycle_lengths = sorted((len(c) for c in cycles), reverse=True) if perm else []

    du, dap, ddt, du_pairs = differential_uniformity(S)
    nl, max_walsh, max_bias, lap, lat, comp_nl = nonlinearity_and_lat(S, n)
    comp_deg_min, comp_deg_max, comp_degrees, comp_anf = component_algebraic_degrees(S, n)
    coord_deg_min, coord_deg_max, coord_degrees, coord_anf = coordinate_algebraic_degrees(S, n)
    sac, sac_dev, sac_worst, sac_avg = sac_matrix(S, n)
    bic_sac_res, bic_sac_worst, bic_sac_avg = bic_sac(S, n)
    bic_nl_min, bic_nl_max, bic_nl_all = bic_nl(S, n)
    beta, bct_info = boomerang_uniformity(S) if perm else (None, None)

    return {
        'n': n,
        'size': size,
        'is_permutation': perm,
        'fixed_points': fp,
        'opposite_fixed_points': ofp,
        'cycle_lengths': cycle_lengths,
        'differential_uniformity': du,
        'DAP': dap,
        'du_pairs': du_pairs,
        'nonlinearity': nl,
        'max_walsh_abs': max_walsh,
        'max_linear_bias': max_bias,
        'LAP': lap,
        'component_nonlinearities': comp_nl,
        'component_degree_min': comp_deg_min,
        'component_degree_max': comp_deg_max,
        'component_degrees': comp_degrees,
        'coordinate_degree_min': coord_deg_min,
        'coordinate_degree_max': coord_deg_max,
        'coordinate_degrees': coord_degrees,
        'SAC_matrix': sac,
        'SAC_deviation_matrix': sac_dev,
        'SAC_worst_deviation': sac_worst,
        'SAC_average_deviation': sac_avg,
        'BIC_SAC_worst_deviation': bic_sac_worst,
        'BIC_SAC_average_deviation': bic_sac_avg,
        'BIC_NL_min': bic_nl_min,
        'BIC_NL_max': bic_nl_max,
        'boomerang_uniformity': beta,
        'component_anf_coeffs': comp_anf,
        'coordinate_anf_coeffs': coord_anf,
        'ddt': ddt,
        'lat': lat,
        'bct': bct_info[0] if bct_info else None,
    }


def print_report(report):
    print(f"Input/output bits           : {report['n']}")
    print(f"S-box size                  : {report['size']}")
    print(f"Permutation                 : {report['is_permutation']}")
    print(f"Fixed points                : {len(report['fixed_points'])} -> {report['fixed_points'][:16]}")
    print(f"Opposite fixed points       : {len(report['opposite_fixed_points'])} -> {report['opposite_fixed_points'][:16]}")
    if report['is_permutation']:
        print(f"Cycle lengths               : {report['cycle_lengths'][:20]}")
    print(f"Differential uniformity     : {report['differential_uniformity']}")
    print(f"DAP                         : {report['DAP']}")
    print(f"Nonlinearity                : {report['nonlinearity']}")
    print(f"Max |Walsh|                 : {report['max_walsh_abs']}")
    print(f"Max linear bias             : {report['max_linear_bias']}")
    print(f"LAP                         : {report['LAP']}")
    print(f"Component degree min/max    : {report['component_degree_min']} / {report['component_degree_max']}")
    print(f"Coordinate degree min/max   : {report['coordinate_degree_min']} / {report['coordinate_degree_max']}")
    print(f"Worst SAC deviation         : {report['SAC_worst_deviation']}")
    print(f"Average SAC deviation       : {report['SAC_average_deviation']}")
    print(f"Worst BIC-SAC deviation     : {report['BIC_SAC_worst_deviation']}")
    print(f"Average BIC-SAC deviation   : {report['BIC_SAC_average_deviation']}")
    print(f"BIC-NL min/max             : {report['BIC_NL_min']} / {report['BIC_NL_max']}")
    print(f"Boomerang uniformity        : {report['boomerang_uniformity']}")


if __name__ == '__main__':
    # Replace this example with your own dictionary in the same format.


    SBOX= {
    '0000': '0023',
    '0001': '2100',
    '0002': '3200',
    '0003': '0221',
    '0010': '1332',
    '0011': '1112',
    '0012': '0112',
    '0013': '3122',
    '0020': '1033',
    '0021': '3230',
    '0022': '1222',
    '0023': '1002',
    '0030': '3232',
    '0031': '2211',
    '0032': '0012',
    '0033': '0301',
    '0100': '3310',
    '0101': '1133',
    '0102': '3302',
    '0103': '1212',
    '0110': '2210',
    '0111': '3032',
    '0112': '2233',
    '0113': '2122',
    '0120': '0333',
    '0121': '2102',
    '0122': '0133',
    '0123': '2003',
    '0130': '0231',
    '0131': '2311',
    '0132': '2032',
    '0133': '1113',
    '0200': '1010',
    '0201': '2320',
    '0202': '3021',
    '0203': '0100',
    '0210': '3201',
    '0211': '0300',
    '0212': '3113',
    '0213': '1102',
    '0220': '0223',
    '0221': '0030',
    '0222': '2321',
    '0223': '1302',
    '0230': '1323',
    '0231': '1022',
    '0232': '2203',
    '0233': '0202',
    '0300': '2232',
    '0301': '3301',
    '0302': '1132',
    '0303': '2010',
    '0310': '1003',
    '0311': '3011',
    '0312': '0001',
    '0313': '2332',
    '0320': '0201',
    '0321': '2020',
    '0322': '0212',
    '0323': '1111',
    '0330': '3003',
    '0331': '2121',
    '0332': '3030',
    '0333': '1223',
    '1000': '3213',
    '1001': '0123',
    '1002': '3000',
    '1003': '3103',
    '1010': '0232',
    '1011': '1313',
    '1012': '2111',
    '1013': '1032',
    '1020': '2031',
    '1021': '1301',
    '1022': '1000',
    '1023': '2231',
    '1030': '0111',
    '1031': '3210',
    '1032': '0032',
    '1033': '1101',
    '1100': '1320',
    '1101': '3133',
    '1102': '0011',
    '1103': '2011',
    '1110': '1120',
    '1111': '0033',
    '1112': '1331',
    '1113': '0131',
    '1120': '1021',
    '1121': '0310',
    '1122': '1201',
    '1123': '0003',
    '1130': '1023',
    '1131': '3110',
    '1132': '0331',
    '1133': '2113',
    '1200': '0200',
    '1201': '2103',
    '1202': '0230',
    '1203': '1030',
    '1210': '2212',
    '1211': '2303',
    '1212': '3112',
    '1213': '2101',
    '1220': '1103',
    '1221': '0110',
    '1222': '2133',
    '1223': '1221',
    '1230': '0130',
    '1231': '2301',
    '1232': '1312',
    '1233': '0122',
    '1300': '3031',
    '1301': '1300',
    '1302': '3010',
    '1303': '0213',
    '1310': '2033',
    '1311': '0000',
    '1312': '1121',
    '1313': '0120',
    '1320': '1123',
    '1321': '2223',
    '1322': '0312',
    '1323': '3130',
    '1330': '2130',
    '1331': '1230',
    '1332': '1013',
    '1333': '0313',
    '2000': '2310',
    '2001': '0010',
    '2002': '1202',
    '2003': '1001',
    '2010': '1322',
    '2011': '0132',
    '2012': '3220',
    '2013': '2120',
    '2020': '3001',
    '2021': '1233',
    '2022': '0322',
    '2023': '3012',
    '2030': '0102',
    '2031': '3101',
    '2032': '2012',
    '2033': '3231',
    '2100': '0320',
    '2101': '3212',
    '2102': '2022',
    '2103': '1110',
    '2110': '1232',
    '2111': '1303',
    '2112': '2013',
    '2113': '0303',
    '2120': '0022',
    '2121': '2030',
    '2122': '2213',
    '2123': '0311',
    '2130': '1231',
    '2131': '3120',
    '2132': '1131',
    '2133': '0031',
    '2200': '2330',
    '2201': '3313',
    '2202': '0121',
    '2203': '3132',
    '2210': '0103',
    '2211': '3233',
    '2212': '1020',
    '2213': '2300',
    '2220': '1122',
    '2221': '3020',
    '2222': '2302',
    '2223': '2132',
    '2230': '1321',
    '2231': '0013',
    '2232': '3033',
    '2233': '2333',
    '2300': '1011',
    '2301': '3100',
    '2302': '1213',
    '2303': '1130',
    '2310': '2202',
    '2311': '0211',
    '2312': '2322',
    '2313': '1330',
    '2320': '2021',
    '2321': '0101',
    '2322': '1203',
    '2323': '1310',
    '2330': '0203',
    '2331': '2221',
    '2332': '1100',
    '2333': '1211',
    '3000': '0222',
    '3001': '2323',
    '3002': '2002',
    '3003': '3111',
    '3010': '1200',
    '3011': '3211',
    '3012': '2220',
    '3013': '2001',
    '3020': '3333',
    '3021': '3123',
    '3022': '3022',
    '3023': '3330',
    '3030': '3332',
    '3031': '0113',
    '3032': '3321',
    '3033': '3222',
    '3100': '3223',
    '3101': '0020',
    '3102': '0321',
    '3103': '2123',
    '3110': '1031',
    '3111': '3013',
    '3112': '1311',
    '3113': '3303',
    '3120': '2331',
    '3121': '0233',
    '3122': '2023',
    '3123': '3221',
    '3130': '2000',
    '3131': '0302',
    '3132': '2312',
    '3133': '3312',
    '3200': '2131',
    '3201': '3300',
    '3202': '2313',
    '3203': '3202',
    '3210': '0210',
    '3211': '3002',
    '3212': '2201',
    '3213': '1210',
    '3220': '2112',
    '3221': '3323',
    '3222': '3131',
    '3223': '0002',
    '3230': '3331',
    '3231': '3102',
    '3232': '1012',
    '3233': '0332',
    '3300': '0323',
    '3301': '1220',
    '3302': '3320',
    '3303': '2222',
    '3310': '3023',
    '3311': '2230',
    '3312': '3322',
    '3313': '0021',
    '3320': '3311',
    '3321': '3121',
    '3322': '0330',
    '3323': '2110',
    '3330': '3203',
    '3331': '1333',
    '3332': '0220',
    '3333': '2200',
}
            






    S, n = decode_sbox_dict(SBOX)
    report = summary_report(S, n)
    print_report(report)