import { For } from 'solid-js'
import { css } from 'solid-styled'
import { useI18n } from '@solid-primitives/i18n'

import { Proficiency } from '~/5esheets-client'
import BorderBox from '~/components/BorderBox'
import LabeledBox from '~/components/LabeledBox'
import LabeledInput from '~/components/LabeledInput'
import MarkdownRenderedEditableBox from '~/components/MarkdownRenderedEditableBox'
import ProficientAttribute from '~/components/ProficientAttribute'
import ScoreBox from '~/components/ScoreBox'
import TrayBox from '~/components/TrayBox'
import { ResolvedCharacter, UpdateCharacterFunction } from '~/store'

export default function CharacterSheet(props: {
  character: ResolvedCharacter
  updateCharacter: UpdateCharacterFunction
}) {
  const [t] = useI18n()

  css`

    .sheet {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      grid-template-rows: auto;
      grid-template-areas:
        "header header header"
        "base combat flavor"
        "base actions features"
        "prof inventory features"
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
    .inventory { grid-area: inventory}
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
            value={props.character.name}
            onChange={(name) =>
              props.updateCharacter((character) => (character.name = name))
            }
          />
        </div>
        <div class="misc">
          <LabeledInput
            id="classlevel"
            label={t('class_and_level')}
            placeholder={`${t('wizard')} 2`}
            value={`${props.character.class_} ${props.character.level}`}
            onChange={(classAndLevel: string) => {
              props.updateCharacter((character) => {
                const lastSpaceIndex = classAndLevel.lastIndexOf(' ')
                character.class_ = classAndLevel.slice(0, lastSpaceIndex).trim()
                character.level =
                  parseInt(classAndLevel.slice(lastSpaceIndex).trim()) || 0
              })
            }}
          />
          <LabeledInput
            id="background"
            label={t('background')}
            placeholder={t('acolyte')}
            value={props.character.data.background}
            onChange={(background: string) =>
              props.updateCharacter(
                (character) => (character.data.background = background)
              )
            }
          />
          <LabeledInput
            id="playername"
            label={t('player_name')}
            placeholder={t('player-mcplayerface')}
            value={props.character.player.name}
            onChange={(playername: string) =>
              props.updateCharacter(
                (character) => (character.player.name = playername)
              )
            }
          />
          <LabeledInput
            id="race"
            label={t('race')}
            placeholder={t('half-elf')}
            value={props.character.data.race}
            onChange={(race: string) =>
              props.updateCharacter((character) => (character.data.race = race))
            }
          />
          <LabeledInput
            id="alignment"
            label={t('alignment')}
            placeholder={t('lawful-good')}
            value={props.character.data.alignment}
            onChange={(alignment: string) =>
              props.updateCharacter(
                (character) => (character.data.alignment = alignment)
              )
            }
          />
          <LabeledInput
            id="experiencepoints"
            label={t('experience_points')}
            placeholder="3240"
            value={props.character.data.xp.toString()}
            onChange={(experiencepoints: string) =>
              props.updateCharacter(
                (character) => (character.data.xp = parseInt(experiencepoints))
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
                  {(ability) => (
                    <ScoreBox
                      ability={ability}
                      label={t(`${ability}_abbr`)}
                      score={props.character.data.abilities[ability].score}
                      modifier={
                        props.character.data.abilities[ability].modifier
                      }
                      onChange={(score: number) => {
                        props.updateCharacter(
                          (character) =>
                          (character.data.abilities[ability].score =
                            Number.isNaN(score) ? 0 : score)
                        )
                      }}
                    />
                  )}
                </For>
              </div>
            </BorderBox>
          </div>
          <div class="attr-applications">
            <TrayBox
              label={t('inspiration')}
              value={props.character.data.inspiration ? '✹' : ''}
              onChange={() =>
                props.updateCharacter(
                  (character) =>
                    (character.data.inspiration = !character.data.inspiration)
                )
              }
            />
            <TrayBox
              label={t('proficiency_bonus')}
              value={props.character.data.proficiency_bonus}
            />
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
                  {(ability) => (
                    <li>
                      <ProficientAttribute
                        id={ability}
                        label={t(ability)}
                        proficiency={
                          props.character.data.abilities[ability].proficiency
                        }
                        value={props.character.data.abilities[ability].save}
                        onChange={(proficiency: Proficiency) =>
                          props.updateCharacter(
                            (character) =>
                              (character.data.abilities[ability].proficiency =
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
                  {([label, skill, ability]) => (
                    <li>
                      <ProficientAttribute
                        id={skill}
                        label={label}
                        proficiency={
                          props.character.data.skills[skill].proficiency
                        }
                        labelDerived={t(`${ability}_abbr`)}
                        value={props.character.data.skills[skill].modifier}
                        onChange={(proficiency: Proficiency) =>
                          props.updateCharacter(
                            (character) =>
                              (character.data.skills[skill].proficiency =
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
          <TrayBox
            label={t('passive_perception')}
            value={props.character.data.passive_perception}
          />
          <TrayBox
            label={t('darkvision')}
            value={props.character.data.darkvision ? '☽' : ''}
            onChange={() =>
              props.updateCharacter(
                (character) =>
                  (character.data.darkvision = !character.data.darkvision)
              )
            }
          />
          <LabeledBox label={t('other_proficiencies_and_languages')}>
            <MarkdownRenderedEditableBox
              id="languages-proficiencies"
              text={props.character.data?.languages_and_proficiencies || ''}
              onChange={(languagesAndProficiencies: string) =>
                props.updateCharacter(
                  (character) =>
                    (character.data.languages_and_proficiencies =
                      languagesAndProficiencies)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabeledBox>
        </div>
      </section>
      <section class="combat-stats flex-container">
        <div class="flex-container horizontal-container">
          <LabeledBox label={t('death_saves')}>
            <div>
              {t('death_saves_successes')}: {props.character.data?.death_saves.successes}
            </div>
            <div>
              {t('death_saves_failures')}: {props.character.data?.death_saves.failures}
            </div>
          </LabeledBox>
        </div>
      </section>
      <section class="actions flex-container">
        <LabeledBox label={t('attacks')}></LabeledBox>
      </section>
      <section class="inventory flex-container">
        <LabeledBox label={t('inventory')}>
          <MarkdownRenderedEditableBox
            id="inventory"
            text={props.character.data.inventory || ''}
            onChange={(inventory: string) =>
              props.updateCharacter(
                (character) => (character.data.inventory = inventory)
              )
            }
          ></MarkdownRenderedEditableBox>
        </LabeledBox>
      </section>
      <section class="flavor flex-container">
        <BorderBox>
          <LabeledBox label={t('personality')}>
            <MarkdownRenderedEditableBox
              id="personality"
              text={props.character.data?.personality || ''}
              onChange={(personality: string) =>
                props.updateCharacter(
                  (character) => (character.data.personality = personality)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabeledBox>
          <LabeledBox label={t('ideals')}>
            <MarkdownRenderedEditableBox
              id="ideals"
              text={props.character.data?.ideals || ''}
              onChange={(ideals: string) =>
                props.updateCharacter(
                  (character) => (character.data.ideals = ideals)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabeledBox>
          <LabeledBox label={t('bonds')}>
            <MarkdownRenderedEditableBox
              id="bonds"
              text={props.character.data?.bonds || ''}
              onChange={(bonds: string) =>
                props.updateCharacter(
                  (character) => (character.data.bonds = bonds)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabeledBox>
          <LabeledBox label={t('flaws')}>
            <MarkdownRenderedEditableBox
              id="flaws"
              text={props.character.data?.flaws || ''}
              onChange={(flaws: string) =>
                props.updateCharacter(
                  (character) => (character.data.flaws = flaws)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabeledBox>
        </BorderBox>
      </section>
      <section class="features_and_traits flex-container">
        <LabeledBox label={t('features_&_traits')}>
          <MarkdownRenderedEditableBox
            id="features-traits"
            text={props.character.data?.features || ''}
            onChange={(features: string) =>
              props.updateCharacter(
                (character) => (character.data.features = features)
              )
            }
          ></MarkdownRenderedEditableBox>
        </LabeledBox>
      </section>
    </section>
  )
}
