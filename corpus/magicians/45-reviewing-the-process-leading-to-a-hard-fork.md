---
source: magicians
topic_id: 45
title: Reviewing the process leading to a hard fork
author: jpitts
date: "2018-02-28"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/reviewing-the-process-leading-to-a-hard-fork/45
views: 1263
likes: 0
posts_count: 3
---

# Reviewing the process leading to a hard fork

[EIP #904 “Community Veto”](https://github.com/ethereum/EIPs/pull/904) was created by GitHub user sfultong in order to create community veto powers as well as clarifying EIP acceptance procedures in the case of Core EIPs (e.g. improvements requiring a consensus fork).

Several key comments helped clarify the process and opined on the appropriateness of a community veto or vote.

What can be learned from these comments is how a Core EIP proceeds to an implementation and acceptance by the All Core Devs group, becomes implemented in clients, gets activated on testnet, and gets activated on mainnet (the hard fork event).

Viewing the [All Core Devs proceedings](https://www.youtube.com/watch?v=GhUtruRZOlo) would also be instructive.

Here, I am focusing on comments that shed light on the process:

- MicahZoltu commented that the process  gives the community an opportunity to “indicate their dislike by not upgrading their nodes to run protocol changes. The community’s role in the governance process (currently) is that of final veto power.”
- Arachnid commented, pointing to a gap in the current process: “nothing that says hard forks have to use EIPs exclusively to describe changes. That process could definitely use formalising and improving.”
- gcolvin commented: “when it comes to changes to the clients the developers of the clients call the shots. The EIP process only provides input. So you can’t actually prevent the core developers from considering an EIP.”
- cdetrio shed a lot of light on the full process in his expanded description.

## Replies

**mks0017** (2018-03-01):

While I agree changes need to be made to the process and that there needs to be more clarity in how EIPs are implemented, giving the community veto powers would make governance much more difficult. Getting the community involved in governance should focus primarily on gathering input so that developers can understand the potential non-technical (moral/ethical/legal) outcomes of implementing an EIP.

I would suggest updating EIP-1 to include a period when community input is gathered before deciding on whether or not to go forward with an EIP. After it’s clear that the EIP could be successfully implemented from a technical standpoint, a period would be opened where interested participants could comment on their support for or against a proposal. This could be as simple as a weekly or monthly stickied post on the ethereum subreddit that includes current EIPs with short summaries that is open for all to comment. This would vastly increase the community’s voice in the process and would allow participants to voice their concerns. This would also allow developers to pose questions to to ensure all issues are addressed before deciding whether or not to implement an EIP.

---

**jpitts** (2018-03-01):

[@mks0017](/u/mks0017), I have created a new topic based on your suggestion:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png)
    [Suggestion to have a community feedback period for each EIP](https://ethereum-magicians.org/t/suggestion-to-have-a-community-feedback-period-for-each-eip/47) [Process Improvement](/c/magicians/process-improvement/6)



> In the topic Reviewing the process leading to a hard fork, @mks0017 suggested that there should be a community feedback period. Each EIP which be allocated a time period for gathering input, voicing concerns, and having Q&As. This time period would be publicized to the community.
> The full text written by @mks0017:
>
> While I agree changes need to be made to the process and that there needs to be more clarity in how EIPs are implemented, giving the community veto powers would make governance much…

