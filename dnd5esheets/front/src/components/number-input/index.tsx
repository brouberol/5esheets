import { css } from 'solid-styled'
import * as numberInput from '@zag-js/number-input'
import { normalizeProps, useMachine } from '@zag-js/solid'
import {
  Component,
  Show,
  createEffect,
  createMemo,
  createUniqueId,
} from 'solid-js'

import { Minus } from '~/components/icons/minus'
import { Plus } from '~/components/icons/plus'
import { getHoverCard } from '~/components/hover-card'

export const NumberInput: Component<{
  iconSize?: string
  label: string
  max?: number
  min?: number
  onChange?: (value: number) => void
  value: number
}> = (props) => {
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
      font-size: 1em;
      font-family: inherit;

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

  const hoverCard = getHoverCard()

  return (
    <div {...{ ...inputApi().rootProps, ...hoverCard.triggerProps }}>
      <input {...inputApi().inputProps} />
      <Show when={props.onChange}>
        <button {...inputApi().decrementTriggerProps}>
          <Minus size={iconSize} />
        </button>
        <button {...inputApi().incrementTriggerProps}>
          <Plus size={iconSize} />
        </button>
      </Show>
      <hoverCard.component>{props.label}</hoverCard.component>
    </div>
  )
}
