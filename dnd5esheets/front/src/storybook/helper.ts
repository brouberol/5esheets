import { useArgs } from '@storybook/preview-api'
import { action } from '@storybook/addon-actions'
import { createEffect, createSignal } from 'solid-js'

export const createControlledSignal = (name: string) => {
  const [args, setArgs] = useArgs()
  const [value, setValue] = createSignal(args[name])

  // Propagate value from story control to component
  createEffect(() => {
    action('onChange')(args.value)
    setValue(args.value)
  }, [args.value])

  // Propagate value from component to store and story control
  const onChange = (value: typeof args.value) => {
    setArgs({ [name]: value })
    setValue(value)
  }

  return [value, onChange] as const
}
