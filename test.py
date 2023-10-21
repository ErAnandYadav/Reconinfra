COMMISSION_SLABS = [
    (1000000, "Level1"),
    (3000000, "Level2"),
    (6000000, "Level3"),
    (15000000, "Level4"),
    (30000000, "Level5"),
    (60000000, "Level6"),
    (100000000, "Level7"),
    (150000000, "Level8"),
    (250000000, "Level9"),
    (400000000, "Level10"),
]

def find_commission_level(total_amount):
    for slab, level in COMMISSION_SLABS:
        if total_amount <= slab:
            return level
    return None  # If total_amount is greater than the highest slab

total_amount = 500000000
commission_level = find_commission_level(total_amount)
if commission_level:
    print(f"Commission Level for {total_amount}: {commission_level}")
else:
    print("Total amount exceeds the highest slab.")

