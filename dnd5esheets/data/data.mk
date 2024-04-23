5etools-data-dir = https://raw.githubusercontent.com/5etools-mirror-1/5etools-mirror-1.github.io/master/data
fr-translations-data-dir = https://gitlab.com/baktov.sugar/foundryvtt-dnd5e-lang-fr-fr/-/raw/master/dnd5e_fr-FR/compendium

$(app-root)/data/items-base.json: $(app-root)/data/translations-items-fr.json
	@echo "\n[+] Fetching base equipment data"
	@curl -s $(5etools-data-dir)/items-base.json | $(python) scripts/preprocess_base_item_json.py

$(app-root)/data/spells.json: $(app-root)/data/translations-spells-fr.json $(app-root)/data/spells-phb.json $(app-root)/data/spells-xge.json $(app-root)/data/spells-tce.json $(app-root)/data/spells-ftd.json
	@$(python) scripts/preprocess_spells_json.py

$(app-root)/data/spells-tce.json:
	@echo "\n[+] Fetching TCE spells"
	@curl -s $(5etools-data-dir)/spells/spells-tce.json > $(app-root)/data/spells-tce.json

$(app-root)/data/spells-xge.json:
	@echo "\n[+] Fetching XGE spells"
	@curl -s $(5etools-data-dir)/spells/spells-xge.json > $(app-root)/data/spells-xge.json

$(app-root)/data/spells-phb.json:
	@echo "\n[+] Fetching PHB spells"
	@curl -s $(5etools-data-dir)/spells/spells-phb.json > $(app-root)/data/spells-phb.json

$(app-root)/data/spells-ftd.json:
	@echo "\n[+] Fetching FTD spells"
	@curl -s $(5etools-data-dir)/spells/spells-ftd.json > $(app-root)/data/spells-ftd.json

$(app-root)/data/translations-spells-fr.json:
	@echo "\n[+] Fetching PHB spells french translations"
	@curl -s $(fr-translations-data-dir)/dnd5e.spells.json > $(app-root)/data/translations-spells-fr.json

$(app-root)/data/translations-items-fr.json:
	@echo "\n[+] Fetching items french translations"
	@curl -s $(fr-translations-data-dir)/dnd5e.items.json > $(app-root)/data/translations-items-fr.json
