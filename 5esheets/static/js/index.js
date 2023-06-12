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
var caracs = ['Strength', 'Dexterity', 'Constitution', 'Wisdom', 'Charisma', 'Intelligence'];

caracs.forEach((carac) => {
    let caracScoreItem = document.getElementsByName(`${carac}score`)[0];
    console.log(caracScoreItem);
    caracScoreItem.addEventListener('change', () => {
        let score = parseInt(caracScoreItem.value);
        let modifier = scoreModifier(score);
        if (modifier > 0) {
            modifier = `+${modifier}`;
        }
        document.getElementsByName(`${carac}mod`)[0].value = modifier;
    })
})
