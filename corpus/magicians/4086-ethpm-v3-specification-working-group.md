---
source: magicians
topic_id: 4086
title: ethPM V3 Specification Working Group
author: njgheorghita
date: "2020-03-04"
category: Magicians > Tooling
tags: [ethpm]
url: https://ethereum-magicians.org/t/ethpm-v3-specification-working-group/4086
views: 4904
likes: 24
posts_count: 44
---

# ethPM V3 Specification Working Group

This is an effort to consolidate various datatype specifications (ethpm, solidity & vyper compiler metadata, input/output json) into a single specification to facilitate interoperability and leverage network effects.

The current V3 spec should be considered a rough draft, so now is the time for proposing any changes. Once we reach general agreement on the spec in this forum, I will update the official human & machine readable specs to reflect the changes.

The timeline for this project is to have a well-defined, agreed upon specification before the Solidity Summit in Berlin (April 29). At least 3 of us ([@chriseth](/u/chriseth), [@gnidan](/u/gnidan), [@njgheorghita](/u/njgheorghita)) plan to be at the Summit, to discuss any final details before freezing the spec. The more the merrier if you’re able to make it to Berlin!

Thanks for all your input and thoughts in advance! There is a range of different interests coalescing here, and it’s exciting to imagine the near-future where we all benefit from using a compatible spec.

Link for the ethPM V3 rough draft can be found [here](https://hackmd.io/@hBXHLw_9Qq2va4pRtI4bIA/H1RFlh8GI). Let’s keep the conversation happening here on ethmagicians, and I’ll make any updates to the spec as necessary.

---

[@jpitts](/u/jpitts): Adding more context to this discussion:

Registry: http://explorer.ethpm.com/

Website: http://www.ethpm.com/

v2 Spec repo: https://github.com/ethpm/ethpm-spec/

Gitter Channel: https://gitter.im/ethpm/Lobby

## Replies

**rumkin** (2020-03-06):

Using `version` for manifest version is confusing for me, it’s totally not what I’d expect `version` to mean. Also this makes package version to be called `package_version` and thus the name of a package to be ` package_name`. I think it’s better to call it `manifest` and remove `package_` prefixes at all. This would make field names clear and obvious:

```auto
{
  "manifest": "ethpm/3.0",
  "name": "package",
  "version": "1.0.0"
}
```

This is what I found after a quick look.

---

**fubuloubu** (2020-03-06):

Agreed, but it may be impractical to change at this point because V1 sort of set these fields in stone (particularly `version`) so you could parse out what version the manifest is encoded in

---

**rumkin** (2020-03-06):

Yep, but before Ethereum 2.0, it’s ok to break things. In my opinion this time is some kind of buffer to experiment,  when you can hardfork yourself. And technologies here should be made user friendly and slick like Ruby IDK, not like C. It’s important because Ethereum 2.0 would be a long-time player and it’s better to invest in this period of technology life. Just not a time to create a legacy.

---

**fubuloubu** (2020-03-06):

I don’t think this standard would be related to ETH 2.0, it sort of sits by itself in relation to current tooling. It has some adoption, so I am unsure if there would be appetite for a breaking change like this, but I could be wrong.

---

**rumkin** (2020-03-06):

I’ve checked the doc again, and it’s actually contains breaking changes. One of them is renaming `manifest_version` into `version` and `version` into `package_version`, which I’m against. So it’s senseless to discuss.

[@njgheorghita](/u/njgheorghita) Also I’d suggest to use camel case instead of underscores in JSON. While underscores has better readability, camel case is de facto standard for JSON, and solidity compiler supports this. I think that host technology style should be chosen, just couldn’t find a good reason to have both of them.

---

**njgheorghita** (2020-03-06):

[@rumkin](/u/rumkin) Yup, I’ve gotta say I do prefer what you’ve proposed, thanks for submitting! Personally, I’ve never been a fan of the old naming conventions, they could be better. We do have breaking changes in this spec update, and all tooling will have to update to satisfy those changes, so now is a great time to squeeze in any breaking improvements. (afaik that responsibility lies mostly b/w myself, brownie ([@iamdefinitelyahuman](/u/iamdefinitelyahuman)) , truffle, and ethpm-rs ([@fubuloubu](/u/fubuloubu)) if that’s still ongoing).

The primary reason I opted for the proposed changes (`version`, `package_name`, `package_version`) is because the solidity compiler currently supports the `version` keyword to define the [metadata specification version](https://solidity.readthedocs.io/en/v0.6.2/metadata.html) - which maps nicely to what used to be the `manifest_version` field. I’d like to hear from [@chriseth](/u/chriseth) his thoughts? And whether the changes proposed by [@rumkin](/u/rumkin) could be easily adopted by the compiler.

In terms of `camelCase` vs `snake_case` - it’s a more significant breaking change. I’m open to the change if there is general consensus that it’s important / worthwhile.

---

**gh1dra** (2020-03-11):

Is there a particular reasoning for why the `devdoc` and `userdoc` are being surfaced for a particular contract inside `contract_types`? From my understanding of the spec, those fields be made available if the `CompilerInformationObject` field is already given. Is the idea to give users the choice about what kind of information they choose to provide about the compilation?

---

**chriseth** (2020-03-12):

I’m fine with breaking Solidity metadata with regards to “version” if it is a dealbreaker for EthPM as long as it is still possible to easily determine whether the given json is a v1 Solidity metadata json.

I would also prefer camelCase.

Funther remarks (I’m really not sure if this forum-style discussion is the best way to do this):

sources: " Paths **must** resolve to a path within the current virtual directory." - do we really need this requirement? What does it mean for a path to resolve to such a path? How do you determine if it resolves to a directory or to a file?

“contract_types”:

If there are multiple contract types specified - is there a way to provide the “main” contract in some way? For Solidity metadata, there is exactly one contract type that is the one currently being compiled. Is the expectation that in this case, there is only one item in this object?

contract alias: In the Solidity compiler, we identify names by prefixing the file name (including path) followed by a “:”. How do contract aliases identify the actual contract in the source?

Why is the compiler a sub-field of the contract type? I see that different compilers could be used for different contract, but in that case, shouldn’t the sources also be a sub-field of the contract type?

---

**rumkin** (2020-03-21):

> I’m really not sure if this forum-style discussion is the best way to do this

What’s the best place to do so? Let’s move it there. It’s possible to separate some questions into issues, but IDK where to put them.

> If there are multiple contract types specified - is there a way to provide the “main” contract in some way?

I think it’s reasonable to define `default` keyword in Solidity to specify it explicitly. It would help to export things with automated tools. Libraries authors usually define single contract per file, but it’s only an agreement and it’s not certain for all libraries. Export such a contract as the main one doesn’t seem correct due to this uncertainty.

---

**njgheorghita** (2020-03-24):

> Is the idea to give users the choice about what kind of information they choose to provide about the compilation?

[@gh1dra](/u/gh1dra) The `compiler` field is for information about the compiler and its settings that were used to generate the outputs (abi, bytecodes, userdoc, devdoc) rather than containing the outputs of the compilation. As you said, this gives the user more flexibility in choosing what fields they want or are able to include in a manifest.

> I’m fine with breaking Solidity metadata with regards to “version” if it is a dealbreaker for EthPM

It’s not a dealbreaker for me, but I do prefer the scheme (`"manifest"`, `"name"`, `"version"`) that [@rumkin](/u/rumkin) proposed the best. It’s the cleanest / easiest to understand.

> as long as it is still possible to easily determine whether the given json is a v1 Solidity metadata json.

If we adopt this scheme, I’m not so sure this will be easily achieved. As [@fubuloubu](/u/fubuloubu) pointed out, there will be ethpm v1 & v2 manifests that have a `"version"` field of `"1"` (referring to the version of that specific package release, rather than the specification it conforms to). These will be impossible to simply distinguish from v1 Solidity metadata json (which also have a `"version"` field of `"1"`). Unless the tooling has the knowledge to search for a `"manifest"` field (required in all ethpm v3 manifests), validate that it is `"3"` - and then it will be able to distinguish b/w the two specifications. So it is possible reliably determine which specification a json object is, but it won’t be trivial. If this is an acceptable amount of complexity for [@chriseth](/u/chriseth), I’ll update the spec to reflect this change.

> I would also prefer camelCase.

![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12) I’m also ok with this change. Unless any of the python/vyper ppl have strong objections, I’ll update the spec.

> sources: " Paths  must  resolve to a path within the current virtual directory." - do we really need this requirement? What does it mean for a path to resolve to such a path?

For ethpm, we need the ability to faithfully recreate the original source tree. Otherwise, when users “install” a package to disk - if the paths are not the same paths of the original source tree, then they might not be able to re-compile the sources.

In ethpm v1/v2 we required all paths to be relative paths that begin with `./` (the root of the virtual directory), which has worked well. Though, I understand the solidity compiler might not want to enforce such a requirement. If we relax this requirement, we’ll need to define an additional mechanism (like a `filesystem` key) that maps the paths used to valid filesystem paths - which will be required for packages to have the capability to be written to disk (“installed”).

> How do you determine if it resolves to a directory or to a file?

If the path points to a content-addressed uri, the uri must be resolved to determine whether it’s a directory or a file. The only other option is for the path to point to an inlined string of the source contract which would always be a single file.

> If there are multiple contract types specified - is there a way to provide the “main” contract in some way? For Solidity metadata, there is exactly one contract type that is the one currently being compiled. Is the expectation that in this case, there is only one item in this object?

Yup, that’s how I’d see it working out.

> contract alias: In the Solidity compiler, we identify names by prefixing the file name (including path) followed by a “:”. How do contract aliases identify the actual contract in the source?

In ethpm a [contract alias](http://ethpm.github.io/ethpm-spec/glossary.html#term-contract-alias) is defined as `<contract-name>[<identifier>]`. In ethpm v1/v2 there was no mechanism to map a contract type to a source - however in v3 it seems to me as though the `compilationTarget` field in the compiler settings would serve this function.

> Why is the compiler a sub-field of the contract type? I see that different compilers could be used for different contract, but in that case, shouldn’t the sources also be a sub-field of the contract type?

I’m not sure I understand this concern exactly. There are packages that would be useful with just `"sources"` and no `"contract_types"`. Also, different compilers could be used to generate different `"contract_types"` for the same source. This would introduce a lot of redundancy if sources were located in `"contract_types"`.

> I’m really not sure if this forum-style discussion is the best way to do this

Agreed, I’m starting to think that it’s time to move this to github, where we can have more nuanced threads around specific concerns. I’ll work on migrating the changes discussed here to the [ethpm-spec](https://github.com/ethpm/ethpm-spec) repository - and link it here once it’s updated.

---

**chriseth** (2020-03-24):

Can we just schedule a call tomorrow or on Thursday and settle most of the questions in on hour? ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**njgheorghita** (2020-03-24):

Good call - let’s aim for 9AM CST / 3PM CET on Thursday. It’s flexible so if anybody would like to join but has a conflict - we can adjust the time as needed. I’ll post a zoom link here a couple minutes before the time we settle on.

---

**njgheorghita** (2020-03-26):

Here’s the zoom link for the call taking place in about 5 minutes

https://us04web.zoom.us/j/902568522?pwd=VlFtTldGNzFFcFpOdUVjOWdlcTFkdz09

---

**njgheorghita** (2020-03-26):

Updated zoom link

https://us04web.zoom.us/j/355814183?pwd=OW5uWWIvZjFUZDl6c3pOUkFZN0NYQT09

---

**chriseth** (2020-03-26):

Thanks for the call, that was very insightful!

During the call, ben was briefly talking about importing interfaces through their JSON-ABI as an interoperability measure. The relevant issue in the Solidity repo is here: https://github.com/ethereum/solidity/issues/1687

A [comment by alex](https://github.com/ethereum/solidity/issues/1687#issuecomment-559143276) suggests to put these abi-json interfaces in their own files in the standard-io-input (as part of the “sources” field) and  add a “kind” field for each source file where this would be something like “abi-json”.

This “kind” field would also make it easier for projects spanning multiple languages.

---

**rumkin** (2020-03-26):

For interfaces import I’d suggest to have an ability of file import, like so:

```nohighlight
interface Token from './erc20.json'
```

And for JSON files with custom structure it’s possible to define a path inside of JSON:

```nohighlight
interface Token from './erc20.json#contracts[0].abi'
```

Where `./erc.json` is a path to ABI file and `#contracts[0].abi` is a path inside of JSON object. It uses some trick as URL suppose hash wouldn’t be sent with a request and should be handled on the client, it’s safe to use hash in paths like so. And handle it with solidity compiler itself.

---

**njgheorghita** (2020-04-07):

[@rumkin](/u/rumkin) I’m not hugely familiar with how the solidity compiler handles imports - but this seems a little out of scope for the ethpm v3 specification. I could be wrong though, so feel free to bring this up at the next sync.

---

**njgheorghita** (2020-04-07):

Hey Guys! Hope everyone’s well.

The ethpm docs now reflect the changes we’ve discussed. http://ethpm.github.io/ethpm-spec/

There is now a machine-readable schema to validate v3 manifests - it can be found under `spec/v3.spec.json` in the ethpm-spec repo.

The examples in the ethpm-spec repo have been updated to reflect the changes in the spec - for a visual idea of what v3 packages might look like. You can find them under their respective folders under `/examples/` with the file name `v3.json` @ https://github.com/ethpm/ethpm-spec

This spec is still a WIP - though we’ll be trying to finalize it within the next sync or two - so the sooner we get any suggested changes, the better. To give everyone enough time to go over the changes / examples, let’s plan our next sync for Thursday, April 16 - at 9AM CST / 3PM CET. If that time doesn’t conflict with anybody, I’ll post a zoom link here shortly before. Cheers!

---

**njgheorghita** (2020-04-16):

Here’s the link for the sync in 5 minutes.

https://us04web.zoom.us/j/79099681560?pwd=S01qaDFmb0c1Z1QvM1BvMTZXNVUxZz09

---

**njgheorghita** (2020-04-30):

Just a heads up, if you’re not already attending the solidity online conference. There’s going to be an ethpm discussion tomorrow at 8:55 pm central european time. The conversation will revolve around ethpm devx and the v3 technical specification. If you can make it, it’d be great to see everyone there!

https://interspace.solidity-summit.ethereum.org/


*(23 more replies not shown)*
