import { For, splitProps } from 'solid-js'
import { Dynamic } from 'solid-js/web'

const defaultAttributes = {
  xmlns: 'http://www.w3.org/2000/svg',
  width: 24,
  height: 24,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  'stroke-width': 2,
  'stroke-linecap': 'round',
  'stroke-linejoin': 'round',
} as const

export interface IconProps {
  color?: string
  size?: string
  strokeWidth?: string
  children?: string
  class?: string
  name?: string
  iconNode?: IconNode
  absoluteStrokeWidth?: string
}

export type IconNode = [string, { d: string; key: string }][]

/**
 * Converts string to KebabCase
 * Copied from scripts/helper. If anyone knows how to properly import it here
 * then please fix it.
 *
 * @param {string} string
 * @returns {string} A kebabized string
 */
export const toKebabCase = (string: string) =>
  string.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase()

const Icon = (props: IconProps) => {
  const [localProps, rest] = splitProps(props, [
    'color',
    'size',
    'strokeWidth',
    'children',
    'class',
    'name',
    'iconNode',
    'absoluteStrokeWidth',
  ])
  return (
    <svg
      {...defaultAttributes}
      width={localProps.size ?? defaultAttributes.width}
      height={localProps.size ?? defaultAttributes.height}
      stroke={localProps.color ?? defaultAttributes.stroke}
      stroke-width={
        localProps.absoluteStrokeWidth
          ? (Number(
              localProps.strokeWidth ?? defaultAttributes['stroke-width']
            ) *
              24) /
            Number(localProps.size)
          : Number(localProps.strokeWidth ?? defaultAttributes['stroke-width'])
      }
      class={`lucide lucide-${toKebabCase(localProps?.name ?? 'icon')} ${
        localProps.class != null ? localProps.class : ''
      }`}
      {...rest}
    >
      <For each={localProps.iconNode}>
        {([elementName, attrs]) => {
          return <Dynamic component={elementName} {...attrs} />
        }}
      </For>
    </svg>
  )
}
export default Icon
