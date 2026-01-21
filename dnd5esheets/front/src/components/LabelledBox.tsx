import { ParentComponent } from 'solid-js'
import { css } from 'solid-styled'

export const LabelledBox: ParentComponent<{ label: string }> = (props) => {
  css`
    .border-box,
    inner-box {
      height: 100%;
      width: 100%;
    }

    .border-box {
      border-image: url(/assets/border-1.svg) 48% stretch;

      --border-top: 16mm;
      --border-side: 6mm;
      --border-bottom: 16mm;
      --margin-top: 1mm;
      --margin-side: 1mm;
      --margin-bottom: 1mm;

      border-style: solid;
      border-width: var(--border-top) var(--border-side) var(--border-bottom)
        var(--border-side);

      position: relative;
      z-index: 1000;
    }

    .border-box .inner-box {
      display: flex;
      flex-direction: column;
      gap: 3pt;

      margin-top: calc(var(--margin-top) - var(--border-top));
      margin-right: calc(var(--margin-side) - var(--border-side));
      margin-bottom: calc(var(--margin-bottom) - var(--border-bottom));
      margin-left: calc(var(--margin-side) - var(--border-side));
    }

    h1 {
      text-transform: uppercase;
      font-size: 0.8rem;
      font-family: var(--font-family-headings);
      text-align: center;
      order: 1;
      margin: 3pt;
    }
  `

  return (
    <section class="border-box">
      <div class="inner-box">
        <h1>{props.label}</h1>
        {props.children}
      </div>
    </section>
  )
}
