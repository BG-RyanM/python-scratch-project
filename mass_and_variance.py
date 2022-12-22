box1 = {
    "barcode": "BG03081",
    "product": "small_bag_container_1",
    #        "weights":[102, 98, 98, 102, 102, 100, 106, 102, 106, 102, 100, 102, 100, 100]}
    "weights": [
        105,
        105,
        105,
        105,
        100,
        105,
        105,
        105,
        105,
        105,
        105,
        105,
        105,
        105,
        105,
        100,
        110,
        105,
        105,
        110,
        105,
        105,
        105,
        100,
        105,
        100,
        105,
        105,
        105,
        100,
    ],
}

box2 = {
    "barcode": "BG03082",
    "product": "hard_drive_enclosure",
    "weights": [170, 170, 170, 170, 140, 175, 175, 170, 170, 170, 170],
}

box3 = {
    "barcode": "BG03083",
    "product": "orange_bag_w_chapstick",
    "weights": [90, 90, 60, 85, 90, 75, 90, 90, 90, 65, 90, 90, 90, 65, 95, 90],
}

box4 = {
    "barcode": "BG03084",
    "product": "white_medium_bag",
    "weights": [535, 530, 530, 545, 525, 545, 540, 545, 530],
}

box5 = {
    "barcode": "BG03085",
    "product": "white_large_bag",
    "weights": [1050, 1035, 1015, 1045, 1055, 1030],
}

box6 = {
    "barcode": "BG03086",
    "product": "large_cuboid",
    "weights": [780, 785, 775, 785, 1815],
}

box7 = {
    "barcode": "BG03087",
    "product": "small_bag_container_7",
    "weights": [
        105,
        105,
        105,
        110,
        105,
        105,
        105,
        105,
        110,
        110,
        105,
        105,
        100,
        105,
        105,
        105,
        105,
        105,
        110,
        105,
        100,
    ],
}

box8 = {
    "barcode": "BG03088",
    "product": "bag_with_sandals",
    "weights": [630, 585, 475, 615, 610, 610, 600, 610, 600],
}

box9 = {
    "barcode": "BG03089",
    "product": "small_cuboid",
    "weights": [190, 295, 285, 290, 285, 285, 305],
}

box10 = {
    "barcode": "BG03090",
    "product": "small_bag_container_10",
    "weights": [100, 105, 100, 100, 100, 105, 110, 100, 105],
}

boxes = [box1, box2, box3, box4, box5, box6, box7, box8, box9, box10]


def calculate_mass_and_variance(weight_list):
    weight_list = list(map(lambda x: x / 1000, weight_list))
    mean = sum(weight_list) / len(weight_list)
    variance = sum(map(lambda x: (x - mean) * (x - mean), weight_list)) / (
        len(weight_list) - 1
    )
    return mean, variance


for b in boxes:
    mean, variance = calculate_mass_and_variance(b["weights"])
    print(
        f"product {b['product']} has mass {mean}, variance {variance}, goes in box {b['barcode']}"
    )
