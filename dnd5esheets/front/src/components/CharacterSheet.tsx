import { For } from 'solid-js'
import { produce } from 'solid-js/store'
import { css } from 'solid-styled'
import { useI18n } from '@solid-primitives/i18n'

import { CharacterSchema } from '~/5esheets-client'
import LabeledInput from '~/components/LabeledInput'
import ProficientAttribute from '~/components/ProficientAttribute'
import LabeledBox from '~/components/LabeledBox'
import ScoreBox from '~/components/ScoreBox'
import BorderBox from '~/components/BorderBox'

export default function CharacterSheet({
  character,
  updateCharacter,
}: {
  character: CharacterSchema
  updateCharacter: (updater: (character: CharacterSchema) => void) => void
}) {
  const [t] = useI18n()

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

  `

  return (
    <section class="sheet">
      <header>
        <div class="character-name">
          <LabeledInput
            id="charname"
            label={t('character_name')}
            placeholder="Irene Wun Kmout"
            value={character.name}
            onChange={(name: string) =>
              updateCharacter((character) => (character.name = name))
            }
          />
        </div>
        <div class="misc">
          <LabeledInput
            id="classlevel"
            label={t('class_and_level')}
            placeholder={`${t('wizard')} 2`}
            value={`${character.class_} ${character.level}`}
            onChange={(classAndLevel: string) => {
              const sanitizedInput = classAndLevel.trim()
              const index = sanitizedInput.lastIndexOf(' ')
              const [class_, level] = [
                sanitizedInput.slice(0, index).trim(),
                parseInt(sanitizedInput.slice(index).trim()) || 0,
              ]
              updateCharacter((character: CharacterSchema) => {
                character.class_ = class_
                character.level = level
              })
            }}
          />
          <LabeledInput
            id="background"
            label={t('background')}
            placeholder={t('acolyte')}
            value={character.data.background}
            onChange={(background: string) =>
              updateCharacter(
                (character) => (character.data.background = background)
              )
            }
          />
          <LabeledInput
            id="playername"
            label={t('player_name')}
            placeholder={t('player-mcplayerface')}
            value={character.player.name}
            onChange={(playername: string) =>
              updateCharacter(
                (character) => (character.player.playername = playername)
              )
            }
          />
          <LabeledInput
            id="race"
            label={t('race')}
            placeholder={t('half-elf')}
            value={character.data.race}
            onChange={(race: string) =>
              updateCharacter((character) => (character.data.race = race))
            }
          />
          <LabeledInput
            id="alignment"
            label={t('alignment')}
            placeholder={t('lawful-good')}
            value={character.data.alignment}
            onChange={(alignment: string) =>
              updateCharacter(
                (character) => (character.data.alignment = alignment)
              )
            }
          />
          <LabeledInput
            id="experiencepoints"
            label={t('experience_points')}
            placeholder="3240"
            value={character.data.xp.toString()}
            onChange={(experiencepoints: string) =>
              updateCharacter(
                (character) => (character.data.xp = +experiencepoints)
              )
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
                      'strength',
                      'dexterity',
                      'constitution',
                      'intelligence',
                      'wisdom',
                      'charisma',
                    ] as const
                  }
                >
                  {(attribute) => (
                    <ScoreBox
                      label={t(`${attribute}_abbr`)}
                      score={character.data.scores[attribute]}
                      modifier={character.data.scores[`${attribute}_mod`]}
                      onChange={(score: number) =>
                        updateCharacter(
                          (character) =>
                            (character.data.scores[attribute] = score)
                        )
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
                  {t('inspiration')}
                </label>
              </div>
              <input
                name="inspiration"
                type="checkbox"
                checked={character.data['inspiration']}
              />
            </div>
            <div class="proficiencybonus box">
              <div class="box-label-container">
                <label class="subtitle" for="proficiencybonus">
                  {t('proficiency_bonus')}
                </label>
              </div>
              <input
                class="square-rounded"
                name="proficiencybonus"
                placeholder="+2"
                value={character.data.proficiency_bonus}
              />
            </div>
            <LabeledBox label={t('saving_throws')}>
              <ul class="saving_throws">
                <For
                  each={
                    [
                      'strength',
                      'dexterity',
                      'constitution',
                      'intelligence',
                      'wisdom',
                      'charisma',
                    ] as const
                  }
                >
                  {(attribute) => (
                    <li>
                      <ProficientAttribute
                        id={attribute}
                        label={t(attribute)}
                        proficiency={
                          character.data.proficiencies.saves[attribute]
                        }
                        value={character.data.scores[`${attribute}_save_mod`]}
                        onChange={(proficiency: number) =>
                          updateCharacter(
                            (character) =>
                              (character.data.proficiencies.saves[attribute] =
                                proficiency)
                          )
                        }
                      />
                    </li>
                  )}
                </For>
              </ul>
            </LabeledBox>
            <LabeledBox label={t('skills')}>
              <ul class="skills">
                <For
                  each={[
                    [t('acrobatics'), 'acrobatics', 'dexterity'] as const,
                    [
                      t('animal_handling'),
                      'animal_handling',
                      'wisdom',
                    ] as const,
                    [t('arcana'), 'arcana', 'intelligence'] as const,
                    [t('athletics'), 'athletics', 'strength'] as const,
                    [t('deception'), 'deception', 'dexterity'] as const,
                    [t('history'), 'history', 'intelligence'] as const,
                    [t('insight'), 'insight', 'wisdom'] as const,
                    [t('intimidation'), 'intimidation', 'charisma'] as const,
                    [
                      t('investigation'),
                      'investigation',
                      'intelligence',
                    ] as const,
                    [t('medicine'), 'medicine', 'wisdom'] as const,
                    [t('nature'), 'nature', 'intelligence'] as const,
                    [t('perception'), 'perception', 'wisdom'] as const,
                    [t('performance'), 'performance', 'charisma'] as const,
                    [t('persuasion'), 'persuasion', 'charisma'] as const,
                    [t('religion'), 'religion', 'intelligence'] as const,
                    [
                      t('sleight_of_hand'),
                      'sleight_of_hand',
                      'dexterity',
                    ] as const,
                    [t('stealth'), 'stealth', 'dexterity'] as const,
                    [t('survival'), 'survival', 'wisdom'] as const,
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
                        value={character.data.scores[`${attribute}_mod`]}
                        onChange={(proficiency: number) =>
                          updateCharacter(
                            (character) =>
                              (character.data.proficiencies.skills[attribute] =
                                proficiency)
                          )
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
                {t('passive_perception')}
              </label>
            </div>
            <div class="tooltip">
              <input
                class="square-rounded"
                name="passiveperception"
                placeholder="10"
                value={character.data['passive_perception']}
              />
              <span class="tooltiptext" id="passiveperception-tooltip"></span>
            </div>
          </div>
          <div class="darkvision large-checkbox">
            <div class="box-label-container">
              <label class="subtitle" for="darkvision">
                {t('darkvision')}
              </label>
            </div>
            <input
              name="darkvision"
              type="checkbox"
              checked={character.data['darkvision']}
            />
          </div>
          <LabeledBox
            label={t('other_proficiencies_and_languages')}
          ></LabeledBox>
        </div>
      </section>
      <section class="combat-stats flex-container">
        <LabeledBox label={t('current_hit_points')}></LabeledBox>
      </section>
      <section class="actions flex-container">
        <LabeledBox label={t('attacks')}></LabeledBox>
      </section>
      <section class="equipment flex-container">
        <LabeledBox label={t('equipment')}></LabeledBox>
      </section>
      <section class="flavor flex-container">
        <LabeledBox label={t('personality')}></LabeledBox>
      </section>
      <section class="features_and_traits flex-container">
        <LabeledBox label={t('features_&_traits')}>
          <div style="height: 100%; width: 100%" contentEditable></div>
        </LabeledBox>
      </section>
    </section>
  )
}
