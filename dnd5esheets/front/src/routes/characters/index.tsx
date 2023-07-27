import { Title } from '@solidjs/meta'

import CharacterList from '~/components/CharacterList'
import { characterStore } from '~/store'

export default function CharacterListPage() {
  return (
    <>
      <Title>Character list</Title>
      <main>
        <CharacterList characters={characterStore.getList()} />
      </main>
    </>
  )
}
