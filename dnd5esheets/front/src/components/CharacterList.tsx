import { A } from "@solidjs/router";
import { createSignal } from "solid-js";
import { css } from "solid-styled";

import { CharacterSchema } from "~/5esheet-client";

export default function CharacterList({
  characters,
}: {
  characters: CharacterSchema[];
}) {
  return (
    <ul>
      {Object.values(characters).map(({ name, slug }) => (
        <A href={"character/" + slug}>{name}</A>
      ))}
    </ul>
  );
}
