
table = [["SKU", "Barcode", "Quantity", "Item Name", "Order"],
         [12345, "blahblah-789846", 3, "Large Feathered Hat", 56789],
         [12346, "blahblah-789847", 2, "Purple Pants", 56777, "extra"]]
#for row in table:
#    print('| {:1} | {:^4} | {:>4} | {:<3} |'.format(*row))

def pretty_table(table: list, has_header: bool = True):
    """
    Given a table, produce a string that contains a "pretty" table
    (i.e. neatly formatted and readable).

    :param table: the table, as a list of lists, one for each row
    :param has_header: True if the first row of data is the header
    :return: string containing printable table
    """
    # Figure out how many columns are necessary
    num_cols = 0
    for row in table:
        cols = len(row)
        if cols > num_cols:
            num_cols = cols

    # Figure out how wide each column should be and make each row
    # the same length.
    column_widths = [0 for i in range(num_cols)]
    for row in table:
        if len(row) < num_cols:
            row.extend(["" for i in range(num_cols - len(row))])
        for col, item in enumerate(row):
            num_chars = len(str(item))
            if num_chars > column_widths[col]:
                column_widths[col] = num_chars

    # Actually generate string for table and add header if needed
    total_str = ""
    for row_num, row in enumerate(table):
        row_str = ""
        for col, item in enumerate(row):
            # produces a string like "| {:>4} "
            item_str = "| {:>" + str(column_widths[col]) + "} "
            row_str += item_str.format(item)
        row_str += "|"
        total_str += row_str + "\n"
        if row_num == 0 and has_header:
            row_str = ""
            for col in range(num_cols):
                item_str = "|-" + "-" * column_widths[col] + "-"
                row_str += item_str
            total_str += row_str + "\n"
    return total_str


table_str = pretty_table(table, True)
print(table_str)

