import { createResource } from 'solid-js'
import { createDeepSignal } from '@solid-primitives/resource'
import { createStore, produce } from 'solid-js/store'

import {
  CharacterSchema,
  ListCharacterSchema,
  OpenAPI,
} from '~/5esheets-client'
import { CharacterService } from '~/5esheets-client'

if (process.env.NODE_ENV === 'development') {
  OpenAPI.BASE = 'http://localhost:8000'
}

export const cycleProficiency = (proficiency: number) => (proficiency + 1) % 3

const emptyCharacter: CharacterSchema = {
  id: 0,
  slug: '',
  class_: '',
  name: '',
  level: 0,
  data: {
    abilities: {
      strength: {
        modifier: 0,
        proficiency: 0,
        score: 10,
        save: 0,
      },
      dexterity: {
        modifier: 0,
        proficiency: 0,
        score: 10,
        save: 0,
      },
      constitution: {
        modifier: 0,
        proficiency: 0,
        score: 10,
        save: 0,
      },
      wisdom: {
        modifier: 0,
        proficiency: 0,
        score: 10,
        save: 0,
      },
      charisma: {
        modifier: 0,
        proficiency: 0,
        score: 10,
        save: 0,
      },
      intelligence: {
        modifier: 0,
        proficiency: 0,
        score: 10,
        save: 0,
      },
    },
    skills: {
      acrobatics: {
        modifier: 0,
        proficiency: 0,
      },
      arcana: {
        modifier: 0,
        proficiency: 0,
      },
      athletics: {
        modifier: 0,
        proficiency: 0,
      },
      stealth: {
        modifier: 0,
        proficiency: 0,
      },
      animal_handling: {
        modifier: 0,
        proficiency: 0,
      },
      sleight_of_hand: {
        modifier: 0,
        proficiency: 0,
      },
      history: {
        modifier: 0,
        proficiency: 0,
      },
      intimidation: {
        modifier: 0,
        proficiency: 0,
      },
      investigation: {
        modifier: 0,
        proficiency: 0,
      },
      medicine: {
        modifier: 0,
        proficiency: 0,
      },
      nature: {
        modifier: 0,
        proficiency: 0,
      },
      perception: {
        modifier: 0,
        proficiency: 0,
      },
      insight: {
        modifier: 0,
        proficiency: 0,
      },
      persuasion: {
        modifier: 0,
        proficiency: 0,
      },
      religion: {
        modifier: 0,
        proficiency: 0,
      },
      performance: {
        modifier: 0,
        proficiency: 0,
      },
      survival: {
        modifier: 0,
        proficiency: 0,
      },
      deception: {
        modifier: 0,
        proficiency: 0,
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
  equipment: [],
  party: { id: 0, name: '' },
  player: { id: 0, name: '' },
}

class CharacterStore {
  private list?: ListCharacterSchema[]
  private characters: Record<
    string,
    [CharacterSchema, (fn: (character: CharacterSchema) => void) => void]
  > = {}

  getList = () => (this.list ??= this.initList())

  private initList = () => {
    const [listResource] = createResource(CharacterService.listCharacters, {
      initialValue: [],
      storage: createDeepSignal,
    })

    const [list] = createStore<ListCharacterSchema[]>(listResource())
    return list
  }

  getCharacter = (
    slug: string
  ): [
    CharacterSchema,
    (updater: (character: CharacterSchema) => void) => void,
  ] => (this.characters[slug] ??= this.initCharacter(slug))

  private initCharacter = (
    slug: string
  ): [CharacterSchema, (fn: (character: CharacterSchema) => void) => void] => {
    const [characterResource] = createResource(
      slug,
      CharacterService.getCharacter,
      { initialValue: emptyCharacter, storage: createDeepSignal }
    )

    const [character, setCharacter] = createStore<CharacterSchema>(
      characterResource()
    )

    const updateCharacter = (fn: (character: CharacterSchema) => void) =>
      setCharacter(produce(fn))

    return [character, updateCharacter]
  }
}

export const characterStore = new CharacterStore()
