import { createComputed, createRoot, getOwner, createEffect } from "solid-js";
import { createStore, reconcile } from "solid-js/store";
import { CharacterSchema } from "~/5esheets-client";
import { ActionType } from "~/5esheets-client";
import { Proficiency } from "~/5esheets-client";
import { SpellOrigin } from "~/5esheets-client";

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
    scores: {
      strength: 8,
      dexterity: 14,
      constitution: 12,
      intelligence: 18,
      wisdom: 12,
      charisma: 14,
    },
    proficiencies: {
      saves: {
        strength: Proficiency._0,
        dexterity: Proficiency._0,
        constitution: Proficiency._1,
        intelligence: Proficiency._1,
        wisdom: Proficiency._0,
        charisma: Proficiency._0,
      },
      skills: {
        acrobatics: Proficiency._0,
        arcana: Proficiency._0,
        athletics: Proficiency._0,
        stealth: Proficiency._0,
        animal_handling: Proficiency._0,
        sleight_of_hand: Proficiency._0,
        history: Proficiency._1,
        intimidation: Proficiency._0,
        investigation: Proficiency._0,
        medicine: Proficiency._0,
        nature: Proficiency._0,
        perception: Proficiency._1,
        insight: Proficiency._1,
        persuasion: Proficiency._1,
        religion: Proficiency._0,
        performance: Proficiency._0,
        survival: Proficiency._0,
        deception: Proficiency._0,
      },
    },
    xp: 0,
    background: "Artistan",
    race: "Gnome",
    alignment: "Chaotique Bon",
    darkvision: true,
    inspiration: true,
    languages_and_proficiencies:
      "**Outils**\r\n- menuisier\r\n- souffleur de verre\r\n- bricolage\r\n- voleur\r\n- forgeron\r\n\r\n**Langues**\r\n- Nain\r\n- Gnome\r\n- Commun\r\n\r\n**Armes**\r\n- légères",
    speed: 25,
    hp: {
      max: 33,
      temp: 0,
      current: 33,
    },
    hit_dice: {
      type: "1d8",
      total: 4,
      remaining: 4,
    },
    custom_resources: [
      {
        header: "Infusions",
        remaining: 3,
        available: 3,
      },
      {
        header: "Canon",
        remaining: 3,
        available: 3,
      },
      {
        header: "Baguette des secrets",
        remaining: 3,
        available: 3,
      },
    ],
    attacks: [
      {
        name: "Arbalète légère",
        damage: "1d8+2",
        bonus: 4,
        damage_type: "piercing",
      },
      {
        name: "Hache à une main",
        damage: "1d6+2",
        bonus: 4,
        damage_type: "slashing",
      },
    ],
    equipment:
      "- Armure de cuir clouté\r\n- [Baguette des secrets](https://roll20.net/compendium/dnd5e/Wand%20of%20Secrets#content) \r\n- Focalisateur arcanique\r\n- Livre traitant de la fabrication d'homoncules en bois\r\n- Carnets de notes de Siméon\r\n",
    money: {
      copper: 0,
      silver: 0,
      electrum: 0,
      gold: 1,
      platinum: 0,
    },
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
    spells: {
      daily_prepared: 6,
      spellcasting_ability: "intelligence",
      cantrips: [
        {
          name: "Mending",
          prepared: true,
          description: "[Mending](https://5e.tools/spells.html#mending_phb)",
          verbal: true,
          somatic: true,
          material: true,
        },
        {
          name: "Fire bolt",
          prepared: true,
          description:
            "[Fire Bolt](https://5e.tools/spells.html#fire%20bolt_phb)  (@cantrip_die@d10 🔥)",
          verbal: true,
          somatic: true,
          invocation: ActionType.ACTION,
        },
      ],
      lvl1: [
        {
          name: "Thunderwave",
          prepared: true,
          description:
            "[Thunderwave](https://5e.tools/spells.html#thunderwave_phb): CON 💾 | 2d8 ⛈️",
          verbal: true,
          somatic: true,
          invocation: ActionType.ACTION,
          origin: SpellOrigin.CLASS
        },
        {
          name: "Shield",
          prepared: true,
          description:
            "[Shield](https://5e.tools/spells.html#shield_phb) + 5AC",
          verbal: true,
          somatic: true,
          invocation: ActionType.REACTION,
        },
        {
          name: "Caustic Brew",
          prepared: true,
          description:
            "[Caustic Brew](https://5e.tools/spells.html#tasha's%20caustic%20brew_tce) DEX 💾 |2d4🧪",
          verbal: true,
          somatic: true,
          material: true,
          invocation: ActionType.ACTION,
          concentration: true,
        },
        {
          name: "Catapult",
          prepared: true,
          description:
            "[Catapult](https://5e.tools/spells.html#catapult_xge) DEX 💾 | 3d8 🔨",
          invocation: ActionType.ACTION,
          somatic: true,
        },
        {
          name: "Detect Magic",
          prepared: true,
          description:
            "[Detect Magic](https://5e.tools/spells.html#detect%20magic_phb)",
          ritual: true,
          verbal: true,
          somatic: true,
        },
        {
          name: "Absorb Elements",
          prepared: true,
          description:
            "[Absorb Elements](https://5e.tools/spells.html#absorb%20elements_xge)",
          somatic: true,
          invocation: ActionType.REACTION,
        },
        {
          name: "False Life",
          prepared: true,
          description:
            "[False Life](https://5e.tools/spells.html#false%20life_phb) 1d4+4 + 5*spell_lvl ❣️",
          verbal: true,
          somatic: true,
          material: true,
          invocation: ActionType.ACTION,
        },
        {
          name: "Sanctuary",
          prepared: true,
          description:
            "[Sanctuary](https://5e.tools/spells.html#sanctuary_phb)",
          verbal: true,
          somatic: true,
          material: true,
          invocation: ActionType.BONUS_ACTION,
        },
      ],
    },
  },
  party: {
    id: 1,
    name: "Famille McTrickfoot"
  },
  player: {
    id: 1,
    name: "Balthazar"
  },
  equipment: [
    {
      item: {
        name: "Longsword",
        data: {
          meta: {
            translations: {
              fr: {
                name: "Épée longue",
                description: "L'épée longue est une arme très polyvalente qui peut également être maniée à deux mains pour des coups plus punitifs."
              }
            },
            rarity: "none",
            weight: 3,
            value: 1500
          },
          attributes: {
            weapon_category: "martial",
            weapon_type: "sword"
          },
          damage: {
            damage_1: "1d8",
            damage_type: "S",
            damage_2: "1d10"
          },
          source: {
            book: "PHB",
            page: 149
          },
          srd: true,
          subtype: "M",
          property: [
            "V"
          ],
          type: "weapon"
        }
      },
      amount: 1,
      equipped: false
    }
  ]
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
      `scores.${attribute}_mod`,
      (character: CharacterSchema) =>
        scoreToSkillModifier(character.data.scores[attribute]),
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
      `scores.${attribute}_save_mod`,
      (character: CharacterSchema) =>
        scoreToProficiencyModifier(
          character.data.scores[attribute],
          character.data.proficiencies.saves[attribute],
          character.data.proficiency_bonus
        ),
    ])
  ),

  // Recompute the passive perception score when the character's wisdom changes
  passive_perception: (character: CharacterSchema) => {
    return (
      10 +
      scoreToProficiencyModifier(
        character.data.scores.wisdom,
        character.data.proficiencies.skills.perception,
        character.data.proficiency_bonus
      )
    );
  },

  // Recompute the initiative bonus when the character's dexterity changes
  initiative: (character: CharacterSchema) => {
    return scoreToSkillModifier(character.data.scores.dexterity);
  },

  // Recompute the spell DC when the spellcasting ability or its associated modifier change, as well as the proficiency bonus
  spell_dc: (character: CharacterSchema) => {
    return (
      8 +
      scoreToSkillModifier(
        character.data.scores[character.data.spells.spellcasting_ability]
      ) +
      character.data.proficiency_bonus
    );
  },

  spell_attack_bonus: (character: CharacterSchema) => {
    return (
      scoreToSkillModifier(
        character.data.scores[character.data.spells.spellcasting_ability]
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
          character.data.scores[secondary],
          character.data.proficiencies.skills[attribute],
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
      ...derivedAttribute.split("."),
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
              scores: {
                ...characters[characterSlug].data.scores,
                ...update.data?.scores,
              },
              hp: {
                ...characters[characterSlug].data.hp,
                ...update.data?.hp,
              },
              hit_dice: {
                ...characters[characterSlug].data.hit_dice,
                ...update.data?.hit_dice,
              },
              money: {
                ...characters[characterSlug].data.money,
                ...update.data?.money,
              },
              spells: {
                ...characters[characterSlug].data.spells,
                ...update.data?.spells,
              },
              proficiencies: {
                ...characters[characterSlug].data.proficiencies,
                ...update.data?.proficiencies,
                skills: {
                  ...characters[characterSlug].data.proficiencies.skills,
                  ...update.data?.proficiencies?.skills,
                },
                saves: {
                  ...characters[characterSlug].data.proficiencies.saves,
                  ...update.data?.proficiencies?.saves,
                }
              },
            },
          })
        );
      },
    },
  ] as const;
}
