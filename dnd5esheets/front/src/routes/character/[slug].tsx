import { Title, useParams } from 'solid-start'

import CharacterSheet from '~/components/CharacterSheet'
import { Layout } from '~/components/Layout'
import useStore from '~/store'

export default function CharacterPage() {
  const params = useParams()
  const [characters, { update }] = useStore()

  return (
    <Layout>
      <Title>{params.slug}</Title>
      <CharacterSheet
        character={characters[params.slug]}
        onChange={(change) => update(params.slug, change)}
      />
    </Layout>
  )
}
