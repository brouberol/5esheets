import { Suspense } from 'solid-js'
import { unwrap } from 'solid-js/store'
import ErrorBoundary, { RouteDataArgs, Title, useRouteData } from 'solid-start'
import CharacterSheet from '~/components/CharacterSheet'
import { Layout } from '~/components/Layout'
import { CharacterList as Store } from '~/store'

export function routeData(data: RouteDataArgs) {
  console.log('character route', unwrap(data))
  const store = new Store()
  return store.getCharacter(data.params.slug)
}

export default function CharacterPage() {
  const [character, updateCharacter] = useRouteData<typeof routeData>()

  return (
    <ErrorBoundary
      fallback={(error: Error) => (
        <p>
          Error: {error.name} {error.message}
        </p>
      )}
    >
      <Suspense fallback={<p>loading ...</p>}>
        <Layout>
          <Title>{character.name}</Title>
          <CharacterSheet
            character={character}
            updateCharacter={updateCharacter}
          />
        </Layout>
      </Suspense>
    </ErrorBoundary>
  )
}
