import { createEffect, createMemo } from 'solid-js'
import { SetStoreFunction, createStore, produce } from 'solid-js/store'

import {
  Abilities,
  CharacterSchema,
  CharacterSheet,
  OpenAPI,
  Proficiency,
} from '~/5esheets-client'
import { CharacterService } from '~/5esheets-client'
import { applyEffects, computeEffect } from '~/effects'

if (process.env.NODE_ENV === 'development') {
  OpenAPI.BASE = 'http://localhost:8000'
}

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

// Types all the possible path to access leaves of an object.
type Leaves<T, D extends number = 10> = [D] extends [never]
  ? never
  : T extends object
  ? { [K in keyof T]-?: Join<K, Leaves<T[K], Prev[D]>> }[keyof T]
  : ''

// Tentative of typing the possible target for an effect, based on the shape of Character.
type Target = Leaves<Character>

export const cycleProficiency = (proficiency: number) =>
  ((proficiency + 1) % 3) as Proficiency

// TODO fix OpenAPI typing around the definition of data:
// listCharacters return UnresolvedCharacter, without data
// getCharacter returns ResolvedCharacter, with data
// UnresolvedCharacter is a strict subset of ResolvedCharacter
export type ResolvedCharacter = Omit<CharacterSchema, 'data'> &
  Record<'data', CharacterSheet>
type UnresolvedCharacter = Omit<CharacterSchema, 'data'>
export type Character = ResolvedCharacter | UnresolvedCharacter

export const resourceState = Symbol('state')

type ResolvedResourceState = Record<typeof resourceState, 'ready'>
type UnresolvedResourceState = Record<
  typeof resourceState,
  'pending' | 'unresolved'
>
type ResourceState = ResolvedResourceState | UnresolvedResourceState

type ResolvedResourceCharacter = ResolvedCharacter & ResolvedResourceState
type UnresolvedResourceCharacter = UnresolvedCharacter & UnresolvedResourceState
export type ResourceCharacter =
  | ResolvedResourceCharacter
  | UnresolvedResourceCharacter
type ResourceCharacterStore = Record<string, ResourceCharacter> & ResourceState

export type UpdateCharacterFunction = (
  update: (character: ResolvedCharacter) => void
) => void

class CharacterStore {
  private characters: ResourceCharacterStore
  private setCharacters: SetStoreFunction<ResourceCharacterStore>

  constructor() {
    const [store, setStore] = createStore<ResourceCharacterStore>({
      [resourceState]: 'unresolved',
    })
    this.characters = store
    this.setCharacters = setStore
  }

  getCharacters = () => {
    if (this.characters[resourceState] !== 'ready') {
      void this.fetchCharacters()
    }

    return this.characters
  }

  private fetchCharacters = async () => {
    this.setCharacters(resourceState, 'pending')
    const characters = await CharacterService.listCharacters()

    for (const character of characters) {
      if (this.characters[character.slug]?.[resourceState] !== 'ready') {
        this.setCharacters(character.slug, {
          ...character,
          [resourceState]: 'unresolved',
        })
      }
    }
    this.setCharacters(resourceState, 'ready')
  }

  getCharacter = (
    slug: string
  ): [ResourceCharacter, UpdateCharacterFunction] => {
    if (this.characters[slug]?.[resourceState] !== 'ready') {
      this.fetchCharacter(slug)
    }

    return [this.characters[slug], this.updateCharacter(slug)]
  }

  private fetchCharacter = async (slug: string) => {
    this.setCharacters(slug, { [resourceState]: 'pending' })
    const character = await CharacterService.getCharacter(slug)

    this.setCharacters(
      slug,
      produce((c) => {
        Object.assign(c, character)
        c[resourceState] = 'ready'
      })
    )

    this.wireEffects(this.characters[slug] as ResolvedCharacter)
  }

  private updateCharacter =
    (slug: string) =>
    (update: (character: ResolvedResourceCharacter) => void) => {
      this.setCharacters(
        slug,
        produce((character: ResourceCharacter) => {
          character[resourceState] == 'ready'
            ? update(character)
            : throwError('Updating a pending character')
        })
      )
    }

  private wireEffects = (character: ResolvedCharacter) => {
    const abilityKeys = Object.keys(character.data.abilities) as Array<
      keyof Abilities
    >

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
      ...abilityKeys.map((ability) => ({
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.abilities.${ability}.modifier := Math.floor((data.abilities.${ability}.score - 10) / 2)`,
          character
        ),
      })),

      // ability saves effects
      ...abilityKeys.map((ability) => ({
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.abilities.${ability}.save := data.abilities.${ability}.modifier + data.abilities.${ability}.proficiency * data.proficiency_bonus`,
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
      ].map(([skill, ability]) => ({
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.skills.${skill}.modifier := data.abilities.${ability}.modifier + data.skills.${skill}.proficiency * data.proficiency_bonus`,
          character
        ),
      })),

      // initiative effect
      {
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.initiative := data.abilities.dexterity.modifier`,
          character
        ),
      },

      // passive perception effect
      {
        name: 'base',
        priority: 10,
        ...computeEffect(
          `data.passive_perception := 10 + data.skills.perception.modifier`,
          character
        ),
      },

      // spell DC effect
      {
        name: 'base',
        priority: 10,
        ...computeEffect(
          `spell_dc := 8 + data.abilities[data.spellcasting_ability].modifier + data.proficiency_bonus`,
          character
        ),
      },

      // spell attack bonus effect
      {
        name: 'base',
        priority: 10,
        ...computeEffect(
          `spell_attack_bonus := data.abilities[data.spellcasting_ability].modifier + data.proficiency_bonus`,
          character
        ),
      },
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
      createEffect(() => {
        this.setCharacters(character.slug, ...path, memo().value)
      })
    }
  }
}

function throwError(message: string) {
  throw new Error(message)
}

export const characterStore = new CharacterStore()
