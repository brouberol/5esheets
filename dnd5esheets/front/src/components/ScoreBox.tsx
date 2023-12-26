import { Component } from 'solid-js'
import { css } from 'solid-styled'

export const ScoreBox: Component<{
  ability: string
  label: string
  score: number
  modifier: number
  onChange: (update: number) => void
}> = (props) => {
  css`
    label {
      text-transform: uppercase;
      font-size: 0.8rem;
      font-family: var(--font-family-headings);
      font-weight: bold;
      text-align: center;
    }

    .score,
    .modifier {
      outline: none;
      text-align: center;
      border: none;
      background: none;
      font-family: var(--font-family-text);
    }

    .score {
      font-size: 20pt;
      width: 100%;
      background: none;
      overflow: visible;
    }

    .modifier {
      width: 3rem;
      color: unset;

      position: absolute;
      bottom: 1.2mm;
    }

    .score-box {
      background: no-repeat center;
      background-size: 100% auto;

      width: 19mm;
      height: 22mm;
      padding-top: 2mm;
      padding-bottom: 1mm;

      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1mm;

      position: relative;
    }

    .strength {
      background: url(/assets/border-ability-strength.svg);
    }
    .dexterity {
      background: url(/assets/border-ability-dexterity.svg);
    }
    .constitution {
      background: url(/assets/border-ability-constitution.svg);
    }
    .intelligence {
      background: url(/assets/border-ability-intelligence.svg);
    }
    .wisdom {
      background: url(/assets/border-ability-wisdom.svg);
    }
    .charisma {
      background: url(/assets/border-ability-charisma.svg);
    }
  `

  const actions = {
    ArrowUp: (score: number) => score + 1,
    ArrowDown: (score: number) => score - 1,
  } as const

  const formatModifier = (mod: number): string =>
    mod > 0 ? `+${mod}` : `${mod}`

  function isKeyOf<T extends object>(obj: T, key: PropertyKey): key is keyof T {
    return Object.prototype.hasOwnProperty.call(obj, key)
  }

  return (
    <div class={`score-box ${props.ability}`}>
      <label>{props.label}</label>
      <input
        class="score"
        type="text"
        value={props.score}
        oninput={(event) => props.onChange(parseInt(event.target.value ?? '0'))}
        onkeydown={({ key }) =>
          isKeyOf(actions, key)
            ? props.onChange(actions[key](props.score))
            : null
        }
      />

      <input
        class="modifier"
        type="text"
        value={formatModifier(props.modifier)}
        disabled
      />
    </div>
  )
}
