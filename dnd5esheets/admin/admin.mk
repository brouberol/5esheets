.PHONY=admin

statics/pygments.css:
	@poetry run pygmentize -S friendly -f html -a .highlight -o statics/pygments.css > /dev/null

admin-statics: statics/pygments.css
