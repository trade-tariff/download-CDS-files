import subprocess
import os
import sys
import string
from codecs import decode


# Get the argument
if len(sys.argv) > 1:
    xml_path = os.path.join(os.getcwd(), "resources", "xml")
    term = ">" + decode(sys.argv[1], 'unicode_escape') + "<"
    grepped_filename = term.translate(str.maketrans('', '', string.punctuation)) + ".txt"
    grep_path = os.path.join(os.getcwd(), "resources", "grep")
    grep_path2 = os.path.join(grep_path, grepped_filename)

    print("\nSearching for term '{term}' in folder '{grep_path2}'.\n".format(term=term, grep_path2=grep_path2))

    grep_string = "grep -r --include='*.xml' '{term}' '{xml_path}' > '{grep_path2}'".format(
        term=term,
        xml_path=xml_path,
        grep_path2=grep_path2
    )
    # print("\n" + grep_string + "\n")
    ret = os.system(grep_string)
    # print(ret)

    # Sort the file by date
    file = open(grep_path2)
    lines = file.readlines()
    lines.sort(reverse=True)
    file.close()
    file = open(grep_path2, "w")

    for element in lines:
        file.write(element)  # + "\n")

    file.close()

    os.system('open "%s"' % grep_path)

else:
    print("\nPlease provide a search term\n")
    sys.exit()
