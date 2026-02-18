---
source: magicians
topic_id: 2929
title: More frequent, smaller hardforks vs. less frequent, larger ones
author: timbeiko
date: "2019-03-15"
category: Magicians > Process Improvement
tags: [ethereum-roadmap, hardfork]
url: https://ethereum-magicians.org/t/more-frequent-smaller-hardforks-vs-less-frequent-larger-ones/2929
views: 13115
likes: 55
posts_count: 45
---

# More frequent, smaller hardforks vs. less frequent, larger ones

In today’s [AllCoreDevs call](https://github.com/ethereum/pm/issues/83) there was discussion about potentially moving from large hard forks containing several EIPs to smaller ones with less (or potentially only a single) EIPs.

The goal of this thread is to start a discussion around the Pros and Cons of each approach. I’ll begin by listing a few, but I don’t feel like I have the full picture, so it would be valuable for others to chime in. Namely, [@AlexeyAkhunov](/u/alexeyakhunov), as you had advocated for smaller hard forks in the past and brought it up again in today’s call ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9).

I will keep editing the argument lists below as people comment on the thread.

**Arguments for Smaller, More Frequent Hard Forks**

- More frequent updates to the protocol;
- Can separate concerns better / isolate changes;
- Multi-hard-fork initiatives, such as State Rent, can drastically reduce their deployment time;
- “Unless we make serious improvements in the way the EIPs are put it, there is little hope that Ethereum 1x will deliver what it is supposed to.”
- Simplifies testing due to a more steady flow of less EIPs to test and less cross-EIP interactions to test.

**Arguments for Larger, Less Frequent Hard Forks**

- Less frequent need for users to update clients;
- There is a coordination cost to each HF, so more frequent ones involve more coordination work across major stakeholders running clients (e.g. miners, exchanges, block explorers, etc.);
- Allows ample time for security evaluation
- If hard forks are too close to each other, bugs found in a given hard fork may delay/push back subsequent hard forks

**Other Considerations**

- Ad-hoc vs. fixed schedule for hard forks
- Smaller hard forks may result in multiple hard forks happening in parallel (where various forks are at different deployment stages)

## Replies

**sneg55** (2019-03-15):

We have to define that Users who need to update clients - it’s mining pools, exchanges, light wallets and infrastructure providers such as Infura.

They all benefiting from Ethereum ecosystem, and I think they will support more frequent updates.

---

**shemnon** (2019-03-15):

For users also consider that exchanges tend to shut down trading in the hours before and after a hard fork.

So is the question about smaller vs. larger hard forks or for ad hoc vs. scheduled hard forks?  If we want smaller more frequent hard forks we can still do that on a fixed schedule, perhaps every three months.  But if we do we will almost certainly have to pipeline and layer the process so that we may have three hard forks in flight: one is in the testing/deployment, one is in client implementation, and one is in EIP review.

I think a predictable and short schedule will result in smaller forks.  A quarterly/semi-annual mandatory update is what would result from a fixed schedule, vs a random and unpredictable mandatory update schedule.

---

**sneg55** (2019-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I think a predictable and short schedule will result in smaller forks. A quarterly/semi-annual mandatory update is what would result from a fixed schedule, vs a random and unpredictable mandatory update schedule.

We could set a quarterly schedule for network updates so that everyone will benefit from predictable timelines. For exchanges, pools and other users it’s easier to allocate resources for HFs when exact schedule is known.

And in case if something goes wrong as it was with Constantinople, EIPs from such hardfork just moving to next scheduled date, instead of creating new hardfork in between.

---

**timbeiko** (2019-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> So is the question about smaller vs. larger hard forks or for ad hoc vs. scheduled hard forks?

Agreed, these two seem to be orthogonal. Will update the initial post.

---

**AlexeyAkhunov** (2019-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> But if we do we will almost certainly have to pipeline and layer the process so that we may have three hard forks in flight: one is in the testing/deployment, one is in client implementation, and one is in EIP review.

Yes, and I think this is absolutely fine. However, it does require to change the ways the changes are done. First and foremost, if we pipeline the changes, we cannot rely on a single testing team to do all the test generation - that would need to happen while EIP is prepared.

Having more frequent upgrades (scheduled or not - it is orthogonal s [@timbeiko](/u/timbeiko) noted) will help avoid half-baked changed that would need to be “squeezed through” before the deadline. Postponing something by 3 months is not as bad as postponing it by 9 months.

Also, it looks like Ethereum 1x has invigorated the appetite for more changes in Ethereum, which is good, but I do not want it to have to create too much tension when changes compete for the limited space in the large releases.

---

**timbeiko** (2019-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Also, it looks like Ethereum 1x has invigorated the appetite for more changes in Ethereum, which is good, but I do not want it to have to create too much tension when changes compete for the limited space in the large releases.

Good point. I think a related issue is that changes compete for limited client implementer resources. Whether hard forks happen every 3, 6, or 9 months, the amount of developers working on clients is more or less constant and if more time is spent implementing/testing/deploying EIPs, because of an overall growth in changes to the protocol, then less time is spent on non-EIP work.

---

**AlexeyAkhunov** (2019-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Whether hard forks happen every 3, 6, or 9 months, the amount of developers working on clients is more or less constant and if more time is spent implementing/testing/deploying EIPs

So far it looks to me that the actual time spent on implementing EIPs in the clients is not that large - especially if EIPs are well-prepared. It is only when EIPs are not well specified, missing tests, there are more iterations to figure things out. As much work as possible needs to be done pre-EIP, so that the client implementers aren’t the bottleneck - and I don’t think they usually are.

---

**xazax310** (2019-03-18):

I think the problem with more frequent HF could be more problems if something like EIP1283 happens again. A 3 month schedule is tight one to make, should something happen, that will then cascade down and possibly delay the rest. I know I may be the only one arguing for this, but I think one year release schedule where EIPs are chosen the previous year Audited, tested though-out the year on testnet etc then implemented at a set date/time/month every year.

This gives ample time for bugs to be found. Processes to be improved and allows Pools and Exchanges the “HF” date every year to be prepared and ready to upgrade.

---

**timbeiko** (2019-03-18):

Thanks for your comment! Is it fair to rephrase this comment:

> I think the problem with more frequent HF could be more problems if something like EIP1283 happens again. A 3 month schedule is tight one to make, should something happen, that will then cascade down and possibly delay the rest.

as "Increases risk that bugs found in `HF x` cause delay in `HF x+1` ?

If that is fine with you, [@xazax310](/u/xazax310), I can add it to the list in the original post.

Similarly, can I rephrase this:

> Audited, tested though-out the year on testnet etc then implemented at a set date/time/month every year.
> This gives ample time for bugs to be found. Processes to be improved and allows Pools and Exchanges the “HF” date every year to be prepared and ready to upgrade.

as “Allows ample time for security evaluation” ? The rest of your concern seems already captured by " * There is a coordination cost to each HF, so more frequent ones involve more coordination work across major stakeholders running clients (e.g. miners, exchanges, block explorers, etc.);", but let me know if it isn’t.

---

**xazax310** (2019-03-18):

> as “Allows ample time for security evaluation” ? The rest of your concern seems already captured by " * There is a coordination cost to each HF, so more frequent ones involve more coordination work across major stakeholders running clients (e.g. miners, exchanges, block explorers, etc.);", but let me know if it isn’t.

Yeah, that seems right in line with what I’m thinking.

> as "Increases risk that bugs found in  HF x  cause delay in  HF x+1  ?

Math has never been my favorite subject ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) so that works for me.

---

**timbeiko** (2019-03-18):

No worries. I meant that this increases the risk that a bug found in a planned hard fork delays the next one. I will rephrase in a less math-y way in the original post.

---

**AlexeyAkhunov** (2019-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xazax310/48/1702_2.png) xazax310:

> I think the problem with more frequent HF could be more problems if something like EIP1283 happens again. A 3 month schedule is tight one to make, should something happen, that will then cascade down and possibly delay the rest. I know I may be the only one arguing for this, but I think one year release schedule where EIPs are chosen the previous year Audited, tested though-out the year on testnet etc then implemented at a set date/time/month every year.

It is my current intuition that unless we make serious improvements in the way the EIPs are put it, there is little hope that Ethereum 1x will deliver what it is supposed to. The current rate of change seems too slow to accommodate the crucial fixes + all the other stuff the people are now proposing since it looks like “the gates are open once again”. I guess it will become very clear in a few months

---

**xazax310** (2019-03-18):

> It is my current intuition that unless we make serious improvements in the way the EIPs are put it, there is little hope that Ethereum 1x will deliver what it is supposed to.

That’s how I’m seeing it too. Is it the EIP process that needs to be reviewed in addition to HF times? I know it sounds unintuitive but would a Committee on EIPs resolve any of those issues? Such as Security concerns, release times, inclusions or exclusions due to security concerns.

```auto
[ WIP ] -> [ DRAFT ] -> [ LAST CALL ] -> [ ACCEPTED ] -> [ FINAL ]
```

```auto
[ WIP ] -> [ DRAFT ] -> [ LAST CALL/REVIEWED ] -> [COMMITTEE  ACCEPTED] -> [PLANNED INCLUSION OF HF SCHEDULED DATE]-> [ FINAL ]
```

I’ll post it here since it relevant but to me looks like another topic for discussion.

---

**lrettig** (2019-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> It is my current intuition that unless we make serious improvements in the way the EIPs are put it, there is little hope that Ethereum 1x will deliver what it is supposed to. The current rate of change seems too slow to accommodate the crucial fixes + all the other stuff the people are now proposing

Seconded, this is my concern and my fear as well. Combined with [Higher standards for EIPs](https://ethereum-magicians.org/t/higher-standards-for-eips/2781), I think we have the beginnings of what needs to be done to improve the EIP process and increase the pace of innovation.

I think testing is definitely one bottleneck in the existing process and we should discuss how to improve throughput - I think a “layered pipeline” approach as discussed here would make sense. Does the testing team have sufficient resources today? CC [@holiman](/u/holiman) (I don’t see Dimitry here)

Another thought to consider: instead of a waterfall approach, would a leaner approach with multiple “sprints” maybe make sense here? It seems like [Afri’s proposal](https://en.ethereum.wiki/roadmap/istanbul#timelines), which we’ve been working with for Istanbul, works this way - we’re pursuing multiple EIPs at the same time, with hard deadlines for EIP submission, implementations, testing, etc. and whatever makes it into the next upgrade goes in, whatever doesn’t must wait until the following one.

---

**timbeiko** (2019-03-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Another thought to consider: instead of a waterfall approach, would a leaner approach with multiple “sprints” maybe make sense here?

I think we get this from having *planned* HFs in advance, regardless of the size ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) At this point, we’re mostly debating the length of the sprint ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12)

---

**holiman** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> I think testing is definitely one bottleneck in the existing process and we should discuss how to improve throughput - I think a “layered pipeline” approach as discussed here would make sense. Does the testing team have sufficient resources today? CC @holiman (I don’t see Dimitry here)

Sufficient resources - I’d say no on that. Testing is a bit thankless task, and what complicates the matter is that it both requires very solid knowledge of EVM internals and Ethereum in general, and it’s also much  case of not much happening, and then suddenly there is *tons* of work to be done, as we finalize eips.

So from that respect, I think having a steadier flow of smaller eips would be a definite win. Then it wouldn’t be this case of coordinating testcases for N new features which may or may have internal interaction in odd ways.

---

**timbeiko** (2019-03-29):

Thanks for sharing! I’ve added this to the original post.

---

**timbeiko** (2019-03-29):

One thing that came up in the AllCoreDevs call today is that the this could potentially change *before* Istanbul. When and how should we get consensus on whether we want to change this?

---

**boris** (2019-03-29):

I think this should be an Informational EIP (of which we have very few). We can update 233 to say that dates are picked based on those guidelines. Let’s get it in and finalized [@shemnon](/u/shemnon).

---

**lrettig** (2019-03-29):

On the all core devs call just now [@holiman](/u/holiman) proposed an “EIP-centric” upgrade process rather than a hard-fork centric model like we have now. [@AlexeyAkhunov](/u/alexeyakhunov) also expressed concern about a deadline, like the May 17 Istanbul deadline, meaning that folks would have to rush their EIPs in before the deadline lest they “miss the boat” and have to wait 9 or 12 months until the next hard fork. I’m also concerned about people submitting half-baked “placeholder” EIPs before the deadline.

I like Martin’s idea a lot, especially in combination with smaller, more frequent hard forks. [@shemnon](/u/shemnon)’s proposal at https://github.com/shemnon/EIPs/blob/4e3069b4f9a30a639b142151dc6295f634712786/EIPS/eip-network_upgrade_windows.md looks reasonable to me.


*(24 more replies not shown)*
