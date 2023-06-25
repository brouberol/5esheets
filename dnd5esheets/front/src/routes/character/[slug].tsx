import { Title, useParams } from "solid-start";

import Character from "~/components/CharacterSheet";
import { Layout } from "~/components/Layout";
import useStore from "~/store";

export default function CharacterPage() {
  const params = useParams();
  const [characters, { update }] = useStore();

  return (
    <Layout>
      <Title>{params.slug}</Title>
      <Character
        character={characters[params.slug]}
        onChange={(change) => update(params.slug, change)}
      />
    </Layout>
  );
}
