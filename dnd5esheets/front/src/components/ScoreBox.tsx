import { Component } from "solid-js";
import { css } from "solid-styled";

const ScoreBox: Component<{
  label: string;
  score: number;
  modifier: number;
}> = ({ label, score, modifier }) => {
  css`
    .score-box {
      display: flex;
      flex-direction: column;
      border: 1px solid black;
      padding: 2mm;
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
      padding: 2mm;
      width: 3rem;
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

  return (
    <div class="score-box">
      <label>{label}</label>
      <div class="score" contentEditable>
        {score}
      </div>
      <div class="modifier" contentEditable>
        {modifier}
      </div>
    </div>
  );
};

export default ScoreBox;
