// @refresh reload
import { Suspense } from "solid-js";
import {
  A,
  Body,
  ErrorBoundary,
  FileRoutes,
  Head,
  Html,
  Meta,
  Routes,
  Scripts,
  Title,
} from "solid-start";
import { css, StyleRegistry, type StyleData } from "solid-styled";
import { I18nContext } from "@solid-primitives/i18n";

import { i18nContext } from "~/i18n";

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

        --font-family-text: "Bookinsanity";
        --font-family-headings: "MrEaves";

        --font-color-dim: rgb(190, 190, 190);
      }

      @font-face {
        font-family: "Bookinsanity";
        src: url("/public/font/Bookinsanity.otf");
      }

      @font-face {
        font-family: "MrEaves";
        src: url("/public/font/Mr Eaves Small Caps.otf");
      }
    }
  `;
  return null;
}

export default function Root() {
  const sheets: StyleData[] = [];

  return (
    <StyleRegistry styles={sheets}>
      <Html lang="en">
        <Head>
          <Title>D&D 5e sheets</Title>
          <Meta charset="utf-8" />
          <Meta name="viewport" content="width=device-width, initial-scale=1" />
        </Head>
        <Body>
          <GlobalStyles />
          <I18nContext.Provider value={i18nContext}>
            <Suspense>
              <ErrorBoundary>
                <Routes>
                  <FileRoutes />
                </Routes>
              </ErrorBoundary>
            </Suspense>
          </I18nContext.Provider>
          <Scripts />
        </Body>
      </Html>
    </StyleRegistry>
  );
}
