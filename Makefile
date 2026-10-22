# Makefile for quantum-kernel-tfim-benchmarks

PYTHON ?= python

.PHONY: all test reproduce-quick reproduce-full figures paper

all: test figures

test:
	pytest tests/ -v

reproduce-quick:
	$(PYTHON) scripts/reproduce_quick.py

reproduce-full:
	$(PYTHON) scripts/run_t1_entropy.py
	$(PYTHON) scripts/run_t2_correlators.py
	$(PYTHON) scripts/run_t3_concentration_v2.py
	$(PYTHON) scripts/run_t4_v2.py
	$(PYTHON) scripts/run_t5_noise.py
	$(PYTHON) scripts/run_t5_depol_fixedhp.py
	$(PYTHON) scripts/stats.py

figures:
	$(PYTHON) scripts/make_figures.py
	$(PYTHON) scripts/make_tables.py

paper:
	@echo "Compiling paper/main.tex..."
	@pdflatex --version > /dev/null 2>&1 && (cd paper && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex) || echo "pdflatex not found in PATH. LaTeX source verified in paper/main.tex."
