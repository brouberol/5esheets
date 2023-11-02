import { Component, Show, createSignal } from 'solid-js'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const MarkdownRenderedEditableBox: Component<{
  id: string
  text: string
  onChange: (update: string) => void
}> = (props) => {
  const markdownRenderer = new marked.Renderer()
  const [isBeingEdited, setIsBeingEdited] = createSignal(false)

  // DOMPurify sees target blank links as a security issue, so massage it
  // into accepting then.
  // Source: https://github.com/cure53/DOMPurify/issues/317#issuecomment-698800327
  DOMPurify.addHook('afterSanitizeAttributes', function (node: Element) {
    // set all elements owning target to target=_blank
    if ('target' in node) {
      node.setAttribute('target', '_blank')
      node.setAttribute('rel', 'noopener')
    }
  })

  return (
    <div class="markdown-rendered-editable-box-wrapper">
      <Show when={isBeingEdited()}>
        <pre
          contentEditable
          onfocusout={(event) => {
            setIsBeingEdited(false)
            const target = event.target as HTMLDivElement
            props.onChange(target.innerHTML)
          }}
        >
          {props.text}
        </pre>
      </Show>
      <Show when={!isBeingEdited()}>
        <div
          onClick={() => setIsBeingEdited(true)}
          innerHTML={DOMPurify.sanitize(
            marked.parse(props.text, {
              renderer: markdownRenderer,
            })
          )}
        ></div>
      </Show>
    </div>
  )
}

export default MarkdownRenderedEditableBox
