import re
import sys
import io

# set the default encoding to utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading file: {file_path}")
        print(type(e), e)
        return []

def parse_lines(data):
    # check if data is a list
    if not isinstance(data, list):
        return {}
    my_dict = {}
    # compile regex pattern
    line_pattern = re.compile(r"(^[A-Za-z0-9_]+)\s*:(.*$)")
    for line in data:
        match = line_pattern.match(line)
        if match:
            key = str(match.group(1))
            value = str(match.group(2))
            my_dict[key] = value
    return my_dict


def merge_dicts(dict1, dict2):
    # this merges two dictionaries, adding the keys from dict2 to dict1
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return {}
    result = dict1.copy()  # 创建一个新的字典，以防修改原始字典
    print ("# Missing strings", "="*62, sep="|")
    for key, value in dict2.items():
        if key not in result:
            result[key] = value
            print(f"{key:<50}:not found in target file")
    print("# String result", "="*64, sep="|")
    return result

if not sys.argv[1:]:
    print("Usage: merge_strings.py <source_file> <target_file>")
    sys.exit(1)
elif len(sys.argv) < 3:
    print("Error: Missing arguments")
    sys.exit(1)
elif len(sys.argv) > 3:
    print("Error: Too many arguments")
    sys.exit(1)
elif sys.argv[1] == sys.argv[2]:
    print("Error: Source file and target file are the same")
    sys.exit(1)

string_list = read_file(sys.argv[1])
target_string_list = read_file(sys.argv[2])
my_dict = merge_dicts(parse_lines(target_string_list), parse_lines(string_list))

# format printed output
for key, value in my_dict.items():
    print(f"{key:<50}:{value}")
