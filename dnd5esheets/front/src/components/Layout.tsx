import { JSX } from 'solid-js'
import { css } from 'solid-styled'

export function Layout({ children }: { children: JSX.Element }) {
  css`
    main {
      margin: 20vh 0;
    }
  `
  return <main>{children}</main>
}
