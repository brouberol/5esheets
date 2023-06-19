spell_count = {
    0: 8,
    1: 13,
    2: 13,
    3: 13,
    4: 12,
    5: 9,
    6: 9,
    7: 8,
    8: 7,
    9: 7,
}
columns = {1: [0, 1, 2], 2: [3, 4, 5], 3: [6, 7, 8, 9]}

for column, spell_levels in columns.items():
    print('<section class="spell-list-column">')
    print(f'<div id="col{column}" class="spell-list-column">')
    for spell_level in spell_levels:
        if spell_level == 0:
            print(
                f"""<div id="cantrips">
            <div class="spells-header">
            <div class="spells-level">{spell_level}</div>
            <div class="spells-slots-container"></div>
          </div>
        """
            )
        else:
            print(
                f"""<div id="spells-lvl{spell_level}" class="spell-list-for-lvl">
            <div class="spells-header">
                <div class="spells-level">{spell_level}</div>
                <div class="spells-slots-container">
                    <div class="spells-slots-available">
                        <input name="spells-slots-available-lvl{spell_level}" type="text" value="{{{{ character.data['spells-slots-available-lvl{spell_level}'] }}}}" />
                    </div>
                    <div class="spells-slots-total">
                        <input name="spells-slots-total-lvl{spell_level}" type="text" value="{{{{ character.data['spells-slots-total-lvl{spell_level}'] }}}}" />
                    </div>
                </div>
            </div>
        """
            )

        if spell_level == 0:
            print(
                """<div class="spell-list cantrips">
                <ul>"""
            )
        else:
            print(
                """<div class="spell-list">
                <ul>"""
            )
        for i in range(1, spell_count[spell_level] + 1):
            spell_id = f"spells-lvl{spell_level}-{i}"
            print("<li>")
            if spell_level != 0:
                print(
                    f"""
                      <input class="bubble" name="{spell_id}-prepped" type="checkbox" {{% if character.data['{spell_id}-prepped'] %}}checked{{% endif %}} />"""
                )
            print(
                f"""<input id="{spell_id}-raw" class="hidden spell" type="text" name="{spell_id}" value="{{{{ character.data['{spell_id}'] }}}}" onfocusout="hideRawTextareaShowRenderedDiv('{spell_id}')"><div id="{spell_id}-rendered" onclick="showRawTextareHideRenderedDiv('{spell_id}')"></div></li>"""
            )
        print(
            """</ul>
        </div>
        </div>
        """
        )
    print("</div>")
    print("</section>")
