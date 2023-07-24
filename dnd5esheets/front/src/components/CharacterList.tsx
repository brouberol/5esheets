import { A } from '@solidjs/router'

import { ListCharacterSchema } from '~/5esheet-client'

export default function CharacterList({
  characters,
  addCharacter,
  state,
}: {
  characters: ListCharacterSchema[]
  addCharacter: (name: string) => void
}) {
  // not ideal to use this let and ref to access the input, but we can change that later
  let input: HTMLInputElement
  return (
    <>
      {/* later, we will have some specific css depending on the state: disabled while the front is syncing with the api */}
      <ul>
        {characters.map(({ name, slug }) => (
          <li>
            <A href={'character/' + slug}>{name}</A>
          </li>
        ))}
      </ul>
      <input ref={input}></input>
      <button
        onClick={() => {
          addCharacter(input.value)
          input.value = ''
        }}
      >
        add
      </button>
    </>
  )
}
