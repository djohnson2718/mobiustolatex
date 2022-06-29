
mkdir "%~p1%~n1_converted\png"

FOR %%i in ("%~p1%~n1_files\*.gif") DO magick "%%i" "%~p1%~n1_converted\png\%%~ni.png"

python motola2.py %1

copy mcexam-v2.sty "%~p1%~n1_converted\latex"

pdflatex -output-directory="%~p1%~n1_converted\latex" -interaction batchmode "%~p1%~n1_converted\latex\%~n1.tex"

explorer "%~p1%~n1_converted"