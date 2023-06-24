import { Component } from "solid-js";
import { css } from "solid-styled";

const ScoreBox: Component<{
  label: string;
  score: number;
  modifier: number;
  onChange: (update: number) => void;
}> = (props) => {
  css`
    .score-box {
      width: 18mm;
      display: flex;
      flex-direction: column;
      border: 1px solid black;
      padding: 2mm 0;
      gap: 2mm;
      margin-bottom: 2mm;
      align-items: center;
    }

    label {
      text-transform: uppercase;
      font-size: 0.8rem;
      font-family: var(--font-family-headings);
      text-align: center;
    }

    .score,
    .modifier {
      outline: none;
      text-align: center;
    }

    .score {
      font-size: 20pt;
      width: 100%;
      border: none;
      background: none;
      font-family: var(--font-family-text);
      overflow: visible;
    }

    .modifier {
      width: 8mm;
      height: 2rem;
      margin-bottom: -1rem;
      background: white;
      border: 1px solid black;
      line-height: 2rem;
    }
  `;

  console.log("score box", props.label);

  return (
    <div class="score-box">
      <label>{props.label}</label>
      <input
        class="score"
        type="text"
        value={props.score}
        oninput={(event) => props.onChange(parseInt(event.target.value ?? "0"))}
      />
      <div class="modifier">{props.modifier}</div>
    </div>
  );
};

export default ScoreBox;
