import { css } from 'solid-styled'

const SingleAttribute = <T extends string | number>(props: {
    value: T
}) => {
    css`
    .single-attribute {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 1.6rem;

      padding: 1rem 0 .3rem;
    }
  `

    return (
        <div class="single-attribute">
            {props.value}
        </div>
    )
}

export default SingleAttribute
