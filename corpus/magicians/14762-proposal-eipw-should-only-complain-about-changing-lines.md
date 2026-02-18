---
source: magicians
topic_id: 14762
title: "Proposal: EIPW should only complain about changing lines"
author: xinbenlv
date: "2023-06-20"
category: Magicians > Process Improvement
tags: [eip-process, eipw]
url: https://ethereum-magicians.org/t/proposal-eipw-should-only-complain-about-changing-lines/14762
views: 2192
likes: 19
posts_count: 14
---

# Proposal: EIPW should only complain about changing lines

Proposed as: [Proposal: Make EIPW only check changed lines except for changing status · Issue #7198 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/7198)

### Proposed Change

Currently some Author Pain comes from the EIPW complains about **lint errors that were not introduced in that specific pull request they are working on**, such as

1. links that were not allowed
2. mandates to call ERC “ERC” or call ERC “EIP”
3. spaces between section
4. order of section

In particular, sometimes new policy will be imposed on EIP, and it means many existing EIP are in the state of inconsistency.

This is particular confusing and painful which requires Authors to get up to date to EIP editorial policy.

I hereby propose a change to EIPW:

1. For any PR that’s not changing state or Draft/Review, only lint the line of code being changed.
2. Only lint full EIP when moving into Last Call or Final

This was inspired by https://twitter.com/sproulM_/status/1671096282482622464?s=20

## Replies

**xinbenlv** (2023-06-20):

Cross-posting some discussion in EIP-editor channel, at permission of [@matt](/u/matt) and [@SamWilsn](/u/samwilsn)

### lightclient — Today at 1:47 PM

i think this is more of a symptom of lots of process changes rather than something that needs to change about eipw - if we stabilize the policy of things, authors won’t have trouble making small PRs because eip is simply up to date

### SamWilsn — Today at 1:49 PM

That’s a really good point. As more EIPs get updated, the number of these rule breaking EIPs goes down.

### xinbenlv — Today at 1:51 PM

Yeah, we should reduce the change of policy (that increases restriction).

And what does it block us from adopting this proposal?  [Proposal: Make EIPW only check changed lines except for changing status · Issue #7198 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/7198)

### SamWilsn — Today at 1:53 PM

There’s a lot of work in implementing that. It’s a hell of a lot more complicated than checking the whole file.

### xinbenlv — Today at 1:57 PM

I could understand if there is technical difficulty, and is there non-technical reason not to? If the only blockage is technical, we can set it as a policy: ignoring errors when you are not touching that line, but right now we can’t implement it in EIPW due to technical challenge. It will create two outcomes:

1. People with EIPW expertise could offer to help implementing it.
2. Editors or editorial contributors could offer to manually signal bypassing it when EIPW make a complaint due to this.

---

**SamWilsn** (2023-06-20):

There’s the “always leave code better than you found it” guideline: if you change an EIP, it’s your responsibility to improve it. I’ve overridden `eipw` for minor changes before, and will continue to do so in the future.

Unpredictable is generally bad. If an author is working on their own EIP, and gets inconsistent feedback depending on what lines they change, they won’t know what to fix. It also shifts a lot of the formatting changes to the status changing commit, instead of providing feedback early.

Lines are a poor level of granularity for this. Most EIPs, as far as I remember, use one line per paragraph, so you won’t end up solving the issue if the edit hits a line with an error on it.

---

**xinbenlv** (2023-06-20):

I hear that Editor [@SamWilsn](/u/samwilsn) (and [@Pandapip1](/u/pandapip1) previously) share the stronger view which is *if you touch it, you have responsibility to fix all linter errors*.

I am generally *pro micro contribution*, therefore, I am arguing for *allowing changes as long as it’s not making the EIP worse*.

---

**SamWilsn** (2023-06-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> allowing changes as long as it’s not making the EIP worse.

Yep, that works for me. If you need to override `eipw`, you can add the [Manual Merge Queue](https://github.com/ethereum/EIPs/milestone/1) milestone and I’ll get to it.

---

**xinbenlv** (2023-06-20):

Cool, glad that it seems we are in consensus? Let me create a Meta EIP to reflect this?

---

**SamWilsn** (2023-06-20):

I don’t think this needs an EIP. `eipw` isn’t even part of the official process; it’s just a tool that enforces the general rules of the process as defined by us, the editors.

---

**xinbenlv** (2023-06-20):

Just wanna officially document down this consensus, make sure there is no ambiguity, so next time when something comes up we can point people to this consensus.

Here it goes

https://github.com/ethereum/EIPs/pull/7199

---

**SamWilsn** (2023-06-20):

If you want to document all these little things, I guess you could put them in [EIP-5069: EIP Editor Handbook](https://eips.ethereum.org/EIPS/eip-5069)

---

**xinbenlv** (2023-06-20):

I personally prefer to put it in a separate EIP.

The problem of updating a line blocked by many errors has historically blocked many attempts to update EIPs, scare away many potential EIP contributors. I think it’s critical to make this policy clear and hence warrant a individual Meta EIP

---

**michaelsproul** (2023-06-21):

I can see the argument for only checking changed lines, but agree with [@SamWilsn](/u/samwilsn)’s point that having consistent whole-file feedback is useful.

Another approach would be to not introduce any lints that don’t already pass on the entire codebase. This would be standard software-engineering practice – the fact that the codebase fails its own CI on the `master` branch is what I found irritating. I’m a fan of the “Bors”/merge queue system, where changes are always integrated into `master` and fully tested before merging (a bit of history on this system [here](https://graydon2.dreamwidth.org/1597.html)).

The downside is that this puts the onus on lint/policy writers to go and fix hundreds of EIPs before their policy can be merged. As a fan of a more lightweight policy, I’m tempted to say that this is an OK tradeoff. If fixing the lint can’t be automated and easily rolled out across the codebase, then maybe it shouldn’t exist. Some lints are easy to automate, e.g. the metadata ordering lint that I ran into. The URL lints are harder to fix automatically, unless URLs can be auto-converted to `archive.org` links or similar.

---

**abcoathup** (2023-06-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I personally prefer to put it in a separate EIP.

I don’t think this needs to be in a separate EIP.  Agreement can be shown in this discussion.  I’d like to avoid a proliferation of small meta EIPs about processes.

[EIP-1: EIP Purpose and Guidelines](https://eips.ethereum.org/EIPS/eip-1) has a style guide section, couldn’t you add any high level linting rules to this (or a separate section on linting)

---

**dror** (2023-11-22):

I strongly recommend running lints only on diffs. Some reasons mentioned above, like encourage people to do small changes, without requiring them to commit to full doc refactor.

Documents are not source code, that requires CI and UT, so existing document can be linted incrementally, over the.

Another reason is document history: I like to use git history to see evolution of source/document.

The current lint system breaks this, since a seamingly small change to a file turns into a huge refactor.

Yes, it would be nice to encourage editors to run a “refactor” session once in a while.

However, editing a document is currently a complex task, with forking and repeatedly running a local linter.

I wonder if there is a way to make it more interactive: first, allow fto view files online with lint marks. Then a web based online editor with integrated linter (eg based on vscode).

I think such a tool will promote linting the docs much better than the current fix-all-on-every-commit mode.

---

**SamWilsn** (2023-11-27):

We do exercise editor discretion here. For example, if someone puts up a pull request fixing a spelling mistake (but doesn’t fix all the linter errors) we generally merge it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> I wonder if there is a way to make it more interactive: first, allow fto view files online with lint marks. Then a web based online editor with integrated linter (eg based on vscode).

I’m not sure about a full web editor, but [@Pandapip1](/u/pandapip1) did some work on a visual studio code plugin for `eipw`: [GitHub - Pandapip1/eipw-vscode: Your companion for writing EIPs](https://github.com/Pandapip1/eipw-vscode)

