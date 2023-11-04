import type { Meta, StoryObj } from 'storybook-solidjs'

import { Editable } from './index'

import { createControlledSignal } from '~/storybook/helper'

const meta: Meta<typeof Editable> = {
  title: 'Editable',
  component: Editable,
  tags: ['autodocs'],
  render: (props) => {
    const [value, setValue] = createControlledSignal('value')

    return <Editable {...props} value={value()} onChange={setValue} />
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Nominal: Story = {
  args: {
    label: 'name',
    value: 'Douglas',
  },
}

export const Small: Story = {
  name: 'Small editable (10pt)',
  args: Nominal.args,
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '10pt' }}>
        <Story />
      </div>
    ),
  ],
}

export const Medium: Story = {
  name: 'Medium editable (16pt)',
  args: Nominal.args,
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '16pt' }}>
        <Story />
      </div>
    ),
  ],
}

export const Large: Story = {
  name: 'Large editable (20pt)',
  args: Nominal.args,
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '20pt' }}>
        <Story />
      </div>
    ),
  ],
}

export const Huge: Story = {
  name: 'Huge editable (50pt)',
  args: Nominal.args,
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '50pt' }}>
        <Story />
      </div>
    ),
  ],
}
