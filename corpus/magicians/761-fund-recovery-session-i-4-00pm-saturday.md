---
source: magicians
topic_id: 761
title: Fund Recovery Session I - 4:00pm Saturday
author: GriffGreen
date: "2018-07-17"
category: Protocol Calls & happenings > Council Sessions
tags: [fund-recovery]
url: https://ethereum-magicians.org/t/fund-recovery-session-i-4-00pm-saturday/761
views: 996
likes: 2
posts_count: 2
---

# Fund Recovery Session I - 4:00pm Saturday

[@jpitts](/u/jpitts)’s Fund Recovery Session II notes are here: [Fund Recovery Session II - 11:30am Sunday](https://ethereum-magicians.org/t/fund-recovery-session-ii-11-30am-sunday/1035)

Stuck Funds -  (that would need a hard fork to recover)

Nothing in these notes are decisions, its really just the magicians talking about how they understand things to work.

3 relevant EIPs!

156 - general process for stuck ether

- Tokenize losses and do one big recovery for everyone using “governance”
- One time clean up
- Vitalik is influential but inactive.
- He is listened to but he is careful… but he has no authority
- This is the one opportunity to do some clean up on lost ETH via a hard fork moving out of beta

867 - (Made by Musiconomy)

- design a process for anyone to create a process to recover funds, even if there is a small request, they could use this to make their request heard.

999 - surgical for multisig recovery

- Really simple way to recover the funds
- Not 867 compatible
- Made specifically to avoid any other dependencies
- There were no technical objections
- It’s a community issue
- Part of the community thinks that this will cause a hard fork and there might be
- Maybe if some of the money that could be unstuck for other purposes that would be cool
- Vitalik said the one time clean up is on the table in his opinion

From the EIP point of view and say, once the LAST CALL happens and there is no TECHNICAL OBJECTIONS, then it can become an EIP.

- Miners adopting xyz is not relevant for ETHMagicians
- But Core Devs actually do have to deal with political or socially contentious!!!
- EIP Editors just standardize without implementing
- Core Devs decide what gets in the hard fork
- It has to be an affirmative user choice

During TheDAO days, there was push back from the community to do SOMETHING.

- Check out voting.slock.it
- Still early but it’s happening!

Should this be bundled in a technical upgrade or should it be separate?

- If we have it combined then we have 3 forks!
- There are 2 hard forks coming up, one in about 3 months? And
- Reducing issuance
- There is an ice age, when the mining reward was lowered from 5 eth to 3eth it was sort of bundled with technical upgrade in october
- Going to happen again likely in the next hard fork!
- Why should we pay so much for security
- Last time there was an invite to the core devs call

Is it too expensive to hard fork? What happens to DAI?

- When people come out with this argument then we should just never fork.
- DApps will need to deal with this problem anyway.
- Do we just need to get better at hard forks.
- Maybe because of the other networks (POA, RSK, UBIQ) the DApp layer might be better label

Signal vs noise is really bad on the stuck ether issue

- How do we understand signalling?
- Should we start with creating a website for signalling?
- There was already a twitter battle over 999 but a lot of people that made hard stances didn’t show up to talk about it
- Is there a community process? The Core devs would need to respect it if it created
- Signalling

Need to be careful that the process to recover funds is especially open and its not just 1-5 large players that can do this, but that if someone has 7 ETH in a smart contract somewhere locked out this get out of jail free card is accessible to them as well

- WHAT IS THE PROCESS!?!?!!?

## Replies

**twel** (2018-07-24):

I don’t believe that contentious changes should be bundled with non-contentious changes because it doesn’t give a *realistic* opportunity for people running the nodes to approve or disapprove the contentious issue. Instead it’s an ultimatum: “you either accept our contentious proposal or be left behind on the non-contentious proposal”.

> Need to be careful that … if someone has 7 ETH in a smart contract somewhere locked out this get out of jail free card is accessible to them as well

I agree, but EIP-999 does not meet this requirement.

