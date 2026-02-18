---
source: magicians
topic_id: 11350
title: Physical Backed Tokens
author: 2pmflow
date: "2022-10-17"
category: Magicians > Primordial Soup
tags: [token]
url: https://ethereum-magicians.org/t/physical-backed-tokens/11350
views: 3769
likes: 10
posts_count: 20
---

# Physical Backed Tokens

A simple extension for tying a physical item to a digital token



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5791)














####


      `master` ← `2pmflow:pbt-eip`




          opened 03:29PM - 17 Oct 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/5/5c2724fde6db5192b90b043b53283441ecf8cf98.png)
            2pmflow](https://github.com/2pmflow)



          [+165
            -0](https://github.com/ethereum/EIPs/pull/5791/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/5791)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**subinium** (2022-10-24):

I’m very excited that the standard for physical assets is coming out. I would like to suggest some comments to make this EIP a better EIP.

### 1. Chip

I think that the word `chip` used in the function alone is insufficient to express the meaning of “Real World” or “Physical Backed”.

I hope to find a more suitable word & function name together with the community.

### 2. Requirements

This sentence is ambiguous.

> This approach requires that the physical item must have a chip attached to it that fulfills the following requirements:

Depending on the reader, there is room for interpretation as “the chip is absolutely essential” or “the following conditions are essential” or both.

`can` and `cannot` are expressions that are ambiguous for EIP/ERC. I think it would be cleaner if you fix the condition using ‘MUST’ and ‘MAY’ clearly.

It would be good to refer to the [recent comments on EIP-5528](https://github.com/ethereum/EIPs/pull/5790#pullrequestreview-1146519906).

### 3. event PBTChipRemapping

`PBTChipRemapping` is a really good idea. Appropriate functions should also be included in this proposal.

### 4. Recover

It would be a better standard if the description of ‘recovery’ had additional explanations in the Specification or Rationale.

---

**2pmflow** (2022-10-24):

Appreciate the comments.

1. We chose the word “chip” in transferTokenWithChip, instead of something like transferTokenWithPhysical, to be more precise in denoting what part of the physical is actually relevant for the txn. Currently feel like it’s both suitable and accurate, but open to hearing other suggestions.
2. There’s no reference to “can” or “cannot” here- we chose the word “requires” and “must” to denote that a chip following those conditions is essential. Could you clarify?
3. I don’t believe the “how” of remapping is in scope for this minimal interface, similar to how mint isn’t defined in 721/PBT. There are lots of ways to implement remapping and I don’t see that as a critical part to standardize yet alongside core transfer functionality, as it can vary heavily per project.
4. Good point, it’s not covered much until the Reference Implementation. We did mention that the signature needs to follow EIP191 and EIP2 (s-value restrictions) but could do a better job clarifying in earlier sections.

---

**subinium** (2022-10-25):

Thanks for the kind and good answer. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

I have additional comments.

I don’t think PBTMint is a minimum implementation requirement. I think it would be better if only remapping event was a minimum.

The user can see that the transition from address 0 to non-zero address is minting.

What is the role of PBTMint, and why do you think it is necessary as a minimum?

---

**2pmflow** (2022-10-25):

One benefit of PBTMint event being emitted is that the event data includes the chip addresses, which lets downstream indexers know about which chip address are relevant for the collection. Without that, there’s no way to get the set of valid chip addresses at the interface level.

---

**Rqueue** (2022-10-28):

Great to see an effort in the area of linking physical to digital.

I had two questions/comments after reading the proposal:

1. transferTokenWithChip(...) arguments

I think the aim to form a protocol that isn’t opinionated is a great approach. However, with the current `transferTokenWithChip` method’s fixed argument list, it seems like it could prevent opinionated approaches from being implemented by protocol conformers and prevent the addition of restrictions implementors may want to add. Protocol conformers may want to add extra required data (such as signatures from other wallets like the PBT owning wallet) for a transfer to happen. Adding any wrapper methods that wrap `transferTokenWithChip` and require extra arguments could currently just be bypassed by calling `transferTokenWithChip` directly so long as someone is able to get a hold of the chip/item with the chip.

What are your thoughts on adding a `payload` parameter to `transferTokenWithChip` for added flexibility? I think requiring the `blockNumberUsedInSig` as a separate argument is still a good idea to better guide devs to incorporate a “time based” check, so `payload` could be an additional argument. My main thought here is to give devs the ability to add extra permission or security features required for transferring if they wish to.

1. Does “chip” need to specified?

I understand the push towards specifying a physical chip to use in the protocol. I will also mention that I am not familiar with how common (or rare) it is for other EIPs to reference physical objects linked to protocols, so forgive me if this comment is a non-issue.

As I was reading the protocol, I couldn’t help but think of how much of a barrier to entry it would be for devs to procure a chip that met the required specifications. There is also the issue that all of the chip requirements cannot be enforced/checked via code such as, “The private key cannot be extracted”. In general it seems to me the chip and its use in the protocol can be generalized to an ECDSA secp256k1 asymmetric key pair, which would lower the barrier to entry as a wallet could be used here instead.

What are your thoughts around removing the “chip” requirements and replacing it with just an ECDSA secp256k1 asymmetric key pair? With this a “chip” could be one use case/implementation while another could be the linkage of whole wallets to tokens where transferring the wallet is like handing over ownership of an entire account. I’m sure there are also other use cases that I cannot think of, but this generalization feels like it could allow for more flexibility as well.

---

**2pmflow** (2022-10-30):

Hey rqueue thanks for the suggestions, and nice pfp ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

**Re: transferTokenWithChip arguments** - “Adding any wrapper methods that wrap `transferTokenWithChip` and require extra arguments could currently just be bypassed by calling `transferTokenWithChip` directly so long as someone is able to get a hold of the chip/item with the chip.”

I don’t actually this is true - if you look at how OpenZeppelin’s widely used 721 implementation played out, it’s very easy to have the standard impl support hooks like beforeTokenTransfer that do appropriate asserts for a custom implementation that wants required data.

Also, the interface intentionally wants to be opinionated on transferTokenWithChip specifically to enable a downstream aggregator-like product that supports transfers of any NFTs that implement this EIP in the future. Supporting custom data encourages transfer implementation customization which makes such a product less feasible.

I noticed 721 safeTransferFrom does have a `data` param in its signature and was considering that for consistency, but upon closer examination, it looks like that `data` isn’t meant for consumption from the direct receiving contract and is meant for the `_to` receiver).

**Re: renaming chip** - We like the word “chip” explicitly called out in the interface instead of “asymmetric keypair” because the word “chip” denotes physical presence. Even if the standard itself can’t enforce that the addresses supported by the contract creator are actually tied to a chip, the physical domain is still what the EIP sets to set a standard for.

---

**definevalue** (2022-10-30):

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/4/4892639d60103d8d3fe76ad6322b11a790075fe4_2_375x500.jpeg)image1920×2560 249 KB](https://ethereum-magicians.org/uploads/default/4892639d60103d8d3fe76ad6322b11a790075fe4)

Like these here? So in 2013 they exposed public key but private key was hidden behind tamper proof seal they were pretty cool but I think integrating a the same chip that you see in the arculus wallets that’s the way I know they’re easily programmable. Didn’t really read to much other then the title ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=15)

---

**Rqueue** (2022-10-30):

- transferTokenWithChip arguments

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/2pmflow/48/7476_2.png) 2pmflow:

> I don’t actually this is true - if you look at how OpenZeppelin’s widely used 721 implementation played out, it’s very easy to have the standard impl support hooks like beforeTokenTransfer that do appropriate asserts for a custom implementation that wants required data.

Ah good point. A sample implementation with that pattern in the repo could be helpful just to seed the idea for people.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/2pmflow/48/7476_2.png) 2pmflow:

> Also, the interface intentionally wants to be opinionated on transferTokenWithChip specifically to enable a downstream aggregator-like product that supports transfers of any NFTs that implement this EIP in the future. Supporting custom data encourages transfer implementation customization which makes such a product less feasible.

Hmm sorry, I’m having trouble seeing how additional arguments or custom transfer implementations would block the creation of a downstream aggregator-like product so long as the 5791 implementation abides by the expectation that calling the `transferTokenWithChip` method “Transfers the token into the message sender’s wallet.”. My thinking is that in order for an aggregator to get the `signatureFromChip`, it will already have to pass the `blockNumberUsedInSig` to the chip, so if we had an additional `payload` argument, it would also pass this to the chip to generate the signature. I do agree this would make creating an aggregator more difficult though. Were you alluding to the complexity tradeoff rather than it being impossible? Let me know if there is some scenario I am not considering that makes it impossible.

More generally, my comment here on customization stems from noticing some of the pitfalls in ERC-721 having a similar simple transfer mechanism. By this I’m referring to how currently NFT owners must `setApprovalForAll` to marketplaces and other apps to allow transfers since the ERC-721 transfer methods are very simple. I don’t know what the best solution is for this type of problem, but my thinking was the addition of a `payload` argument would allow other devs the ability to easily experiment with creative solutions for problems like this or other unforeseen problems. There is of course a tradeoff here, so I think an argument can be made both for or against it. Just wanted to throw the idea out there.

- renaming chip

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/2pmflow/48/7476_2.png) 2pmflow:

> Re: renaming chip - We like the word “chip” explicitly called out in the interface instead of “asymmetric keypair” because the word “chip” denotes physical presence. Even if the standard itself can’t enforce that the addresses supported by the contract creator are actually tied to a chip, the physical domain is still what the EIP sets to set a standard for.

Fair point. Wording does help guide the direction people will develop for.

---

**2pmflow** (2022-10-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rqueue/48/7586_2.png) Rqueue:

> A sample implementation with that pattern in the repo could be helpful just to seed the idea for people.

Agreed, this is actually [in the works](https://github.com/chiru-labs/PBT/pull/21#pullrequestreview-1153726378)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rqueue/48/7586_2.png) Rqueue:

> I’m having trouble seeing how additional arguments or custom transfer implementations would block the creation of a downstream aggregator-like product so long as the 5791 implementation abides by the expectation that calling the transferTokenWithChip method “Transfers the token into the message sender’s wallet.”

It wouldn’t block per se, but encouraging custom implementations of transfer would make transfers more unlikely to succeed. For example, if every PBT contract implementation had its own custom additional constraints on what is required in a transfer (e.g. requiring that the `payload` argument includes X), a generic UX that facilitates PBT transfers would fail when a user tries to transfer that PBT. It’s similar to how soulbound NFTs on OpenSea aren’t transferable and can have unexpected behavior on Opensea UX when their transfers fail.

---

**Rqueue** (2022-11-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/2pmflow/48/7476_2.png) 2pmflow:

> It wouldn’t block per se, but encouraging custom implementations of transfer would make transfers more unlikely to succeed. For example, if every PBT contract implementation had its own custom additional constraints on what is required in a transfer (e.g. requiring that the payload argument includes X), a generic UX that facilitates PBT transfers would fail when a user tries to transfer that PBT. It’s similar to how soulbound NFTs on OpenSea aren’t transferable and can have unexpected behavior on Opensea UX when their transfers fail.

For sure, I agree a generic UX is much easier to build without the custom `payload`. Part of my thinking was that by including the `payload` in the protocol it would *force* apps such as an Opensea to have to account for customization from the start (especially if popular PBTs started adding customization). If the only way to add customization to the transfers is by adding in `_before` hooks, that seems near impossible for an aggregator to support unless they define a new protocol that gains adoption. That being said, customization for transfers could be YAGNI and overcomplicate things. In web2 I think keeping it simple would 100% be the way to go, but given the protocol is immutable in web3, I think it could go either way. Again, I just wanted to state my thoughts as I don’t think there is a clear best choice. I also would love to see what sorts of customizations developers would come up with.

---

**2pmflow** (2022-11-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rqueue/48/7586_2.png) Rqueue:

> For sure, I agree a generic UX is much easier to build without the custom payload. Part of my thinking was that by including the payload in the protocol it would force apps such as an Opensea to have to account for customization from the start (especially if popular PBTs started adding customization). If the only way to add customization to the transfers is by adding in _before hooks, that seems near impossible for an aggregator to support unless they define a new protocol that gains adoption. That being said, customization for transfers could be YAGNI and overcomplicate things. In web2 I think keeping it simple would 100% be the way to go, but given the protocol is immutable in web3, I think it could go either way. Again, I just wanted to state my thoughts as I don’t think there is a clear best choice. I also would love to see what sorts of customizations developers would come up with.

Gotcha. These are fair points- ultimately I don’t think there’s a right answer and currently think that it’s a YAGNI situation in practice. Absolute worst case, a new EIP can define that extension, but similar to how it wasn’t created for 721 I suspect that won’t happen.

---

**harshjv** (2022-11-03):

Re-voicing my thoughts here (shared on discord before);

To prevent unauthorised transfer of NFT, can the transfer happen in N stages? The real owner needs to tap the chip N times at least Y blocks apart to get make the final transfer;

So it would look something like this;

```auto
MIN_DELAY = 5
prepareTokenTransferWithChip(signatureFromChip, blkHash10) // sets _transferChecks[chipAddr] = 10
transferTokenWithChip(signatureFromChip, blkHash16) // checks if _transferChecks[chipAddr] is set and blkHash16 is over MIN_DELAY + map[chipAddr]
```

This can be done only for transfers or mint & transfers?

---

**2pmflow** (2022-11-03):

Hey harshjv, that can absolutely be built on top of PBT. PBT is meant to be just the base layer scan-to-own primitive, but we also currently have people chatting about custom validation layers on top in the repo through beforeTokenTransfer hooks (see thread here [Added new PBT example with transaction auth by Arkay92 · Pull Request #21 · chiru-labs/PBT · GitHub](https://github.com/chiru-labs/PBT/pull/21#pullrequestreview-1153726378)). Feel free to check it out!

---

**xtools-at** (2023-01-17):

thanks for this proposal, it really triggered my curiosity ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

i’m working on a prototype device with BLE interface, which fully implements the EIP-5791 specs, created from an off-the-shelf chip one can get freely for $5-10. it’s not as sexy as the Kongcash NFC chips, but would enable everyone to dabble in PBTs.

will report back if you guys are interested in this, will probably open source it when done.

---

**2pmflow** (2023-01-17):

Cool, looking forward to it!

---

**xtools-at** (2023-01-24):

[@2pmflow](/u/2pmflow) still ironing out some kinks before announcing it officially (as if anyone would care for the stuff i build ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12)) , but here’s a sneak preview of the status quo ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) https://xtools-at.github.io/esp5791/

will also add bulk scanning of chips to the gui, just want to E2E test everything properly first. if there’s any interest, i could also integrate it into the pbt js lib: https://github.com/chiru-labs/pbt-chip-client

---

**2pmflow** (2023-01-24):

Sounds awesome, keep us posted!

---

**tbergmueller** (2023-10-23):

I had mentioned this in ERC-6956, but since your proposal’s status is still in draft [I had to remove the link in order to proceed to Review](https://github.com/ethereum/EIPs/pull/7903). Please ping me in case this proposal moves forward.

---

**2pmflow** (2023-10-23):

Hey [@tbergmueller](/u/tbergmueller), we’re discussing some small additions to the spec atm, should have an update soon.

