import { css } from 'solid-styled'
import * as hoverCard from '@zag-js/hover-card'
import { normalizeProps, useMachine } from '@zag-js/solid'
import { ParentComponent, Show, createMemo, createUniqueId } from 'solid-js'
import { Portal } from 'solid-js/web'

export type HoverCard = ParentComponent

export const getHoverCard: () => {
  triggerProps: hoverCard.Api['triggerProps']
  component: ParentComponent
} = () => {
  css`
    * {
      box-sizing: border-box;
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
  `

  const [hoverCardState, hoverCardSend] = useMachine(
    hoverCard.machine({
      id: createUniqueId(),
    })
  )
  const hoverCardApi = createMemo(() =>
    hoverCard.connect(hoverCardState, hoverCardSend, normalizeProps)
  )

  const component: HoverCard = (props) => (
    <Show when={hoverCardApi().isOpen}>
      <Portal>
        <div {...hoverCardApi().positionerProps}>
          <div {...hoverCardApi().arrowProps}>
            <div {...hoverCardApi().arrowTipProps} />
          </div>
          <div {...hoverCardApi().contentProps}>{props.children}</div>
        </div>
      </Portal>
    </Show>
  )

  return {
    triggerProps: hoverCardApi().triggerProps,
    component,
  }
}
