import { css } from 'solid-styled'

const TrayBox = <T extends string | number>(props: {
  label: string
  value: T
  onChange?: (value: T) => void
}) => {
  css`
    .tray-box {
      --outer-box-size: 12.2mm;
      --inner-box-size: 10mm;

      background:
        url(/assets/border-proficiency-bonus-right.svg) no-repeat right,
        url(/assets/border-proficiency-bonus-left.svg) no-repeat left,
        url(/assets/border-proficiency-bonus-center.svg) no-repeat center;
      background-size:
        auto 100%,
        auto 100%,
        auto 100%;

      width: 100%;
      min-height: var(--outer-box-size);
      max-height: var(--outer-box-size);

      display: flex;
      align-items: center;

      gap: 2mm;
    }

    .value {
      width: var(--inner-box-size);
      height: var(--inner-box-size);
      border-radius: 100%;
      margin-left: calc((var(--outer-box-size) - var(--inner-box-size)) / 2);

      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.1rem 0.2rem 0 0;

      font-size: 1.2rem;
    }

    label {
      text-transform: uppercase;
      font-size: 0.8rem;
      font-weight: bold;
      font-family: var(--font-family-headings);
      text-align: center;
    }
  `

  return (
    <div class="tray-box">
      <span
        class="value"
        onClick={() => (props.onChange ? props.onChange(props.value) : null)}
      >
        {props.value}
      </span>
      <label>{props.label}</label>
    </div>
  )
}

export default TrayBox
