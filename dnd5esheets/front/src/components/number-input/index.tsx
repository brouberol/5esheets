import { css } from 'solid-styled'
import * as numberInput from '@zag-js/number-input'
import * as hoverCard from '@zag-js/hover-card'
import { normalizeProps, useMachine } from '@zag-js/solid'
import { Show, createEffect, createMemo, createUniqueId } from 'solid-js'
import { Portal } from 'solid-js/web'

import { Minus } from '~/components/icons/minus'
import { Plus } from '~/components/icons/plus'

export default function NumberInput(props: {
  iconSize?: string
  label: string
  max?: number
  min?: number
  onChange?: (value: number) => void
  value: number
}) {
  const { iconSize = '1rem' } = props

  css`
    * {
      box-sizing: border-box;
    }

    div {
      --border-size: 2pt;
      --button-size: calc(${iconSize} * 2);
      display: inline-block;

      position: relative;
    }

    input {
      font-weight: bold;
      font-size: 1em;

      width: 2em;
      height: 2em;

      border: var(--border-size) solid black;
      border-radius: 50%;
      outline: none;

      text-align: center;
      caret-color: transparent;
    }

    input:focus {
      color: red;
      border-color: red;
    }

    button {
      font-weight: bold;

      width: var(--button-size);
      height: var(--button-size);

      display: flex;
      justify-content: center;
      align-items: center;

      padding: 0;
      border: 0;

      border-radius: 50%;

      text-align: center;
      position: absolute;
    }

    /* animation */
    button {
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.5s;
    }

    button:hover,
    div:hover button,
    input:focus ~ button {
      opacity: 1;
      pointer-events: auto;
      transition: opacity 0.5s;
    }

    /* TODO hover, focus, active etc... */

    button[data-part='increment-trigger'] {
      top: calc(50% - var(--button-size) / 2);
      left: calc(100% - min(var(--button-size) * 0.7, 20%));
    }

    button[data-part='decrement-trigger'] {
      top: calc(50% - var(--button-size) / 2);
      right: calc(100% - min(var(--button-size) * 0.7, 20%));
    }

    [data-part='positioner'] {
      position: absolute;
      top: var(--y);
      left: var(--x);
    }

    [data-part='content'] {
      animation: appear 0.5s linear;

      font-size: 1rem;
      background-color: #000;
      color: #fff;
      padding: 0.5em;
      border-radius: 0.3em;
    }

    @keyframes appear {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  `

  const [inputState, inputSend] = useMachine(
    numberInput.machine({
      id: createUniqueId(),
      value: props.value.toString(),
      onValueChange: (details) =>
        props.onChange ? props.onChange(details.valueAsNumber) : null,
      min: props.min,
      max: props.max,
    })
  )

  const inputApi = createMemo(() =>
    numberInput.connect(inputState, inputSend, normalizeProps)
  )
  createEffect(() => inputApi().setValue(props.value))

  const [hoverCardState, hoverCardSend] = useMachine(
    hoverCard.machine({
      id: createUniqueId(),
    })
  )
  const hoverCardApi = createMemo(() =>
    hoverCard.connect(hoverCardState, hoverCardSend, normalizeProps)
  )

  return (
    <div {...{ ...inputApi().rootProps, ...hoverCardApi().triggerProps }}>
      <input {...inputApi().inputProps} />
      <button {...inputApi().decrementTriggerProps}>
        <Minus size={iconSize} />
      </button>
      <button {...inputApi().incrementTriggerProps}>
        <Plus size={iconSize} />
      </button>
      <Show when={hoverCardApi().isOpen}>
        <Portal>
          <div {...hoverCardApi().positionerProps}>
            <div {...hoverCardApi().arrowProps}>
              <div {...hoverCardApi().arrowTipProps} />
            </div>
            <div {...hoverCardApi().contentProps}>{props.label}</div>
          </div>
        </Portal>
      </Show>
    </div>
  )
}
