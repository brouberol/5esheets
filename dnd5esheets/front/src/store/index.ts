import {
  Resource,
  createComputed,
  createResource,
  createReaction,
  createMemo,
  createEffect,
  Accessor,
} from 'solid-js'
import {
  SetStoreFunction,
  Store,
  createStore,
  produce,
  reconcile,
  unwrap,
} from 'solid-js/store'
import { createRouteData } from 'solid-start'
import { CharacterSchema, ListCharacterSchema } from '~/5esheets-client'
import { Proficiency } from '~/5esheets-client'
import { Scores } from '~/5esheets-client'
import { SaveProficiencies } from '~/5esheets-client'
import { SkillProficiencies } from '~/5esheets-client'
import { CharacterService } from '~/5esheets-client'
import { applyEffects, computeEffect, Effect } from '~/effects'
import { AssignmentOperator } from '~/effects/parser'

type Join<K, P> = K extends string | number
  ? P extends string | number
    ? `${K}${'' extends P ? '' : '.'}${P}`
    : never
  : never

type Split<S extends string, D extends string> = string extends S
  ? string[]
  : S extends ''
  ? []
  : S extends `${infer T}${D}${infer U}`
  ? [T, ...Split<U, D>]
  : [S]

type Prev = [
  never,
  0,
  1,
  2,
  3,
  4,
  5,
  6,
  7,
  8,
  9,
  10,
  11,
  12,
  13,
  14,
  15,
  16,
  17,
  18,
  19,
  20,
  ...0[],
]

type Leaves<T, D extends number = 10> = [D] extends [never]
  ? never
  : T extends object
  ? { [K in keyof T]-?: Join<K, Leaves<T[K], Prev[D]>> }[keyof T]
  : ''

export const cycleProficiency = (proficiency: number) => (proficiency + 1) % 3

const emptyCharacter: CharacterSchema = {
  id: 0,
  slug: '',
  class_: '',
  name: '',
  level: 0,
  data: {
    scores: {
      strength: 10,
      dexterity: 10,
      constitution: 10,
      wisdom: 10,
      charisma: 10,
      intelligence: 10,
    },
    proficiencies: {
      saves: {
        strength: 0,
        dexterity: 0,
        constitution: 0,
        intelligence: 0,
        charisma: 0,
        wisdom: 0,
      },
      skills: {
        acrobatics: 0,
        arcana: 0,
        athletics: 0,
        stealth: 0,
        animal_handling: 0,
        sleight_of_hand: 0,
        history: 0,
        intimidation: 0,
        investigation: 0,
        medicine: 0,
        nature: 0,
        perception: 0,
        insight: 0,
        persuasion: 0,
        religion: 0,
        performance: 0,
        survival: 0,
        deception: 0,
      },
    },
    xp: 0,
    race: '',
    background: '',
    alignment: '',
    darkvision: false,
    inspiration: false,
    speed: 0,
    hp: {
      max: 0,
      temp: 0,
      current: 0,
    },
    hit_dice: {
      type: 'd4',
      total: 1,
      remaining: 1,
    },
    money: {
      copper: 0,
      silver: 0,
      electrum: 0,
      gold: 0,
      platinum: 0,
    },
    custom_resources: [],
    attacks: [],
    equipment: '',
    languages_and_proficiencies: '',
    personality: '',
    ideals: '',
    bonds: '',
    flaws: '',
    features: '',
    spells: {
      daily_prepared: 0,
      spellcasting_ability: 'wisdom',
    },
    proficiency_bonus: 0,
    ac: 0,
    initiative: 0,
    spell_dc: 0,
    spell_attack_bonus: 0,
    passive_perception: 0,
  },
  party: { id: 0, name: '' },
  player: { id: 0, name: '' },
}

type Target = `data.scores.${Leaves<CharacterSchema['data']['scores']>}`

export class CharacterList {
  public list: Resource<ListCharacterSchema[]>
  // private mutate: (list: ListCharacterSchema[]) => ListCharacterSchema[]
  // private refetch: () =>
  //   | Promise<ListCharacterSchema[] | undefined>
  //   | ListCharacterSchema[]
  //   | undefined
  //   | null

  constructor() {
    const [list] = createResource(CharacterService.listCharacters)

    this.list = list
    // this.mutate = mutate
    // this.refetch = refetch
  }

  // addCharacter = (name: string) => {
  //   console.log('add character', name)
  //   const character = {
  //     id: 0,
  //     name,
  //     slug: name.replace(' ', '-'),
  //     class_: '',
  //     level: 0,
  //     player: {id: 0, name: ''},
  //     party: {id: 0, name: ''},
  //   }

  //   const newList = [...(this.list() ?? []), character]
  //   console.log(newList)

  //   this.mutate(newList)
  //   // await CharacterService.addCharacter(character)
  //   // if there is an error with the api call, we could refetch to make sure the local state is up-to-date with the remote.
  // }

  // removeCharacter = (slug: string) => {
  //   this.mutate((this.list() ?? []).filter(character => character.slug !== slug))
  //   // CharacterService.deleteCharacter(id)
  //   // if there is an error with the api call, we could refetch to make sure the local state is up-to-date with the remote.
  // }

  getCharacter = (
    slug: string
  ): [
    CharacterSchema,
    (updater: (character: CharacterSchema) => void) => void,
  ] => {
    // TODO we might want to use createDeepSignal to allow updating only the parts of the store that changes when re-fetching resource: https://github.com/solidjs-community/solid-primitives/tree/main/packages/resource#createdeepsignal
    const [characterResource, { mutate, refetch }] = createResource(
      slug,
      CharacterService.displayCharacter,
      { initialValue: emptyCharacter }
    )

    const [character, setCharacter] = createStore<CharacterSchema>(
      characterResource()
    )

    const abilityKeys = Object.keys(character.data.proficiencies.saves)

    const baseEffects = [
      // proficiency bonus effect
      {
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.proficiency_bonus := Math.ceil(1 + level / 4)`,
          character
        ),
      },

      // ability modifiers effects
      ...abilityKeys.map((score) => ({
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.scores.${score}_mod := Math.floor((data.scores.${score} - 10) / 2)`,
          character
        ),
      })),

      // ability saves effects
      ...abilityKeys.map((score) => ({
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.scores.${score}_save_mod := data.scores.${score}_mod + data.proficiencies.saves.${score} * data.proficiency_bonus`,
          character
        ),
      })),

      // skills effects
      ...[
        ['acrobatics', 'dexterity'],
        ['animal_handling', 'wisdom'],
        ['arcana', 'intelligence'],
        ['athletics', 'strength'],
        ['deception', 'dexterity'],
        ['history', 'intelligence'],
        ['insight', 'wisdom'],
        ['intimidation', 'charisma'],
        ['investigation', 'intelligence'],
        ['medicine', 'wisdom'],
        ['nature', 'intelligence'],
        ['perception', 'wisdom'],
        ['performance', 'charisma'],
        ['persuasion', 'charisma'],
        ['religion', 'intelligence'],
        ['sleight_of_hand', 'dexterity'],
        ['stealth', 'dexterity'],
        ['survival', 'wisdom'],
      ].map(([skill, secondary]) => ({
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.scores.${skill}_mod := data.scores.${secondary}_mod + data.proficiencies.skills.${skill} * data.proficiency_bonus`,
          character
        ),
      })),

      // initiative effect
      {
        name: 'base',
        priority: 10,
        ...computeEffect(`initiative := data.scores.dexterity_mod`, character),
      },

      // passive perception effect
      {
        name: 'base',
        priority: 10,
        ...computeEffect(
          `passive_perception := data.scores.perception_mod`,
          character
        ),
      },

      // TODO the effect language and CharacterSchema currently doesn't allow to write spell DC and attack bonus.
      // // spell DC effect
      // {
      //   name: 'base',
      //   priority: 10,
      //   ...computeEffect(`spell_dc := 8 + data.scores[data.spells.spellcasting_ability] + data.proficiency_bonus`, character)
      // },

      // // spell attack bonus effect
      // {
      //   name: 'base',
      //   priority: 10,
      //   ...computeEffect(`spell_attack_bonus := data.scores[data.spells.spellcasting_ability] + data.proficiency_bonus`, character)
      // },
    ]

    const targets = baseEffects.reduce(
      (set, effect) => set.add(effect.target),
      new Set<Target>()
    )

    // Create reactive effects to recompute target derived attributes when characteristics change
    for (const derived of targets) {
      const memo = createMemo(() => {
        const sortedEffects = [
          ...baseEffects.filter(({ target }) => target === derived),
          // TODO here goes the equipement effects
        ]
          .sort((a, b) => b.priority - a.priority)
          .map((effect) => ({ ...effect, value: createMemo(effect.value) }))

        return applyEffects<Target>(sortedEffects)
      })

      const path = derived.split('.') as Split<typeof derived, '.'>

      // TODO memo() also returns the effect history, but we need to store it somewhere else in the character,
      // to allow referencing derived attribute directly, rather than with .value at the end, e.g. data.scores.wisdom_mod.value
      createEffect(() => setCharacter(...path, memo().value))
    }

    const updateCharacter = (fn: (character: CharacterSchema) => void) =>
      setCharacter(produce(fn))

    return [character, updateCharacter]
  }
}

// export const characterList = new CharacterList()
