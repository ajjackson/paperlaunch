filename=paper
si=si

all: pdf si

pdf:
	pdflatex ${filename}
	bibtex ${filename}
	pdflatex ${filename}
	pdflatex ${filename}

si:
	pdflatex ${si}
	pdflatex ${si}

clean:
	rm -f ${filename}.{ps,pdf,log,aux,out,dvi,bbl,blg}
	rm -f ${si}.{ps,pdf,log,aux,out,dvi,bbl,blg}
