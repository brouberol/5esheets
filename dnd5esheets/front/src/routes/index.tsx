import { Title, useRouteData } from 'solid-start'
import CharacterList from '~/components/CharacterList'
import { ErrorBoundary, Suspense } from 'solid-js'
import { CharacterList as Store } from '~/store'
import { unwrap } from 'solid-js/store'

export function routeData(data) {
  console.log('index route', unwrap(data))
  return new Store()
}

export default function Home() {
  const characterList = useRouteData<typeof routeData>()

  return (
    <main>
      <Title>D&D 5e sheets</Title>
      <ErrorBoundary
        fallback={(error: Error) => (
          <p>
            Error: {error.name} {error.message}
          </p>
        )}
      >
        <Suspense fallback={<p>loading ...</p>}>
          <CharacterList
            characters={characterList.list() ?? []}
            addCharacter={characterList.addCharacter}
            state={characterList.list.state}
          />
        </Suspense>
      </ErrorBoundary>
    </main>
  )
}
