---
source: magicians
topic_id: 25955
title: EIP-7732 Breakout Room Call #27, November 7, 2025
author: system
date: "2025-10-25"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eip-7732-breakout-room-call-27-november-7-2025/25955
views: 46
likes: 0
posts_count: 4
---

# EIP-7732 Breakout Room Call #27, November 7, 2025

### Agenda

#### Specifications & testing

New consensus specifications: [v1.6.0-beta.2](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-beta.2) & [v1.6.0](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0)

- eip7732: add tests for process_withdrawals block processing
- eip7732: add fork choice tests (part1)
- Clean up Gloas specs (part 2)
- Clean up Gloas specs (part 3)
- Clean up Gloas specs (part 4)
- eip7732: add gossip rule for old payloads
- eip7732: remove uniqueness requirement in comment
- eip7732: clarify PTC description
- Remove merkle proof tests in Gloas
- Add pending payment withdrawal epoch asserts
- eip7732: add PTC subsection to validator assignment section
- Process same-slot slashings before builder payments in Gloas
- Fix randao mix processing in Gloas

#### Implementation updates from client teams

- Prysm
- Lighthouse
- Teku
- Nimbus
- Lodestar
- Grandine

#### Add off-protocol-value to the bid?



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908)












####



        opened 02:31AM - 25 Oct 25 UTC



          closed 03:22PM - 07 Nov 25 UTC



        [![](https://avatars.githubusercontent.com/u/95511699?v=4)
          jtraglia](https://github.com/jtraglia)





          Breakout


          ePBS


          protocol-call







### UTC Date & Time

[November 07, 2025, 14:00 UTC](https://savvytime.com/conver[…]()ter/utc/nov-7-2025/2pm)

### Agenda

#### Specifications & testing

New consensus specifications: [v1.6.0-beta.2](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-beta.2) & [v1.6.0](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0)

- [ ] [eip7732: add tests for `process_withdrawals` block processing](https://github.com/ethereum/consensus-specs/pull/4468)
- [ ] [eip7732: add fork choice tests (part1)](https://github.com/ethereum/consensus-specs/pull/4489)
- [x] [Clean up Gloas specs (part 2)](https://github.com/ethereum/consensus-specs/pull/4693)
- [x] [Clean up Gloas specs (part 3)](https://github.com/ethereum/consensus-specs/pull/4694)
- [x] [Clean up Gloas specs (part 4)](https://github.com/ethereum/consensus-specs/pull/4721)
- [x] [eip7732: add gossip rule for old payloads](https://github.com/ethereum/consensus-specs/pull/4695)
- [x] [eip7732: remove uniqueness requirement in comment](https://github.com/ethereum/consensus-specs/pull/4708)
- [x] [eip7732: clarify PTC description](https://github.com/ethereum/consensus-specs/pull/4719)
- [x] [Remove merkle proof tests in Gloas](https://github.com/ethereum/consensus-specs/pull/4700)
- [x] [Add pending payment withdrawal epoch asserts](https://github.com/ethereum/consensus-specs/pull/4701)
- [x] [eip7732: add PTC subsection to validator assignment section](https://github.com/ethereum/consensus-specs/pull/4713)
- [ ] [Process same-slot slashings before builder payments in Gloas](https://github.com/ethereum/consensus-specs/pull/4726)
- [ ] [Fix randao mix processing in Gloas](https://github.com/ethereum/consensus-specs/pull/4728)

#### Implementation updates from client teams

* Prysm
* Lighthouse
* Teku
* Nimbus
* Lodestar
* Grandine

#### Add off-protocol-value to the bid?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Add a censoring flag to the engine api return on new_payload?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Move `process_builder_pending_payments` above `process_effective_balance_updates`?

https://github.com/ethereum/pm/issues/1783#issuecomment-3500921455

#### The `verify prev randao` check uses the post state of the block with different randao mixes

https://github.com/ethereum/pm/issues/1783#issuecomment-3502321691

https://discord.com/channels/595666850260713488/874767108809031740/1436303424294752407

### Call Series

EIP-7732 Breakout Room

<details>
<summary>🔧 Meeting Configuration</summary>

### Duration

60 minutes

### Occurrence Rate

bi-weekly

### Use Custom Meeting Link (Optional)

- [ ] I will provide my own meeting link

### Facilitator Emails (Optional)

jtraglia@ethereum.org

### Display Zoom Link in Calendar Invite (Optional)

- [x] Display Zoom link in invite

### YouTube Livestream Link (Optional)

- [x] Create YouTube livestream link
</details>












#### Add a censoring flag to the engine api return on new_payload?



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908)












####



        opened 02:31AM - 25 Oct 25 UTC



          closed 03:22PM - 07 Nov 25 UTC



        [![](https://avatars.githubusercontent.com/u/95511699?v=4)
          jtraglia](https://github.com/jtraglia)





          Breakout


          ePBS


          protocol-call







### UTC Date & Time

[November 07, 2025, 14:00 UTC](https://savvytime.com/conver[…]()ter/utc/nov-7-2025/2pm)

### Agenda

#### Specifications & testing

New consensus specifications: [v1.6.0-beta.2](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-beta.2) & [v1.6.0](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0)

- [ ] [eip7732: add tests for `process_withdrawals` block processing](https://github.com/ethereum/consensus-specs/pull/4468)
- [ ] [eip7732: add fork choice tests (part1)](https://github.com/ethereum/consensus-specs/pull/4489)
- [x] [Clean up Gloas specs (part 2)](https://github.com/ethereum/consensus-specs/pull/4693)
- [x] [Clean up Gloas specs (part 3)](https://github.com/ethereum/consensus-specs/pull/4694)
- [x] [Clean up Gloas specs (part 4)](https://github.com/ethereum/consensus-specs/pull/4721)
- [x] [eip7732: add gossip rule for old payloads](https://github.com/ethereum/consensus-specs/pull/4695)
- [x] [eip7732: remove uniqueness requirement in comment](https://github.com/ethereum/consensus-specs/pull/4708)
- [x] [eip7732: clarify PTC description](https://github.com/ethereum/consensus-specs/pull/4719)
- [x] [Remove merkle proof tests in Gloas](https://github.com/ethereum/consensus-specs/pull/4700)
- [x] [Add pending payment withdrawal epoch asserts](https://github.com/ethereum/consensus-specs/pull/4701)
- [x] [eip7732: add PTC subsection to validator assignment section](https://github.com/ethereum/consensus-specs/pull/4713)
- [ ] [Process same-slot slashings before builder payments in Gloas](https://github.com/ethereum/consensus-specs/pull/4726)
- [ ] [Fix randao mix processing in Gloas](https://github.com/ethereum/consensus-specs/pull/4728)

#### Implementation updates from client teams

* Prysm
* Lighthouse
* Teku
* Nimbus
* Lodestar
* Grandine

#### Add off-protocol-value to the bid?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Add a censoring flag to the engine api return on new_payload?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Move `process_builder_pending_payments` above `process_effective_balance_updates`?

https://github.com/ethereum/pm/issues/1783#issuecomment-3500921455

#### The `verify prev randao` check uses the post state of the block with different randao mixes

https://github.com/ethereum/pm/issues/1783#issuecomment-3502321691

https://discord.com/channels/595666850260713488/874767108809031740/1436303424294752407

### Call Series

EIP-7732 Breakout Room

<details>
<summary>🔧 Meeting Configuration</summary>

### Duration

60 minutes

### Occurrence Rate

bi-weekly

### Use Custom Meeting Link (Optional)

- [ ] I will provide my own meeting link

### Facilitator Emails (Optional)

jtraglia@ethereum.org

### Display Zoom Link in Calendar Invite (Optional)

- [x] Display Zoom link in invite

### YouTube Livestream Link (Optional)

- [x] Create YouTube livestream link
</details>












#### Move process_builder_pending_payments above process_effective_balance_updates?



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/1783#issuecomment-3500921455)












####



        opened 02:31AM - 25 Oct 25 UTC



          closed 03:22PM - 07 Nov 25 UTC



        [![](https://avatars.githubusercontent.com/u/95511699?v=4)
          jtraglia](https://github.com/jtraglia)





          Breakout


          ePBS


          protocol-call







### UTC Date & Time

[November 07, 2025, 14:00 UTC](https://savvytime.com/conver[…]()ter/utc/nov-7-2025/2pm)

### Agenda

#### Specifications & testing

New consensus specifications: [v1.6.0-beta.2](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-beta.2) & [v1.6.0](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0)

- [ ] [eip7732: add tests for `process_withdrawals` block processing](https://github.com/ethereum/consensus-specs/pull/4468)
- [ ] [eip7732: add fork choice tests (part1)](https://github.com/ethereum/consensus-specs/pull/4489)
- [x] [Clean up Gloas specs (part 2)](https://github.com/ethereum/consensus-specs/pull/4693)
- [x] [Clean up Gloas specs (part 3)](https://github.com/ethereum/consensus-specs/pull/4694)
- [x] [Clean up Gloas specs (part 4)](https://github.com/ethereum/consensus-specs/pull/4721)
- [x] [eip7732: add gossip rule for old payloads](https://github.com/ethereum/consensus-specs/pull/4695)
- [x] [eip7732: remove uniqueness requirement in comment](https://github.com/ethereum/consensus-specs/pull/4708)
- [x] [eip7732: clarify PTC description](https://github.com/ethereum/consensus-specs/pull/4719)
- [x] [Remove merkle proof tests in Gloas](https://github.com/ethereum/consensus-specs/pull/4700)
- [x] [Add pending payment withdrawal epoch asserts](https://github.com/ethereum/consensus-specs/pull/4701)
- [x] [eip7732: add PTC subsection to validator assignment section](https://github.com/ethereum/consensus-specs/pull/4713)
- [ ] [Process same-slot slashings before builder payments in Gloas](https://github.com/ethereum/consensus-specs/pull/4726)
- [ ] [Fix randao mix processing in Gloas](https://github.com/ethereum/consensus-specs/pull/4728)

#### Implementation updates from client teams

* Prysm
* Lighthouse
* Teku
* Nimbus
* Lodestar
* Grandine

#### Add off-protocol-value to the bid?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Add a censoring flag to the engine api return on new_payload?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Move `process_builder_pending_payments` above `process_effective_balance_updates`?

https://github.com/ethereum/pm/issues/1783#issuecomment-3500921455

#### The `verify prev randao` check uses the post state of the block with different randao mixes

https://github.com/ethereum/pm/issues/1783#issuecomment-3502321691

https://discord.com/channels/595666850260713488/874767108809031740/1436303424294752407

### Call Series

EIP-7732 Breakout Room

<details>
<summary>🔧 Meeting Configuration</summary>

### Duration

60 minutes

### Occurrence Rate

bi-weekly

### Use Custom Meeting Link (Optional)

- [ ] I will provide my own meeting link

### Facilitator Emails (Optional)

jtraglia@ethereum.org

### Display Zoom Link in Calendar Invite (Optional)

- [x] Display Zoom link in invite

### YouTube Livestream Link (Optional)

- [x] Create YouTube livestream link
</details>












#### The verify prev randao check uses the post state of the block with different randao mixes



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/1783#issuecomment-3502321691)












####



        opened 02:31AM - 25 Oct 25 UTC



          closed 03:22PM - 07 Nov 25 UTC



        [![](https://avatars.githubusercontent.com/u/95511699?v=4)
          jtraglia](https://github.com/jtraglia)





          Breakout


          ePBS


          protocol-call







### UTC Date & Time

[November 07, 2025, 14:00 UTC](https://savvytime.com/conver[…]()ter/utc/nov-7-2025/2pm)

### Agenda

#### Specifications & testing

New consensus specifications: [v1.6.0-beta.2](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-beta.2) & [v1.6.0](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0)

- [ ] [eip7732: add tests for `process_withdrawals` block processing](https://github.com/ethereum/consensus-specs/pull/4468)
- [ ] [eip7732: add fork choice tests (part1)](https://github.com/ethereum/consensus-specs/pull/4489)
- [x] [Clean up Gloas specs (part 2)](https://github.com/ethereum/consensus-specs/pull/4693)
- [x] [Clean up Gloas specs (part 3)](https://github.com/ethereum/consensus-specs/pull/4694)
- [x] [Clean up Gloas specs (part 4)](https://github.com/ethereum/consensus-specs/pull/4721)
- [x] [eip7732: add gossip rule for old payloads](https://github.com/ethereum/consensus-specs/pull/4695)
- [x] [eip7732: remove uniqueness requirement in comment](https://github.com/ethereum/consensus-specs/pull/4708)
- [x] [eip7732: clarify PTC description](https://github.com/ethereum/consensus-specs/pull/4719)
- [x] [Remove merkle proof tests in Gloas](https://github.com/ethereum/consensus-specs/pull/4700)
- [x] [Add pending payment withdrawal epoch asserts](https://github.com/ethereum/consensus-specs/pull/4701)
- [x] [eip7732: add PTC subsection to validator assignment section](https://github.com/ethereum/consensus-specs/pull/4713)
- [ ] [Process same-slot slashings before builder payments in Gloas](https://github.com/ethereum/consensus-specs/pull/4726)
- [ ] [Fix randao mix processing in Gloas](https://github.com/ethereum/consensus-specs/pull/4728)

#### Implementation updates from client teams

* Prysm
* Lighthouse
* Teku
* Nimbus
* Lodestar
* Grandine

#### Add off-protocol-value to the bid?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Add a censoring flag to the engine api return on new_payload?

https://github.com/ethereum/pm/issues/1783#issuecomment-3498690908

#### Move `process_builder_pending_payments` above `process_effective_balance_updates`?

https://github.com/ethereum/pm/issues/1783#issuecomment-3500921455

#### The `verify prev randao` check uses the post state of the block with different randao mixes

https://github.com/ethereum/pm/issues/1783#issuecomment-3502321691

https://discord.com/channels/595666850260713488/874767108809031740/1436303424294752407

### Call Series

EIP-7732 Breakout Room

<details>
<summary>🔧 Meeting Configuration</summary>

### Duration

60 minutes

### Occurrence Rate

bi-weekly

### Use Custom Meeting Link (Optional)

- [ ] I will provide my own meeting link

### Facilitator Emails (Optional)

jtraglia@ethereum.org

### Display Zoom Link in Calendar Invite (Optional)

- [x] Display Zoom link in invite

### YouTube Livestream Link (Optional)

- [x] Create YouTube livestream link
</details>













      ![](https://discord.com/assets/favicon.ico)

      [Discord](https://discord.com/channels/595666850260713488/874767108809031740/1436303424294752407)



    ![](https://cdn.discordapp.com/assets/og_img_discord_home.png)

###



Discord is great for playing games and chilling with friends, or even building a worldwide community. Customize your own space to talk, play, and hang out.










**Meeting Time:** Friday, November 07, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1783)

## Replies

**poojaranjan** (2025-11-07):

Quick notes [Tweet thread](https://x.com/poojaranjan19/status/1986795781207044361)

---

**system** (2025-11-07):

### Meeting Summary:

The team discussed updates on two new specification releases and reviewed several merged and open PRs, including changes related to gloss, attestation gossip, and block processing. Client implementation progress was shared across various team members, with most focusing on the Fusaka mainnet and DevNet Zero timeline pushed to mid-January. The team explored potential additions to the protocol, including off-protocol values for bids and censorship detection flags, while also discussing concerns about state update ordering and quorum threshold calculations in Process Builder.

**Click to expand detailed summary**

The team discussed two new specification releases, V1.6.0 Beta 2 and V1.6.0 stable, which primarily focused on gloss and included new tests and spec changes. Justin mentioned that several team members had already updated to track the changes. They also briefly touched on a few merged PRs and one new open PR shared by Potuz in the chat. The meeting was scheduled to start 1 hour earlier than usual due to a time change in the US, catching some team members off guard.

The team provided updates on client implementations, with most focusing on the Fusaka mainnet. Terence reported progress on merging container objects but noted limited progress on ePBS-related implementation. Shane mentioned that PRs related to block processing were being merged into Lighthouse, while Stefan and NC shared updates on attestation gossip changes and block production work. Subhasish reported progress on GossipSub and RPC changes, with sync work nearly complete. The team agreed that DevNet Zero might not be ready until mid-January, and Justin suggested focusing on the Fusaka mainnet release for the remainder of the year.

The team discussed adding an off-protocol value to bids, with Potuz initially opposing but later agreeing it could be beneficial for client validation. They debated whether to include an “enforced payment” boolean flag, with Francesco suggesting this as an alternative to having both in-protocol and off-protocol values. Potuz proposed adding a censoring flag to the Engine API to allow EL clients to detect and report censorship, but decided to wait for the Fossil proposal outcome before discussing it further at ACDC.

The team discussed whether to use previous epoch balances or updated balances for quorum threshold calculations in Process Builder pending payments. Francesco suggested it might not matter much due to bounded balance changes between epochs, while Justin noted the current implementation uses current epoch balances. Potuz and Shane proposed moving the quorum calculation before effective balance updates, but Justin expressed concern about potential side effects of changing the order of functions. The team agreed to further consider the implications of this change.

The team discussed concerns about the order of state updates in the compute epoch and update churn functions, with Potuz and Francesco agreeing that the current implementation likely doesn’t need changes despite potential inconsistencies. They also reviewed a PR for fixing prevAN DAO verification during block processing, with Stefan and Potuz agreeing to use the bit container for storing the prevAN DAO value. The team decided to create separate PRs for adding off-protocol values to the bid and RANDAO mix, with Justin suggesting “el_payment” as a potential field name. Terence explained that current tests only cover SSZ static and block operation tests, with limited coverage for payload and state transition functions.

### Next Steps:

- Potuz: Write a quick PR for the RANDAO thing
- Potuz: Open PR for adding off-protocol value field to the bid
- Potuz: Add regression test in the PR for the prevRANDAO issue
- Shane: Make a thread on Discord in the ePBS channel to continue discussing the process_builder_pending_payments ordering issue
- Justin: Review and merge Potuz’s prevRANDAO PR after client approvals
- Justin: Talk with Leo about adding more extensive testing for consensus spec tests
- Justin: Think about naming for the off-protocol value field
- Client teams: Approve Potuz’s prevRANDAO PR
- Justin: Make a new 1.6.1 release when needed

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: N6*T+*38)
- Download Chat (Passcode: N6*T+*38)

---

**system** (2025-11-07):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=j3Bx6EgCAOo

