box1 = {"barcode": "R:71831", "product": "white_bag_800Grams_1",
        "weights": [857, 853, 803, 880, 852, 862, 907]}

box2 = {"barcode": "R:71875", "product": "white_bag_800Grams_2",
        "weights": [769, 837, 863, 874, 851, 880, 874]}

box3 = {"barcode": "R:71900", "product": "white_bag_1800Grams_1",
        "weights": [1792, 1803, 1851, 1855]}

box4 = {"barcode": "R:71915", "product": "white_bag_1800Grams_2",
        "weights": [1790, 1800, 1850, 1825]}

box5 = {"barcode": "R:71904", "product": "white_bag_500Grams",
        "weights": [534, 534, 527, 540, 530, 523, 551, 517, 500, 512, 521, 521, 519, 521, 532, 513]}

box6 = {"barcode": "R:71909", "product": "white_bag_1000Grams_1",
        "weights": [1181, 1036, 1050, 1041, 1102]}

box7 = {"barcode": "R:71887", "product": "white_bag_1000Grams_2",
        "weights": [1050, 1043, 970, 984, 1084]}

box8 = {"barcode": "R:71861", "product": "white_bag_130Grams_1",
        "weights": [134, 111, 120, 142, 100, 126, 100, 135, 100, 115, 105, 138, 139, 102, 138, 136, 105, 115]}

box9 = {"barcode": "R:71862", "product": "white_bag_130Grams_2",
        "weights": [117, 102, 141, 132, 98, 128, 101, 100, 115, 156, 150, 133, 129, 123, 108, 110, 122]}

box10 = {"barcode": "NONE", "product": "test",
         "weights": [10000, 8000, 10000, 8000, 8000, 4000]}

boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9, box10]


def calculate_mass_and_variance(weight_list):
    weight_list = list(map(lambda x: x / 1000, weight_list))
    mean = sum(weight_list) / len(weight_list)
    variance = sum(map(lambda x: (x - mean) * (x - mean), weight_list)) / (len(weight_list) - 1)
    return mean, variance


for b in boxes:
    mean, variance = calculate_mass_and_variance(b["weights"])
    print(f"product {b['product']} has mass {mean}, variance {variance}, goes in box {b['barcode']}")