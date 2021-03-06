from time import time
from sys import argv
import os

st = time()

def main(filename):
    if ".html" not in filename: filename+=".html"

    looking = [
        "src",
        "href"
    ]

    with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
        html = f.read()
    print("Input html length:", len(html), "characters\n")

    for target in looking:
        _idx = 0
        while(0 <= (idx:=html[_idx:].find(f"{target}=\"assets")) < len(html)):
            head = html[:_idx+idx+len(target)+2]
            eurl = html[_idx+idx+len(target)+2:].find("\"")
            body = html[_idx+idx+len(target)+2:_idx+idx+len(target)+2+eurl]
            foot = html[_idx+idx+len(target)+2+eurl:]
            part = "{{url_for('static', filename='" + body + "')}}"
            html = head + part + foot
            _idx = _idx + idx + len(target) + 2 + len(part)

            print("Fixed:", part)

    with open(os.path.join(os.path.dirname(__file__), "output.html"), "w") as f:
        f.write(html)
    print("\nFixed html length:", len(html), "characters")


if len(argv) > 1:
    main(argv[1])
else:
    print("\nWrong Usage:\n--correct usage: \n\tpython [this_pyfile_name.py] [html_file_name.html]\n--example usage:\n\tpython makeTemplate.py index.html")
print("\nFinish execution in:", time()-st)