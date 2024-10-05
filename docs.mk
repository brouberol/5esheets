docs/images/model_graph.png: $(app-root)/models.py
	@echo "\n[+] Generating SQL model graph"
	@$(python) scripts/generate_model_graph.py $@

docs/images/makefile.png: Makefile scripts/cleanup_makefile2dot_output.py
	@echo "\n[+] Generating a visual graph representation of the Makefile"
	@$(poetry-run) makefile2dot | $(python) scripts/cleanup_makefile2dot_output.py | dot -Tpng > $@

docs/include/make.txt: Makefile
	@make help-plain > $@
