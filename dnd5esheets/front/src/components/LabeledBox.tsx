import { Component } from "solid-js";
import { css } from "solid-styled";

const LabeledBox: Component<{ label: string; children: any }> = ({
  label,
  children,
}) => {
  css`
    .labeled-box, inner-box {
      height: 100%;
      width: 100%;
    }
    
    .labeled-box {
      border-image: url(/border-1.svg) 48% repeat;

      --border-top: 16mm;
      --border-side: 6mm;
      --border-bottom: 16mm;
      --margin-top: 1mm;
      --margin-side: 1mm;
      --margin-bottom: 1mm;
    
      border-style: solid;
      border-width: var(--border-top) var(--border-side) var(--border-bottom) var(--border-side);
    }
    
    .labeled-box .inner-box {
      display: flex;
      flex-direction: column
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
  `;

  return (
    <section class="labeled-box">
      <div class="inner-box">
        <h1>{label}</h1>
        {children}
      </div>
    </section>
  );
};

export default LabeledBox;