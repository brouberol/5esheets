import { A } from "@solidjs/router";
import { createSignal } from "solid-js";
import { css } from "solid-styled";

import { ListCharacterSchema } from "~/5esheet-client";

export default function CharacterList({
  characters,
}: {
  characters: ListCharacterSchema[];
}) {
  return (
    <ul>
      {Object.values(characters).map(({ name, slug }) => (
        <li>
          <A href={"character/" + slug}>{name}</A>
        </li>
      ))}
    </ul>
  );
}
