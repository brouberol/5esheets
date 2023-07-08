import { For, createSignal } from "solid-js";
import { css } from "solid-styled";
import { useI18n } from "@solid-primitives/i18n";

import { CharacterSchema } from "~/5esheets-client";
import LabeledInput from "~/components/LabeledInput";
import ProficientAttribute from "~/components/ProficientAttribute";
import LabeledBox from "~/components/LabeledBox";
import ScoreBox from "~/components/ScoreBox";
import BorderBox from "~/components/BorderBox";

export default function CharacterSheet({
  character,
  onChange,
}: {
  character: CharacterSchema;
  onChange: (change: Partial<CharacterSchema>) => void;
}) {
  const [t] = useI18n();

  css`

    .sheet {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      grid-template-rows: auto 1.1fr 1fr .9fr;
      grid-template-areas:
        "header header header"
        "base combat flavor"
        "base actions features"
        "prof equipment features"
      justify-items: stretch;
      align-items: stretch;
      justify-content: stretch;
      align-content: stretch;
      gap: 2mm;
    }

    header {
      display: flex;
      grid-area: header
    }

    .misc {
      --horizontal-gap: 4mm;
      --vertical-gap: 2mm;
      display: flex;
      flex-wrap: wrap;
      border: 1px solid black;
      padding: var(--vertical-gap) var(--horizontal-gap);
      gap: var(--vertical-gap) var(--horizontal-gap);
    }

    .misc > :global(*) {
      flex-grow: 1;
      flex-basis: calc(100% / 3 - var(--horizontal-gap));
      min-width: 10em;
    }

    .base {grid-area: base;}
    .proficiencies-and-languages { grid-area: prof;}
    .combat-stats { grid-area: combat;}
    .actions { grid-area: actions;}
    .equipment { grid-area: equipment}
    .flavor { grid-area: flavor}
    .features_and_traits { grid-area: features}

    .flex-container {
      height: 100%;
      width: 100%;

      display: flex;
      flex-direction: column;
      gap: 2mm;
    }

    .horizontal-container {
      flex-direction: row;
    }

    .scores {
      align-items: center;
      justify-content: space-between;
    }

    .scores, .skills, .saving_throws {
      margin: 0;
      padding: 0;

      li {
        list-style: none;
      }
    }

    .score-box {
      flex-grow: 0;
    }

    .attr-applications {
      display: flex;
      flex-direction: column;
      gap: 2mm;
      flex-grow: 1;
    }

  `;

  return (
    <section class="sheet">
      <header>
        <div class="character-name">
          <LabeledInput
            id="charname"
            label={t("character_name")}
            placeholder="Irene Wun Kmout"
            value={character.name}
            onChange={(name: string) => onChange({ name })}
          />
        </div>
        <div class="misc">
          <LabeledInput
            id="classlevel"
            label={t("class_and_level")}
            placeholder={`${t("wizard")} 2`}
            value={`${character.class_} ${character.level}`}
            onChange={(classAndLevel: string) => {
              const sanitizedInput = classAndLevel.trim();
              const index = sanitizedInput.lastIndexOf(" ");
              const [class_, level] = [
                sanitizedInput.slice(0, index).trim(),
                parseInt(sanitizedInput.slice(index).trim()) || 0,
              ];
              onChange({ class_, level });
            }}
          />
          <LabeledInput
            id="background"
            label={t("background")}
            placeholder={t("acolyte")}
            value={character.data.background}
            onChange={(background: string) =>
              onChange({ data: { background } })
            }
          />
          <LabeledInput
            id="playername"
            label={t("player_name")}
            placeholder={t("player-mcplayerface")}
            value={character.player.name}
            onChange={(playername: string) =>
              onChange({ player: { playername } })
            }
          />
          <LabeledInput
            id="race"
            label={t("race")}
            placeholder={t("half-elf")}
            value={character.data.race}
            onChange={(race: string) => onChange({ data: { race } })}
          />
          <LabeledInput
            id="alignment"
            label={t("alignment")}
            placeholder={t("lawful-good")}
            value={character.data.alignment}
            onChange={(alignment: string) => onChange({ data: { alignment } })}
          />
          <LabeledInput
            id="experiencepoints"
            label={t("experience_points")}
            placeholder="3240"
            value={character.data.xp}
            onChange={(experiencepoints: string) => onChange({ data: { xp } })}
          />
        </div>
      </header>
      <section class="base flex-container">
        <section class="flex-container horizontal-container">
          <div class="scores-box">
            <BorderBox>
              <div class="scores flex-container">
                <For
                  each={[
                    "strength",
                    "dexterity",
                    "constitution",
                    "intelligence",
                    "wisdom",
                    "charisma",
                  ]}
                >
                  {(attribute) => (
                    <ScoreBox
                      label={t(`${attribute}_abbr`)}
                      score={character.data.scores[attribute]}
                      modifier={character.data.scores[`${attribute}_mod`]}
                      onChange={(score: number) =>
                        onChange({ data: { scores: { [attribute]: score } } })
                      }
                    />
                  )}
                </For>
              </div>
            </BorderBox>
          </div>
          <div class="attr-applications">
            <div class="inspiration large-checkbox">
              <div class="box-label-container">
                <label class="subtitle" for="inspiration">
                  {t("inspiration")}
                </label>
              </div>
              <input
                name="inspiration"
                type="checkbox"
                checked={character.data["inspiration"]}
              />
            </div>
            <div class="proficiencybonus box">
              <div class="box-label-container">
                <label class="subtitle" for="proficiencybonus">
                  {t("proficiency_bonus")}
                </label>
              </div>
              <input
                class="square-rounded"
                name="proficiencybonus"
                placeholder="+2"
                value={character.data.proficiency_bonus}
              />
            </div>
            <LabeledBox label={t("saving_throws")}>
              <ul class="saving_throws">
                <For
                  each={[
                    "strength",
                    "dexterity",
                    "constitution",
                    "intelligence",
                    "wisdom",
                    "charisma",
                  ]}
                >
                  {(attribute) => (
                    <li>
                      <ProficientAttribute
                        id={attribute}
                        label={t(attribute)}
                        proficiency={
                          character.data.proficiencies.saves[attribute]
                        }
                        value={character.data[`${attribute}_save_mod`]}
                        onChange={(proficiency: number) =>
                          onChange({
                            data: {
                              proficiencies: {
                                saves: { [attribute]: proficiency },
                              },
                            },
                          })
                        }
                      />
                    </li>
                  )}
                </For>
              </ul>
            </LabeledBox>
            <LabeledBox label={t("skills")}>
              <ul class="skills">
                <For
                  each={[
                    [t("acrobatics"), "acrobatics", "dexterity"],
                    [t("animal_handling"), "animal_handling", "wisdom"],
                    [t("arcana"), "arcana", "intelligence"],
                    [t("athletics"), "athletics", "strength"],
                    [t("deception"), "deception", "dexterity"],
                    [t("history"), "history", "intelligence"],
                    [t("insight"), "insight", "wisdom"],
                    [t("intimidation"), "intimidation", "charisma"],
                    [t("investigation"), "investigation", "intelligence"],
                    [t("medicine"), "medicine", "wisdom"],
                    [t("nature"), "nature", "intelligence"],
                    [t("perception"), "perception", "wisdom"],
                    [t("performance"), "performance", "charisma"],
                    [t("persuasion"), "persuasion", "charisma"],
                    [t("religion"), "religion", "intelligence"],
                    [t("sleight_of_hand"), "sleight_of_hand", "dexterity"],
                    [t("stealth"), "stealth", "dexterity"],
                    [t("survival"), "survival", "wisdom"],
                  ].sort()}
                >
                  {([label, attribute, secondary]) => (
                    <li>
                      <ProficientAttribute
                        id={attribute}
                        label={label}
                        proficiency={
                          character.data.proficiencies.skills[attribute]
                        }
                        labelSecondary={t(`${secondary}_abbr`)}
                        value={character.data[attribute]}
                        onChange={(proficiency: number) =>
                          onChange({
                            data: {
                              proficiencies: {
                                skills: { [attribute]: proficiency },
                              },
                            },
                          })
                        }
                      />
                    </li>
                  )}
                </For>
              </ul>
            </LabeledBox>
          </div>
        </section>
      </section>
      <section class="proficiencies-and-languages flex-container">
        <div class="flex-container">
          <div class="passive-perception box">
            <div class="box-label-container">
              <label class="subtitle" for="passiveperception">
                {t("passive_perception")}
              </label>
            </div>
            <div class="tooltip">
              <input
                class="square-rounded"
                name="passiveperception"
                placeholder="10"
                value={character.data["passive_perception"]}
              />
              <span class="tooltiptext" id="passiveperception-tooltip"></span>
            </div>
          </div>
          <div class="darkvision large-checkbox">
            <div class="box-label-container">
              <label class="subtitle" for="darkvision">
                {t("darkvision")}
              </label>
            </div>
            <input
              name="darkvision"
              type="checkbox"
              checked={character.data["darkvision"]}
            />
          </div>
          <LabeledBox
            label={t("other_proficiencies_and_languages")}
          ></LabeledBox>
        </div>
      </section>
      <section class="combat-stats flex-container">
        <LabeledBox label={t("current_hit_points")}></LabeledBox>
      </section>
      <section class="actions flex-container">
        <LabeledBox label={t("attacks")}></LabeledBox>
      </section>
      <section class="equipment flex-container">
        <LabeledBox label={t("equipment")}></LabeledBox>
      </section>
      <section class="flavor flex-container">
        <LabeledBox label={t("personality")}></LabeledBox>
      </section>
      <section class="features_and_traits flex-container">
        <LabeledBox label={t("features_&_traits")}>
          <div style="height: 100%; width: 100%" contentEditable></div>
        </LabeledBox>
      </section>
    </section>
  );
}
