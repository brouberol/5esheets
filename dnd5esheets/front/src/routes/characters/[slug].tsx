import { Show } from 'solid-js'
import { A, useParams } from '@solidjs/router'
import { Title } from '@solidjs/meta'

import CharacterSheet from '~/components/CharacterSheet'
import { Layout } from '~/components/Layout'
import { ResolvedCharacter, characterStore, resourceState } from '~/store'

export default function CharacterSheetPage() {
  const params = useParams()
  const [character, updateCharacter] = characterStore.getCharacter(params.slug)

  return (
    <>
      <Title>{params.slug}</Title>
      <A href={'/characters'}>← Character list</A>
      <Layout>
        <Show
          when={character[resourceState] === 'ready'}
          fallback={<div>loading...</div>}
        >
          <CharacterSheet
            character={character as ResolvedCharacter}
            updateCharacter={updateCharacter}
          />
        </Show>
      </Layout>
    </>
  )
}
