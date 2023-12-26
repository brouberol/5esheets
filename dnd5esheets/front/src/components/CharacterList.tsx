import { A } from '@solidjs/router'
import { Component } from 'solid-js'

import { Character } from '~/store'

export const CharacterList: Component<{ characters: Character[] }> = (
  props
) => {
  return (
    <ul>
      {Object.values(props.characters).map((character) => (
        <li>
          <A href={character.slug}>
            {character.name}: lvl {character.level}
          </A>
        </li>
      ))}
    </ul>
  )
}
