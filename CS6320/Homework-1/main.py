import re
import argparse


def process_matched_strings(_list):
    """Post-processing the sub-groups returned by re.findall()
    for the matched pattern elements.
    """
    matched_strings = []
    for _tuple in _list:
        filtered_tuple = [x for x in _tuple if x != '']
        matched_strings.append(filtered_tuple[0].strip('\n'))
    return matched_strings


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CS6320: Homework 1')
    parser.add_argument('--run', dest='run', type=str,
                        choices=['ssn', 'tno'],
                        required=True, help='Identifier program to run, choices are:\
                        (a) ssn: Social Security Numbers\
                        (b) tno: Telephone Numbers')
    parser.add_argument('--input-path', dest='input_path', type=str,
                        required=True, help='Path to input .txt file.')

    args = parser.parse_args()

    with open(args.input_path, 'r') as text_file:
        text = text_file.read()

    if args.run == 'ssn':
        pattern = (r"((\s|^)(00[1-9]|0[1-9]\d|[1-9]\d\d)\d{2}"
                   r"(000[1-9]|00[1-9]\d|0[1-9]\d\d|[1-9]\d\d\d)(\s|$))"
                   r"|"
                   r"((\s|^)(00[1-9]|0[1-9]\d|[1-9]\d\d)-\d{2}-"
                   r"(000[1-9]|00[1-9]\d|0[1-9]\d\d|[1-9]\d\d\d)(\s|$))")
        print("Printing matching Social Security Numbers: ")
    elif args.run == "tno":
        pattern = (r"((\s|^)(\+\((0[1-9]|[1-9]\d)\)-\((00[1-9]|0[1-9]\d|[1-9]\d\d)\)-"
                   r"\((00[1-9]|0[1-9]\d|[1-9]\d\d)\)-"
                   r"\((000[1-9]|00[1-9]\d|0[1-9]\d\d|[1-9]\d\d\d)\))(\s|$))"
                   r"|"
                   r"((\s|^)(\+\((0[1-9]|[1-9]\d)\)-(00[1-9]|0[1-9]\d|[1-9]\d\d)-"
                   r"(00[1-9]|0[1-9]\d|[1-9]\d\d)-"
                   r"(000[1-9]|00[1-9]\d|0[1-9]\d\d|[1-9]\d\d\d))(\s|$))"
                   r"|"
                   r"((\s|^)(\+(0[1-9]|[1-9]\d)-(00[1-9]|0[1-9]\d|[1-9]\d\d)-"
                   r"(00[1-9]|0[1-9]\d|[1-9]\d\d)-"
                   r"(000[1-9]|00[1-9]\d|0[1-9]\d\d|[1-9]\d\d\d))(\s|$))")
        print("Printing matching Telephone Numbers:")

    matches = re.findall(pattern, text, re.M)

    matches = [match for match in process_matched_strings(matches)]

    for match in matches:
        print(match)
