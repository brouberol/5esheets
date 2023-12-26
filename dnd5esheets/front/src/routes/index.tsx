import { Title } from '@solidjs/meta'
import { A } from '@solidjs/router'
import { Component } from 'solid-js'

export const HomePage: Component = () => (
  <>
    <Title>D&D 5e sheets</Title>
    <main>
      <A href={'/characters'}>Characters</A>
    </main>
  </>
)
