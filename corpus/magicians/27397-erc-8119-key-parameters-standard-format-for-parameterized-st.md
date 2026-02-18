---
source: magicians
topic_id: 27397
title: "ERC-8119: Key Parameters - Standard Format for Parameterized String Keys"
author: nxt3d
date: "2026-01-07"
category: ERCs
tags: [nft, metadata]
url: https://ethereum-magicians.org/t/erc-8119-key-parameters-standard-format-for-parameterized-string-keys/27397
views: 54
likes: 4
posts_count: 5
---

# ERC-8119: Key Parameters - Standard Format for Parameterized String Keys

This ERC proposes a standard format for parameterized string keys used in EVM key-value storage. It defines a simple convention using a colon and space separator (`: `) to represent variations or instances of metadata types, enabling better interoperability across different implementations.

**PR:** https://github.com/ethereum/ERCs/pull/1455/

Many EVM-based smart contracts use key-value storage (e.g., Solidity mappings, Vyper hash maps) to store metadata where string keys may need to represent multiple instances or variations of the same metadata type. Without a standardized format, different implementations use inconsistent formats like `“registration-1”`, `“registration:1”`, or `“registration1”`, leading to:

- **Interoperability issues** between contracts and tooling

- **Parsing difficulties** for clients and indexers

- **Fragmentation** in the ecosystem

This standard enables consistent parameterized keys that are both human-readable and easy to parse programmatically. Standards such as ERC-8048 (Onchain Metadata for Token Registries) and ERC-8049 (Contract-Level Onchain Metadata) can leverage this ERC to support parameterized metadata keys.

When string keys include parameters, they **MUST** use a colon and space separator (`: `).

**Valid formats:**

- `“registration: 1”`

- `“registration: 2”`

- `“user: alice”`

- `“key: value:with:colons”` (colons allowed in parameter, but not `: `)

**Invalid formats:**

- `“registration-1”` (hyphen separator)

- `“registration:1”` (colon without space)

- `“registration1”` (no separator)

The colon and space separator (`: `) was chosen because:

- It improves human readability compared to formats like `key:value` or `key-value`

- It provides a clear, unambiguous separator that is easy to parse programmatically

- It maintains compatibility with existing parsers that support this format

This format was inspired by TOON format (developed by Johann Schopplich), and we acknowledge this preceding work.

## Replies

**jkm.eth** (2026-02-02):

One potential problem I can see, is that “x: y” is a pattern commonly used by many languages and data formats to indicate that key “x” has value “y”. This is true in JSON, and even in TOON. I don’t know of any language or data format that uses “x: y” as a way to point to attribute “y” in object “x” or member “y” of array “x”.

If human-readability is important, it seems better to follow these norms which others are already familiar with.

The format “x[y]” is widely used to reference “y” as being a key name or index belonging to object/array “x”, and I feel like that would be a much better format for parameterization.

---

**nxt3d** (2026-02-02):

Thank for the feedback! Is there a functional difference between `x[y]` and `x: y`? If it’s just a style thing, I tend towards keeping `x: y` because it might have broader appeal beyond just developers? Also, just in general `name: Lena` reads more naturally than `name[Lena]` to me. I think a counter example is passing a struct as a parameter to a function, and using `key: value` syntax for initialization, like in Solidity when calling a function with a struct as a parameter: `setPerson(P({name: "Lena", age: 30}))`?

---

**jkm.eth** (2026-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nxt3d/48/16100_2.png) nxt3d:

> it might have broader appeal beyond just developers?

I think we *should* focus on developers, because they are the only ones who will be consuming the data at this level ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

I believe it is a functional issue to follow established norms and expectations and avoid confusion wherever possible. Key-value pairs are represented by different languages as objects/dictionaries/maps, and so we should choose a pattern that accurately represents that way of thinking.

Imagine if our key-value data was being indexed and passed along to other systems through APIs. In JSON, the proposed system could end up with something like `{ “bestNumber: 1": 42 }`.  Although it is possible to understand, it is more confusing than it needs to be and looks like a mistake. If a frontend developer were to put that into a JavaScript object and print to console, it would turn into: `bestNumber: 1: 42`.  This is very ambiguous.

In YAML, TOON, and other related systems where quotes around key names are optional unless the key name includes a space, you would be requiring quotes to be used every time. This reduces efficiency by requiring an additional 2 characters per entry, and increases the chance for operator error.

If we instead used brackets, which is commonly used for objects/dictionaries/maps, the above example would turn into `bestNumber[1]: 42`. This logically makes sense, because in the majority of programming languages `bestNumber[1]`would refer to the first entry in an array titled `bestNumber`, and then we are using the commonly-understood pattern of `x: y` to show what the value of that entry is. Quotes are never needed, and it should be immediately obvious if something is incomplete after a copy-paste.

In summary, I don’t see any benefits to used the proposed format but I do see many risks of causing developer headaches. If there are some benefits that I’m missing, please highlight them so I can rethink it!

---

**nxt3d** (2026-02-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jkm.eth/48/17229_2.png) jkm.eth:

> bestNumber: 1: 42

![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=15) I think this is a good point. I hadn’t thought about representing this as a pair like this before. What if we use something like `<label>/<parameter>?`

`name/Maria: 42`

I am unsure about using `<label>[<parameter>]`, because I feel like the closing square bracket can easily get lost when the parameter is large or spans multiple lines.

For example, a long scene description:

```auto
scene/A cinematic wide-angle illustration of a quiet coastal town at dawn, soft pink and blue light reflecting off calm water, wooden fishing boats tied to a weathered pier, mist drifting low across the surface of the harbor. In the background, rolling hills with scattered pine trees fade into the fog. The style is painterly and detailed, with subtle grain and a slightly muted color palette inspired by Studio Ghibli and classic European landscape paintings.

```

This feels easier to read and more robust than relying on a closing bracket at the end of a long parameter.

**With brackets:**

```auto
scene[A cinematic wide-angle illustration of a quiet coastal town at dawn, soft pink and blue light reflecting off calm water, wooden fishing boats tied to a weathered pier, mist drifting low across the surface of the harbor. In the background, rolling hills with scattered pine trees fade into the fog. The style is painterly and detailed, with subtle grain and a slightly muted color palette inspired by Studio Ghibli and classic European landscape paintings.]

```

