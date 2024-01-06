import { Component, For, JSXElement, ParentComponent, Show } from 'solid-js'
import { css } from 'solid-styled'

import { Proficiency } from '~/5esheets-client'
import { Editable } from '~/components/editable'
import { LabelledBox } from '~/components/LabelledBox'
import { MarkdownRenderedEditableBox } from '~/components/MarkdownRenderedEditableBox'
import { NumberInput } from '~/components/number-input'
import { ProficientAttribute } from '~/components/ProficientAttribute'
import { ScoreBox } from '~/components/ScoreBox'
import { TrayBox } from '~/components/TrayBox'
import { t } from '~/i18n'
import { ResolvedCharacter, UpdateCharacterFunction } from '~/store'

const Portrait = () => {
  css`
    .portrait {
      width: 90%;
      margin: auto;
      aspect-ratio: 1;
      border: 2px solid black;
      border-radius: 50%;
      margin-bottom: -25%;
    }
  `

  return <div class="portrait"></div>
}

const Box: ParentComponent = (props) => {
  css`
    .box {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      border: 2px solid black;
      background: white;
      padding: 0 0.3rem;
    }
  `

  return <div class="box">{props.children}</div>
}

const Level: Component<{
  level: number
  onChangeLevel?: (level: number) => void
  onChangeXp: (xp: number) => void
  proficiency: number
  xp: number
}> = (props) => {
  css`
    .level-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 1.4rem;
    }

    .proficiency-row {
      font-size: 1.1rem;
      padding-left: 2.5em;
      margin-top: -0.7rem;
    }

    .proficiency-value {
      font-size: 1.2rem;
      height: 1.5rem;
      margin-top: -1pt;
    }

    .level-label,
    .xp-label,
    .proficiency-label {
      margin-left: 0.3rem;
    }
  `

  return (
    <>
      <div class="level-row">
        <div class="level-cell">
          <NumberInput
            label={t('level')}
            max={20}
            min={0}
            onChange={props.onChangeLevel}
            value={props.level}
          />
          <span class="level-label">{t('level')}</span>
        </div>
        <div class="xp-cell">
          <span class="xp">{props.xp}</span>
          <span class="xp-label">exp</span>
        </div>
      </div>
      <div class="proficiency-row">
        <NumberInput label={t('proficiency_bonus')} value={props.proficiency} />
        <span class="proficiency-label">{t('proficiency_bonus')}</span>
      </div>
    </>
  )
}

const HitPoints: Component<{ current: number; max: number; temp: number }> = (
  props
) => {
  css`
    .row {
      display: grid;
      grid-template-columns: min-content;
      grid-template-areas:
        'hit-points max-hp    plus  temp-hp'
        '.          max-label .     temp-label';
      padding: 0.2rem;
      align-items: end;
      margin: auto;
    }

    .hit-points {
      grid-area: hit-points;
    }
    .max-hp {
      grid-area: max-hp;
    }
    .plus {
      grid-area: plus;
    }
    .temp-hp {
      grid-area: temp-hp;
    }
    .max-label {
      grid-area: max-label;
    }
    .temp-label {
      grid-area: temp-label;
    }

    .hit-points,
    .temp-hp {
      font-size: 2rem;
      padding: 0 0.2rem;
    }

    .temp-label,
    .max-label {
      text-transform: uppercase;
      font-size: 0.7rem;
      color: #bbb;
    }

    .plus {
      margin: 0 0.5rem;
      align-self: center;
    }
  `

  return (
    <div class="row">
      <span class="hit-points">{props.current}</span>
      <span class="max-hp">/ {props.max}</span>
      <span class="max-label">max</span>
      <span class="plus">+</span>
      {/* <Show when={props.temp > 0}> */}
      <span class="temp-hp">{props.temp}</span>
      <span class="temp-label">temp</span>
      {/* </Show> */}
    </div>
  )
}

const ClassTable: Component<{ classes: JSXElement[] }> = (props) => {
  css`
    ul {
      --border-size: 2pt;

      border: var(--border-size) solid black;
      padding: 0 0.3rem;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    ul > li {
      list-style: none;
      flex-grow: 1;
      display: flex;
      align-content: center;
    }

    ul > li + li {
      border-top: 1px solid black;
    }
  `

  return (
    <ul>
      <For each={props.classes}>{(child) => <li>{child}</li>}</For>
    </ul>
  )
}

const ClassName: Component<{
  icon: string
  name: string
  level: number
  onChangeLevel?: (level: number) => void
  onChangeName: (className: string) => void
}> = (props) => {
  css`
    .row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.3rem;
      margin: 0.3rem 0;
    }

    .icon {
    }

    .name {
      font-size: 2rem;
      width: 100%;
    }

    .level {
      font-size: 2rem;
    }
  `

  return (
    <div class="row">
      <Show when={props.onChangeLevel}>
        <NumberInput
          label={t('class_level', { class: props.name })}
          max={20}
          min={0}
          onChange={props.onChangeLevel}
          value={props.level}
        />
      </Show>
      <span class="icon">{props.icon}</span>
      <Editable
        class={'name'}
        label={t('class')}
        onChange={props.onChangeName}
        value={props.name}
      />
    </div>
  )
}

const ClassHitDice: Component<{ total: number; type: string; used: number }> = (
  props
) => {
  css`
    .row {
      display: flex;
      padding: 0.2rem;
      align-items: center;
      gap: 0.3rem;
      padding: 0.3rem;
    }

    .used {
      font-size: 2rem;
    }

    .total {
      align-self: end;
    }
  `

  return (
    <div class="row">
      <span class="used">{props.total - props.used}</span>
      <span class="total">/ {props.total}</span>
      <span class="type">{props.type}</span>
    </div>
  )
}

export const CharacterSheet: Component<{
  character: ResolvedCharacter
  updateCharacter: UpdateCharacterFunction
}> = (props) => {
  css`
    .sheet {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: 1fr min-content auto;
      grid-template-areas:
        'portrait   status    status'
        'passive    abilities shortcuts';
      gap: 2mm;
    }

    #portrait {
      grid-area: portrait;
    }
    #passive {
      grid-area: passive;
    }
    #level {
      grid-area: level;
    }
    #classes {
      grid-area: classes;
    }
    #hit-points {
      grid-area: hit-points;
    }
    #hit-dice {
      grid-area: hit-dice;
    }
    #abilities {
      grid-area: abilities;
    }
    #shortcuts {
      grid-area: shortcuts;
    }

    #status {
      grid-area: status;
    }

    #status {
      display: grid;

      grid-template-columns: repeat(3, 1fr) 1fr;
      grid-template-rows: auto min-content;
      grid-template-areas:
        'classes classes classes    hit-dice'
        'level   level   conditions hit-points';
      gap: 2mm;
    }

    #level,
    #conditions,
    #hit-points {
      align-self: stretch;
    }

    #classes,
    #hit-dice {
      align-self: end;
    }

    header {
      display: flex;
      grid-area: header;
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

    .flex-container {
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

    .scores,
    .skills,
    .saving_throws {
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

  // // Mock multiclassing
  const mockedHitDice = {
    total: props.character.level ?? 0,
    type: 'd8',
    used: 1,
  }

  return (
    <section class="sheet">
      <section id="portrait" class="flex-container">
        <Portrait />
        <Box>
          <Editable
            label={t('character_name')}
            onChange={(name: string) =>
              props.updateCharacter((character) => (character.name = name))
            }
            value={props.character.name}
          />
          <Editable
            label={t('player_name')}
            onChange={(name: string) =>
              props.updateCharacter(
                (character) => (character.player.name = name)
              )
            }
            value={props.character.player.name}
          />
          <Editable
            label={t('party_name')}
            onChange={(name: string) =>
              props.updateCharacter(
                (character) => (character.party.name = name)
              )
            }
            value={props.character.party.name}
          />
        </Box>
      </section>
      <section id="passive">
        <div class="flex-container">
          <Box>
            <h1>{t('appearance')}</h1>
            <Editable
              label={t('race')}
              onChange={(race: string) =>
                props.updateCharacter(
                  (character) => (character.data.race = race)
                )
              }
              value={props.character.data.race}
            />
          </Box>
          <Box>
            <h1>{t('personality')}</h1>
            <Editable
              label={t('background')}
              onChange={(background: string) =>
                props.updateCharacter(
                  (character) => (character.data.background = background)
                )
              }
              value={props.character.data.background}
            />
            <div>
              <h2>{t('personality')}</h2>
              <MarkdownRenderedEditableBox
                id="personality"
                text={props.character.data.personality}
                onChange={(personality: string) =>
                  props.updateCharacter(
                    (character) => (character.data.personality = personality)
                  )
                }
              />
            </div>
            <div>
              <h2>{t('ideals')}</h2>
              <MarkdownRenderedEditableBox
                id="ideals"
                text={props.character.data.ideals}
                onChange={(ideals: string) =>
                  props.updateCharacter(
                    (character) => (character.data.ideals = ideals)
                  )
                }
              />
            </div>
            <div>
              <h2>{t('bonds')}</h2>
              <MarkdownRenderedEditableBox
                id="bonds"
                text={props.character.data.bonds}
                onChange={(bonds: string) =>
                  props.updateCharacter(
                    (character) => (character.data.bonds = bonds)
                  )
                }
              />
            </div>
            <div>
              <h2>{t('flaws')}</h2>
              <MarkdownRenderedEditableBox
                id="flaws"
                text={props.character.data.flaws}
                onChange={(flaws: string) =>
                  props.updateCharacter(
                    (character) => (character.data.flaws = flaws)
                  )
                }
              />
            </div>
          </Box>
          <Box>
            <TrayBox
              label={t('passive_perception')}
              value={props.character.data.passive_perception}
            />
            <TrayBox
              label={t('passive_investigation')}
              value={0 /*props.character.data.passive_investigation*/}
            />
            <TrayBox
              label={t('passive_insight')}
              value={0 /*props.character.data.passive_insight*/}
            />
            <TrayBox
              label={t('darkvision')}
              value={props.character.data.darkvision ? '🌖' : '🌑'}
              onChange={() =>
                props.updateCharacter(
                  (character) =>
                    (character.data.darkvision = !character.data.darkvision)
                )
              }
            />
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
            />
          </Box>
        </div>
      </section>
      <section id="status">
        <section id="level">
          <Level
            level={props.character.data.classes.reduce(
              (sum, c) => sum + (c.level ?? 0),
              0
            )}
            onChangeLevel={
              props.character.data.classes.length === 1
                ? (level: number) =>
                    props.updateCharacter(
                      (character) => (character.data.classes[0].level = level)
                    )
                : undefined
            }
            onChangeXp={(xp: number) =>
              props.updateCharacter((character) => (character.data.xp = xp))
            }
            proficiency={props.character.data.proficiency_bonus}
            xp={props.character.data.xp}
          />
        </section>
        <section id="classes">
          <ClassTable
            classes={props.character.data.classes.map((class_, index) => (
              <ClassName
                icon={class_.name === 'guerrier' ? '⚔️' : '🛠️'}
                name={class_.name}
                level={class_.level ?? 0}
                onChangeLevel={
                  props.character.data.classes.length === 1
                    ? undefined
                    : (level) =>
                        props.updateCharacter(
                          (character) =>
                            (character.data.classes[index].level = level)
                        )
                }
                onChangeName={(className) =>
                  props.updateCharacter(
                    (character) =>
                      (character.data.classes[index].name = className)
                  )
                }
              />
            ))}
          />
        </section>
        <section id="conditions">
          <div>conditions</div>
        </section>
        <section id="hit-points">
          <Box>
            <HitPoints {...props.character.data.hp} />
          </Box>
        </section>
        <section id="hit-dice">
          <ClassTable
            classes={props.character.data.classes.map(() => (
              <ClassHitDice {...mockedHitDice} />
            ))}
          />
        </section>
      </section>
      <section id="abilities" class="flex-container">
        <div class="flex-container horizontal-container">
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
                  modifier={props.character.data.abilities[ability].modifier}
                  onChange={(score: number) => {
                    props.updateCharacter(
                      (character) =>
                        (character.data.abilities[ability].score = Number.isNaN(
                          score
                        )
                          ? 0
                          : score)
                    )
                  }}
                />
              )}
            </For>
          </div>
          <div class="attr-applications">
            <LabelledBox label={t('saving_throws')}>
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
            </LabelledBox>
            <LabelledBox label={t('skills')}>
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
            </LabelledBox>
          </div>
        </div>
      </section>
      <section id="shortcuts">
        <Box>shortcuts</Box>
      </section>
      {/*       
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
            // TEMP We currently do not support display multiple classes/levels, so we only display the first one
            value={`${props.character.data.classes[0].name} ${props.character.data.classes[0].level}`}
            onChange={(classAndLevel: string) => {
              props.updateCharacter((character) => {
                const lastSpaceIndex = classAndLevel.lastIndexOf(' ')
                character.data.classes[0].name = classAndLevel
                  .slice(0, lastSpaceIndex)
                  .trim()
                character.data.classes[0].level =
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
            placeholder={t('player_mcplayerface')}
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
            <LabelledBox label={t('saving_throws')}>
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
            </LabelledBox>
            <LabelledBox label={t('skills')}>
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
            </LabelledBox>
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
          <LabelledBox label={t('other_proficiencies_and_languages')}>
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
          </LabelledBox>
        </div>
      </section>
      <section class="combat-stats flex-container">
        <LabelledBox label={t('current_hit_points')}></LabelledBox>
      </section>
      <section class="actions flex-container">
        <LabelledBox label={t('attacks')}></LabelledBox>
      </section>
      <section class="equipment flex-container">
        <LabelledBox label={t('equipment')}>
          <MarkdownRenderedEditableBox
            id="inventory"
            text={props.character.data.inventory || ''}
            onChange={(inventory: string) =>
              props.updateCharacter(
                (character) => (character.data.inventory = inventory)
              )
            }
          ></MarkdownRenderedEditableBox>
        </LabelledBox>
      </section>
      <section class="flavor flex-container">
        <BorderBox>
          <LabelledBox label={t('personality')}>
            <MarkdownRenderedEditableBox
              id="personality"
              text={props.character.data?.personality || ''}
              onChange={(personality: string) =>
                props.updateCharacter(
                  (character) => (character.data.personality = personality)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabelledBox>
          <LabelledBox label={t('ideals')}>
            <MarkdownRenderedEditableBox
              id="ideals"
              text={props.character.data?.ideals || ''}
              onChange={(ideals: string) =>
                props.updateCharacter(
                  (character) => (character.data.ideals = ideals)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabelledBox>
          <LabelledBox label={t('bonds')}>
            <MarkdownRenderedEditableBox
              id="bonds"
              text={props.character.data?.bonds || ''}
              onChange={(bonds: string) =>
                props.updateCharacter(
                  (character) => (character.data.bonds = bonds)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabelledBox>
          <LabelledBox label={t('flaws')}>
            <MarkdownRenderedEditableBox
              id="flaws"
              text={props.character.data?.flaws || ''}
              onChange={(flaws: string) =>
                props.updateCharacter(
                  (character) => (character.data.flaws = flaws)
                )
              }
            ></MarkdownRenderedEditableBox>
          </LabelledBox>
        </BorderBox>
      </section>
      <section class="features_and_traits flex-container">
        <LabelledBox label={t('features_&_traits')}>
          <MarkdownRenderedEditableBox
            id="features-traits"
            text={props.character.data?.features || ''}
            onChange={(features: string) =>
              props.updateCharacter(
                (character) => (character.data.features = features)
              )
            }
          ></MarkdownRenderedEditableBox>
        </LabelledBox>
      </section> */}
    </section>
  )
}
