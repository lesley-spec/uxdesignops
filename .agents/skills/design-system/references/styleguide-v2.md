# Styleguide V2 catalog

Source file: [Styleguide V2](https://www.figma.com/design/Uwg1IvlTgvVA2IvX6WLxOd/Styleguide--V2-)
File key: `Uwg1IvlTgvVA2IvX6WLxOd`
Published library name: **Styleguide (V2)**
Variable collection: **Design Tokens**

This is a catalog read from that file and its published library. It is not a
trained model. When a value is missing here, open the page and read the
component. Do not invent a token, a state, or a hex.

V2 mode is retired. Do not set Design Tokens to **V2**, and do not take type
or color from the V2 column.

Every screen uses **VNext Light** or **VNext Dark** on the Design Tokens
collection (`VariableCollectionId:11424:35287`).

- Light screens: mode **VNext Light** (`14329:2`)
- Dark screens: mode **VNext Dark** (`14329:3`)

Do the work in a new Figma file. Do not add or edit frames in the Styleguide
file. Create the file in the Impact org, then import Styleguide (V2)
components, text styles, and variables so that library is attached. Theme the
new file by setting Design Tokens to **VNext Light** or **VNext Dark** on the
page. The collection id inside the Styleguide file is local to that file.
In a new file, import the variable and set the mode by name.

VNext Light and VNext Dark both resolve
`typography/font family/font-family` to **Sarabun**. Mulish is the retired V2
value. Bind the text style. Do not set a font by hand.

This Figma file is the component and token source. Existing Brand and Partner
screens live in the Screen DB, and each row links to the VNext Figma frame to
duplicate:
https://docs.superhuman.com/d/Screen-DB_d4K5aqNTMna/All-Screens_suJvIBge#_lucIMxeq

Brand click-through prototypes still start from `lesley-spec/ai-inplatform`
([live](https://lesley-spec.github.io/ai-inplatform/)). That repo is the
prototype shell, not the screen inventory.

## Draw rules

1. Create a new Figma design file. Leave the Styleguide file unchanged.
2. Attach Styleguide (V2) by importing its published components, text styles, and variables.
3. Theme the file to VNext Light or VNext Dark.
4. Use the closest Page Template or Page Example only as the reference. Build the screen in the new file from published components.
5. Bind paints to `color/…` variables and text to the named text styles.
6. Pick the component variant that matches the state (Default, Hover, Disabled, Error, Read Only). Do not fake a state with opacity.
7. If the library has no component, stop and say so.

## Pages

Foundations, under DESIGN:

| Page | Id |
|---|---|
| Color | `11456:34171` |
| Grid + Layout | `14939:29688` |
| Space + Size | `14939:29689` |
| Typography | `14939:59626` |
| Illustrations | `35337:111764` |
| Page Templates | `5314:16` |
| AI | `37792:204229` |

Screens to clone, on Page Templates: Checklist Example, Wizard Example,
Table Example / Spacious, Table Example / Condensed, Form, Form Section.

More product screens, on Page Examples (`15445:43918`, sandbox): Current Brand
Dashboard, Brand / Performance / One Column / Narrow, Data Lab, Form Example,
Table Example / Spacious.

Component pages live under COMPONENTS. Open the VNext frame on the page.
Skip the V2 frame. The component list is in the skill index below.

## Text styles

Read the named text styles below. In VNext Light and VNext Dark the family is
**Sarabun**. HTML code uses **Source Code Pro**. Bind the style. Do not set a
font by hand. Sizes below were measured on the V2 typography section
`25502:60440`; re-read the frame if a VNext section disagrees.

| Style | Size | Weight | Line height |
|---|---|---|---|
| Display Title | 40 | Bold 700 | 52 |
| Display Text | 24 | Regular 400 | 33 |
| Wizard Header | 32 | Bold 700 | 40 |
| Wizard Subheader | 22 | SemiBold 600 | 30 |
| Header | 24 | Bold 700 | 33 |
| Subheader | 18 | SemiBold 600 | 23 |
| Field Label | 16 | SemiBold 600 | 20 |
| Secondary Field Label | 14 | SemiBold 600 | 18 |
| Regular Text | 14 | Regular 400 | 18 |
| Description Text | 14 | Regular 400 | 18 |
| Regular Text Link | 14 | SemiBold 600 | 18, `color/text/text-interactive` |
| Ghost Text | 14 | Regular 400 | 18 |
| Help Text | 12 | Regular 400 | 15 |
| Table (1st column) | 12 | SemiBold 600 | 15 |
| Table Subtext | 10 | Regular 400 | 13 |
| HTML Code | 14 | Regular 400 | 18, Source Code Pro |

Also published: Small Text Link, Reporting/Header, Reporting/Header Placeholder,
Reporting/Table Column Header, Reporting/Axis Label, Reporting/Legend Label,
Reporting/Legend Label Subtext, Reporting/Text Link, Reporting/Regular Text.

## Color tokens

Names from the Styleguide (V2) Design Tokens collection. Resolved hexes are
only listed where a frame returned them. Re-read `get_variable_defs` on the
frame you clone before you paint.

Text:

- `color/text/text-default` `#25282f`
- `color/text/text-subdued` `#606672`
- `color/text/text-placeholder` `#969ea7` on the typography section, `#a7a7a7` on Text Inputs. Read the frame.
- `color/text/text-disabled`
- `color/text/text-invert`
- `color/text/text-interactive` `#14b1f7`

Background:

- `color/background/background-default` `#ffffff`
- `color/background/background-subdued`
- `color/background/background-hover`
- `color/background/background-dimmed`
- `color/background/background-invert`
- `color/background/background-overlay`
- Social: `background-x`, `background-line`, `background-tiktok`, `background-twitch`

Border:

- `color/border/border-default` `#e0e9f0`
- `color/border/border-subdued`
- `color/border/border-hover`
- `color/border/border-active`
- `color/border/border-interactive` `#8a959d`

Icon:

- `color/icon/icon-default` `#25282f`
- `color/icon/icon-subdued`
- `color/icon/icon-disabled`
- `color/icon/icon-active`
- `color/icon/icon-invert` `#ffffff`
- `color/icon/icon-invert-disabled`

Primary button:

- `color/primary/button-primary-background-default` `#1d66de`
- `color/primary/button-primary-background-hover`
- `color/primary/button-primary-background-disabled`
- `color/primary/button-text-on-primary-default` `#ffffff`
- `color/primary/button-text-on-primary-disabled`

Secondary button:

- `color/secondary/button-secondary-background-default`
- `color/secondary/button-secondary-background-hover`
- `color/secondary/button-secondary-background-disabled`
- `color/secondary/button-secondary-border-default`
- `color/secondary/button-secondary-border-hover`
- `color/secondary/button-secondary-border-disabled`
- `color/secondary/button-text-on-secondary-default`
- `color/secondary/button-text-on-secondary-hover`
- `color/secondary/button-text-on-secondary-disabled`

Tertiary button:

- `color/tertiary/button-tertiary-background-default` `#ffffff00` (transparent)
- `color/tertiary/button-tertiary-background-hover` `#e4e5e8`
- `color/tertiary/button-tertiary-background-disabled`
- `color/tertiary/button-text-on-tertiary-default` `#25282f`
- `color/tertiary/button-text-on-tertiary-disabled`

Feedback. Each of success, warning, and critical has text, icon, border, and
background. Critical also has `text-critical-subdued` and
`background-critical-subdued`.

AI:

- `color/ai/text-ai-default` `#625df5`
- `color/ai/icon-ai-default` `#625df5`
- `color/ai/icon-ai-subdued`
- `color/ai/background-ai-purple`
- `color/ai/background-ai-green`
- `color/ai/gradient-purple` `#625df5`
- `color/ai/gradient-green` `#06d1a3`
- `color/ai/dropshadow-purple`
- `color/ai/dropshadow-green`

Brand: `color/brand/brand-red`, `color/brand/brand-gray`, `color/brand/brand-neutral`.

Navigation: `nav-text-default`, `nav-text-active`, `nav-text-subdued`,
`nav-text-disabled`, `nav-icon-default`, `nav-icon-active`, `nav-border-default`,
`top-nav-background-hover`, `side-nav-background-default`,
`side-nav-background-hover`, `side-nav-background-active`,
`side-nav-background-subdued`, `secondary-side-nav-background-hover`,
`secondary-side-nav-background-active`, `nav-brand-icon-background-default`,
partner: `top-nav-partner-tab-hover`, `v2-nav-partner-text-active`.

Filter: text, border, and background, each with default, hover, active, and
disabled. Also `filter-border-active-hover`.

Decorative: red, blue (background, text, text-subdued, icon, border), orange
(text, icon, border, background), warm gradient 1 and 2, cool gradient 1 and 2.

Reporting: `color/reporting/primary`, `secondary`, `tertiary`.

## Space

Gap: `gap-small` 4, `gap-default` 8, `gap-large` 16, `gap-nav`,
`page-section-gap-default`.

Padding: `card-padding`, `input-padding-leftright` 12,
`button-padding-leftright-default` 16, `button-padding-leftright-large` 24,
`label-padding-leftright`, `badge-padding-leftright`, `tab-padding-leftright`,
`tab-padding-topbottom`, `menu-padding-leftright`, `menu-padding-topbottom`,
`nav-padding-leftright`, `nav-padding-topbottom`, `nav-item-padding-right`,
`selector-padding-default`, `selector-padding-small`,
`select-item-padding-leftright-default` 16, `select-item-padding-topbottom` 8.

Height: button small / default 40 / large 48. Input small / default 40.
Icon small 12 / default 16 / large / xlarge. Badge, label small and default,
select item, nav child item.

Width: `input-width` 246, `selector-width`, `empty-state-card-width`,
icon small through xlarge, avatar xs, s, m, l, xl, xxl.

Radius: input 8, button 9999 (pill), also menu, pill, page, card, badge,
label, avatar, selector 8, tooltip, checkbox, select item, social icons.

Grid variables seen: `grid/brand-collapsed-1-column`,
`grid/brand-expanded-1-column`.

## Components and states

Only states read off the component pages are listed. Open the page for any
component not in this table before drawing it.

| Component | Page | V2 variants |
|---|---|---|
| Buttons | `5346:227` | Primary, Secondary, Tertiary, Danger, Close, Button Group, SSO, Pagination arrow. State: Default, Hover, Keyboard Focus, Disabled. Size: Small, Default, Large. Some have Responsive true/false. SSO accounts: Impact, Google, Apple, LinkedIn, facebook, instagram, x, youtube. |
| Alerts / Banners | `11485:55193` | Alert Type: Info, Warning, Critical, Success. Toast: Success, Error. Also Release Note, Partner Dashboard Alert, AI Results Banner, AI Activation Banner. |
| Badges | `11433:35484` | vnext badge Color: Gray, Subdued Gray, Gradient, Green, Red, Yellow, Blue, Orange, ai (purple), with or without icon. Finance: Not Yet Due, Paid, Past Due (V2 frame uses Default, Success, Critical). Discover: Unclaimed, Dormant, Inactive, Pre-Qualified, New, Recommended, ITP. Campaign: Participating, Eligible, Invited, Applied, Completed, In Negotiation, Pre-Qualified, New, Negotiable, Declined. Partner size: Small, Medium, Large, Extra Large, plus icon-only and text-only. Creator tier: Nano, Micro, Mid-tier, Macro, Mega. Status: approved, pending, declined, counter, new, Invalid. |
| Checkbox | `11446:35481` | Icon States: Default, Hover, Active, Multi, Add, each Disabled true/false. Input Check: Unchecked, Checked, Indeterminate. Tooltip true/false. Column states: Default, Hover, Disabled, Read only. Groups of 3, 5, or 8. |
| Inputs | `11095:33894` | Text, dropdown, date, file. State: Default, Hover, Active, Keyboard Focus, Inputted, Selected, Disabled, Read Only, Error. Size: Default, Small. Responsive true/false. Dropdown position Left or Right. Dates: Single, Range, Multiple joined, Start to End, Lock true/false. File: Choose file, Drop area, Loading, Uploaded, with preview Default, Icon, or Thumbnail. Also Input with label. |
| Menu (Select) | `11446:35576` | Type: Regular, Parent, Child. State: Default, Hover, Disabled. Responsive true/false. Also search bar and scrollable true/false. Actions: Create New, Edit, Settings, Mobile Actions. |
| Data Table | `11159:31755` | Density: Condensed, Spacious. Screen: Desktop, Mobile. Hover, Sorted, Row type Child or Default or Parent. Header states for bulk select: Default, Bulk Selected, All Selected, All Possible Rows Selected. Empty and Error Loading. Expanded true/false. Style: Full Page or Table only. |
| Navigation | `6366:10651` | Brand and Partner. State: Default, Hover, Active, Disabled, Selected. Expanded true/false. Products include Advocate, Discover, Engage, Optimize, Protect, Insights, Finance, Settings. Type Brand or Partner. Do not rebuild the nav. Clone Nav Expanded or Nav Collapsed from a page template. |
| Modals / Pop-ups | `11034:31038` | Confirmation pop-up and Modal. Size: Desktop Default (650), Desktop Large (900), Mobile (375). Pieces: Modal Header, Modal Content slot, Modal Footer. Mobile footer stacks. More than two mobile CTAs use the Mobile CTAs drawer. Overlay is Modal Background Overlay. |
| Text Inputs (AI) | `40135:67157` | Generate copy: Help Me Write, then Generate. Refine copy: Refine, then Shorten, Elaborate, More Casual, More Formal. Uses Field Label, Text Input, Primary Button, Tertiary Icon Button, AI Activation Button. |

Other component pages to open by name when needed: Accordion, Avatar,
Breadcrumb, Calendar, Cards, Checklist, Color Picker, Countries, Errors,
Field Label, File Format Table, Filter, Icons, Inline Fields, Labels (Tags),
Logo, Kanban Tiles, Loading Dots, Mobile App, Navigation - Email,
Notification Slideout, Progress Bar, Radio, Rating Input, Reporting,
Rich Text Input, Rulebuilder, Selector, Separator, Skeleton, Slideout,
Stage Coach, Tabs, Timeline, Toggle, Tooltips, Wizard.

## Text Inputs example

Node `40135:67157`. Use a text input or text area when copy can be generated.
It can write new copy or refine existing copy. This is a pattern example, not
the type source. Type comes from the typography page.
