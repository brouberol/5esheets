import { Component } from 'solid-js'
import { css } from 'solid-styled'

const BorderBox: Component<{ children: any }> = ({ children }) => {
  css`
    .outer-box {
      --border-top: 10mm;
      --border-side: 10mm;
      --border-bottom: 10mm;
      --margin-top: 4mm;
      --margin-side: 0mm;
      --margin-bottom: 4mm;

      height: calc(100% - var(--border-top) - var(--border-bottom));
      width: calc(100% - 2 * var(--border-side));

      border-image: url(/src/assets/background-1.svg) 49.5% repeat;
      background: #deddde;
      border-style: solid;
      border-image-width: var(--border-top) var(--border-side)
        var(--border-bottom) var(--border-side);
      border-image-outset: calc(var(--border-top) - 1px)
        calc(var(--border-side) - 1px) calc(var(--border-bottom) - 1px)
        calc(var(--border-side) - 1px);
      margin: var(--border-top) var(--border-side) var(--border-bottom);
    }

    .inner-box {
      height: calc(
        100% - var(--margin-top) + var(--border-top) - var(--margin-bottom) +
          var(--border-bottom)
      );
      width: calc(100% - 2 * (var(--margin-side) - var(--border-side)));
      display: flex;
      flex-direction: column;
      margin-top: calc(var(--margin-top) - var(--border-top));
      margin-right: calc(var(--margin-side) - var(--border-side));
      margin-bottom: calc(var(--margin-bottom) - var(--border-bottom));
      margin-left: calc(var(--margin-side) - var(--border-side));
    }
  `

  return (
    <div class="outer-box">
      <div class="inner-box">{children}</div>
    </div>
  )
}

export default BorderBox
