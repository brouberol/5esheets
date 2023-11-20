import Icon, { IconNode, IconProps } from './icon'

const iconNode: IconNode = [['path', { d: 'M5 12h14', key: '1ays0h' }]]
const Minus = (props: IconProps) => (
  <Icon {...props} name="Minus" iconNode={iconNode} />
)
export { Minus }
