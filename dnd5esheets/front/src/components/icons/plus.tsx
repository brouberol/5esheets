import Icon, { IconNode, IconProps } from './icon'
const iconNode: IconNode = [
  ['path', { d: 'M5 12h14', key: '1ays0h' }],
  ['path', { d: 'M12 5v14', key: 's699le' }],
]
const Plus = (props: IconProps) => (
  <Icon {...props} name="Plus" iconNode={iconNode} />
)
export { Plus }
