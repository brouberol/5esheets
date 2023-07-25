import CharacterList from '~/components/CharacterList'
import { CharacterService } from '~/5esheets-client'
import { createResource } from 'solid-js'
import { Title } from '@solidjs/meta'

export default function CharacterListPage() {
  const [characters] = createResource(CharacterService.listCharacters)
  return (
    <>
      <Title>Character list</Title>
      <main>{characters() && <CharacterList characters={characters()} />}</main>
    </>
  )
}
