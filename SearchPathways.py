import sys
import getopt
import re
import json


def search_pathways(argv):
    input_file = ""
    input_regex = r"^(.)*\.json$"

    output_file = ""
    output_regex = r"^(.)*\.json$"
    try:
        opts, args = getopt.getopt(argv, "hi:o:s:", ["input=", "output=", "help=", "search="])
    except getopt.GetoptError:
        print("SearchPathways.py -s \"search query\" -i <inputfile.csv/.tsv> -o <outputfile.json>")
        sys.exit(2)
    valid_in = "-i" in argv or "--input" in argv
    valid_out = "-o" in argv or "-output" in argv
    valid_search = "-s" in argv or "-search" in argv
    if ((valid_in or valid_search or valid_out) and not (valid_in and valid_out and valid_search)) \
            and ("-h" not in argv and "--help" not in argv):
        print("Missing valid flags!\nValid Examples:\n\tSearchPathways.py -s \"search query\" -i <inputfile.csv/.tsv> -o <outputfile.json>\n\t" +
              "SearchPathways.py --search \"search query\" --input <inputfile.csv/.tsv> --output <outputfile.json>\n\t" +
              "SearchPathways.py -h\n\tSearchPathways.py --help")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("SearchPathways.py -s \"search query\" -i <inputfile.csv/.tsv> -o <outputfile.json>")
            sys.exit()
        elif opt in ("-i", "--input"):
            if re.fullmatch(input_regex, arg):
                input_file = arg
            else:
                print("Input file must be .json")
                sys.exit(2)
        elif opt in ("-o", "--output"):
            if re.fullmatch(output_regex, arg):
                output_file = arg
            else:
                print("Output file must be a .json")
                sys.exit(2)
        elif opt in ("-s", "--search"):
            if arg != "":
                search_term = arg
            else:
                print("A search term must be provided")
                sys.exit(2)

    build_pathways(input_file=input_file, output_file=output_file, search_term=search_term)


def build_pathways(input_file, output_file, search_term):

    with open(input_file) as json_file:
        data = json.load(json_file)

    results = dict()
    results[search_term] = dict()
    results[search_term]["count"] = 0
    results[search_term]["percent"] = 0
    results[search_term]["results"] = dict()

    search_json(results=[results[search_term]], kegg_json=data, term=search_term)

    with open(output_file, "w") as outfile:
        json.dump(results, outfile, indent=2)
    outfile.close()
    json_file.close()

    print("Search Term: " + search_term)
    print("Total Transcripts: " + str(results[search_term]["count"]))
    print("Percent of Total Transcripts: " + str(results[search_term]["percent"]) + "%")
    pathways = ""
    for p in results[search_term]["results"]:
        pathways += ("\t" + p + "\n")
    print("Pathways taken:\n" + pathways[:-1])
    print("***To see associated transcripts view \"" + output_file + "\", your output file.***")


def search_json(results, kegg_json, term, path=""):
    for k in kegg_json:
        if term.lower() in k.lower() or term.lower() == k.lower():
            results[0]["count"] += kegg_json[k]["count"]
            results[0]["percent"] += kegg_json[k]["percent"]
            if "Sub" in kegg_json[k]:
                transcripts = [[]]
                get_nested_transcripts(kegg_json[k]["Sub"], transcripts)
                kegg_json[k]["Transcripts"] = transcripts[0]
                del kegg_json[k]["Sub"]
            results[0]["results"][path[4:] + " -> " + k] = kegg_json[k]
        else:
            if "Sub" in kegg_json[k]:
                search_json([results[0]], kegg_json[k]["Sub"], term=term, path=(path + " -> " + k))
            else:
                continue


def get_nested_transcripts(kegg_json, transcripts):
    for k in kegg_json:
        if "Sub" in kegg_json[k]:
            get_nested_transcripts(kegg_json[k]["Sub"], transcripts)
        else:
            hits_trans = []
            for t in kegg_json[k]["Transcripts"]:
                transcripts[0].append(t)


if __name__ == "__main__":
    search_pathways(sys.argv[1:])