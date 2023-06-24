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
      display: flex;
      flex-direction: column;

      justify-content: space-between;
    }

    .scores, .skills, .saving_throws {
      margin: 0;
      padding: 2mm;

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
                sanitizedInput.slice(index).trim() || 0,
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
            value={character.data.playername}
            onChange={(playername: string) =>
              onChange({ data: { playername } })
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
            value={character.data.experiencepoints}
            onChange={(experiencepoints: string) =>
              onChange({ data: { experiencepoints } })
            }
          />
        </div>
      </header>
      <section class="base flex-container">
        <section class="flex-container horizontal-container">
          <div class="scores-box">
            <BorderBox>
              <div class="scores flex-container">
                <For
                  each={
                    [
                      "Strength",
                      "Dexterity",
                      "Constitution",
                      "Intelligence",
                      "Wisdom",
                      "Charisma",
                    ] as const
                  }
                >
                  {(label) => (
                    <ScoreBox
                      label={t(`${label.toLowerCase()}_abbr`)}
                      score={character.data[`${label}score`]}
                      modifier={character.data[`${label}mod`]}
                      onChange={(score: number) =>
                        onChange({ data: { [`${label}score`]: score } })
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
                  {t("proficiency bous")}
                </label>
              </div>
              <input
                class="square-rounded"
                name="proficiencybonus"
                placeholder="+2"
                value="{{ character.data['proficiencybonus'] }}"
              />
            </div>
            <LabeledBox label={t("saving_throws")}>
              <ul class="saving_throws">
                <For
                  each={[
                    {
                      id: "strength",
                      label: t("strength"),
                      proficiency: character.data["Strength-save-prof"]
                        ? "master"
                        : "none",
                      value: character.data["Strength-save"],
                    },
                    {
                      id: "dexterity",
                      label: t("dexterity"),
                      proficiency: character.data["Dexterity-save-prof"]
                        ? "master"
                        : "none",
                      value: character.data["Dexterity-save"],
                    },
                    {
                      id: "constitution",
                      label: t("constitution"),
                      proficiency: character.data["Constitution-save-prof"]
                        ? "master"
                        : "none",
                      value: character.data["Constitution-save"],
                    },
                    {
                      id: "intelligence",
                      label: t("intelligence"),
                      proficiency: character.data["Intelligence-save-prof"]
                        ? "master"
                        : "none",
                      value: character.data["Intelligence-save"],
                    },
                    {
                      id: "wisdom",
                      label: t("wisdom"),
                      proficiency: character.data["Wisdom-save-prof"]
                        ? "master"
                        : "none",
                      value: character.data["Wisdom-save"],
                    },
                    {
                      id: "charisma",
                      label: t("charisma"),
                      proficiency: character.data["Charisma-save-prof"]
                        ? "master"
                        : "none",
                      value: character.data["Charisma-save"],
                    },
                  ]}
                >
                  {(skill) => (
                    <li>
                      <ProficientAttribute {...skill} />
                    </li>
                  )}
                </For>
              </ul>
            </LabeledBox>
            <LabeledBox label={t("skills")}>
              <ul class="skills">
                <For
                  each={[
                    {
                      id: "acrobatics",
                      label: t("acrobatics"),
                      proficiency: character.data["Acrobatics-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("dexterity_abbr"),
                      value: character.data.Acrobatics,
                    },
                    {
                      id: "animal-handling",
                      label: t("animal_handling"),
                      proficiency: character.data["Animal Handling-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("wisdom_abbr"),
                      value: character.data["Animal Handling"],
                    },
                    {
                      id: "arcana",
                      label: t("arcana"),
                      proficiency: character.data["Arcana-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("intelligence_abbr"),
                      value: character.data.Arcana,
                    },
                    {
                      id: "athletics",
                      label: t("athletics"),
                      proficiency: character.data["Athletics-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("strength_abbr"),
                      value: character.data.Athletics,
                    },
                    {
                      id: "deception",
                      label: t("deception"),
                      proficiency: character.data["Deception-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("dexterity_abbr"),
                      value: character.data.Deception,
                    },
                    {
                      id: "history",
                      label: t("history"),
                      proficiency: character.data["History-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("intelligence_abbr"),
                      value: character.data.History,
                    },
                    {
                      id: "insight",
                      label: t("insight"),
                      proficiency: character.data["Insight-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("wisdom_abbr"),
                      value: character.data.Insight,
                    },
                    {
                      id: "intimidation",
                      label: t("intimidation"),
                      proficiency: character.data["Intimidation-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("charisma_abbr"),
                      value: character.data.Intimidation,
                    },
                    {
                      id: "investigation",
                      label: t("investigation"),
                      proficiency: character.data["Investigation-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("intelligence_abbr"),
                      value: character.data.Investigation,
                    },
                    {
                      id: "medicine",
                      label: t("medicine"),
                      proficiency: character.data["Medicine-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("wisdom_abbr"),
                      value: character.data.Medicine,
                    },
                    {
                      id: "nature",
                      label: t("nature"),
                      proficiency: character.data["Nature-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("intelligence_abbr"),
                      value: character.data.Nature,
                    },
                    {
                      id: "perception",
                      label: t("perception"),
                      proficiency: character.data["Perception-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("wisdom_abbr"),
                      value: character.data.Perception,
                    },
                    {
                      id: "performance",
                      label: t("performance"),
                      proficiency: character.data["Performance-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("charisma_abbr"),
                      value: character.data.Performance,
                    },
                    {
                      id: "persuasion",
                      label: t("persuasion"),
                      proficiency: character.data["Persuasion-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("charisma_abbr"),
                      value: character.data.Persuasion,
                    },
                    {
                      id: "religion",
                      label: t("religion"),
                      proficiency: character.data["Religion-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("intelligence_abbr"),
                      value: character.data.Religion,
                    },
                    {
                      id: "sleight-of-hand",
                      label: t("sleight_of_hand"),
                      proficiency: character.data["Sleight of Hand-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("dexterity_abbr"),
                      value: character.data["Sleight of Hand"],
                    },
                    {
                      id: "stealth",
                      label: t("stealth"),
                      proficiency: character.data["Stealth-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("dexterity_abbr"),
                      value: character.data["Stealth"],
                    },
                    {
                      id: "survival",
                      label: t("survival"),
                      proficiency: character.data["Survival-prof"]
                        ? "master"
                        : "none",
                      labelSecondary: t("wisdom_abbr"),
                      value: character.data["Survival"],
                    },
                  ].sort((a, b) => (a.label > b.label ? 1 : -1))}
                >
                  {(skill) => (
                    <li>
                      <ProficientAttribute {...skill} />
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
                value="{{ character.data['passiveperception'] }}"
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
