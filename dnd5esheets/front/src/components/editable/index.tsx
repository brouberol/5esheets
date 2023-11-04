import { css } from 'solid-styled'
import * as editable from '@zag-js/editable'
import { normalizeProps, useMachine } from '@zag-js/solid'
import { Component, createEffect, createMemo, createUniqueId } from 'solid-js'

import { getHoverCard } from '~/components/hover-card'

export const Editable: Component<{
  class?: string
  label: string
  onChange?: (value: string) => void
  value: string
}> = (props) => {
  css`
    * {
      box-sizing: border-box;
    }

    [data-part='preview'] {
      display: block;
    }

    [data-part='input']::placeholder,
    [data-placeholder-shown] {
      color: gray;
    }

    [data-part='area'] {
      --line-height: 1.5em;
      border: none;
      outline: none;
      font-family: inherit;
      font-size: inherit;
      border-bottom: 2pt solid #eee;
      padding: 0;
      display: flex;
      align-items: end;
    }

    [data-part='area']:hover {
      border-bottom: 2pt solid black;
    }

    [data-part='area'][data-focus] {
      border-bottom: 2pt solid red;
    }
  `

  const [editableState, editableSend] = useMachine(
    editable.machine({
      autoResize: true,
      id: createUniqueId(),
      onValueChange: ({ value }) =>
        props.onChange ? props.onChange(value) : null,
      placeholder: props.label,
      value: props.value,
    })
  )

  const editableApi = createMemo(() =>
    editable.connect(editableState, editableSend, normalizeProps)
  )
  createEffect(() => editableApi().setValue(props.value))

  const hoverCard = getHoverCard()

  return (
    <div
      {...{ ...editableApi().rootProps, ...hoverCard.triggerProps }}
      class={props.class}
    >
      <div {...editableApi().areaProps}>
        <input {...editableApi().inputProps} />
        <div {...editableApi().previewProps} />
      </div>
      <hoverCard.component>{props.label}</hoverCard.component>
    </div>
  )
}
