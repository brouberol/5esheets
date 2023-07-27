import { Component, createEffect } from 'solid-js'
import { css } from 'solid-styled'
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const MarkdownRenderedEditableBox: Component<{
  id: string,
  text: string
  onChange: (update: string) => void
}> = (props) => {

  css`

    .markdown-rendered-editable-box-wrapper {
      padding: 1em;
      height: 100%;
    }

    .markdown-raw {
      width: 100%;
    }

  `;

  const hiddenClass = "hidden";
  const markdownRenderer = new marked.Renderer();
  const linkRenderer = markdownRenderer.link;
  marked.setOptions({
    mangle: false,
    headerIds: false,
  });

  // always render links so they open in a new tab
  markdownRenderer.link = (href: string, title: string, text: string): string => {
    const html = linkRenderer.call(markdownRenderer, href, title, text);
    return html.replace(/^<a /, '<a target="_blank" ');
  };

  // DOMPurify sees target blank links as a security issue, so massage it
  // into accepting then.
  // Source: https://github.com/cure53/DOMPurify/issues/317#issuecomment-698800327
  DOMPurify.addHook("afterSanitizeAttributes", function (node: HTMLElement) {
    // set all elements owning target to target=_blank
    if ("target" in node) {
      node.setAttribute("target", "_blank");
      node.setAttribute("rel", "noopener");
    }
  });

  const hideRawTextareaShowRenderedDiv = () => {
    props.text;
    const textarea = document.getElementById(`${props.id}-raw`);
    if (!textarea) {
      return;
    }
    const neighbourDiv = document.getElementById(`${props.id}-rendered`);
    if (!neighbourDiv) {
      return;
    }
    if (textarea.value) {
      textarea.textContent = textarea.value;

      const rendered: string = marked.parse(textarea.textContent, {
        renderer: markdownRenderer,
      });
      neighbourDiv.innerHTML = DOMPurify.sanitize(rendered);
      textarea.classList.add(hiddenClass);
      neighbourDiv.classList.remove(hiddenClass);
    } else {
      // The textarea does not contain any text, so hiding it would prevent us from
      // writing in it in the first place.
      textarea.classList.remove(hiddenClass);
      neighbourDiv.classList.add(hiddenClass);
    }
  }

  const showRawTextareHideRenderedDiv = () => {
    props.text;
    const textarea = document.getElementById(`${props.id}-raw`);
    if (!textarea) {
      return
    }
    const neighbourDiv = document.getElementById(`${props.id}-rendered`);
    if (!neighbourDiv) {
      return
    }
    textarea.classList.remove(hiddenClass);
    textarea.focus({ preventScroll: true });
    neighbourDiv.classList.add(hiddenClass);
  };

  createEffect(() => hideRawTextareaShowRenderedDiv());

  return (
    <div class="markdown-rendered-editable-box-wrapper">
      <textarea
        id={props.id + "-raw"}
        class="markdown-raw hidden"
        onfocusout={() => hideRawTextareaShowRenderedDiv()}
        onChange={() => props.onChange(props.text)}>{props.text}
      </textarea>
      <div
        class="markdown-rendered"
        id={props.id + "-rendered"}
        onclick={() => showRawTextareHideRenderedDiv()}>
      </div>
    </div>
  )
}

export default MarkdownRenderedEditableBox;
