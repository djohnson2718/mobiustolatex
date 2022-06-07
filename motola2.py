
from bs4 import BeautifulSoup, NavigableString
import re
import data
import sys
import os
from pathlib import Path


filename = sys.argv[1]
#filename = r"C:/Users/Johnson/GitHub/motola/mobius/finalv5.html"
wname = Path(filename).stem

print(f"Using instructor names {data.instructors} and {data.semester}, edit the data.py file to change.")

with open(filename, errors = "ignore") as f:
    mo = BeautifulSoup(f, 'html.parser')

exam_num_tag = mo.find("td", string=re.compile("Exam \d"))

exam_num_tag = mo.find("td", string=re.compile("Exam \d"))

if exam_num_tag:
    exam_name = exam_num_tag.string
else:
    exam_name = "Final Exam"

def is_question(tag):
    if tag.name != "td":
        return False
    if tag.b is None:
        return False
    return tag.b.string.startswith("Question")

nonBreakSpace = u'\xa0'

abc = "Xabcdefghijklm"
answer_key = dict()

def process_children(tag, output, question_num, is_mc_option):

    for q_item in tag.children:  
        paragraph_text = ""
        #print("item", str(q_item)[:100])      
        if q_item.name == "p":
            process_children(q_item,output,question_num,is_mc_option)
        elif q_item.name == "script":
            if q_item["type"] ==  "math/tex; mode=display":
                if q_item.string.startswith(r"\begin{align*}"):
                    paragraph_text = q_item.string
                else:
                    paragraph_text = r"\[" + q_item.string.replace("$",r"\$") + r"\]"
            elif q_item["type"]== "math/tex":
                paragraph_text = "$" + q_item.string.replace("$",r"\$") + "$"
            elif q_item["type"] == "math/mml":
                #don't really know what this is, but seems ok to ignore it
                pass
            else:
                output("Unexpected! a script whose type is not one we know" + q_item["type"])
            output(paragraph_text)

        elif isinstance(q_item, NavigableString):
            paragraph_text = q_item.replace(nonBreakSpace, " ")
            if len(paragraph_text) > 0:
                output(paragraph_text.replace("$",r"\$"))

        elif q_item.name in ["br","b"]:
            pass
        elif q_item.name == "span":
            sc = q_item.get("class")
            if sc:
                if sc == ["MathJax_Preview"] or sc == ["MathJax"]:
                    pass
                else:
                    print("Unexpected! a span with class that is not MJ or MJ preview", str(q_item["class"]))
            else:
                #print("Unexpected, a span without class!")
                process_children(q_item,output,question_num,is_mc_option)
        elif q_item.name == "div":
            dc = q_item.get("class")
            if dc:
                if dc == ["MathJax_Display"]:
                    pass
                else:
                    print("Unexpected, a div with class", dc)
            else:
                # a div with no class
                process_children(q_item,output,question_num,is_mc_option)
                #print("div!!!!!!!!!!!!!!!!")
        elif q_item.name == "table":
            if not  q_item.get("border"):
                #the multiple choice options
                output(r"\begin{enumerate}")
                output("\n")
                cur_option_num = 0
                for option in q_item.find_all(["p","correct"]):
                    if option.name == "p":
                        output("\item ")
                        process_children(option,output,question_num, True)
                        output("\n")
                        cur_option_num += 1
                    elif option.name == "correct":
                        answer_key[question_num] = abc[cur_option_num]
                output(r"\end{enumerate}")
            else:
                #it is a table with info for the problem
                numcols = len(q_item.tbody.tr.contents)
                output("\n" + r"\begin{center}\begin{tabular}{|" + "|".join(["c"]*numcols) + "|}\n\hline\n")
                for tr in q_item.tbody.children:
                    if isinstance(tr, NavigableString):
                        continue
                    is_first = True
                    for td in tr.children:
                        if isinstance(td, NavigableString):
                            continue
                        if not is_first:
                            output(" & ")
                        is_first = False
                        process_children(td,output,question_num,is_mc_option)
                    output(r" \\" + "\n" + r"\hline" + "\n")
                output(r"\end{tabular}\end{center}" + "\n")
        elif q_item.name == "img":
            mo_src_file = q_item['src']
            if mo_src_file[-4:] == ".gif":
                src_file = f"../png/{Path(mo_src_file).stem}.png"
            else:
                src_file = "." + mo_src_file

            if is_mc_option:
                output(r"\begin{minipage}[c]{0.25\textwidth}\fbox{\includegraphics[width=4cm]{" + src_file + r"}}\end{minipage}")
            else:
                output("\\begin{center}\n")
                output("\\includegraphics[width=9cm]{" + src_file +"}\n")
                output("\\end{center}\n")

        elif q_item.name == "em":
            output(r"\emph{" + q_item.string + "}")


        elif q_item.name == "correct":
            answer_key[question_num] = abc[int(q_item["choice"])]

        else:
            print("Unknown item, name = ", str(q_item.name))
            if not q_item.name:
                print(q_item)




from string import Template 
header = Template(r"""
\documentclass[11pt]{article}

%opening
\usepackage[]{mcexam-v2}
\usepackage{amsmath,mathtools}

%\usepackage[margin=1.2in]{geometry}

\everymath{\displaystyle}

\begin{document}
    	\vspace*{-1.5cm}
	{\huge RED --- DO NOT WRITE ON THIS EXAM}
	\vspace{.7cm}
	\Large
	\begin{center}
		\textbf{Math 110 \\ College Algebra \\$EXAM_NAME \\ $SEMESTER}\\
		Instructors: $INST
	\end{center}

\begin{questions}
""")

latex_dir = os.path.dirname(filename) + f"\{wname}_converted\latex"
os.makedirs(latex_dir, exist_ok=True)
with open(f"{latex_dir}\{wname}.tex","w") as f:
    output = f.write

    output(header.substitute(EXAM_NAME = exam_name, SEMESTER = data.semester, INST = ", ".join(data.instructors)))

    count = 1
    questions = mo.find_all(is_question) 

    for q in questions:
        #print("Question ",count)
        output("%%%%%% Question " + str(count) + "\n")
        output(r"""\begin{minipage}{\textwidth}
        \question """)
        process_children(q, output, count, False)
        output(r"""\vspace{.25cm}\hrule\vspace{1cm}
        \end{minipage}
        """)
        output("\n")

        if not answer_key.get(count):
            answer_key[count] = "?"
        count +=1


    output(r"""
    \end{questions}
    \end{document}
    """)

print(f"Latex file created: {latex_dir}\{wname}.tex" )

key_dir = os.path.dirname(filename) + f"\{wname}_converted"

with open(f"{key_dir}\key.txt","w") as f:
    num = 1
    ans = answer_key.get(num)
    while ans:
        f.write(str(num) + str(ans) + "\n")
        num += 1
        ans = answer_key.get(num)

print(f"Answer key created: {key_dir}\key.txt")