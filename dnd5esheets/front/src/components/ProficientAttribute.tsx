import { createEffect, createSignal, Show } from 'solid-js'
import { css } from 'solid-styled'
import { cycleProficiency } from '~/store'
import { Proficiency } from '~/5esheets-client'

export default function ProficientAttribute(props: {
  id: string
  label: string
  labelSecondary?: string
  proficiency: Proficiency
  value: number
  onChange: (update: number) => void
}) {
  css`
    .attribute, .proficiency {
      display: flex;
      flex-direction: row
      align-items: baseline;
    }

    .attribute {
      gap: .5em;
      padding: 0 2mm;
    }

    .highlight {
      background: red;
    }

    .attribute:not(.highlight) {
      transition: background-color 5s;
    }

    .proficiency-master, .proficiency-expert {
      -webkit-appearance: none;
      appearance: none;
      background-color: #fff;

      color: currentColor;
      width: .9em;
      height: .9em;
      margin: auto 0;
      border: 1px solid currentColor;
      border-radius: 50%;
      transform: translateY(.15em);
      background: white;

      position: relative;

      outline: 2px solid white;
    }

    .proficiency-expert {
      color: var(--border-inactive-color);
      margin-left: -.15em;
      z-index: -1;
    }

    .proficiency-master:checked,
    .proficiency-expert:checked {
      color: currentColor;
      background: currentColor;
    }


    input.value {
      order: 1;
      border: none;
      border-bottom: 1px solid var(--border-static-color);
      padding: 3pt 0;
      outline: none;
      font-family: var(--font-family-text);
      width: 2em;
      text-align: right;
      background: none;
    }

    input.value:hover {
      border-bottom-color: var(--border-hover-color);
    }

    input.value:active {
      border-bottom-color: var(--border-active-color);
    }

    input.value:focus {
      border-bottom-color: var(--border-focus-color);
    }

    input.value:disabled {
      color: unset;
    }

    .name {
      text-transform: capitalize;
      font-size: 0.8rem;
      font-family: var(--font-family-text);
      order: 2
    }

    .secondary {
      color: var(--font-color-dim);
    }
  `

  const [highlight, setHighlight] = createSignal(false)

  createEffect((prevTimeout?: number) => {
    props.value // needed to trigger the effect at each value change
    if (prevTimeout) {
      setHighlight(true)
      clearTimeout(prevTimeout)
    }
    return setTimeout(() => setHighlight(false), 1000)
  })

  const formatModifier = (mod: number): string =>
    mod > 0 ? `+${mod}` : `${mod}`

  return (
    <div class={`attribute ${highlight() ? 'highlight' : ''}`}>
      <label for={props.id} class="name">
        {props.label}
        <Show when={props.labelSecondary}>
          {' '}
          <span class="secondary">({props.labelSecondary})</span>
        </Show>
      </label>
      <input
        class="value"
        type="text"
        name={props.id}
        value={formatModifier(props.value)}
        disabled
      />
      <label
        for={`${props.id}-master`}
        class="proficiency"
        onClick={() => props.onChange(cycleProficiency(props.proficiency))}
      >
        <input
          class="proficiency-master"
          name={`${props.id}-master`}
          type="checkbox"
          checked={props.proficiency >= 1}
        />
        <input
          class="proficiency-expert"
          name={`${props.id}-expert`}
          type="checkbox"
          checked={props.proficiency >= 2}
        />
      </label>
    </div>
  )
}
