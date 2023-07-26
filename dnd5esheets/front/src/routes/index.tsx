import { Title } from '@solidjs/meta'
import { createResource } from 'solid-js'

import CharacterList from '~/components/CharacterList'
import { CharacterService } from '~/5esheets-client'

export default function CharacterListPage() {
  const [characters] = createResource(CharacterService.listCharacters)
  return (
    <>
      <Title>Character list</Title>
      <main>{characters() && <CharacterList characters={characters()} />}</main>
    </>
  )
}
