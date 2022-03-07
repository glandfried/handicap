all: informe.pdf clean
	
informe.pdf: informe.tex
	# pdflatex informe.tex
	# bibtex informe.aux
	pdflatex informe.tex
	pdflatex informe.tex

pdf:
	pdflatex informe.tex

clean: 
	@echo "Cleaning..."	
	- rm -f *.log
	- rm -f *.soc
	- rm -f *.toc
	- rm -f *.aux
	- rm -f *.out
	- rm -f plan.idx
	- rm -f *.bbl
	- rm -f *.bbg
	- rm -f *.dvi
	- rm -f *.blg
	- rm -f *.lof
	- rm -f *~
