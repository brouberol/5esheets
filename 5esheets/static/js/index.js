const caracs = ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Charisma', 'Intelligence'];
const skillsByCarac = {
    'Strength': ['Athletics'],
    'Dexterity': ['Acrobatics', 'Sleight of Hand', 'Stealth'],
    'Constitution': [],
    'Wisdom': ['Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival'],
    'Charisma': ['Deception', 'Intimidation', 'Performance', 'Persuasion'],
    'Intelligence': ['Arcana', 'History', 'Nature', 'Investigation', 'Religion']
}

const scoreModifier = (score) => {
    switch (score) {
        case 0:
        case 1:
            return -5
        case 2:
        case 1:
            return -4
        case 4:
        case 5:
            return -3;
        case 6:
        case 7:
            return -2;
        case 8:
        case 9:
            return -1;
        case 10:
        case 11:
            return 0;
        case 12:
        case 13:
            return 1;
        case 14:
        case 15:
            return 2;
        case 16:
        case 17:
            return 3;
        case 18:
        case 19:
            return 4;
        case 20:
        case 21:
            return 5
        case 22:
        case 23:
            return 6;
        case 24:
        case 25:
            return 7;
        default:
            return 0;
    }
}

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
}

const formatBonus = (bonus) => {
    if (bonus < 0) {
        return String(bonus);
    } else {
        return `+${bonus}`;
    }
}

const updateCaracSavingThrowModifier = (carac) => {
    let caracModifier = parseInt(document.getElementsByName(`${carac}mod`)[0].value);
    let savingThrowModifierInput = document.getElementsByName(`${carac}-save`)[0]
    let savingThrowProficiencyCheckbox = document.getElementsByName(`${carac}-save-prof`)[0];
    if (savingThrowProficiencyCheckbox.checked) {
        var proficiencyBonus = parseInt(document.getElementsByName("proficiencybonus")[0].value);
        var savingThrowBonus = caracModifier + proficiencyBonus;
    } else {
        var savingThrowBonus = caracModifier;
    }
    savingThrowModifierInput.value = formatBonus(savingThrowBonus);
}

const updateSkillModifier = (carac, skill) => {
    let skillDashed = skill.replace(/ /g, '-')
    let caracModifier = parseInt(document.getElementsByName(`${carac}mod`)[0].value);
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
}

const updateCaracScoreAndDependents = (carac) => {
    let caracScoreItem = document.getElementsByName(`${carac}score`)[0];
    let score = parseInt(caracScoreItem.value);
    let modifier = formatBonus(scoreModifier(score));
    document.getElementsByName(`${carac}mod`)[0].value = modifier;
    updateCaracSavingThrowModifier(carac);
    skillsByCarac[carac].forEach((skill) => {
        updateSkillModifier(carac, skill);
    })
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
})

document.getElementsByName("classlevel")[0].addEventListener("change", () => {
    let tokens = document.getElementsByName("classlevel")[0].value.split(" ");
    let level = parseInt(tokens[tokens.length - 1]);
    let bonus = formatBonus(proficiencyBonus(level));
    let proficiencyBonusInput = document.getElementsByName("proficiencybonus")[0];
    proficiencyBonusInput.value = bonus;
    proficiencyBonusInput.dispatchEvent(new Event('change'));
})

document.getElementsByName('proficiencybonus')[0].addEventListener('change', () => {
    console.log("COUCOU");
    caracs.forEach((carac) => {
        updateCaracSavingThrowModifier(carac);
        skillsByCarac[carac].forEach((skill) => {
            updateSkillModifier(carac, skill);
        })
    })
});
