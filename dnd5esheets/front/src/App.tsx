import { Route, Router, Routes } from '@solidjs/router'
import type { Component } from 'solid-js'
import { I18nContext } from '@solid-primitives/i18n'
import { StyleData, StyleRegistry, css } from 'solid-styled'
import { MetaProvider } from '@solidjs/meta'

import HomePage from '~/routes'
import CharacterListPage from '~/routes/characters'
import CharacterSheetPage from '~/routes/characters/[slug]'
import { i18nContext } from '~/i18n'

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

const App: Component = () => {
  const sheets: StyleData[] = []

  return (
    <MetaProvider>
      <I18nContext.Provider value={i18nContext}>
        <StyleRegistry styles={sheets}>
          <GlobalStyles />
          <Router>
            <header>
              <h1>D&D 5e sheets</h1>
            </header>
            <Routes>
              <Route path="/" component={HomePage} />
              <Route path="/characters" component={CharacterListPage} />
              <Route path="/characters/:slug" component={CharacterSheetPage} />
            </Routes>
          </Router>
        </StyleRegistry>
      </I18nContext.Provider>
    </MetaProvider>
  )
}

export default App
