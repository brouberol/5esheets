import { Title } from '@solidjs/meta'
import { A } from '@solidjs/router'

export default function HomePage() {
  return (
    <>
      <Title>D&D 5e sheets</Title>
      <main>
        <A href={'/characters'}>Characters</A>
      </main>
    </>
  )
}
