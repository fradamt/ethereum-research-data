---
source: ethresearch
topic_id: 7013
title: The werewolf game problem
author: Wanseob-Lim
date: "2020-02-23"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/the-werewolf-game-problem/7013
views: 2344
likes: 5
posts_count: 5
---

# The werewolf game problem

# Werewolf game problem

During EF SBC workshop, I, [@weijiekoh](/u/weijiekoh) , Yutaro, and Kendrick tried to find a way to implement the werewolf game on Ethereum. It is pretty complex to use only semaphore and maci, we need more ideas. Please leave some comments here if you have any idea on this.

## Game rule

Please see the details of the werewolf game [here](https://en.wikipedia.org/wiki/Werewolf_(social_deduction_game))

## Constraints

1. Smart contract is the game master for the werewolf game.
2. 9 players participate in the game
3. Smart contract designates the 2 werewolves among the players.
4. Every player knows that they are a villager or a werewolf.
5. Werewolves can collude. (Werewolves can know each other.)
6. Villagers cannot collude. (Villagers can’t know who is a werewolf and who is a villager at all).
7. Werewolves pick someone to kill during the night using a secret voting.
8. Everyone picks someone to kill during the day using a public voting.
9. Final survivor’s party wins.

## Replies

**MaverickChow** (2020-02-24):

No idea what’s the purpose of this game but I can see that given sufficient enough repeat of such game, the werewolves will almost always win. The werewolves would win by way of strategy. On the other hand, in case the villagers win it would be the result of sheer luck. Personally, I would pick strategy over luck any time. If the 2 werewolves survive the 1st day, the chance of the villagers to win declines much in the next. If one villager gets killed during the day, another will certainly die during the night, leaving only 5 surviving villagers in the 2nd day. The villagers’ chance of survival is high only if they manage to luckily kill off 1 werewolf in the 1st day to substantially reduce the odd of dying. The werewolves do not need to act rashly during the day. They may wait until one villager got voted by another villager to get killed and the werewolves would just add onto the existing vote to make it at least 3, of course during the day’s voting. Even though 3 out of 9 = 33% does not make it a majority, since villagers do not collude, the remaining 63% may be distributed enough to render the werewolves safer from harm compare to the villagers.

The chance of the final surviving party being a werewolf is higher than being a villager, in my opinion.

---

**Wanseob-Lim** (2020-02-25):

Thanks, [@MaverickChow](/u/maverickchow). In the real game, seer and protector exist who can check the team of a player every night and who can save one from being killed every night. With these roles, it might become harder for the werewolves to win easily. But we want to start with the simplest rule to get rid of some complexities.

---

**barryWhiteHat** (2020-02-27):

We can assign roles using https://en.wikipedia.org/wiki/Mental_poker

Need to think more about how to coordinate players.

---

**Wanseob-Lim** (2024-08-01):

It seems now is a good time to revisit this topic to think about how to make this happen using FHE/MPC primitives.

