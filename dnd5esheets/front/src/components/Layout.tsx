import { ParentComponent } from 'solid-js'
import { css } from 'solid-styled'

export const Layout: ParentComponent = (props) => {
  css`
    main {
      margin: 20vh 0;
    }
  `
  return <main>{props.children}</main>
}
