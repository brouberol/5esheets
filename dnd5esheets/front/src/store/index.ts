import { SetStoreFunction, createStore, produce } from 'solid-js/store'

import {
  CharacterSchema,
  CharacterSheet,
  OpenAPI,
  Proficiency,
} from '~/5esheets-client'
import { CharacterService } from '~/5esheets-client'

if (process.env.NODE_ENV === 'development') {
  OpenAPI.BASE = 'http://localhost:8000'
}

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
}

function throwError(message: string) {
  throw new Error(message)
}

export const characterStore = new CharacterStore()
