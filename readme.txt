The critical files in this directory are:
  motola2.py
  motola.bat
  data.py
  mcexam-v2.sty

The requirments to run this script are:

(1) Python (https://www.python.org/)
(2) The Beautiful Soup python module (type "pip install bs4" after installing Python)
(3) ImageMagick (https://imagemagick.org/) 
(4) Latex (https://miktex.org/)

(When installing, choose the options to add them to your path, so that you can run "python" and "magick" from the command prompt.)

From Mobius, go the the exam you want to convert. Click the Print button. 

Mobius creates a webpage and opens a print pop-up. Close/ignore the pop-up, and then right click on the page and select "Save As...". Save it as a "Webpage complete." For example, suppose you saved it the "mobius" folder of this directory as "exam1.html". (An "exam1_files" directory will also be created). (The mobius directory is for convenience, you can save it anywhere.)

Open Windows "Command Prompt" (type cmd in the search), and navigate to the folder where the script motola.bat is located.

Type (following the example),
	
	motola mobius\exam1.html

The script will run and create a folder named  mobius\exam1_converted\. Within that folder, there will be

	-- a folder png\ with the gifs converted to png.
	-- a folder latex\ with a document exam1.tex. It will also copy the style file and run latex and produce exam1.pdf in the latex folder.
	-- an file key.txt with the answer key. (In order for this feature to work, you need to have the answers encoded in the mobius problem in a certain way.)

Note that the latex output is surpressed, so if you need to troubleshoot something, you might want to run latex manually to get the full error messages.

To set the instructors' names and the semester, edit the file data.py. It should like like, for example,

  instructors = ["instructor1 name", "instructor2 name"]
  semester = "Spring 2022"

Questions? Comments? I'm happy to help you make it work!

Drew Johnson werd2.718@gmail.com





