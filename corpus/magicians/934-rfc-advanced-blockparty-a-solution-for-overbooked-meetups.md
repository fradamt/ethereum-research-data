---
source: magicians
topic_id: 934
title: "[RFC] Advanced Blockparty: a solution for overbooked meetups"
author: Ethernian
date: "2018-08-02"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/rfc-advanced-blockparty-a-solution-for-overbooked-meetups/934
views: 657
likes: 1
posts_count: 3
---

# [RFC] Advanced Blockparty: a solution for overbooked meetups

**TLDR:** If a Blockparty gets overbooked, candidates should be able to put a additional stake for other candidates, which means: “I stake 1eth for you because I will see you there”. Finally a meetup organizer invites those subset of all candidates with the most eth on stake.

**Introduction**

Planning a venue for some free meetup is a risk, because attendee’s applications are not binding. People can easily miss the meetup if they suddenly see better choices to spend their time. It is nothing unusual to have on day 10 of 100 attendees in the meetup and another day 95 of 100. An event becomes unpredictable for all: organizer can’t plan the venue and catering. Participants are unaware who will come to the meetup and who not.

A [Blockparty](https://github.com/makoto/blockparty) made by [@makoto](/u/makoto) creates a simple solution for the problem: an attendee should stake 1 eth, which he will get back only if he really comes to the event. If not - his stake becomes redistributed between other participants who came to the event as promised.

Nevertheless there is a drawback: The maximal number of applicants is limited. Extra applicants are going to wait list. A Blockparty creates a priority based on application time, which has nothing to do with meetup and the person. It is not that good.

I propose to extend the Blockparty by simple additional rule selecting participants (in case of overbooking) not by their application time but by some kind of “WantedBy” ranking.  This improvement will allow more useful and focused events.

It will also allow to better split overbooked meetups by topics and interest groups.

**How it works**

Consider, we have a Blockparty with capacity of 6 participants (a medium table in a restaurant). Consider we have 12 candidates willing to come. Besides usual Blockparty staking, we allow any candidate to put 1Eth on stake for *some another candidate* to express “I want you”. By doing this candidate increases *recepient’s* “WantedBy” ranking, but owns the stake. After some time we will become a relationship graph, like this:

A will see C,D,E (and puts 3 eth on stake)

B -> D,F

C-> B,D,E

D -> (no preference)

…

L -> A,D

A subgraph with 6 nodes with most eths on stake gives us the set of candidates who fits the size of the event and are most interested to talk to each other.

An meetup organizer could select the next subgraph with 2nd biggest “WantedBy” stake (and reserve a second table in restaurant). And so on.

Old Blockparty rules apply here too. In particular if somebody doesn’t appear, he loses all his

stake.

**[DISCLAIMER]**: Work in progress. Some details are intentionally missed.

RSVP: [@makoto](/u/makoto) [@JosefJ](/u/josefj)

P.S. [@boris](/u/boris) Would you see this proposal as a solution for the problem of insane high ticket prices for popular community events?

## Replies

**boris** (2018-08-03):

No, this has nothing to do with ticket prices. The ticket prices are high because the event is designed in such a way to have high costs.

FOSDEM hosts 4000 attendees with no fees to attendees.

---

**makoto** (2018-08-03):

Hey, we moved the discussion to https://github.com/makoto/blockparty/issues/179 as this is more specific issue to a Dapp rather than for the entire ecosystem. Feel free to close down the thread here.

