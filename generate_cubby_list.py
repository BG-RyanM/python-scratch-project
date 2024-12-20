num_modules = 5
rows_and_columns = [(8, 3), (6, 3), (3, 3), (3, 3), (6, 3), (8, 3)]
sides = ["E", "W"]

cubby_idx = 1
for mod_idx, module in enumerate(rows_and_columns):
    for side in sides:
        for row_idx in range(module[0]):
            for col_idx in range(module[1]):
                row_letter = chr(ord("A") + row_idx)
                out_str = f"{side}{mod_idx}{row_letter}{col_idx}: {cubby_idx}"
                print(out_str)
                cubby_idx += 1
