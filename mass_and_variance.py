box1 = {"barcode":"BG03081", "product":"white_bag_type_1",
        "weights":[102, 98, 98, 102, 102, 100, 106, 102, 106, 102, 100, 102, 100, 100]}

box2 = {"barcode":"BG03082", "product":"hard_drive_enclosure",
        "weights":[170, 172, 140, 170, 170, 172, 170, 170, 170, 170]}

box3 = {"barcode":"BG03083", "product":"orange_bag_w_chapstick",
        "weights":[88, 90, 90, 90, 92, 90, 90, 56, 90, 90, 82, 90, 90, 92, 90, 66, 68, 92]}

box4 = {"barcode":"BG03084", "product":"white_10_bag",
        "weights":[540, 520, 522, 528, 520]}

box5 = {"barcode":"NONE", "product":"test",
        "weights":[10000, 8000, 10000, 8000, 8000, 4000]}

boxes = [box1, box2, box3, box4, box5]

def calculate_mass_and_variance(weight_list):
    weight_list = list(map(lambda x: x / 1000, weight_list))
    mean = sum(weight_list) / len(weight_list)
    variance = sum(map(lambda x: (x - mean) * (x - mean), weight_list)) / (len(weight_list) - 1)
    return mean, variance

for b in boxes:
    mean, variance = calculate_mass_and_variance(b["weights"])
    print(f"product {b['product']} has mass {mean}, variance {variance}, goes in box {b['barcode']}")