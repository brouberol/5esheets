.PHONY=admin

$(app-root)/admin/statics/pygments.css:
	@poetry run pygmentize -S lightbulb -f html -a .highlight > $(app-root)/admin/statics/pygments.css

admin-statics: $(app-root)/admin/statics/pygments.css
