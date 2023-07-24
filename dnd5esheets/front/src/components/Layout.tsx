import { css } from 'solid-styled'

export function Layout({ children }: any) {
  css`
    main {
      margin: 20vh 0;
    }
  `
  return <main>{children}</main>
}
