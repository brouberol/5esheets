import type { Meta, StoryObj } from 'storybook-solidjs'

import NumberInput from './index'

import { createControlledSignal } from '~/storybook/helper'

const meta: Meta<typeof NumberInput> = {
  title: 'NumberInput',
  component: NumberInput,
  tags: ['autodocs'],
  render: (props) => {
    const [value, setValue] = createControlledSignal('value')

    return (
      <div>
        <NumberInput {...props} value={value()} onChange={setValue} />
      </div>
    )
  },
}

export default meta
type Story = StoryObj<typeof meta>

export const Nominal: Story = {
  args: {
    label: 'level',
    max: 20,
    min: 0,
    value: 10,
  },
}

export const Small: Story = {
  name: 'Small input (10pt)',
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
  name: 'Medium input (16pt)',
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
  name: 'Large input (20pt)',
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
  name: 'Huge input (50pt)',
  args: Nominal.args,
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '50pt' }}>
        <Story />
      </div>
    ),
  ],
}

export const SmallLargeButton: Story = {
  name: 'Small input (10pt), large button (3rem)',
  args: { iconSize: '6rem', ...Nominal.args },
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '10pt' }}>
        <Story />
      </div>
    ),
  ],
}

export const MediumLargeButton: Story = {
  name: 'Medium input (16pt), large button (3rem)',
  args: { iconSize: '6rem', ...Nominal.args },
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '16pt' }}>
        <Story />
      </div>
    ),
  ],
}

export const LargeLargeButton: Story = {
  name: 'Large input (20pt), large button (3rem)',
  args: { iconSize: '6rem', ...Nominal.args },
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '20pt' }}>
        <Story />
      </div>
    ),
  ],
}

export const HugeLargeButton: Story = {
  name: 'Huge input (50pt), large button (3rem)',
  args: { iconSize: '6rem', ...Nominal.args },
  decorators: [
    (Story) => (
      <div style={{ 'font-size': '50pt' }}>
        <Story />
      </div>
    ),
  ],
}
