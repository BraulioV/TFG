all: doc clean

doc:
	@pdflatex -shell-escape  -output-directory ./release titulo.tex
	@bibtex ./release/titulo.aux
	@pdflatex -shell-escape  -output-directory ./release titulo.tex
	@pdflatex -shell-escape  -output-directory ./release titulo.tex
	

clean_output:
	@rm release/titulo.pdf

clean:
	@rm release/*.aux release/*.toc release/*.out release/*.log release/*.pyg
	@rm -r release/release

purge:
	@rm release/*
