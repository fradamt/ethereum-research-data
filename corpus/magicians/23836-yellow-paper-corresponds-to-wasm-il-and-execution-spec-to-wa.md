---
source: magicians
topic_id: 23836
title: Yellow paper corresponds to wasm IL, and execution spec to wasm AL
author: u59149403
date: "2025-04-24"
category: Magicians > Primordial Soup
tags: [evm, yellow-paper, wasm, executable-specs]
url: https://ethereum-magicians.org/t/yellow-paper-corresponds-to-wasm-il-and-execution-spec-to-wasm-al/23836
views: 60
likes: 0
posts_count: 2
---

# Yellow paper corresponds to wasm IL, and execution spec to wasm AL

**Yellow paper corresponds to wasm IL, and execution spec to wasm AL**

Webassembly recently adopted SpecTec: [SpecTec has been adopted - WebAssembly](https://webassembly.org/news/2025-03-27-spectec/) . In short, this is machine readable description of wasm, which is used to generate all other artifacts: human-readable spec, reference interpreter and definitions for Coq/Rocq! (Note: “reference interpreter” part is not finished yet.) Here is an analogy: this is **as if we had single machine readable text, which is used to generate both yellow paper and python execution layer spec** !!! ![:heart_eyes:](https://ethereum-magicians.org/images/emoji/twitter/heart_eyes.png?v=12)![:heart_eyes:](https://ethereum-magicians.org/images/emoji/twitter/heart_eyes.png?v=12)![:heart_eyes:](https://ethereum-magicians.org/images/emoji/twitter/heart_eyes.png?v=12) From that news article: “it [SpecTec] takes Wasm to a new level of rigor and assurance that is unprecedented when it comes to language standards… One feature that sets Wasm apart from other mainstream programming technologies is that it comes with a complete formalization… it enabled the *soundness* of the language — i.e., the fact that it has no undefined behavior and no runtime type errors can occur — to be [machine-verified](https://github.com/WasmCert) before the first version of the standard was published”.

We definitely can learn a lot from Wasm approach.

Note that SpecTec is declarative, similarly to Yellow paper. During processing, it is converted to so-called IL (see diagram at [SpecTec has been adopted - WebAssembly](https://webassembly.org/news/2025-03-27-spectec/) ), which is declarative, too. But then this IL translates to AL (again, see diagram). And this AL is algorithmic/executable as opposed to declatative. I. e. this AL is similar to our execution specs. Again: IL is yellow paper, and AL is execution specs.

Thus, if we adopt wasm approach to bytecode specification, then we can generate both (declarative) yellow paper and (algorithmic) execution specs from same source!

## Replies

**u59149403** (2025-04-24):

ping [@RenanSouza2](/u/renansouza2) , [@pldespaigne](/u/pldespaigne) , [@shemnon](/u/shemnon)

