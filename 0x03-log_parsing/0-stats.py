#!/usr/bin/python3
"""
log parsing script
"""


if __name__ == "__main__":
    import sys
    import re

    def line_checker(line):
        """
        Check the line if it comforms with certain predefined rules
        Arg:
            line: line to check
        """
        pattern = r'\"GET /projects/260 HTTP/1.1\"'
        match = re.search(pattern, line)
        line_split_list = line.split(" ")
        if match and len(line_split_list) > 5:
            return line_split_list
        return []

    def printer(codes_dict, file_size):
        """
        Print output to the stdout
        Arg:
            codes_int: A dict with codes and number of times their appear
            files_size: cumulative total size of the file
        """
        print("File size: {}".format(file_size))
        try:
            ordered_codes = [int(key) for key in codes_dict.key()]
            ordered_codes.sort()
            for code in ordered_codes:
                print("{}: {}".format(code, codes_dict[str(code)]))
        except ValueError as e:
            pass

        file_size = 0
        possible_codes = ["200", "301", "400", "401", "403", "404", "405", "500"]
        codes = {}
        tally = 0
        try:
            for line in sys.stdin:
                line = line.rstrip()
                line_list = line_checker(line)
                if len(line_list) > 1:
                    tally += 1
                    file_size += int(line_list[-1])
                    if line_list[-2] in possible_codes:
                        if codes.get(line_list[-2]):
                            codes[line_list[-2]] += 1
                        else:
                            codes[line_list[-2]] = 1
                    if tally % 10 == 0:
                        printer(codes, file_size)
            printer(codes, file_size)
        except KeyboardInterrupt as err:
            printer(codes, file_size)
            raise
