import { createSignal } from 'solid-js'
import { css } from 'solid-styled'

export default function LabeledInput({
  id,
  label,
  placeholder,
  value,
  onChange,
}: {
  id: string
  label: string
  placeholder: string
  value: string
  onChange: (value: string) => void
}) {
  css`
    .labeled-input {
      display: flex;
      flex-direction: column
      gap: 3pt;
    }

    label {
      text-transform: uppercase;
      font-size: 0.8rem;
      font-family: var(--font-family-headings);
    }

    input {
      order: -1;
      border: none;
      border-bottom: 1px solid var(--border-static-color);
      padding: 3pt 0;
      outline: none;
      font-family: var(--font-family-text);
      transition: border-color .5s;
    }

    input:hover {
      border-bottom-color: var(--border-hover-color);
      outline: none;
    }

    input:active {
      border-bottom-color: var(--border-active-color);
      outline: none;
    }

    input:focus {
      border-bottom-color: var(--border-focus-color);
      outline: none;
    }
  `

  return (
    <div class="labeled-input">
      <label for={id}>{label}</label>
      <input
        name={id}
        placeholder={placeholder}
        value={value}
        oninput={(event) => onChange(event.target.value)}
      />
    </div>
  )
}
