import sys
import getopt
import re


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

    build_pathway(input_file=input_file, output_file=output_file, search_term=search_term)


def build_pathway(input_file, output_file, search_term):
    print("input file = " + input_file + "; output file = " + output_file + "; search term =\"" + search_term + "\"")



if __name__ == "__main__":
    search_pathways(sys.argv[1:])