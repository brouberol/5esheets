import { Component } from 'solid-js'
import { css } from 'solid-styled'

const ScoreBox: Component<{
  label: string
  score: number
  modifier: number
  onChange: (update: number) => void
}> = (props) => {
  css`
    .score-box {
      width: 16mm;
      display: flex;
      flex-direction: column;
      border: 1px solid black;
      padding: 2mm 0;
      gap: 2mm;
      margin-bottom: 2mm;
      align-items: center;
    }

    label {
      text-transform: uppercase;
      font-size: 0.8rem;
      font-family: var(--font-family-headings);
      text-align: center;
    }

    .score,
    .modifier {
      outline: none;
      text-align: center;
    }

    .score {
      font-size: 20pt;
      width: 100%;
      border: none;
      background: none;
      font-family: var(--font-family-text);
      overflow: visible;
    }

    .modifier {
      width: 8mm;
      height: 2rem;
      margin-bottom: -1rem;
      background: white;
      border: 1px solid black;
      line-height: 2rem;
      color: unset;
      font-family: var(--font-family-text);
    }
  `

  const actions = {
    ArrowUp: (score: number) => score + 1,
    ArrowDown: (score: number) => score - 1,
  } as const

  const formatModifier = (mod: number): string =>
    mod > 0 ? `+${mod}` : `${mod}`

  return (
    <div class="score-box">
      <label>{props.label}</label>
      <input
        class="score"
        type="text"
        value={props.score}
        oninput={(event) => props.onChange(parseInt(event.target.value ?? '0'))}
        onkeydown={(event) =>
          event.key in actions &&
          props.onChange(actions[event.key](props.score))
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

export default ScoreBox
