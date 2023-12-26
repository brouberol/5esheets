import { Title } from '@solidjs/meta'
import { Component, Show } from 'solid-js'

import { CharacterList } from '~/components/CharacterList'
import { characterStore, resourceState } from '~/store'

export const CharacterListPage: Component = () => {
  const characterList = characterStore.getCharacters()

  return (
    <>
      <Title>Character list</Title>
      <main>
        <Show
          when={characterList[resourceState] === 'ready'}
          fallback={<div>loading...</div>}
        >
          <CharacterList characters={Object.values(characterList)} />
        </Show>
      </main>
    </>
  )
}
