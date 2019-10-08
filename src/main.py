from random import randint


def calc_rev(d, c):
    p = d['efficiency'] * c
    if p > d['output-capacity']:
        p = d['output-capacity']
    if p > 50000:
        p0 = 50000
        p1 = p - 50000
    else:
        p0 = p
        p1 = 0
    return (p0 * 5) + (p1 * 3.5)


def profit_model(dam_1, dam_2, c1_values, c2_values, i1_values, i2_values):
    c1 = c1_values[0]
    c2 = c2_values[0]
    dam_1['level'] += i1_values[0] - c1_values[0]
    dam_2['level'] += i2_values[0] - c2_values[0] + c2

    # hard bounds checking

    # negative conversions aren't reasonable
    if c1 < 0 or c2 < 0:
        return 0, None
    # over conversions aren't reasonable
    elif dam_1['level'] < dam_1['minimum'] or dam_2['level'] < dam_2['minimum']:
        return 0, None

    # spill way used ?

    if dam_1['level'] > dam_1['maximum']:
        dam_1['level'] = dam_1['maximum']
    if dam_2['level'] > dam_2['maximum']:
        dam_2['level'] = dam_2['maximum']

    # base case

    if len(c1_values) == 1:  # base case
        return calc_rev(dam_1, c1) + calc_rev(dam_2, c2), [(c1, c2)]

    # continuation case

    else:
        rev, conversions = profit_model(dam_1, dam_2, c1_values[1:], c2_values[1:], i1_values[1:], i2_values[1:])
        if conversions is None:  # bubble up hard bounds errors
            return 0, None
        else:
            return rev + calc_rev(dam_1, c1) + calc_rev(dam_2, c2), conversions + [(c1, c2)]


def main(conversions_for_dam_1, conversion_for_dam_2):
    revenue, conversions = profit_model(
        dam_1={
            'maximum': 2000,
            'minimum': 1200,
            'level': 1900,
            'efficiency': 400,
            'output-capacity': 60000
        },
        dam_2={
            'maximum': 1500,
            'minimum': 800,
            'level': 850,
            'efficiency': 200,
            'output-capacity': 35000
        },
        c1_values=conversions_for_dam_1,
        c2_values=conversion_for_dam_2,
        i1_values=[200, 130, 160, 190],
        i2_values=[40, 15, 25, 30]
    )
    if conversions is None:
        return 0, None
    else:
        return revenue, list(reversed(conversions))


centers1 = [900, 900, 900, 900]
centers2 = [900, 900, 900, 900]
margin = 900
best_rev = 0
best_conversion = None


for _ in range(0, 20):
    for i in range(0, 1000):
        rev, conv = main(
            [
                randint(centers1[0] - margin, centers1[0] + margin),
                randint(centers1[1] - margin, centers1[1] + margin),
                randint(centers1[2] - margin, centers1[2] + margin),
                randint(centers1[3] - margin, centers1[3] + margin),
            ], [
                randint(centers2[0] - margin, centers2[0] + margin),
                randint(centers2[1] - margin, centers2[1] + margin),
                randint(centers2[2] - margin, centers2[2] + margin),
                randint(centers2[3] - margin, centers2[3] + margin),
            ])
        if rev > best_rev:
            # print(f"\t {best_rev} -> {rev}")
            best_rev = rev
            best_conversion = conv
    # print(best_rev, best_conversion, margin)
    margin *= 0.75
    margin = int(margin)
    for i, best_conv in enumerate(best_conversion):
        centers1[i] = best_conv[0]
        centers2[i] = best_conv[1]

print(f"The highest possible revenue is ${best_rev} with a sequence of monthly water -> power conversion values equal to {best_conversion}.")
