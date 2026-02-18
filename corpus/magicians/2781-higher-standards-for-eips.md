---
source: magicians
topic_id: 2781
title: Higher standards for EIPs
author: lrettig
date: "2019-03-01"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/higher-standards-for-eips/2781
views: 3345
likes: 18
posts_count: 14
---

# Higher standards for EIPs

Copying over some ideas that [@AlexeyAkhunov](/u/alexeyakhunov) shared on the [recent all core devs meeting agenda](https://github.com/ethereum/pm/issues/82#issuecomment-468637885) of ways that we can make the EIP process better and more efficient for Istanbul and beyond:

> Before we dive into the EIPs for Instanbul, I suggest we try to address some issues with how we deal with the proposed changes, and what are our priorities.
> I proposed to look at these things:
>
>
> Introduce higher standards for EIPs - they require Proof Of Concept implementation + pre-generated test cases (so that that testing is not an afterthought as usual)
> Revisit the assumption that we need to bundle a lot of updates into one big release instead of making smaller releases more frequently. I heard before on this call that coordination costs are too high to afford smaller releases - but are they really?
> Appoint dedicated reviewers (not necessary from the people who are regularly attending the call) for changes rather than wait for someone on the call to look into the changes
> Do we need to create a deluge of EIPs for Istanbul now or do we spend some time on discussing what the most important changes are?

I strongly support this initiative, and I see value in all of these ideas, especially #1. The way Alexey phrased it on the call is, if we follow these steps, we don’t need to hold everyone (all the core devs) hostage to each individual EIP for months.

A few more questions I have:

- What do other folks think?
- What’s missing here? What else can/should be included/improved?
- How do we appoint reviewers for EIPs? How does this fit into the existing EIP editor process (or not), and what pool are these reviewers drawn from? How do we determine which EIPs are worthy of being reviewed?
- What does this (especially #1, requiring a POC implementation) mean for less technical EIPs?

CC [@Arachnid](/u/arachnid)

## Replies

**timbeiko** (2019-03-01):

+1.

One thing that had been mentioned before was to have an explicit “Security” component to

EIPs. I’m no expert on what such a component would need to include, but it seems that a thorough analysis of the security considerations of EIPs would help avoid future ConstantiNOPEs.

---

**shemnon** (2019-03-01):

For point (4) I think we need EIP authors to signal Istanbul intent now, and have reviewable EIPs by mid-April so we can do a reject/accept by mid May.  My informal reckoning (based on AllCoreDev calls) is that we have intent from

- EIP-615 (subroutines/static jumps in EVM),
- EIP-1057 (ProgPOW) and
- EIP-??? State Fees phase I.

State pruning and faster sync don’t require hard forks, so I don’t think it’s critical for them to get in line now.  If there are other EIPs looking to get on board then we need to figure out where they can signal their intent.

---

**timbeiko** (2019-03-01):

Related: [one just did](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783).

---

**shemnon** (2019-03-01):

Are they targeting Istanbul?  That’s unclear in that text which is why I think we need a formal place/way to get “on the list.”

---

**econoar** (2019-03-01):

I would like it to be but was unaware of the procedure to signal that. I can edit the post if you’d like it to be included.

---

**shemnon** (2019-03-01):

I think that is the crux of the issue, how do EIP authors/advocates signal?  If you edit your post to say something to the effect of “I’de like this in Istanbul” that is as good as we can do for now.

Possibly an “official” FEM thread with the top post maintaining a running list would be a better step, but that’s for the release managers to do once they get organized IMHO.

---

**boris** (2019-03-02):

Yes. I proposed a security review period:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)
    [Security Review Period for Hardfork Roadmap](https://ethereum-magicians.org/t/security-review-period-for-hardfork-roadmap/2721) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)



> I’ve added a section to the Istanbul Roadmap page on the Ethereum wiki proposing a security review period for proposed Core EIPs.
> This means having some people do security reviews – which might mean engaging external auditors. But it also means communication around the Core EIP proposals that are effectively Last Call, but focused on security issues. Pay attention, have a look, does this impact your current or future use cases.
> I’ve suggested 2019-06-21 (June 21st), this is half way between th…

---

**boris** (2019-03-02):

Yeah these should really be signalling.

I have two ways of doing this. One is that anyone can edit the Ethereum wiki roadmap https://en.ethereum.wiki/roadmap/istanbul

The other, is that there should be PRs to EIP-1679.

We might very well accept PRs to the EIP in a “proposed” section. How to get that into a new state — eg Accepted, which then goes into progress tracking for implementation -/ is unclear.

Without accepting the PRs — they aren’t trackable.

Unless we turn on tags/labels in the EIPs repo, or the projects feature.

I am volunteering to help with management of any of all of this. And will discuss EIPs + hardfork process at EthMagicians in Paris.

---

**shemnon** (2019-03-02):

The signaling process is useful to both the EIP author as well as the client implementors.  A month or two lead time on what work may be needed could affect current non-hard-fork work, so we can include schedule time as well as design space for the features.

---

**fubuloubu** (2019-03-02):

Definitely an advocate for a wider review process (number 3). I wrote something up and implemented a PR a against the EIP process.

Proposal: [Proposal: Add Ring tags to EIPs; solicit comments from Ring(s)](https://ethereum-magicians.org/t/proposal-add-ring-tags-to-eips-solicit-comments-from-ring-s/1592)

PR against EIP-1: https://github.com/ethereum/EIPs/pull/1725

The TL;DR is to allow a suggestion of “review tags” during Draft which would have to be conducted by relevant subgroups/rings before a move to Last Call. This means that if a proposal needs a security review, we tag it with that. If it needs an economic analysis, we tag it with that. If it needs neither, we don’t have to tag it. Let the process define the needs of the proposal, and have completion of the process actually mean something more than “well, no one has a problem with this. I guess it’s fine?”

---

**fubuloubu** (2019-03-02):

Number 1 sounds very similar to this:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/expede/48/4738_2.png)
    [Jello Paper as Canonical EVM Spec](https://ethereum-magicians.org/t/jello-paper-as-canonical-evm-spec/2389) [Primordial Soup](/c/primordial-soup/9)



> Hello all
> During Devcon 4, there was some discussion about moving the canonical EVM spec to the Jello Paper. I think that this is a fantastic idea. Very few people seem happy with the Yellow Paper as written, and the ambiguous state of maintenance. I am partway through an EVM implementation myself, and have found the Jello Paper to be far superior to the Yellow and Beige Papers. Some of the reasons include:
>
> Much clearer
> Fewer edge cases
> Took the time to formalize the semantics
> Executab…

TL;DR is the spec, test suite, and formal semantics are kept together, and each proposal must modify those items in feature branches so they are kept up to date.

---

**fubuloubu** (2019-03-02):

Definitely like the concept of 2. There has to be some optimal trade-off between hard fork coordination and release cycles. I’m willing to bet it’s less than 9 months.

We could improve things by cycling the release manager through each hard fork, so that this job doesn’t become a taxing thing on a person’s time. I sort of think of it like a public service position to be honest.

---

**boris** (2019-03-03):

Ideally there is overlap: with 9 months, realistically you have a 12 month cycle. Three months out from the hard fork you can kick off next hard fork timing and planning.

And also at least two people - I can handle EIP feedback and timing, but not the technical coordination of testnets & the actual hardfork.

