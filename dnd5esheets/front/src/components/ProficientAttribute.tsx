import { Show, createSignal } from "solid-js";
import { css } from "solid-styled";
import { Proficiency, proficiencies } from "~/store";

function cycleProficiency(proficiency: Proficiency): Proficiency {
  const index = proficiencies.indexOf(proficiency);
  return proficiencies[(index + 1) % proficiencies.length];
}

export default function ProficientAttribute({
  id,
  label,
  labelSecondary,
  proficiency = "none",
  value,
}: {
  id: string;
  label: string;
  labelSecondary?: string;
  proficiency: Proficiency;
  value: number;
}) {
  css`
    .attribute, .proficiency {
      display: flex;
      flex-direction: row
      align-items: baseline;
    }

    .attribute {
      gap: .5em;
    }
    
    .proficiency-master, .proficiency-expert {
      -webkit-appearance: none;
      appearance: none;
      background-color: #fff;

      color: currentColor;
      width: .9em;
      height: .9em;
      margin: auto 0;
      border: 1px solid currentColor;
      border-radius: 50%;
      transform: translateY(.15em);
      background: white;

      position: relative;

      outline: 2px solid white;
    }

    .proficiency-expert {
      color: var(--border-inactive-color);
      margin-left: -.15em;
      z-index: -1;
    }

    .proficiency-master:checked,
    .proficiency-expert:checked {
      color: currentColor;
      background: currentColor;
    }


    input.value {
      order: 1;
      border: none;
      border-bottom: 1px solid var(--border-static-color);
      padding: 3pt 0;
      outline: none;
      font-family: var(--font-family-text);
      width: 2em;
      text-align: right;
    }

    input.value:hover {
      border-bottom-color: var(--border-hover-color);
    }

    input.value:active {
      border-bottom-color: var(--border-active-color);
    }

    input.value:focus {
      border-bottom-color: var(--border-focus-color);
    }

    label {
      text-transform: capitalize;
      font-size: 0.8rem;
      font-family: var(--font-family-text);
      order: 2
    }

    .secondary {
      color: var(--font-color-dim);
    }
  `;

  const [proficiencyValue, setProficiency] = createSignal(proficiency);

  return (
    <div class="attribute">
      <label for={id}>
        {label}
        <Show when={labelSecondary}>
          {" "}
          <span class="secondary">({labelSecondary})</span>
        </Show>
      </label>
      <input class="value" type="text" name={id} value={value} />
      <span class="proficiency">
        <input
          class="proficiency-master"
          name={`${id}-master`}
          type="checkbox"
          checked={["master", "expert"].includes(proficiencyValue())}
          onClick={() => setProficiency(cycleProficiency(proficiencyValue()))}
        />
        <input
          class="proficiency-expert"
          name={`${id}-expert`}
          type="checkbox"
          checked={["expert"].includes(proficiencyValue())}
          onClick={() => setProficiency(cycleProficiency(proficiencyValue()))}
        />
      </span>
    </div>
  );
}
