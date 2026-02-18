---
source: magicians
topic_id: 283
title: "ERC-1066: Ethereum Status Codes (ESC)"
author: expede
date: "2018-05-05"
category: EIPs
tags: [erc-1066, dx]
url: https://ethereum-magicians.org/t/erc-1066-ethereum-status-codes-esc/283
views: 14869
likes: 41
posts_count: 50
---

# ERC-1066: Ethereum Status Codes (ESC)

Hi everyone ![:waving_hand:t2:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand/2.png?v=15)

I’ve submitted an EIP to bring status codes to the Ethereum ecosystem (link below). This proposal is purely about convention, requires no changes to the EVM, and is usable today. Further investigation is being done to potentially add these to the transaction status field, but that is out of scope of this EIP.

ERC-1066 outlines a common set of Ethereum status codes (ESC) in the same vein as HTTP statuses or BEAM tagged tuples. This is a shared set of signals to allow smart contracts to react to situations autonomously, expose localized error messages to users, and so on.

Feedback, discussion, and suggested statuses are all greatly appreciated ![:raising_hands:t2:](https://ethereum-magicians.org/images/emoji/twitter/raising_hands/2.png?v=15)

# Links

- ERC-1066
- Helper library and examples (WIP)

## Replies

**chfast** (2018-05-18):

Hi there,

I understand the scope of this EIP is much bigger, but see the EVM status codes: https://github.com/ethereum/evmc/blob/master/include/evmc/evmc.h#L199.

---

**expede** (2018-05-23):

Ah, good point! Will update that mention in the EIP; thanks!

---

**alexvandesande** (2018-05-28):

Solidity has [support for revert with messages since 0.4.22](https://github.com/ethereum/solidity/releases/tag/v0.4.22), so I suppose the idea here would be to use these status codes on these error messages too, correct?

---

**expede** (2018-05-28):

Status codes in this proposal are orthogonal to revert-with-message, and are fully compatible with them. Revert really ends the transaction, and status codes are meant primarily for communicating between contracts, in much the same way as an actor system would. As such, the scope extends far beyond just types of failure or reverting, and are ideally used to automate system flow and user feedback.

Part of the design goal is to make these compatible with revert-with-message, including a message in the correct language, level of technical detail, and so on. [Here is an example](https://github.com/Finhaven/EthereumStatusCodes/blob/master/contracts/Status.sol#L88) from the helper library of a function that will fail with a message when the status is not `ok`. Further work is being done to translate codes in on-chain registry to fail with an automated message based on the caller’s preferences. Here is an example of some early work in that direction with [English translations of codes](https://github.com/Finhaven/EthereumStatusCodes/pull/16/files#diff-3f6431823099c7468ff4199ec78ed4a8R5).

---

**alexvandesande** (2018-05-29):

Thanks for doing this [@expede](/u/expede)!

I was looking at some default contracts in the [ethereum.org](http://ethereum.org) and I already felt the need for a few error codes for very common situations, as I found myself overusing “disallowed” and “failure” for everything. I suggest adding:

- Not enough balance: this can be used for sending tokens, checking allowances, buying stuff etc. Maybe 0x36?
- We have 0x10 Disallowed but I would like the errors to be more specific: User not authorized for functions that are onlyOwner, onlyMember and other generic auths, and Action not authorized for when the action itself, not the users, are forbidden. Maybe I would even be more specific and add a Not allowed at this time for actions that timestamp specific (can only be done before or after a given deadline).

Maybe I’m being too specific, one could argue that all `Disallowed` erros always mean **that user cannot do this action at this time** and that asking for too much specificity will pollute the error table. But from the point of view of a user interface wallet that is warning the user that an action will not be permitted, it would be good to have a distinction to show the user why the action is returning an error: is it that *you* cannot to it, or is that you must wait?

Maybe we should add sub-error-tables?

```auto
0x10 Disallowed
0x101 User not permitted
0x102 Action not permitted
0x103 Disallowed at this time
```

(Just noticed `0x15	No Longer Allowed`. Maybe we also need a `0x16 Not Allowed Yet` then?)

Also… What should be the error code for **integer overflow**?

---

**shrugs** (2018-06-12):

Is including application-specific error contexts part of this EIP? i.e., adding “reasons” to the status codes.

I bring this up because in protocols like HTTP, status codes are used for informing clients of errors in a standard way so that that they can retry a request, disable a feature, require a login, etc. This EIP accomplishes that ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=9) . Generally, though, people also include information in the request body beyond the status code, to indicate application-specific things like `Permission Denied: Upgrade your Account to Pro` which the UI can then display to the user.

Anyway that would be useful for contracts as well, primarily for compatibility between revert-with-reason, which people have already started adding english error messages to.

revert-with-reason using english messages isn’t a really great way of accomplishing this:

1. strings are expensive to store/transmit if a smaller identifier would suffice
2. english, while the canonical language of the web, shouldn’t really be expected

It’d be cool if I could return an error context along with the status code, but also if that error context were compacted like:

```auto
returns (byte status, bytes4 reasonId)
```

where `reasonId` is perhaps `bytes4(keccak256("Account is not Pro"))`.

The mapping of `reasonId->humanReadableReason` can be managed within a single-address registry contract that anyone is free to add to (perhaps a custom ENS registry!). This gives everyone with access to Ethereum a way to resolve, off-chain, what the context of the error is and display it within things like truffle. If internationalization is desired, an off-chain service can be made (similar to the 4 byte directory) which tracks the mapping of `reasonId` to the error string.

This would also be cool for revert with reason: `require(thing, )`

The reasonId could also be the first 3 bytes, so that it could be concatenated with the status byte to create a compact `returns (bytes4 statusAndReason)` syntax. smart contracts can just do `byte(statusAndReason)` to get their status code, and off-chain tools can easily splice to get the reason, and then perform the lookup on their own (a smart contract shouldn’t really need to do any lookups on-chain for a reason string).

Anyway, just looking for feedback on whether or not that approach is 1) worth discussion and 2) should be part of this EIP or another, later EIP

---

**expede** (2018-06-20):

Hi [@shrugs](/u/shrugs),

Yes, indeed both are part of the EIP! Glad to see that others are on the same wavelength. There are two distinct use cases for status codes:

1. Automation
2. User feedback

Automation is pretty straightforward: we just need a lightweight code. User feedback is very broad, and should account for things like translation and varying levels of detail.

# Custom Codes

The `0xA*` range is dedicated to application-specific codes for contract authors to define. This assumes that 16 codes is sufficient for application-specific codes. I don’t think that I’ve worked with a module that needs more than a handful, but hey, it could happen? I would expect this to be a code smell, though.

In that case, the appropriate thing may be to do as you suggest: serialize a bunch of context or come up with a custom scheme of subcodes. (Imposing a design up front would lead to edge cases on this edge case, I think).

# Human Readable Messages

[Status code translation contracts](https://github.com/expede/ethereum-status-codes/tree/master/contracts/localization) are currently being sourced in English, Polish, French, Japanese, and German. If you (or anyone you know) are able to translate to other languages, that would be very welcome! The ones in the repo are meant as a starting point, with ongoing, community-controlled voting on better/preferred translations that live in a smart contract. However, I  think that contract authors should have the choice to use alternate translations if they choose, and may point their application

Context-specific information probably *shouldn’t* be passed around in messages, but kept right at the message site (ex. revert with reason). There are edge cases where it’s appropriate, and nothing is stopping people from doing that if the need arises. The messages that are going to come out of the translation table aren’t sacred, and authors should feel free to append or otherwise alter them as needed.

# ENS

Ah, I hadn’t considered giving them all ENS names! Great idea ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=15)

---

**expede** (2018-06-20):

Hi [@alexvandesande](/u/alexvandesande),

## Permissions

Ah, good idea on `onlyOwner`, &c! I hadn’t considered these, but they’re exceedingly common. Will add!

There actually is a `Not allowed Yet` ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=15) An earlier draft even was called that verbatim, but we reprhrased it as `0x13 Awaiting Permission`.

## Sub-codes

We’ve explored this, and are not a fan. There’s an infinite level of granularity, and the combinatoral complexity makes translation nearly impossible. It’s a less-is-more case: by limiting ourselves (if 256 is “limited” ![:stuck_out_tongue_winking_eye:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue_winking_eye.png?v=15)), we can do more with each code. Situations that are deeply context-specific can come along something like one of the following:

```sol
returns (byte status, string message)
// ex. (hex"A0", "System went boom")

returns(byte status, uint8 customSubcode)
// ex. (hex"10", 1)

returns (byte status, uint8 requiredAuthLevel, address[] requestAuthFrom)
// ex. (hex"10", 4, [0x123f6..., 0x3c6ae...])
```

## Integer Overflow

First let me say that the fact that overflows are part of the EVM spec drives me crazy. I could rant all day about this, so I’ll leave it at that ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=15)

![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=15) I suppose that it could be covered under `0x25 Out of Range`, but perhaps there is a case for low-level codes to cover arithmetic errors to cover the same cases as `SafeMath`. I’m of two minds on this one:

### 1. Status Codes are for Communication

Integer overflow is a bug and should never be allowed to occur in a contract. Codes are meant for communicating between contracts, or for *user* feedback, not debugging. It also may be a bit granular/lacks semantics. As an end user, I don’t care that `0x66 Integer Overflow`, I care that `0xA6 Namespace Full`.

### 2. Overflows are Common

Because of the way the EVM is designed, over- and underflows are sadly an easy mistake to make. Maybe communicating that there was an arithmetic error would have some internal utility? Translations here are better than not having them, for instance.

---

I’ll be honest: working through the idea has pushed me back into the “status codes are for communication” camp. `0x66 Integer Overflow` (or similar) isn’t terribly helpful, and can probably be handled with a simple revert. A more semantically rich message would be more helpful to a user. Again, not to say that I’m totally opposed to the idea, but I’m just not convinced yet.

I’d love to hear any further thoughts that you have!

---

**expede** (2018-06-20):

![:rotating_light:](https://ethereum-magicians.org/images/emoji/twitter/rotating_light.png?v=9) I should also mention that the implementation/helper library is moving here: https://github.com/expede/ethereum-status-codes. I will be updating the link in the EIP shortly.

---

**alexvandesande** (2018-06-20):

[@expede](/u/expede) I agree with your points and I take back my suggestion of subcodes and even for integer overflow (in there probably some “internal error”/“out of bounds” would suffice)

I maintain my request to have these errors:

- Action not allowed / User not allowed / Not allowed yet / Not allowed anymore / Not enough balance

I understand “waiting permission” as “your action was executed, we are just waiting for someone to give an ok”, while “not allowed yet” means “you can’t do this now, please try again later”.

---

**shrugs** (2018-06-21):

Agreed that permission layer status codes would be useful. Primarily I think it’d be really good to have them for informing users who are doing two-step transfers (where one side proposes a transfer and the other directly accepts it on-chain).

Re: reason codes; awesome, sorry I didn’t see that on the first read-through ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=9)

I still think it would be valuable to have a registry to keep track of `contract address` → `status code` → `english string` just like that `StatusCodeLocalization` contract.

`0x05.default.statuscodes.eth` has a nice ring to it, and removes the need for the `StatusCodeLocalization` registry. The `default` namespace is so that we could also have alternative namespaces for contracts like `0x05.0xdeadbeef.statuscodes.eth` and include those application specific error codes. Although now we need to deploy an ENS resolver, and that can get annoying pretty quickly. ¯\_(ツ)_/¯

---

**gregc** (2018-09-22):

A bit orthogonal, but might be relevant.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/118)












####



        opened 03:58PM - 19 Jun 16 UTC



          closed 02:24AM - 30 Jan 22 UTC



        [![](https://avatars.githubusercontent.com/u/158211?v=4)
          wanderer](https://github.com/wanderer)





          stale







## DESCRIPTION

If block.number >= METROPOLIS_FORK_BLKNUM, then opcode 0xfa func[…]()tions equivalently to a CALL, except it takes 6 arguments not including value, and makes an ASYNC calls the child. No Items are PUSHED on to the stack. Normal Calls made after an Async call work as normal.

In the current execution model, async calls are executed after the parent execution is finished.  If more than one Async calls (ac₀, ac₁ .... acₙ) happened during a given execution then after the parent execution has stopped then the async calls are ran in the order that they were generated (ac₀, ac₁ .... acₙ).

Here is a Sequence Diagram of the current model
![current](https://docs.google.com/drawings/d/1GJV7coOiVV14ksFmRXw9rcojKC66MrEBrTZL2O-nkRA/pub?w=300&amp;h=500)

The first instance of A (A₀) Make a call to contract B which then make a call back to A which creates a new instance of A (A₁)

Here is how Async calls would look
![async](https://docs.google.com/drawings/d/1bvBVicUu6TH2b9b7_uJbBDSrviyBY0NjWomWbxMQa80/pub?w=278&amp;h=365)

Only one instance of A is every created. All calls are run sequential.

In the future we maybe able to loosen the restriction on running calls sequentially. In a Concurrent Model Async calls could run in parallel.  It is assumed that contracts running concurrently would be running at the same "speed" (gas Per clock cycles).

![concurrent](https://docs.google.com/drawings/d/1HNnFhFia_bIyrUZgtCluzXKcFnDBEgWRMYDfJwl8Sqs/pub?w=278&h=365)
## REVERTS

Reverting also work that same way as the current model. If the parent execution run out of gas the child async calls will not be executed. (although a future improvement could this restriction optional)
## GAS PRICE

The gas price should be half that of CALL (20 gas) since you could view an async call as one half of a sync call.
## RATIONALE

By using async calls a contract programmer can guarantees about the state of storage and contract re-entry.

The async call can also be used in the future for cross shard communications. In this scenario async call would have to be modified to accept a port (which parent shard to call). It would work similar to `ETHLOG` except there would be no need for a get log.

Last async calls can be used to recall a contract if recursive calling is disable (in an actor model where contracts are actors or It can also be thought of as contracts being singleton instances). [See here ](https://docs.google.com/document/d/1A_f4NOZelNq1R3LAnZLNCcITWkcp3BYXD8zohGRg9cA/edit?usp=sharing)
## REFERENCES
- [mauve paper](vitalik.ca/files/mauve_paper.html)
- [An Alternative Hardfork Strategy](https://docs.google.com/document/d/1A_f4NOZelNq1R3LAnZLNCcITWkcp3BYXD8zohGRg9cA/edit?usp=sharing)
## ALTERNATIVES
- static calls #116
- sandboxed calls #117

---

**expede** (2018-09-24):

`ASYNC_CALL` is orthogonal, but totally compatible! I was very happy to see that proposal ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9) Concurrency and asynchrony are inevitable IMO, and it’s good to see progress in that direction ![:muscle:](https://ethereum-magicians.org/images/emoji/twitter/muscle.png?v=9)

---

**gcolvin** (2018-09-24):

Unfortunately, I don’t think this proposal hasn’t progressed since 2016, [@expede](/u/expede).  You’d have to ask Martin whether he plans to move forward with it.

---

**expede** (2018-09-24):

[@gcolvin](/u/gcolvin) Okay good to know; thanks! My hands are pretty full with [#erc-1066](https://ethereum-magicians.org/tag/erc-1066) and [#erc-1444](https://ethereum-magicians.org/tag/erc-1444) at the moment, but I would love to champion these kinds of changes as soon as I have the bandwidth. I’ll reach out to Martin ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=9)

---

**gcolvin** (2018-10-11):

[@expede](/u/expede) To note what little more I can remember so that I can finish forgetting it…  Martin, Axic & I talked over ASYNC_CALL in Shanghai, after the discussion ended on EIP issue #118.  Our take was that under the Actor model there was no mechanism needed for contracts to wait for responses.  Rather, after an ASYNC_CALL the contract just runs to completion, and any responses come back as a ordinary message calls to the contract.  Linking up messages is an application level encoding issue.  I can’t find it now, but Greg Meredith then joined the discussion online somewhere; he has a lot actual experience implementing Actor models.  He pointed out that we would need to ensure that messages got queued “fairly” in a precise sense.  Note that at present there is no true asynchrony; everything runs in lockstep.  That may change with sharding.

---

**schemar** (2018-10-11):

[@expede](/u/expede) great, love this EIP.

Would it help to specify a whole range as application specific successes or failures? E.g. use `0xB*` and `0xC*` for app specific failures and successes, respectively?

I am afraid that, right now, if an app needs multiple custom success or failure response codes, they could start using the currently unassigned codes, e.g. `0xA6` through `0xAC`. Or even `0x16` through `0x1C` ![:scream:](https://ethereum-magicians.org/images/emoji/twitter/scream.png?v=9)

That could potentially lead to incompatibility or at least confusion if there will be official meanings assigned to these codes later on. Or for some apps `0xAA` could be a success while for others it is regarded a failure.

Having an “officially always empty” range of success and failure codes prevents apps from requiring multiple return values (e.g. official code plus app specific code). We do not have the luxury of a response body to go into detail, like HTTP does.

The drawback is that the caller only knows more specifics about the response if the caller knows the callee’s custom code usage. And that it would break the neat property that, at the moment, `0x*0` always indicates a failure. (Possibly remove `0x*0` and `0x*1` from the custom code range?).

Another way (taking up less codes) could be reserving `0xA6` through `0xA9` for custom failures and `0xAA` through `0xAD` for custom success codes. The caller could still reliably identify what’s a success case and what’s a failure case.

Just a thought ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=9)

---

**expede** (2018-10-11):

[@schemar](/u/schemar) thanks for sharing your thoughts! Yeah, I fully agree with the spirit of what you’ve written, though I think a few parts of the spec may have been missed.

## Aside

I have a WIP blog post(s) that I’m trying to wrap up clarifying a lot of what’s bellow, since people seem to jump to “oh this is a port of HTTP” (different problem space and design), and the way the EIPs folks asked for the text to be laid out is confusing (ie: as just a list of codes, rather than [as a table](https://fission.codes/#code-table)).

I should also mention that the EIP itself is in the process of getting an overhaul (for clarity and adding a *bunch* of codes after gather feedback from a number of teams the past month). The aforementioned article is mostly to help clarify things for people looking to use the standard, but also to help collect thoughts for the upgrade.

## Code Design

> Would it help to specify a whole range as application specific successes or failures? E.g. use 0xB* and 0xC* for app specific failures and successes, respectively?

We’ve designed the codes is as a [2D grid](https://fission.codes/#code-table), so it’s easy to parse out the category and reason, so it’s better for programmatic reasoning and developer experience (only have to memorize what 32 numbers mean, not 256). This is *much* more structured than HTTP, where you have random stuff in each range

> that could potentially lead to incompatibility or at least confusion if there will be official meanings assigned to these codes later on. Or for some apps 0xAA could be a success while for others it is regarded a failure. […] prevents apps from requiring multiple return values (e.g. official code plus app specific code)

Indeed, and this is what we’re seeking to avoid in the spec! The app-specific range still adheres to the same reasons (the rows in the grid) as the rest of the spec. If used correctly, there should be no ambiguity about what each code means at a high level

For example, making `0xA0` mean “success” is not following the spec. `0xA0` *must* mean “application-specific failure”, `0xAF` *must* mean “application-specific metadata”, and so on. This range exists only to say “this failure isn’t generic, and has something to do with the specific application’s special domain”. It’s also a way of mapping internal state-machine enums to codes. Consumers of the codes should be able to understand that this is a failure/success/metadata/etc from the lower nibble alone.

> Another way (taking up less codes) could be reserving 0xA6 through 0xA9 for custom failures and 0xAA through 0xAD for custom success codes. The caller could still reliably identify what’s a success case and what’s a failure case.

Yeah, this is a good idea ![:grinning_face_with_smiling_eyes:](https://ethereum-magicians.org/images/emoji/twitter/grinning_face_with_smiling_eyes.png?v=15) I’m not sure that it’ll work with the spec as it stands, since we want those reason codes to work universally (the flip side of a more structured approach). That said, we do need to make the spec flexible, but also parsable, so there’s a balance here ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=15)

> Just a thought

It’s good feedback — thank you!

I hope that some of the above clarified parts of spec that were unclear. I’ll noodle on the wider ranges idea ![:grinning_face_with_smiling_eyes:](https://ethereum-magicians.org/images/emoji/twitter/grinning_face_with_smiling_eyes.png?v=15)

---

**schemar** (2018-10-11):

Thank you [@expede](/u/expede) ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

The spec is clear. As a recommendation I would put “reserved” in all unused table cells to nudge app developers away from defining custom codes in (currently) unused cells. Or make “Unspecified codes are *not* free for arbitrary use, but rather open for further specification.” much more prominent ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/expede/48/4738_2.png) expede:

> We’ve designed the codes is as a 2D grid, so it’s easy to parse out the category and reason, so it’s better for programmatic reasoning and developer experience (only have to memorize what 32 numbers mean, not 256). This is much more structured than HTTP, where you have random stuff in each range

Right, I understand that and I really like that approach. However, some apps will need codes that are not covered by whatever the EIP specifies. And in that case the two options are:

1. multiple return values (additional custom return codes)
2. an available range of codes to use

Maybe a second return value for codes in the `0xA*` range is actually the cleaner solution ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/expede/48/4738_2.png) expede:

> It’s also a way of mapping internal state-machine enums to codes.

How can the EIP guarantee that there will be a code for every enum value of the app? ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

For now I’ll wait for the additional codes after the overhaul ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**0age** (2018-11-05):

Hello ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=9) - great presentation on ERC-1066 at devcon, [@expede](/u/expede)!

I’d like to propose a group of status codes specifically tailored to token transfers in the `0x5*` range (as a pretty significant proportion of transactions deal specifically in that department ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=9)). 5 is unused so far, and looks a bit like $ so seems a natural fit to me. Here’s the proposal for that range:

| code | description |
| --- | --- |
| 0x50 | transfer failure |
| 0x51 | transfer success |
| 0x52 | insufficient balance |
| 0x53 | insufficient allowance |
| 0x54 | invalid sender |
| 0x55 | invalid receiver |
| 0x56 | invalid operator |
| 0x57 | invalid value |
| 0x58 | invalid data |
| 0x59 | invalid approval |
| 0x5a | invalid state |
| 0x5b | contract paused |
| 0x5c | funds locked |
| 0x5d | invalid issuance |
| 0x5e | invalid redemption |
| 0x5f | token meta or info |

`0x50` / `0x51` would be for generic success / failure, `0x52` & `0x53` for the most common failure modes in a standard ERC20 token, then `0x54` through `0x58` would signify invalid parameters in more restrictive permissioned tokens. `0x59` would show that the transfer lacks approval (above and beyond the standard allowance), and `0x5a` would mean that the transfer would put the token into an impermissible state (for instance, maybe the token restricts the number of holders). `0x5b` would signal that all transfers are frozen (maybe the token has been retired or migrated to a new contract) and `0x5c` would mean that the particular tokens in question were frozen (e.g. there is a lock-up period for the tokens that is still in effect). `0x5d` & `0x5e` would be returned if the token transfer would invoke an invalid mint or burn operation, respectively, and `0x5f` would signal metadata in the same vein as the rest of the specification.


*(29 more replies not shown)*
