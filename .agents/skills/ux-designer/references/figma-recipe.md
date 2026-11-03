# Figma recipe

Library: **Styleguide (V2)**. Library key:
`lk-6470a9011d08f785e09e9db87e63dc8933b79436f0d83a05a3cfbe8c937d4cfb28194eb63856824b3710fdcd94701bf1a10415eea76c162ad3bed50a83bfe045`.
Pass it as `includeLibraryKeys` on every `search_design_system` call.

Create a file only after the user says to. New files go in plan `organization::1068571974229129913` (Impact). Never draw in the Styleguide file.

## Keys

Text styles (`$fig.getStyle`):

| Style | Key |
|---|---|
| Header | `d4eadd9d2e66add0c318e49d3965939eb903c6c7` |
| Subheader | `fcc0ce98f1ee489e5495c3cdd2ae8c41595a2ced` |
| Field Label | `9c8000024ac106d0f076a4eabd24fd1c852a9699` |
| Secondary Field Label | `aabb072a705f3ae1f797d5441c060a6fa2351605` |
| Regular Text | `c13f8c6debc9ea53e10224347b2e23d85198612b` |
| Regular Text Link | `f7d413fdb47099f4a806f618c021d6cf134b4b93` |
| Help Text | `1514004eaf78ce524d665112b722abb7ddaf7695` |
| Description Text | `42f71ed2d83e8491409c0211d71fff401a03ce89` |

Variables (`$fig.getVar`):

| Variable | Key |
|---|---|
| color/background/background-default | `ea325f20a68ec1448b2b352df4060fbda1d58733` |
| color/background/background-subdued | `77e939eb3e10ff5b2a80ec34fbe040a1e7a62299` |
| color/text/text-default | `46dc79351556ccbebdba5ad5f774333f0590af29` |
| color/text/text-subdued | `f6b6ecfa8a5f47df8a4ba5e7628c73b628811a52` |
| space/gap/gap-small | `74b55c6464ebde07c5465b6310dfef8592b76adc` |
| space/gap/gap-default | `c9ac22e2cc750c8350ca82941b74cb11a651c15c` |
| space/gap/gap-large | `21283d81a54b6bf00bfc7e27bdec59fc309ee72a` |

Components (`$fig.instance`):

| Component | Set key | Props |
|---|---|---|
| Primary Button | `5a89d24cfb2c06341a00c485d6b1e20fba4cd9c7` | `State` Default/Hover/Disabled/Keyboard Focus, `Size` Default/Small/Large, `Responsive` True/False, `Text#11562:19`, `Show Icon#11562:5`, `Show Dropdown#11562:12` |
| Alert | `e4816846f22e988f6ff316dfd0ec927b22d951eb` | `Type` Info/Warning/Critical/Success, `Text#32202:0` |
| VNext Side Nav (Brand) | `e6f34e38a250b6ac8ae052aee51c75a65a6990b9` | `Product` Engage/Discover/…, `Menu Item` Dashboard/Partners/…, `Expanded` True/False |
| VNext Desktop Top Nav | `e3d800dc969c8c592df49a1cba9a09e6b9d415f6` | `Type` Brand/Partner/…, `Show User Menu#14994:8` |
| Partner Nav | `ee6f21e3e8764125f1adad6b7481ba07b8afd4d1` | read before use |
| Secondary Button | `ec05ec3a4ec6231e8ed4b3792c06cdcace5ff717` | `Text#11562:40`, `State`, `Size`, `Responsive` |
| Tertiary Button | `b489aac4694601c6d227be3caaa0421bcb92f9f9` | `Text#11562:68`, `State`, `Size`, `Responsive` |
| Data Table | `0f2d090894a3c8cc1c28a9986b0ceaaa2b350796` | `State` Default/No Data/Empty/…, `Pagination#14522:128` |
| Table Actions | `305561762d0e1d4e607c38da329197aa23c92f44` | `States` Default/Bulk Selected/…, `Total Count#11852:15`, `Show Select All#11852:14` |
| Row Hover Actions | `364bc8379c75ccc6fee3b61bc4227bb1f607479b` | `Densities`, `Mode` Light/Dark |
| Empty State Card | `0830d5703df84e5e6819aaa1f9bf243bf748aa2a` | read before use |

Data Table Default has three visible columns (text, number, number) and five
rows. Change the cell text inside the instance; load each node's font first.
Row Hover Actions carries its own `Mode`. It does not follow the page theme,
so set `Mode=Dark` on dark pages.

Not every `Product` and `Menu Item` pair exists on VNext Side Nav. Read the
variant names before picking one.

## Theme

Import any Design Tokens variable, read its collection, and set the mode by
name. Collection ids differ between files.

```js
const v = await figma.variables.importVariableByKeyAsync('46dc79351556ccbebdba5ad5f774333f0590af29');
const tokens = await figma.variables.getVariableCollectionByIdAsync(v.variableCollectionId);
const light = tokens.modes.find((m) => m.name === 'VNext Light');
figma.currentPage.setExplicitVariableModeForCollection(tokens, light.modeId);
```

Setting the page mode is not enough for frames that already carry another
mode. Set the frame too.

## Screen shape

One auto-layout frame, 1440 wide, horizontal: nav instance, then a `Content`
column that fills. Content padding and gaps use `space/gap/*` variables.

## Audit

Run on each variation frame. Pass means every list is empty and `font` is
Sarabun.

```js
const frame = await figma.getNodeByIdAsync(FRAME_ID);
const ownNodes = frame.findAll((n) => {
  let p = n.parent;
  while (p && p !== frame) { if (p.type === 'INSTANCE') return false; p = p.parent; }
  return true;
});
const rawFills = [];
const unstyledText = [];
const fonts = new Set();
for (const n of [frame, ...ownNodes]) {
  if ('fills' in n && Array.isArray(n.fills)) {
    n.fills.forEach((f, i) => {
      const bound = n.boundVariables && n.boundVariables.fills && n.boundVariables.fills[i];
      if (f.type === 'SOLID' && f.visible !== false && !bound) rawFills.push(n.name);
    });
  }
  }
  if ('strokes' in n && Array.isArray(n.strokes)) {
    n.strokes.forEach((f, i) => {
      const bound = n.boundVariables && n.boundVariables.strokes && n.boundVariables.strokes[i];
      if (f.type === 'SOLID' && f.visible !== false && !bound) rawFills.push(n.name + ' (stroke)');
    });
  }
  {
    if (n.type === 'TEXT') {
      if (!n.textStyleId) unstyledText.push(n.characters.slice(0, 40));
    if (n.fontName !== figma.mixed) fonts.add(n.fontName.family);
  }
}
const instances = ownNodes.filter((n) => n.type === 'INSTANCE');
const notLibrary = instances.filter((n) => !(n.mainComponent && n.mainComponent.remote)).map((n) => n.name);
return { rawFills, unstyledText, notLibrary, fonts: [...fonts], instances: instances.length };
```

Text inside library instances is the component's own styling, so the audit
skips it.
