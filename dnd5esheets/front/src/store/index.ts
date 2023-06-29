import { createComputed, createRoot, getOwner } from "solid-js";
import { createStore, reconcile } from "solid-js/store";
import { CharacterSchema } from "~/5esheets-client";

export const proficiencies = [0, 1, 2] as const; // none | master | expert
export type Proficiency = (typeof proficiencies)[number];

export const cycleProficiency = (proficiency: number) => (proficiency + 1) % 3;

const douglas: CharacterSchema = {
  id: 1,
  player_id: 1,
  party_id: 1,
  name: "Douglas McTrickfoot",
  slug: "douglas-mctrickfoot",
  class_: "Artilleur",
  level: 4,
  data: {
    strength: 8,
    dexterity: 14,
    constitution: 12,
    intelligence: 18,
    wisdom: 12,
    charisma: 14,

    strength_mod: 0,
    dexterity_mod: 0,
    constitution_mod: 0,
    intelligence_mod: 0,
    wisdom_mod: 0,
    charisma_mod: 0,

    proficiencies: {
      strength: 0,
      dexterity: 0,
      constitution: 1,
      intelligence: 1,
      wisdom: 0,
      charisma: 0,

      acrobatics: 0,
      arcana: 0,
      athletics: 0,
      stealth: 0,
      animal_handling: 0,
      sleight_of_hand: 0,
      history: 1,
      intimidation: 0,
      investigation: 0,
      medicine: 0,
      nature: 0,
      perception: 1,
      insight: 1,
      persuasion: 1,
      religion: 0,
      performance: 0,
      survival: 0,
      deception: 0,
    },

    experiencepoints: 0,
    background: "Artistan",
    playername: "Balthazar",
    race: "Gnome",
    alignment: "Chaotique Bon",
    darkvision: true,
    otherprofs:
      "**Outils**\r\n- menuisier\r\n- souffleur de verre\r\n- bricolage\r\n- voleur\r\n- forgeron\r\n\r\n**Langues**\r\n- Nain\r\n- Gnome\r\n- Commun\r\n\r\n**Armes**\r\n- légères",
    ac: "14",
    speed: "25",
    maxhp: "33",
    temphp: "0",
    currenthp: "33",
    totalhd: "1d8",
    remaininghd: "4",
    "custom-1-header": "Infusions",
    "custom-1-remaining": "3",
    "custom-1-available": "3",
    "custom-2-header": "Canon",
    "custom-2-remaining": "1",
    "custom-2-available": "1",
    "custom-3-header": "Bag. secrets",
    "custom-3-remaining": "3",
    "custom-3-available": "3",
    atkname1: "Arbalète légère",
    atkbonus1: "+4",
    atkdamage1: "1d8+2 perçants",
    atkname2: "Marteau léger",
    atkbonus2: "+4",
    atkdamage2: "1d4+2 contondants",
    atkname3: "Hache à une main",
    atkbonus3: "+4",
    atkdamage3: "1d6+2 tranchants",
    equipment:
      "- Armure de cuir clouté\r\n- [Baguette des secrets](https://roll20.net/compendium/dnd5e/Wand%20of%20Secrets#content) \r\n- Focalisateur arcanique\r\n- Livre traitant de la fabrication d'homoncules en bois\r\n- Carnets de notes de Siméon\r\n",
    gp: "1",
    personality:
      "Douglas est astucieux et fait preuve d'une répartie rapide. Il est fidèle envers ses amis et curieux d'apprendre des nouveaux sujets.",
    ideals:
      "Douglas rêve de maîtriser la magie à la seule force de son intellect.",
    bonds:
      "Douglas est particulièrement fidèle envers les membres de sa famille, et se sent responsable de Crounch.",
    flaws:
      "Douglas est impulsif. Son besoin de paraître intelligent cache un manque de confiance en soi. ",
    features:
      "**Bricolage**\r\n- 1h pour bricoler 1 objet\r\n- jusqu'à 3 objets \r\n  * boîte à musique\r\n  * jouet mécanique en bois\r\n  * allume feu\r\n\r\n**Bricolage magique**\r\n- sur objet minuscule\r\n- jusqu'à 3\r\n  * peut jouer un message enregistré\r\n  * peut jouer un son continu\r\n\r\n**Infusions**\r\n- 4 connues\r\n- jusqu'à 3 objets en même temps\r\n- dure 3 jours\r\n\r\n**Right tool**\r\n1h pour crafter des objets d'artisan\r\n\r\n**Canon occulte**\r\n- 1 action pour invoquer/faire disparaître\r\n- 1 action bonus pour utiliser\r\n * lance-flamme: 🔺 DEX save ? 2d8 🔥 : 1/2\r\n * baliste: 🏹 40m. 2d8 💪 + 1.5m recul\r\n * protecteur: 3m ⭕, 1d8@int_mod temp HP",
    remainingdailyspells: "0",
    dailypreparedspells: "6",
    spellcasting_ability: "intelligence",
    "spells-lvl0-1":
      "🗣️ 👋 💎 [Mending](https://5e.tools/spells.html#mending_phb)",
    "spells-lvl0-2":
      "🅰️ 🗣️ 👋 [Fire Bolt](https://5e.tools/spells.html#fire%20bolt_phb)  (@cantrip_die@d10 🔥)",
    "spells-slots-available-lvl1": "3",
    "spells-slots-total-lvl1": "3",
    "spells-lvl1-1":
      "🅰️ 🗣️ 👋 🧙 [Thunderwave](https://5e.tools/spells.html#thunderwave_phb): CON 💾 | 2d8 ⛈️",
    "spells-lvl1-2":
      "➰ 🗣️ 👋 🧙 [Shield](https://5e.tools/spells.html#shield_phb) + 5AC",
    "spells-lvl1-3-prepped": true,
    "spells-lvl1-3":
      "🅰️ 🗣️ 👋 💎 ©️ [Caustic Brew](https://5e.tools/spells.html#tasha's%20caustic%20brew_tce) DEX 💾 |2d4🧪",
    "spells-lvl1-4-prepped": true,
    "spells-lvl1-4":
      "🅰️ 👋 [Catapult](https://5e.tools/spells.html#catapult_xge) DEX 💾 | 3d8 🔨",
    "spells-lvl1-5-prepped": true,
    "spells-lvl1-5":
      "®️ 🗣️ 👋 [Detect Magic](https://5e.tools/spells.html#detect%20magic_phb)",
    "spells-lvl1-6-prepped": true,
    "spells-lvl1-6":
      "➰ 👋 [Absorb Elements](https://5e.tools/spells.html#absorb%20elements_xge)",
    "spells-lvl1-7-prepped": true,
    "spells-lvl1-7":
      "🅰️ 🗣️ 👋 💎 [False Life](https://5e.tools/spells.html#false%20life_phb) 1d4+4 + 5*spell_lvl ❣️",
    "spells-lvl1-8-prepped": true,
    "spells-lvl1-8":
      "🆎 🗣️ 👋 💎 [Sanctuary](https://5e.tools/spells.html#sanctuary_phb)",
  },
};

const scoreToSkillModifier = (score: number): number =>
  Math.floor((score - 10) / 2);

const scoreToProficiencyModifier = (
  score: number,
  proficiency: Proficiency,
  proficiencyBonus: number
): number => scoreToSkillModifier(score) + proficiency * proficiencyBonus;

const levelToProficiencyBonus = (level: number): number => {
  return Math.ceil(1 + level / 4);
};

const store = { [douglas.slug]: douglas };
const [characters, setCharacters] = createStore(store);

const effects = {
  // Recompute the characteristic modifiers when a characteristic changes
  ...Object.fromEntries(
    [
      "strength",
      "dexterity",
      "constitution",
      "intelligence",
      "wisdom",
      "charisma",
    ].map((attribute) => [
      `${attribute}_mod`,
      (character: CharacterSchema) =>
        scoreToSkillModifier(character.data[attribute]),
    ])
  ),

  // Recompute the proficiency bonus when the level changes
  proficiency_bonus: (character: CharacterSchema) =>
    levelToProficiencyBonus(character.level),

  // Recompute the saving throw modifiers when a characteristic score changes
  ...Object.fromEntries(
    [
      "strength",
      "dexterity",
      "constitution",
      "intelligence",
      "wisdom",
      "charisma",
    ].map((attribute) => [
      `${attribute}_save_mod`,
      (character: CharacterSchema) =>
        scoreToProficiencyModifier(
          character.data[attribute],
          character.data.proficiencies[attribute],
          character.data.proficiency_bonus
        ),
    ])
  ),

  // Recompute the passive perception score when the character's wisdom changes
  passive_perception: (character: CharacterSchema) => {
    return (
      10 +
      scoreToProficiencyModifier(
        character.data.wisdom,
        character.data.proficiencies.perception,
        character.data.proficiency_bonus
      )
    );
  },

  // Recompute the initiative bonus when the character's dexterity changes
  initiative: (character: CharacterSchema) => {
    return scoreToSkillModifier(character.data.dexterity);
  },

  // Recompute the spell DC when the spellcasting ability or its associated modifier change, as well as the proficiency bonus
  spell_dc: (character: CharacterSchema) => {
    return (
      8 +
      scoreToSkillModifier(
        character.data[character.data.spellcasting_ability]
      ) +
      character.data.proficiency_bonus
    );
  },

  spell_attack_bonus: (character: CharacterSchema) => {
    return (
      scoreToSkillModifier(
        character.data[character.data.spellcasting_ability]
      ) + character.data.proficiency_bonus
    );
  },

  // Recompute the skill modifiers when a characteristic changes
  ...Object.fromEntries(
    [
      ["acrobatics", "dexterity"],
      ["animal_handling", "wisdom"],
      ["arcana", "intelligence"],
      ["athletics", "strength"],
      ["deception", "dexterity"],
      ["history", "intelligence"],
      ["insight", "wisdom"],
      ["intimidation", "charisma"],
      ["investigation", "intelligence"],
      ["medicine", "wisdom"],
      ["nature", "intelligence"],
      ["perception", "wisdom"],
      ["performance", "charisma"],
      ["persuasion", "charisma"],
      ["religion", "intelligence"],
      ["sleight_of_hand", "dexterity"],
      ["stealth", "dexterity"],
      ["survival", "wisdom"],
    ].map(([attribute, secondary]) => [
      attribute,
      (character: CharacterSchema) =>
        scoreToProficiencyModifier(
          character.data[secondary],
          character.data.proficiencies[attribute],
          character.data.proficiency_bonus
        ),
    ])
  ),
};

for (const derivedAttribute in effects) {
  createComputed(() =>
    setCharacters(
      douglas.slug,
      "data",
      derivedAttribute,
      effects[derivedAttribute](characters[douglas.slug])
    )
  );
}

export default function useStore() {
  return [
    characters,
    {
      update: (characterSlug: string, update: Partial<CharacterSchema>) => {
        setCharacters(
          characterSlug,
          reconcile({
            ...characters[characterSlug],
            ...update,
            data: {
              ...characters[characterSlug].data,
              ...update.data,
              proficiencies: {
                ...characters[characterSlug].data.proficiencies,
                ...update.data?.proficiencies,
              },
            },
          })
        );
      },
    },
  ] as const;
}
