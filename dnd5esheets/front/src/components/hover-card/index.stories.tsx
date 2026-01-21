import type { Meta, StoryObj } from 'storybook-solidjs'

import { getHoverCard, HoverCard } from './index'

const meta: Meta<HoverCard> = {
  title: 'HoverCard',
  tags: ['autodocs'],
  render: () => {
    const hoverCard = getHoverCard()
    return (
      <>
        <div {...hoverCard.triggerProps}>hover me</div>
        <hoverCard.component>card content</hoverCard.component>
      </>
    )
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Nominal: Story = {
  args: {},
}
