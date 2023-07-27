import { useParams } from '@solidjs/router'
import { Title } from '@solidjs/meta'

import CharacterSheet from '~/components/CharacterSheet'
import { Layout } from '~/components/Layout'
import { characterStore } from '~/store'

export default function CharacterSheetPage() {
  const params = useParams()
  const [character] = characterStore.getCharacter(params.slug)

  return (
    <>
      <Title>{params.slug}</Title>
      <Layout>
        <CharacterSheet character={character} onChange={() => {}} />
      </Layout>
    </>
  )
}
