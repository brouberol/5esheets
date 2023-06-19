const caracs = ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Charisma', 'Intelligence'];
const skillsByCarac = {
  'Strength': ['Athletics'],
  'Dexterity': ['Acrobatics', 'Sleight of Hand', 'Stealth'],
  'Constitution': [],
  'Wisdom': ['Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival'],
  'Charisma': ['Deception', 'Intimidation', 'Performance', 'Persuasion'],
  'Intelligence': ['Arcana', 'History', 'Nature', 'Investigation', 'Religion']
};
const modToCarac = {
  'int_mod': 'Intelligence',
  'wis_mod': 'Wisdom',
  'str_mod': 'Strength',
  'dex_mod': 'Dexterity',
  'cha_mod': 'Charisma',
  'con_mod': 'Constitution',
};

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

const formatBonus = (bonus) => {
  if (bonus < 0) {
    return String(bonus);
  } else {
    return `+${bonus}`;
  }
};

const getProficiencyBonus = () => {
  return parseInt(document.getElementsByName("proficiencybonus")[0].value);
};

const getCaracModifier = (carac) => {
  return parseInt(document.getElementsByName(`${carac}mod`)[0].value);
};

const updateCaracSavingThrowModifier = (carac) => {
  let caracModifier = getCaracModifier(carac);
  let savingThrowModifierInput = document.getElementsByName(`${carac}-save`)[0]
  let savingThrowProficiencyCheckbox = document.getElementsByName(`${carac}-save-prof`)[0];
  if (savingThrowProficiencyCheckbox.checked) {
    var proficiencyBonus = getProficiencyBonus()
    var savingThrowBonus = caracModifier + proficiencyBonus;
  } else {
    var savingThrowBonus = caracModifier;
  }
  savingThrowModifierInput.value = formatBonus(savingThrowBonus);
};

const updateSkillModifier = (carac, skill) => {
  let skillDashed = skill.replace(/ /g, '-')
  let caracModifier = getCaracModifier(carac);
  let skillModifierInput = document.getElementsByName(skill)[0]
  let skillProficiencyCheckbox = document.getElementsByName(`${skillDashed}-prof`)[0];
  if (skillProficiencyCheckbox.checked) {
    var proficiencyBonus = parseInt(document.getElementsByName("proficiencybonus")[0].value);
    var skillBonus = caracModifier + proficiencyBonus;
  } else {
    var skillBonus = caracModifier;
  }
  skillModifierInput.value = formatBonus(skillBonus);

  if (skill === "Perception") {
    let passivePerceptionInput = document.getElementsByName("passiveperception")[0];
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
  })
};

const updateSpellAttackBonus = (spellcastingAbility) => {
  let extraSpellAttackBonus = parseInt(document.getElementById("extraspellattackbonus").value || 0);
  let totalSpellAttackBonus = getCaracModifier(spellcastingAbility) + extraSpellAttackBonus + getProficiencyBonus();
  document.getElementById("totalspellattackbonus").value = formatBonus(totalSpellAttackBonus);
};

const updateRemainingDailyPreparedSpells = () => {
  let totalDailyPeparedSpellsInput = parseInt(document.getElementById("totaldailypreparedspells").value || 0);
  let remainingDailyPeparedSpellsInput = document.getElementById("remainingdailyspells");
  let currentlyPreparedSpells = document.querySelectorAll("div#spells input.bubble[type=checkbox]:checked").length;
  remainingDailyPeparedSpellsInput.value = totalDailyPeparedSpellsInput - currentlyPreparedSpells;
};

const generateCaracMacroRegex = (searchTerm) => {
  return new RegExp(`${searchTerm}`, 'g')
}

const replaceCaracModMacroByValue = (text) => {
  for (const [mod_str, carac] of Object.entries(modToCarac)) {
    let searchTerm = `@${mod_str}`
    let replacement = formatBonus(getCaracModifier(carac));
    if (text.includes(searchTerm)) {
      let re = generateCaracMacroRegex(searchTerm);
      text = text.replace(re, replacement);
    }
  }
  return text;
};

const sortChildrenByText = (parent) => {
  [...parent.children].sort((a,b)=>a.innerText>b.innerText?1:-1).forEach(node=>parent.appendChild(node));
}

const sortSkillsElements = () => {
  // todo: fix class into id
  let skillList = document.querySelectorAll(".skills > ul")[0];
  sortChildrenByText(skillList);
}


const hideRawTextareaShowRenderedDiv = (id) => {
  textarea = document.getElementById(`${id}-raw`);
  neighbourDiv = document.getElementById(`${id}-rendered`);
  if (textarea.textContent) {
    textarea.textContent = textarea.value;
    textContentWithRenderedMacros = replaceCaracModMacroByValue(textarea.textContent)
    rendered = marked.parse(textContentWithRenderedMacros, {mangle: false, headerIds: false});
    neighbourDiv.innerHTML = DOMPurify.sanitize(rendered);
    textarea.classList.add('hidden');
    neighbourDiv.classList.remove('hidden');
  } else {
    // The textarea does not contain any text, so hiding it would prevent us from
    // writing in it in the first place.
    textarea.classList.remove('hidden');
    neighbourDiv.classList.add('hidden');
  }
}

const showRawTextareHideRenderedDiv = (id) => {
  textarea = document.getElementById(`${id}-raw`);
  neighbourDiv = document.getElementById(`${id}-rendered`);
  textarea.classList.remove("hidden");
  textarea.focus({preventScroll: true});
  neighbourDiv.classList.add("hidden");
}

caracs.forEach((carac) => {
  let caracScoreItem = document.getElementsByName(`${carac}score`)[0];
  caracScoreItem.addEventListener('change', () => {
    updateCaracScoreAndDependents(carac);
  })

  let caracSavingThrowProficiencyCheckbox = document.getElementsByName(`${carac}-save-prof`)[0];
  caracSavingThrowProficiencyCheckbox.addEventListener('change', () => {
    updateCaracSavingThrowModifier(carac);
  });

  skillsByCarac[carac].forEach((skill) => {
    let skillDashed = skill.replace(/ /g, '-')
    let skillProficiencyCheckbox = document.getElementsByName(`${skillDashed}-prof`)[0];
    skillProficiencyCheckbox.addEventListener('change', () => {
      updateSkillModifier(carac, skill)
    })
  })
});


document.getElementsByName("classlevel")[0].addEventListener("change", () => {
  let tokens = document.getElementsByName("classlevel")[0].value.split(" ");
  let level = parseInt(tokens[tokens.length - 1]);
  let bonus = formatBonus(proficiencyBonus(level));
  let proficiencyBonusInput = document.getElementsByName("proficiencybonus")[0];
  proficiencyBonusInput.value = bonus;
  proficiencyBonusInput.dispatchEvent(new Event('change'));
});

document.getElementsByName('proficiencybonus')[0].addEventListener('change', () => {
  caracs.forEach((carac) => {
    updateCaracSavingThrowModifier(carac);
    skillsByCarac[carac].forEach((skill) => {
      updateSkillModifier(carac, skill);
    })
  })
});

document.getElementById("spellcastingability-select").addEventListener('change', () => {
  let spellcastingAbility = document.getElementById("spellcastingability-select").value;
  let spellDc = 8 + getProficiencyBonus() + getCaracModifier(spellcastingAbility);
  document.getElementById("spelldc").value = spellDc;

  updateSpellAttackBonus(spellcastingAbility);
});

document.getElementById("extraspellattackbonus").addEventListener('change', () => {
  let spellcastingAbility = document.getElementById("spellcastingability-select").value;
  let extraSpellAttackBonus = parseInt(document.getElementById("extraspellattackbonus").value || 0);
  let totalSpellAttackBonus = getCaracModifier(spellcastingAbility) + extraSpellAttackBonus + getProficiencyBonus();
  document.getElementById("totalspellattackbonus").value = formatBonus(totalSpellAttackBonus);
});

document.querySelectorAll('div#spells input.bubble[type=checkbox]').forEach((node) => {
  node.addEventListener("change", () => {
    updateRemainingDailyPreparedSpells();
  })
});

document.onreadystatechange = function () {
  if (document.readyState == "complete") {
    updateRemainingDailyPreparedSpells();
    sortSkillsElements();
    ['features', 'equipment', 'otherprofs'].forEach((id) => {
      hideRawTextareaShowRenderedDiv(id);
    })
  }
}
