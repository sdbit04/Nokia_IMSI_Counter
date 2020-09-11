import os
import re
import gzip
import argparse

# "IMSI|time" "count"

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(project_path, "Input_data\\data.bin_decoded.txt.2020-09-09-165.log.gz")

# input_path = os.path.join(project_path, "Input_data\\data.bin_decoded.txt.2020-09-09-165.log")
# print("input_path {}".format(input_path))


# def get_imsi_vs_time(input_file_path, imsi_vs_time: dict = {}):
#     imsi_exp = re.compile("\s+iMSI\s+=", re.IGNORECASE)
#     start_of_block = re.compile("[0-9]+\s([0-9]{2,2}\s+[0-9]{2,2}\s[0-9]{2,2}\s+[0-9]{3,3})")
#     input_path = input_file_path
#     with open(input_path, 'r') as file_ob:
#         file_lines = file_ob.readlines()
#         for ind, line in enumerate(file_lines):
#             if re.match(imsi_exp, line):
#                 imsi = "{}".format(line.strip()).upper().lstrip("IMSI = ")
#                 # TODO if imsi into the filter
#                 imsi_time = None
#                 for i in range(ind-7, ind-600, -1):
#                     if re.match(start_of_block, file_lines[i]):
#                         imsi_time = re.match(start_of_block, file_lines[i]).group(1)
#                         break
#                 imsi_vs_time[imsi] = imsi_time
#     return imsi_vs_time


def get_imsi_vs_time_gz(input_file_path, imsi_list, imsi_vs_time: dict = {}):
    imsi_exp = re.compile(rb"\s+iMSI\s+=", re.IGNORECASE)
    start_of_block = re.compile(rb"[0-9]+\s([0-9]{2,2}\s+[0-9]{2,2}\s[0-9]{2,2}\s+[0-9]{3,3})")
    input_path = input_file_path

    with gzip.open(input_path, 'r') as file_ob:
        file_lines = file_ob.readlines()
        for ind, line in enumerate(file_lines):
            if re.match(imsi_exp, line):
                imsi = "{}".format(line.decode().strip()).upper().lstrip("IMSI = ")
                # TODO if imsi into the filter
                if imsi in imsi_list:
                    print("IMSI matched! with IMSI filter")
                    imsi_time = None
                    for i in range(ind-7, ind-600, -1):
                        start_block = re.match(start_of_block, file_lines[i])
                        if start_block is not None:
                            imsi_time = start_block.group(1)
                            if imsi_time is not None:
                                imsi_time = imsi_time.decode()
                                print(imsi_time)
                            break
                else:
                    continue
                imsi_vs_time[imsi] = imsi_time
    return imsi_vs_time


def read_config_file(file_path):
    config_dict = {}
    with open(file_path, 'r') as config_ob:
        lines = config_ob.readlines()
        for line in lines:
            input_dir = re.match(re.compile("input_dir", re.IGNORECASE), line)
            if input_dir is not None:
                print(line)
                input_dir = line.strip().split("=")[1].strip()
                config_dict["input_dir"]=input_dir
            output_dir = re.match(re.compile("output_dir", re.IGNORECASE), line)
            if output_dir is not None:
                output_dir = line.strip().split("=")[1].strip()
                config_dict["output_dir"]=output_dir
            imsi_list = re.match(re.compile("imsi_list", re.IGNORECASE), line)
            if imsi_list is not None:
                imsi_list = line.strip().split("=")[1].strip()
                config_dict["imsi_list"]=set(imsi_list.split(","))
    return config_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file_path", help="Please provide config file path")
    arguments = parser.parse_args()
    config_path = arguments.config_file_path
    config_dict = read_config_file(config_path)
    print(config_dict)
    input_path = config_dict["input_dir"]
    output_directory = config_dict["output_dir"]
    imsi_list = config_dict["imsi_list"]
    output = get_imsi_vs_time_gz(input_path, imsi_list )
    print(output)

