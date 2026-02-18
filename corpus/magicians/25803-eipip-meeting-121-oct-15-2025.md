---
source: magicians
topic_id: 25803
title: EIPIP Meeting #121, Oct 15, 2025
author: system
date: "2025-10-14"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/eipip-meeting-121-oct-15-2025/25803
views: 43
likes: 0
posts_count: 3
---

# EIPIP Meeting #121, Oct 15, 2025

### Agenda

## Call for Input

- Discussion on new EIP editor – Mercy
- Allow links to Protocol Buffers specification

## Editors’ Discussion

- Linking a discussion to section for reference implementation Ref: Discord
- EIP-1 Updates & Editorial Policies
Discuss and decide on possible additions to EIP-1 regarding EIPs/ERCs, including:

Policy on accepting typo-only PRs
- Policy on edits to Final EIPs allowing EIP editors to merge PRs after 4 weeks with consensus when the author is absent/unavailable

Any other Process Change Recommendations (Community Feedback, if any)
PRs for Editors review and/or consensus
Misc

- Website: Add dark mode toggle to nav EIPs#10154 [Keep or Close]

Force merge

- Update EIP-1014: Complete address formula rationale explanation EIPs#10074
- Update EIP-969: fix broken discussion link EIPs#10513
- CI: Generate ordered lists of pull requests needing review EIPs#8831

Typo

- Update EIP-2025: fix typo in EIPS/eip-2025.md EIPs#10326
- Update EIP-712: typo, reference ERC spec correctly and formats EIPs#9872 [Author not around/responding]
- Update ERC-601: fix a typo ERCs#1150
- Update ERC-7092: Fix typos in ERC-7092 documentation ERCs#1190
- Update ERC-7573: Fix typo ERCs#1202
- Update ERC-5773: Fix typo ERCs#1205

## PR analytics & Editors’ Updates

- Observations from incoming PRs over the past month
- Availability for hosting EIP Editing Office Hours → add to the schedule

## EIP Insight

- October 2025

## Community update

- Project Showcase or feedback

more feedback for dip.box

## Next meeting - 12 or 19 or 26 November (Nov 19 is the week of Devconnect)?

**Meeting Time:** Wednesday, October 15, 2025 at 16:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1762)

## Replies

**system** (2025-10-15):

### Meeting Summary:

The meeting focused on discussing various EIP process improvements and policy updates, including handling typo PRs, automating final EIP approvals, and expanding contributor tools. The team reviewed upcoming events like the EIP summit at DevConnect and demonstrated new tools for tracking Ethereum upgrades and proposal status. A new EIP editing platform called DIP.Box was presented, followed by discussions about improving the EIP editor tool with features like color-coding and live feedback, and the team agreed to reschedule their next meeting to November 12th.

**Click to expand detailed summary**

The meeting, led by Pooja, began with a discussion on the agenda items for the day, including a call for input and policy updates for contributors, authors, and editors. Sam took over to address the call for input, noting the lack of editor responses despite the 30-day window. The team decided to wait a bit longer for more editor input before proceeding with the agenda.

The team discussed closing an open issue in favor and agreed to create a call for input on allowing links to Ethereum Magicians in reference implementations. They also considered creating a formal decision on accepting typo-only PRs, given the high volume of such PRs in the EIP repository. Pooja emphasized the need to document official decisions to avoid confusion for new editors and participants in the ecosystem.

Pooja and Sam discussed the handling of typo PRs for EIPs. Pooja proposed implementing a bot to review these PRs and close them for stagnant or withdrawn proposals unless there’s an intention to revive them. Sam expressed disagreement, arguing that fixing typos, even on inactive proposals, maintains the EIP process’s credibility. He offered to personally clean up typo PRs and suggested getting the spell checker working again.

The team discussed automating PRs and policy changes for final EIPs. They agreed to allow editors to merge PRs for final EIPs after a long period of inactivity, provided the changes are trivial. Pooja and Sam decided to document this policy in contributing.md and link it to EIP1. They also considered adding it to the “deciding section” of EIP 5069. The team agreed to come up with specific wording for acceptable types of changes. No other process changes or community feedback were mentioned.

Pooja announced an EIP summit at DevConnect on September 21st, which will focus on protocol team interactions and EIP proposals. Sam agreed to participate in a live session on the 21st, replacing a previously scheduled session on the 18th. The team discussed closing several PRs, including one that Sam and Gajendra felt was not important, and agreed that editors could close PRs after six months if they appear to be abandoned. Pooja also mentioned that a new schedule for editor availability is now live, allowing editors to sign up for the weekly editing office hours.

Dhanush demonstrated two tools developed by the EIPs Insight team: a live countdown for Ethereum’s next major upgrade (Fusaka) and an expanded EIP boards page that will provide richer proposal tracking and contributor mapping. The countdown tool shows remaining blocks and epochs for different networks, while the EIP boards expansion aims to improve governance transparency by showing contributor activity and proposal status.

The team discussed expanding the list of EIPs and adding PR titles for better context. Dhanush mentioned an upcoming Contributors Analytics page featuring a leaderboard and a transaction tracker for monitoring on-chain transactions. Pooja inquired about a previous website issue, which Dhanush confirmed was resolved. The team also reviewed the October EIP insights, which were now visible on the website.

Peersky presented a prototype called DIP.Box, which aims to simplify the EIP editing process by abstracting authors from GitHub usage. The platform offers a multi-tenant environment for different ecosystems, including Ethereum, and provides features like form validation, markdown editing, and pull request submission. While the current version is in the development phase and requires GitHub integration, the long-term goal is to eliminate the need for GitHub accounts and create a more inclusive workspace environment.

The team discussed a demo of a new EIP editor tool, with Pooja and Sam providing positive feedback on features like color-coding for EIP status and a PR creation document. Sam suggested integrating EIP Warrior, a Rust-based linter, to provide live feedback on proposals. The group agreed to move their next meeting from the third Wednesday to November 12th due to DevConnect Week, and discussed potential features for the editor including spell-checking, policy enforcement, and notifications for authors.

### Next Steps:

- Sam to clean up typo PRs and work on getting a spell checker working again.
- Sam/Pooja to create a PR to document the policy on allowing editors to merge typo PRs for final EIPs without author approval in contributing.md and link to it from EIP1.
- Sam to review PR #10513.
- Editors to add their availability to the schedule for upcoming EIP editing office hours.
- EIPs Insight team to expand the EIP boards page to include more proposals and add PR titles.
- EIPs Insight team to develop the Contributors Analytics page with a leaderboard for weekly, monthly, yearly, and overall contributions.
- Pooja to move the EIP editing office hour from September 18th to September 21st during DevConnect.
- Pooja to create the agenda for the next EIPIP meeting on November 12th.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: %Ciu*2F=)
- Download Chat (Passcode: %Ciu*2F=)

---

**system** (2025-10-15):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=EDrhgOhQ_YI

