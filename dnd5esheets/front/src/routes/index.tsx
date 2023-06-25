import { Title } from "solid-start";
import CharacterList from "~/components/CharacterList";
import useStore from "~/store";

export default function Home() {
  const [characters, { update }] = useStore();

  return (
    <main>
      <Title>D&D 5e sheets</Title>
      <CharacterList characters={characters} />
    </main>
  );
}
