def get_commands(file_path: str):
    with open(file_path, "r") as file:
        # Read each line in the file
        for line in file:
            line_parts = line.strip().split(" ")
            file_info = line_parts[1]
            try:
                colons_index = file_info.index("::")
            except ValueError:
                continue

            filename = file_info[:colons_index]
            testname = file_info[colons_index + 2 :]
            print(
                f"python3 -m pytest --log-level INFO -o log_cli=true {filename} -k '{testname}'"
            )


get_commands("failed_tests.txt")
