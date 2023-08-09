import { A } from '@solidjs/router'

import { Character } from '~/store'

export default function CharacterList(props: { characters: Character[] }) {
  return (
    <ul>
      {Object.values(props.characters).map((character) => (
        <li>
          <A href={character.slug}>
            {character.name}: {character.class_} {character.level}
          </A>
        </li>
      ))}
    </ul>
  )
}
