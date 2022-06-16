import json


def trans_break(input_file, output_file):
    seperator = ""

    if input_file[len(input_file) - 4:] == ".csv":
        seperator = ","
    else:
        seperator = "\t"
    in_file = open(input_file, "r")
    lines = in_file.readlines()

    total_count = len(lines) - 1

    count_dict = dict()

    for line in lines[1:]:
        trans_id = line.split(seperator)[0]
        tax_column = line.split(seperator)[7]
        taxonomy = tax_column.split(";")
        i = 0
        target = [count_dict]
        while i < len(taxonomy):
            tax = taxonomy[i].strip("\n").strip()
            if ":::" in tax:
                i += 1
                continue
            if tax not in target[0].keys():
                target[0][tax] = dict()
                target = [target[0][tax]]
                target[0]["count"] = 1
                target[0]["percent"] = (1 / total_count) * 100
                if i != len(taxonomy) - 1:
                    target[0]["Sub"] = dict()
                    target = [target[0]["Sub"]]
                elif i == len(taxonomy) - 1:
                    target[0]["Transcripts"] = []
                    target[0]["Transcripts"].append(trans_id)
                    target[0]["Transcripts"].sort()
            else:
                target = [target[0][tax]]
                target[0]["count"] += 1
                target[0]["percent"] += (1 / total_count) * 100
                if i != len(taxonomy) - 1:
                    # if "Sub" not in target[0]:
                    #     target[0]["Sub"] = dict()
                    target = [target[0]["Sub"]]
                elif i == len(taxonomy) - 1:
                    # if "Transcripts" not in target[0]:
                    #     target[0]["Transcripts"] = []
                    target[0]["Transcripts"].append(trans_id)
                    target[0]["Transcripts"].sort()
            i += 1

    with open(output_file, "w") as outfile:
        json.dump(count_dict, outfile, indent=2)
    outfile.close()
    in_file.close()
