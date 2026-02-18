---
source: magicians
topic_id: 17295
title: "EIP-7577: Versioning Scheme for EIPs"
author: danceratopz
date: "2023-12-13"
category: EIPs > EIPs Meta
tags: []
url: https://ethereum-magicians.org/t/eip-7577-versioning-scheme-for-eips/17295
views: 2762
likes: 19
posts_count: 14
---

# EIP-7577: Versioning Scheme for EIPs

[Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7577)





###



Use a versioning scheme for EIPs based on changes made to their Specification section.










This EIP suggests a semantic versioning scheme for Standard Track EIPs based on their Specifications section to help remove ambiguity when discussing changes and tracking implementations.

An extended rationale that demonstrates how this can be used within the EVM Testing Toolchain can be found [here](https://notes.ethereum.org/@danceratopz/eip-versioning).

## Replies

**poojaranjan** (2023-12-19):

[@danceratopz](/u/danceratopz) & Ahmad Bitar thanks for sharing about this proposal in [EIPIP Meeting 96](https://www.youtube.com/watch?v=poqOUTvvaoc&t=1085s).

This obviously will help in testing `Standard Track - Core` proposals. However, I can imagine a few other use cases of this proposal across EIP types/categories.

> The EIP versioning scheme MUST follow a semantic versioning scheme of MAJOR.MINOR.PATCH, which is applied as follows:
>
>
> MAJOR: A breaking change to the specifications that requires an implementation change and a change to the reference tests.
> MINOR: An addition to the specifications that does not require changing an existing implementation, but requires additional implementation and additional test coverage to be added to the reference tests.
> PATCH: Any cosmetic change to, or a reformulation of, the EIP without specification change.

In my mind, with slight changes, we can perhaps increase use cases. Instead of `MAJOR.MINOR.PATCH` may we consider `STATUS.SPECS.PATCH` (x.y.z)?

1. STATUS: When a proposal is being proposed/merged in a new status.

*Acceptable values* (for **x**)

- 0 - Living
- 1 - Draft
- 2 - Review
- 3 - Last Call
- 4 - Final
- 5 - Stanant
- 6 - Withdrawn

1. SPECS: Any update to the “Specification” field of the “EIP-template” that requires changing an existing implementation, requires additional implementation and additional test coverage to be added to the reference tests.

*Acceptable values* (for **y**)

- Default value = 0
- Max can be any number

*Change of value to default*

- The value will go to default (y=0) every time with the change of the value of “x”

1. PATCH: Any other changes including but not limited to fixing typos, non-significant specs changes, and updates on the EIP authors list. (This list can be increased as we see PRs with different update suggestions.)

*Acceptable values* (for **z**)

- Default value = 0
- Max can be any number

*Change of value to default*

- The value will go to default (z=0) every time with the change of the value of “x”

I wonder what are the thoughts on

- Adding “Version” to EIP-Preamble:  This will help read the proposal status by just checking the version. It can be checked and automatically/manually allocated to a proposal by an EIP editor and be super helpful for toolings around EIPs.
- Implementing retroactively to all EIPs: When implemented retroactively (with a script) to all existing EIPs (715+) let’s say from March 01, 2024, it will help to keep track of the number of merged changes to a Final EIPs among other changes.

*Recommendation on the default value for retroactive implementations will be STATUS.0.0*

eg. For proposals in `Final` status, the Version = 4.0.0.

Advancing [EIP-7577](https://github.com/ethereum/EIPs/pull/8034) using the versioning feature as described can be a good example. However, I understand it may not be doable instantaneously without updating bots.

---

**dror** (2023-12-21):

In the current architecture of the EIP repository, once an EIP reaches a “final” status there is no way to modify it, not even if a security consideration is found.

My suggestion: add a mechanism that is available in the IETF’s RFC repository: an “Updated-by” or “Replaced-by” tag.

This way, a reader of an EIP can clearly see there is further discussion after the current ERC was finalized.

Updated-by should be marked even if the updating EIP is in “draft” (its an “FYI” notice)

Replaced-by should only be marked once the referencing EIP is finalized, and thus the current one becomes completely obsolete.

(both tags are added to existing EIPs once a new document with “Updates” or “Replaces” header tags, respectively, is added to the repository)

---

**poojaranjan** (2023-12-22):

Thanks [@dror](/u/dror) for adding feedback.

It is correct that the `Final` EIP represents the final standard and is not open to accept modification.

However, there is a small room for non-normative changes.  As per [EIP-1](https://eips.ethereum.org/EIPS/eip-1#eip-process)

> “A Final EIP exists in a state of finality and should only be updated to correct errata and add non-normative clarifications.”

So, if there is a general agreement of moving forward with the version scheme for EIPs, perhaps Final EIPs can also be updated to 4.0.1 where

- 4 will indicate status = Final
- 0 will indicate there is no significant specs change that may require additional implementation (any change is anyway not allowed for Final EIP) and
- 1 will indicate the correction after the status change by adding the preamble header.

If not, then moving EIP versioning ahead with non-Final EIPs should be okay as well.

I am aware of the interest in discussing the process for updating Final Ethereum Standards under exceptional circumstances like security considerations. It was mentioned in the [last meeting](https://www.youtube.com/watch?v=poqOUTvvaoc) and is in active discussion in [EIPIP meetings](https://github.com/ethereum-cat-herders/EIPIP/issues/302) and we hope to get to talk about specific conditions under which `Final` EIPs can be updated. We encourage people to join the meeting or leave comments to participate in discussing edits to `Final` standards.

---

**chaals** (2024-01-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> My suggestion: add a mechanism that is available in the IETF’s RFC repository: an “Updated-by” or “Replaced-by” tag.

Just to be clear that this is more or less exactly [the proposal in a parallel discussion](https://ethereum-magicians.org/t/modification-of-eip-process-to-account-for-security-treatments/16265/23), motivated especially by finding new security considerations.

---

**chaals** (2024-01-08):

The idea that a standard will be final is really appealing, but seems to push hard against reality. My 25-odd years working with W3C suggest that the goal of making a final complete standard (as opposed to the next version of something that needs to be tweaked at least from time to time) causes a lot of problems.

Over time it gets harder to fix things (update to EIP-1 anyone?) but they can still be fixed - or get completely replaced by something people believe will be easier to manage into the future. So I would like to see this discussion continue, until it reaches the point where we have a working visible concept of “this EIP is obsolete, go look at that one that replaces it”, without simply allowing anyone to *claim* their new thing obsoletes what the world is using.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> In my mind, with slight changes, we can perhaps increase use cases. Instead of MAJOR.MINOR.PATCH may we consider STATUS.SPECS.PATCH (x.y.z)?

I’m not a fan of “living” as a status - that is the status of anything that is still used.

I have an approach that is a bit like [@poojaranjan](/u/poojaranjan) backwards: Version, then status (I have “draft” and “done”). I think it’s critical to have a mechanism for a specific spec (or version) to point forward to its replacement, and this is not hard. I’m not that keen on patching old versions - if they are hanging around long enough that it is really important, then it means the next version didn’t reach the status people thought, and some more work needs to be done on re-doing the transition.

But I think people in this community understand “semantic versioning” and are used to it. It’s probably more useful to question whether we’re prepared to accept that “Final” is not real and that we should version things or not, and expect that the answer if we do versioning will be that.

---

**drllau** (2024-01-11):

Philosophically, it comes down to are you optimising for **stability** or **innovation**? In particular what is the meaning of a standard?

[![LexDAO-DLTontology](https://ethereum-magicians.org/uploads/default/optimized/2X/3/3fe0481db4c771ad245b9bf303fa2ad6cd5bbd43_2_690x489.png)LexDAO-DLTontology1718×1218 112 KB](https://ethereum-magicians.org/uploads/default/3fe0481db4c771ad245b9bf303fa2ad6cd5bbd43)

Using the above as a mental map:

1. technical discussions (technical control along bottome) in the rough consensus, working code stage  need more precise versioning so details can be thrashed and matters that have been settled, can pinhole cite in case later participants raise variations of the same objective.
2. on the other hand businesses that are looking to invest significant resources into an DLT, would like to see certainty in the timescale of decades (middle left)… which means distrust of anything too new so finality is welcome … even with known bugs (cough browser feature sets), they can be worked around because cross-chain consistency is more important.
3. the gap between where new knowledge (eg of vulnerabilities) arises and the standards are slow to update are where attacks have the biggest detrimental impact. You can have different “standards” (eg tech and legal) moving at different speeds, so long as there is a clear coupling / stapling between the two. For example, the tech standard might say every 5-7 years have a review which then gets compiled in the market accepted practices which can be ratified at the legislative/regulative level (middle right of centre).

However, there should be some way of clustering closely related topics … at the moment, variations of treating NFTs are numbers across quite unrelated pull requests. An complementary proposal would be

> For easy human memonics, EIPeditors should have the discretionary power to alias ERC-??? [alpha] to a future EIP …

eg ERC-20A might be aliased to that EIP which calls a recipient function upon transfer if commonly used). That way you’d only need to recall the shortened form.

---

**danceratopz** (2024-06-05):

Hi [@poojaranjan](/u/poojaranjan), many thanks for your input! And please excuse my delayed response!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> In my mind, with slight changes, we can perhaps increase use cases. Instead of MAJOR.MINOR.PATCH may we consider STATUS.SPECS.PATCH (x.y.z)?
>
>
> STATUS: When a proposal is being proposed/merged in a new status.

Ahmad and I discussed this and while we understand the motivation behind this suggestion, we’d prefer to maintain a pure semantic versioning scheme (semver). For the main part, developers and authors should be familiar with semver and will hopefully intuitively understand how it should be applied.

Using `STATUS` in `STATUS.SPECS.PATCH` (x.y.z) will duplicate information. Additionally, one disadvantage of this approach is that versions will not strictly monotonically increase, as an EIP’s `STATUS` can move from, for example, `DRAFT` → `STAGNANT` → `DRAFT`.

Here’s a comment on the usefulness of each field: Assuming we use `MAJOR.MINOR.PATCH`. We expect that the vast majority of changes will be either:

- MAJOR “A breaking change to the specification…”, or,
- PATCH “Any cosmetic change to, or a reformulation of, the EIP without specification change.”.

We expect that the `MINOR` field “*An addition to the specifications that requires additional implementation…*.” will not see heavy use, as this kind of change appears to be rarely made to EIPs (see, the EIP-4788 Case Study [here](https://notes.ethereum.org/@danceratopz/eip-versioning#EIP-4788-Case-Study-as-from-the-EIP-but-with-links-to-Github-PRs) or [in the PR](https://github.com/danceratopz/EIPs/blob/92fb8ba71fe8b686634df5b469f642dcada5c977/EIPS/eip-7577.md?plain=1#L58)). We feel, however, that the intention of bumping the `MINOR` version matches semver well in the context of specification changes. But we are open to other suggestions!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Adding “Version” to EIP-Preamble: This will help read the proposal status by just checking the version. It can be checked and automatically/manually allocated to a proposal by an EIP editor and be super helpful for toolings around EIPs.

Yes, this should be added to an EIP’s metadata. This has been added to the proposal (see [92fb8ba7#L43](https://github.com/danceratopz/EIPs/blob/92fb8ba71fe8b686634df5b469f642dcada5c977/EIPS/eip-7577.md?plain=1#L43)).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Implementing retroactively to all EIPs: When implemented retroactively (with a script) to all existing EIPs (715+) let’s say from March 01, 2024, it will help to keep track of the number of merged changes to a Final EIPs among other changes.

We don’t feel that retroactively applying versioning to EIPs is necessary or particularly valuable, as the main value of versioning is during the development phase. I don’t think it’d be possible to automate this process reliably. We could allow EIP authors to apply it retrospectively their EIPs if they wish.

---

**danceratopz** (2024-06-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> In the current architecture of the EIP repository, once an EIP reaches a “final” status there is no way to modify it, not even if a security consideration is found.

Thanks [@dror](/u/dror) for this comment and [@chaals](/u/chaals) for linking the discussion and further comments on how to deal with obsolete EIPS, specifically EIPs that have been superseded by a subsequent EIP.

As per [@poojaranjan](/u/poojaranjan)’s [comment above](https://ethereum-magicians.org/t/add-eip-versioning-scheme-for-eips/17295/4) (as per EIP-1, non-normative changes are allowed), 7577 would allow for a transparent history of errata made to EIPs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dror/48/2438_2.png) dror:

> My suggestion: add a mechanism that is available in the IETF’s RFC repository: an “Updated-by” or “Replaced-by” tag.

I see the value in an “Updated-by” tag (or new metadata field?). I’m not sure if it should be scoped in 7577, as this EIP is concerned with helping to improve the current development process of **active** EIPs, respectively, maintaining a transparent history of changes to EIPs (including errata). I hope the discussion around this continues! If the community agrees and it fits in within the scope of 7577 we can consider to include it later. However, I feel this would deserve its own separate proposal.

---

**xinbenlv** (2024-06-05):

Thank you for your proposal [@danceratopz](/u/danceratopz)

On a high level I like supporting versioning of EIPs.

Some brief thought:

0. Currently any EIP author can add versions in their draft already by adding to their EIP text body. We just need to advocate for [@danceratopz](/u/danceratopz) 's proposal to be adopted as as drafting practice.

1. I think we can split this EIP into two EIPs: (1) an Informational EIP suggesting EIP authors to use semantic versioning in their own EIP drafting. (2), once we get a lot of adoption, create a Meta EIP updating preamble.

I would be supportive of adding version to preemble if-and-only-if we see many authors using EIP versioning within their own EIP drafts already.

---

**timbeiko** (2024-06-06):

I like this idea overall, with some caveats:

1. Getting EIPs moved through the spec stages is already very friction-heavy and I’d lean against any hard requirements. Specifically, I’d consider adding the Changelog section as optional and basically having every MUST in your spec be a MAY.
2. Semantic versioning is bound to create bikeshedding and delays when reviewing changes to EIPs. A much simpler tweak which would provide most of the same value is an updated-on header field that is changed to the current date every time the EIP bot merges a PR. This means that unless we get many changes in a single day, we’d easily be able to differentiate between two versions of an EIP.

With these two changes, people can always know if/when an EIP was updated and authors are nudged to track changes, but EIPs aren’t stuck with open PRs for longer than they currently are. Avoiding PRs being open for a long time seems like the most critical thing, as the “true spec” isn’t even reflected in the EIP.

---

**danceratopz** (2024-06-11):

Thanks for the comments [@xinbenlv](/u/xinbenlv)!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Currently any EIP author can add versions in their draft already by adding to their EIP text body. We just need to advocate for @danceratopz 's proposal to be adopted as as drafting practice.

Would you suggest the version gets added to a “Changelog” section?

Whilst it would be possible, albeit a bit clunky, for external tooling to parse the version from an ordered Changelog section, it could get messy (and be more of a burden to EIP authors) without adding the suggested automated tooling (i.e., allow bumping of the version based on commit message, cf [45587bd0/EIPs/eip-7577.md#L43-L50](https://github.com/ethereum/EIPs/blob/45587bd019487b0bd59bec941bc0e2d708811cc8/EIPS/eip-7577.md?plain=1#L43-L50)).

As I understand, it would also require EIP-7577’s status to be bumped from Draft to Review, so that the EIP using 7577 versioning could add EIP-7577 to it’s `requires` header preamble?

---

**danceratopz** (2024-06-11):

Thanks a lot for checking out the proposal, [@timbeiko](/u/timbeiko)!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Getting EIPs moved through the spec stages is already very friction-heavy and I’d lean against any hard requirements. Specifically, I’d consider adding the Changelog section as optional and basically having every MUST in your spec be a MAY.

First, as versioning is not required before **Review** status, authors can iterate freely without considering versioning whilst the EIP has **Draft** status (versioning adds value when multiple teams are involved and implementation starts).

Secondly, also with regards to bikeshedding, assessing the impact of a PR made to an EIP should be a relatively simple task in the majority of cases (i.e., spec change: bump major version, improve rationale: bump patch). Additionally, the version bumping and Changelog line should be largely automated (the version gets bumped based on one of the PR’s commit messages and the changelog line could come from the PR’s title, see [45587bd0/EIPs/eip-7577.md#L43-L50](https://github.com/ethereum/EIPs/blob/45587bd019487b0bd59bec941bc0e2d708811cc8/EIPS/eip-7577.md?plain=1#L43-L50)).

This needs further discussion though! Also with client teams as maintaining a list of EIPs and their implemented versions will cause additional effort for them.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Semantic versioning is bound to create bikeshedding and delays when reviewing changes to EIPs. A much simpler tweak which would provide most of the same value is an updated-on header field that is changed to the current date every time the EIP bot merges a PR. This means that unless we get many changes in a single day, we’d easily be able to differentiate between two versions of an EIP.

Whilst an `updated-on` header field could help resolve ambiguities across software components and discussions, without expressing the change richly as a semver, we won’t be able to automatically evaluate changes within the testing framework when testing client implementations (for example, in order to apply “xfails” or issue warnings, cf [45587bd0/EIPs/eip-7577.md#L56](https://github.com/ethereum/EIPs/blob/45587bd019487b0bd59bec941bc0e2d708811cc8/EIPS/eip-7577.md?plain=1#L56)). The idea of comparing client implementation, test implementation and spec versions is also explained in more depth in [Example 3: EVM Testing Toolchain](https://notes.ethereum.org/@danceratopz/eip-versioning#Example-3-EVM-Testing-Toolchain) in the extended rationale.

I suspect that if EIP versioning consisted of an `updated-on` preamble field as a timestamp it would not receive adoption in client implementations and test frameworks. Issuing a warning in test frameworks upon any change to an EIP would be too noisy for it to be useful.

Additionally, I think it’s simpler to compare versions (rather than a timestamp) in an ACD discussion or a devnet spec page ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12).

---

**timbeiko** (2024-06-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danceratopz/48/11156_2.png) danceratopz:

> This needs further discussion though!

I agree with you that this seems simple in theory! That said, after spending good part of my morning trying to move a bunch of EIPs from `Draft` to `Review`, and being blocked on about half of them for various reasons ([context](https://github.com/ethereum/EIPs/pull/8651)), I’ll reemphasize that any extra *mandatory* checks on EIPs probably is a net negative in terms of productivity given the extra friction. My suggestion would be to try and run the process in a 100% optional way at first, see it working, and then determine what you want to make mandatory and how ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

I think your concerns with `updated-on` are valid. IDK if there’s another type of status you could auto-generate based on EIP updates?

