const caracs = [
  "Strength",
  "Dexterity",
  "Constitution",
  "Wisdom",
  "Charisma",
  "Intelligence",
];
const skillsByCarac = {
  Strength: ["Athletics"],
  Dexterity: ["Acrobatics", "Sleight of Hand", "Stealth"],
  Constitution: [],
  Wisdom: ["Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
  Charisma: ["Deception", "Intimidation", "Performance", "Persuasion"],
  Intelligence: ["Arcana", "History", "Nature", "Investigation", "Religion"],
};
const modToCarac = {
  int_mod: "Intelligence",
  wis_mod: "Wisdom",
  str_mod: "Strength",
  dex_mod: "Dexterity",
  cha_mod: "Charisma",
  con_mod: "Constitution",
};
const hiddenClass = "hidden";
const markdownTextareaClasses = ["features", "equipment", "otherprofs"];

const markdownRenderer = new marked.Renderer();
const linkRenderer = markdownRenderer.link;
marked.setOptions({
  mangle: false,
  headerIds: false,
});

// always render links so they open in a new tab
markdownRenderer.link = (href, title, text) => {
  const html = linkRenderer.call(markdownRenderer, href, title, text);
  return html.replace(/^<a /, '<a target="_blank" ');
};

// DOMPurify sees target blank lnks as a security issue, so massage it
// into accepting then.
// Source: https://github.com/cure53/DOMPurify/issues/317#issuecomment-698800327
DOMPurify.addHook("afterSanitizeAttributes", function (node) {
  // set all elements owning target to target=_blank
  if ("target" in node) {
    node.setAttribute("target", "_blank");
    node.setAttribute("rel", "noopener");
  }
});

const scoreModifier = (score) => {
  return Math.ceil((score - 10) / 2);
};

const proficiencyBonus = (level) => {
  if (level <= 4) {
    return 2;
  } else if (level >= 5 && level <= 8) {
    return 3;
  } else if (level >= 9 && level <= 12) {
    return 4;
  } else if (level >= 13 && level <= 16) {
    return 5;
  } else if (level >= 17 && level <= 20) {
    return 6;
  }
};

const numberOfDieForCantrip = () => {
  level = getCharacterLevel();
  if (level < 5) {
    return 1;
  } else if (level < 11) {
    return 2;
  } else if (level < 17) {
    return 3;
  } else {
    return 4;
  }
};

const formatBonus = (bonus) => {
  if (bonus < 0) {
    return String(bonus);
  } else {
    return `+${bonus}`;
  }
};

const getProficiencyBonusInput = () => {
  return document.getElementsByName("proficiencybonus")[0];
}

const getProficiencyBonus = () => {
  return parseInt(getProficiencyBonusInput().value);
};

const getCaracModifier = (carac) => {
  return parseInt(document.getElementsByName(`${carac}mod`)[0].value);
};

const updateProficiencyBonus = () => {
  level = getCharacterLevel();
  bonus = proficiencyBonus(level);
  getProficiencyBonusInput().value = formatBonus(bonus);
}

const updateCaracSavingThrowModifier = (carac) => {
  let caracModifier = getCaracModifier(carac);
  let savingThrowModifierInput = document.getElementsByName(`${carac}-save`)[0];
  let savingThrowProficiencyCheckbox = document.getElementsByName(
    `${carac}-save-prof`
  )[0];
  if (savingThrowProficiencyCheckbox.checked) {
    var proficiencyBonus = getProficiencyBonus();
    var savingThrowBonus = caracModifier + proficiencyBonus;
  } else {
    var savingThrowBonus = caracModifier;
  }
  savingThrowModifierInput.value = formatBonus(savingThrowBonus);
};

const updateSkillModifier = (carac, skill) => {
  let skillDashed = skill.replace(/ /g, "-");
  let caracModifier = getCaracModifier(carac);
  let skillModifierInput = document.getElementsByName(skill)[0];
  let skillProficiencyCheckbox = document.getElementsByName(
    `${skillDashed}-prof`
  )[0];
  if (skillProficiencyCheckbox.checked) {
    var proficiencyBonus = getProficiencyBonus();
    var skillBonus = caracModifier + proficiencyBonus;
  } else {
    var skillBonus = caracModifier;
  }
  skillModifierInput.value = formatBonus(skillBonus);

  if (skill === "Perception") {
    let passivePerceptionInput =
      document.getElementsByName("passiveperception")[0];
    passivePerceptionInput.value = 10 + skillBonus;
  }
};

const updateCaracScoreAndDependents = (carac) => {
  let caracScoreItem = document.getElementsByName(`${carac}score`)[0];
  let score = parseInt(caracScoreItem.value);
  let modifier = formatBonus(scoreModifier(score));
  document.getElementsByName(`${carac}mod`)[0].value = modifier;
  updateCaracSavingThrowModifier(carac);
  skillsByCarac[carac].forEach((skill) => {
    updateSkillModifier(carac, skill);
  });
};

const updateSpellAttackBonus = (spellcastingAbility) => {
  let extraSpellAttackBonus = parseInt(
    document.getElementById("extraspellattackbonus").value || 0
  );
  let totalSpellAttackBonus =
    getCaracModifier(spellcastingAbility) +
    extraSpellAttackBonus +
    getProficiencyBonus();
  document.getElementById("totalspellattackbonus").value = formatBonus(
    totalSpellAttackBonus
  );
};

const updateRemainingDailyPreparedSpells = () => {
  let totalDailyPeparedSpellsInput = parseInt(
    document.getElementById("totaldailypreparedspells").value || 0
  );
  let remainingDailyPeparedSpellsInput = document.getElementById(
    "remainingdailyspells"
  );
  let currentlyPreparedSpells = document.querySelectorAll(
    "div#spells input.bubble[type=checkbox]:checked"
  ).length;
  remainingDailyPeparedSpellsInput.value =
    totalDailyPeparedSpellsInput - currentlyPreparedSpells;
};

const generateCaracMacroRegex = (searchTerm) => {
  return new RegExp(`${searchTerm}`, "g");
};

const replaceCaracModMacroByValue = (text) => {
  for (const [mod_str, carac] of Object.entries(modToCarac)) {
    let searchTerm = `@${mod_str}`;
    let replacement = formatBonus(getCaracModifier(carac));
    if (text.includes(searchTerm)) {
      let re = generateCaracMacroRegex(searchTerm);
      text = text.replace(re, replacement);
    }
  }
  return text;
};

const replaceCantripNumberOfDieMacroByValue = (text) => {
  return text.replace("@cantrip_die@", numberOfDieForCantrip());
};

const sortChildrenByText = (parent) => {
  [...parent.children]
    .sort((a, b) => (a.innerText > b.innerText ? 1 : -1))
    .forEach((node) => parent.appendChild(node));
};

const sortSkillsElements = () => {
  // todo: fix class into id
  let skillList = document.querySelectorAll(".skills > ul")[0];
  sortChildrenByText(skillList);
};

const hideRawTextareaShowRenderedDiv = (id) => {
  textarea = document.getElementById(`${id}-raw`);
  neighbourDiv = document.getElementById(`${id}-rendered`);
  if (textarea.value) {
    textarea.textContent = textarea.value;

    // todo: extract into some less ad-hoc macro processor logic
    textContentWithRenderedMacros = replaceCaracModMacroByValue(
      textarea.textContent
    );
    textContentWithRenderedMacros = replaceCantripNumberOfDieMacroByValue(
      textContentWithRenderedMacros
    );
    // end todo

    rendered = marked.parse(textContentWithRenderedMacros, {
      renderer: markdownRenderer,
    });
    neighbourDiv.innerHTML = DOMPurify.sanitize(rendered);
    textarea.classList.add(hiddenClass);
    neighbourDiv.classList.remove(hiddenClass);
  } else {
    // The textarea does not contain any text, so hiding it would prevent us from
    // writing in it in the first place.
    textarea.classList.remove(hiddenClass);
    neighbourDiv.classList.add(hiddenClass);
  }
};

const showRawTextareHideRenderedDiv = (id) => {
  textarea = document.getElementById(`${id}-raw`);
  neighbourDiv = document.getElementById(`${id}-rendered`);
  textarea.classList.remove(hiddenClass);
  textarea.focus({ preventScroll: true });
  neighbourDiv.classList.add(hiddenClass);
};

const getCharacterLevel = () => {
  let tokens = document.getElementsByName("classlevel")[0].value.split(" ");
  return parseInt(tokens[tokens.length - 1]);
};

// Recompute the modifier for each skill and saving throw when the base scores change
caracs.forEach((carac) => {
  let caracScoreItem = document.getElementsByName(`${carac}score`)[0];
  caracScoreItem.addEventListener("change", () => {
    updateCaracScoreAndDependents(carac);
  });

  let caracSavingThrowProficiencyCheckbox = document.getElementsByName(
    `${carac}-save-prof`
  )[0];
  caracSavingThrowProficiencyCheckbox.addEventListener("change", () => {
    updateCaracSavingThrowModifier(carac);
  });

  skillsByCarac[carac].forEach((skill) => {
    let skillDashed = skill.replace(/ /g, "-");
    let skillProficiencyCheckbox = document.getElementsByName(
      `${skillDashed}-prof`
    )[0];
    skillProficiencyCheckbox.addEventListener("change", () => {
      updateSkillModifier(carac, skill);
    });
  });
});

// Recompute the proficiency bonus when the level changes
document.getElementsByName("classlevel")[0].addEventListener("change", () => {
  let level = getCharacterLevel();
  let bonus = formatBonus(proficiencyBonus(level));
  let proficiencyBonusInput = getProficiencyBonusInput();
  proficiencyBonusInput.value = bonus;
  proficiencyBonusInput.dispatchEvent(new Event("change"));
});

// Recompute all saving throw modifers as well as skill modifiers when the
// proficiency bonus changes
document
  .getElementsByName("proficiencybonus")[0]
  .addEventListener("change", () => {
    caracs.forEach((carac) => {
      updateCaracSavingThrowModifier(carac);
      skillsByCarac[carac].forEach((skill) => {
        updateSkillModifier(carac, skill);
      });
    });
  });

// Recompute the spell DC and the spell attack bonus when the spellcasting
// ability changes
document
  .getElementById("spellcastingability-select")
  .addEventListener("change", () => {
    let spellcastingAbility = document.getElementById(
      "spellcastingability-select"
    ).value;
    let spellDc =
      8 + getProficiencyBonus() + getCaracModifier(spellcastingAbility);
    document.getElementById("spelldc").value = spellDc;

    updateSpellAttackBonus(spellcastingAbility);
  });

// When the extra spell attack bonus (ex: provided by a magic object) value changes,
// recompute the total spell attack bonus
document
  .getElementById("extraspellattackbonus")
  .addEventListener("change", () => {
    let spellcastingAbility = document.getElementById(
      "spellcastingability-select"
    ).value;
    let extraSpellAttackBonus = parseInt(
      document.getElementById("extraspellattackbonus").value || 0
    );
    let totalSpellAttackBonus =
      getCaracModifier(spellcastingAbility) +
      extraSpellAttackBonus +
      getProficiencyBonus();
    document.getElementById("totalspellattackbonus").value = formatBonus(
      totalSpellAttackBonus
    );
  });

// Update the number of remaining spells to prepare when the state of a
// spell "prepared" checkbox changes
document
  .querySelectorAll("div#spells input.bubble[type=checkbox]")
  .forEach((node) => {
    node.addEventListener("change", () => {
      updateRemainingDailyPreparedSpells();
    });
  });

document.onreadystatechange = () => {
  if (document.readyState == "complete") {
    // Update the number of remaining spells to prepare depending on the state of the checkboxes
    updateRemainingDailyPreparedSpells();

    // Sort the skill according to their translated names
    sortSkillsElements();

    // Update the proficiency bonus according to the level
    updateProficiencyBonus();

    // Allow each textarea to be clicked on to change its markdown content, and rendered when unfocused
    markdownTextareaClasses.forEach((id) => {
      var _id = id;
      hideRawTextareaShowRenderedDiv(_id);
    });

    // Allow each spell to be clicked on to change its markdown content, and rendered when unfocused
    document
      .querySelectorAll(".spell-list input[type=text]")
      .forEach((node) => {
        var id = node.attributes.name.nodeValue;
        hideRawTextareaShowRenderedDiv(id);
      });
  }
};
