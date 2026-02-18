---
source: magicians
topic_id: 3561
title: "Hardfork Meta EIP-2070: Berlin discussion"
author: axic
date: "2019-08-19"
category: EIPs > EIPs Meta
tags: [hardfork]
url: https://ethereum-magicians.org/t/hardfork-meta-eip-2070-berlin-discussion/3561
views: 59497
likes: 4
posts_count: 7
---

# Hardfork Meta EIP-2070: Berlin discussion

I am adding this as the discussion URL for the Berlin hardfork meta and propose this thread to be dedicated for discussing proposed EIPs and to judge the sentiment when to move them between the stages.

https://eips.ethereum.org/EIPS/eip-2070

## Replies

**adamluc** (2019-10-28):

There has been a lot of discussion around EIP1559, is this something we can include in Berlin?


      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-1559)




###

Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.

---

**tvanepps** (2019-10-30):

exploratory work has been done, now waiting on funding to come through, things are happening behind the scenes. it’s a significant change and requires a lot of work, including a wallet PoC and experimental Geth implementation. also economic studies.

hopefully some news on this soon (i’m not part of any of the teams, just following it closely)

---

**jochem-brouwer** (2020-06-28):

Can we have a discussion here about the meta-process where we accept EIPs into a hardfork? It apparently seems to be OK to accept EIPs who are still in Draft status.

The current [BLS EIP (2537)](https://eips.ethereum.org/EIPS/eip-2537) is in Draft. How is it possible that an EIP which can change in the future get accepted in a call? Also, why is it not a mandatory requirement to have a complete test suite available at the point where the EIP gets accepted?

I find this process extremely dangerous and very error prone. If we have to make cross-client implementations for an EIP, I do not think we can do so if we do not have official, complete test vectors. [The CSV files in the EIP](https://github.com/matter-labs/eip1962/tree/master/src/test/test_vectors/eip2537), which are not in official state test format, are not complete: they miss a few error cases and also the gas usage is not included. How can we make cross-client implementations if we do not have a testbed for them to work on?

My points:

1. Make it mandatory for an EIP to be Final/Accepted status if it wants to be included in a hard fork.
2. Make it mandatory for hard fork EIPs to have a complete test suite.

I think as extension for point (2) reviewers of the EIP should explicitly check that the test cases are “complete”. That is, if error cases are listed in the EIP, at least one of these error cases (but more is of course better) should be added as state test. Also the tests should be in state tests format and a PR of this should be open in the [ethereum/tests](https://github.com/ethereum/tests) repository.

Another thing which I find very weird is that it seems that no developer of any client has raised these points. I do not understand how you can implement an EIP without a complete testbed. How can we be confident that the implementation matches the intended spec if a complete test suite is missing? I find this very confusing. Maybe someone can enlighten me on this point.

CC [@shamatar](/u/shamatar) [@MariusVanDerWijden](/u/mariusvanderwijden) [@tkstanczak](/u/tkstanczak) [@holiman](/u/holiman) [@axic](/u/axic) [@karalabe](/u/karalabe)

---

**tkstanczak** (2020-06-28):

I would like to upvote it 100x. The first hard fork that we were implementing when we already had a functional system was Byzantium. Byzanitum went through without even official list of accepted EIPs, without public test cases and with all the EIPs marked as Draft or so. It barely improved since then.

---

**holiman** (2020-06-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Another thing which I find very weird is that it seems that no developer of any client has raised these points. I do not understand how you can implement an EIP without a complete testbed. How can we be confident that the implementation matches the intended spec if a complete test suite is missing? I find this very confusing. Maybe someone can enlighten me on this point.

I think this all stems from a misconception about how the fork process used to be, and how it is now. We used to schedule a fork, then decide that EIP X, Y and Z went into it.

The change now is that we “Accept” early on, but in a more vague fashion. We say, “It’s eligible for inclusion, at some point in the future, if it meets the expectations”.

The expectations at that future point, are among other things,

- That testcases exist, and test coverage is good (happy-paths, cornercases etc)
- That PRs are merged in all clients,
- That sufficient security-testing has been performed,
- That the EIP is finalized.

So the initial accept is basically a signal for the EIP-author whether it’s worth spending all the effort on pursuing this. If we say “Eligible”, that means client developers will be open to accepting PRs.

Now, ok, let’s talk about BLS. Is it ready to be included in a HF?

- No official testcases exist, so no on that front (although it would be easy to fix them from the existing vectors)
- PRs merged in all clients: No,
- Sufficient security testing: No, it hasn’t been possible to fuzz it via statetests, since only geth exposed it for state-tests,
- Finalized EIP: No, it’s been changed since the Yolo-spec. The implementations do not match with what’s in the EIP right now (unless it’s changed again).

So now we have a more iterative process. And iterative processes are probably better. It’s very difficult to actually produce the statetests unless you have a client which has it implemented. Whereas if you iterate on, and feed back through Implemenation ↔ Testcases ↔ EIP , then it’s easier to make all these three components mature and good, without placing the burden on any single one of these different roles to carry all the burden.

---

**holiman** (2020-06-30):

Some more context around EIP-centric forking: https://notes.ethereum.org/JcsYSdDnSSClUM0ohPykfw

