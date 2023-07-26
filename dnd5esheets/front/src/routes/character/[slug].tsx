import { useParams } from '@solidjs/router'
import { createResource } from 'solid-js'
import { Title } from '@solidjs/meta'

import CharacterSheet from '~/components/CharacterSheet'
import { Layout } from '~/components/Layout'
import { CharacterService } from '~/5esheets-client'

export default function CharacterSheetPage() {
  const params = useParams()
  const [character] = createResource(params.slug, CharacterService.getCharacter)

  return (
    <>
      <Title>{params.slug}</Title>
      <Layout>
        {character.state === 'ready' ? (
          <CharacterSheet character={character()} onChange={() => {}} />
        ) : (
          <p>loading...</p>
        )}
      </Layout>
    </>
  )
}
