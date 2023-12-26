import { Route, Router } from '@solidjs/router'
import type { Component, ParentComponent } from 'solid-js'
import { StyleData, StyleRegistry, css } from 'solid-styled'
import { MetaProvider } from '@solidjs/meta'

import { HomePage } from '~/routes'
import { CharacterListPage } from '~/routes/characters'
import { CharacterSheetPage } from '~/routes/characters/[slug]'

function GlobalStyles() {
  css`
    @global {
      * {
        margin: 0;
        box-sizing: border-box;
      }

      html {
        padding: 4mm;
      }

      body {
        width: 100%;
        max-width: 700pt;
        margin: auto;
      }

      :root {
        --border-static-color: rgb(220, 220, 220);
        --border-hover-color: rgb(255, 49, 90);
        --border-focus-color: rgb(255, 49, 90);
        --border-active-color: rgb(255, 49, 90);
        --border-inactive-color: rgb(200, 200, 200);

        --font-family-text: 'Bookinsanity';
        --font-family-headings: 'MrEaves';

        --font-color-dim: rgb(190, 190, 190);
      }

      @font-face {
        font-family: 'Bookinsanity';
        src: url('/assets/font/Bookinsanity.otf');
      }

      @font-face {
        font-family: 'MrEaves';
        src: url('/assets/font/Mr Eaves Small Caps.otf');
      }

      .hidden {
        display: none;
      }
    }
  `
  return null
}

const Header: ParentComponent = (props) => (
  <>
    <header>
      <h1>D&D 5e sheets</h1>
    </header>
    {props.children}
  </>
)

const App: Component = () => {
  const sheets: StyleData[] = []

  return (
    <MetaProvider>
      <StyleRegistry styles={sheets}>
        <GlobalStyles />
        <Router>
          <Route path="/" component={Header}>
            <Route path="/" component={HomePage} />
            <Route path="/characters">
              <Route path="/" component={CharacterListPage} />
              <Route path="/:slug" component={CharacterSheetPage} />
            </Route>
          </Route>
        </Router>
      </StyleRegistry>
    </MetaProvider>
  )
}

export default App
