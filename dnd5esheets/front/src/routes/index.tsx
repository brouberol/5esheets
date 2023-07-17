import { Title } from "solid-start";
import CharacterList from "~/components/CharacterList";
import { CharacterService } from "~/5esheets-client";
import { createResource } from "solid-js";

const listCharacters = async () => {
  return await CharacterService.listCharacters();
}

export default function Home() {
  const [characters] = createResource(listCharacters);
  return (
    <main>
      <Title>D&D 5e sheets</Title>
      {characters() &&
        <CharacterList characters={characters()} />
      }
    </main>
  );
}
