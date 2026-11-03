# Current screen

The current screen is the one the person shares. Do not fetch the Screen DB. The Coda doc is private and this session cannot log in. Do not mention it. Do not guess the screen from memory, from the Styleguide sandbox page, or from `lesley-spec/ai-inplatform`.

## Ask before drawing

1. Prefer a Figma link to the frame. That is a file URL with the node, or the file URL plus which page.
2. If they do not have a link, a screenshot of the screen is enough to see what is there now.
3. If they share neither, stop. Do not invent the current screen.

The link they share is the source. The working file is where the three variations go. Those are different files. Leave the source file unchanged. Leave the Styleguide file unchanged. Page Templates are read, then duplicated into the working file. Page Examples and the sandbox page are not the working file and not the template source.

## What to do with the answer

- **Figma link.** Open that file. Read the linked frame. Duplicate it into the working file and use it for the content. If the duplicate has a raw hex, an unbound fill, or text with no text style, rebind it to a Styleguide (V2) token. Do not keep the raw paint because the source had it.
- **Screenshot only.** Use it for layout and the header. Build from the closest Page Template and published Styleguide (V2) components. Do not sample a hex from the image. Say that the screenshot is not a frame that can be cloned, so spacing and content are matched by eye.

## Page Templates

Read [Page Templates](https://www.figma.com/design/Uwg1IvlTgvVA2IvX6WLxOd/Styleguide--V2-?node-id=5314-16) before building. File key `Uwg1IvlTgvVA2IvX6WLxOd`, node `5314:16`. Do not add or edit frames on that page.

Open the page, name the templates on it, and pick the closest one to the screen they shared. Re-read the page in Figma. Duplicate that template into the working file. Keep its component instances and token bindings. Then apply the person's screen content and the three variations.

## Tokens

Styleguide (V2) is the only token source. Theme the working file to **VNext Light**, or **VNext Dark** when the screen ships in dark mode or the person asks. Never set Design Tokens to V2.

Bind fills and strokes to `color/…` variables. Bind text to a named text style. The style resolves to Sarabun. Do not set a font by hand. Buttons, alerts, nav, badges, tables, and inputs are library instances.
