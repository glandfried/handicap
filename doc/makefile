all: submodules talk clean

talk:
	pdflatex talk.tex

submodules: aux/tex/.git aux/images/.git 

auxiliar/tex/.git:
	git submodule update --init auxiliar/tex/

auxiliar/images/.git:
	git submodule update --init auxiliar/images/

clean:
	- rm -f *.log
	- rm -f *.soc
	- rm -f *.toc
	- rm -f *.aux
	- rm -f *.out
	- rm -f main.idx
	- rm -f *.bbl
	- rm -f *.bbg
	- rm -f *.dvi
	- rm -f *.blg
	- rm -f *.lof
	- rm -f *.nav
	- rm -f *.snm
	- rm -f *~

