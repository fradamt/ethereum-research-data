---
source: ethresearch
topic_id: 2218
title: Channels in our dapp
author: superdcc
date: "2018-06-12"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/channels-in-our-dapp/2218
views: 1925
likes: 0
posts_count: 5
---

# Channels in our dapp

We build a Channels which already using  in our casino.

Call “PG Channels”, let the player only on-chain 1 time and play a lot of time off-chain.

share to you all!

---

**Preparation work**

Player send ERC-20 token to Game Contract(Lock Token)

---

**PG Channels (Go through API)**

Step 1

Dealer Generate “Random D”, and Hash  “Random D”. Announce “Random D’s Hash”

Step 2

Players Generate “Random P”, and Hash  “Random P”. Announce “Random P’s Hash”

Step 3

Players announced “Bets”

Step 4

Hash(“Random D’s Hash”, “Random P’s Hash”, “Bets”). Announce “All Hash”

Step 5

Players Sign the “All Hash”,“Random P” with private key and Announce

Step 6

Dealer Announce “Random D”

Step 7

Hash all Random D & P (Game Result’s random seed)

after step 7, player can know the game result immediately.

and starting next game.

---

**After Playing**

We upload the record to Game Smart Contract .

So player:

1. no need to pay fee.
2. no need to wait transaction confirmation.

we call this: hybrid decentralized casino.

since we upload the record at batch, so we have a small average gas used in every game record.

or we will upload the “result” only, and if the result which we upload is not correct , player can challenge.

---

**Withwraw**

if a player want to withdraw from our platform, he need to wait a period(2 hours or half day)

make sure we are already upload all the record about him.

---


      [github.com](https://github.com/pigworld/Smart-Contract/blob/master/dice.sol)




####

```sol
pragma solidity ^0.4.16;

contract PICOMainContract {
    function requestToPay(address _paidAddress,uint _Amount) public {}
    function requestToAward(address _winAddress,uint _Amount) public {}
    function balanceOf(address tokenOwner) public constant returns (uint balance) {}
    function isGameContract(address _GameContract) public constant returns (bool success) {}
}

contract Dice {

    PICOMainContract PICOMainContract_;
    address public Picomaincontract;

    address public Owner;
    address Dealer;

    struct SimpleTicket {
        address Addrs;
        bytes32 SecretKey_P;
```

  This file has been truncated. [show original](https://github.com/pigworld/Smart-Contract/blob/master/dice.sol)








but it still have 1 problem, player need to trust us will upload.

**so we will do plasma next stage after this modal stable.**

play pig world here:https://pig.world/

## Replies

**tomclose** (2018-06-12):

Looks like a cool game - and a great use for state channels!

I’m you *need* to use plasma to fix your trust issue - it seems like a different state channel approach could help. For example, you could try a commit-reveal strategy for this game (like in the rock-paper-scissors force-move game example [here](https://github.com/magmo/force-move-games/tree/master/packages/fmg-rock-paper-scissors)). I’d be happy to help you work through that, if you’re interested.

Also, is there anything to stop someone from calling the `chargeTicketStep*` functions with `byte32` values that haven’t yet had corresponding `SimpleTickets` uploaded via the `sendSimpleTicket` function? I could be wrong, but it looks like that could get quite expensive for the dealer.

---

**superdcc** (2018-06-15):

Dear [@tomclose](/u/tomclose)

I am interesting what you are saying…

Can your elaborate more about commit-reveal strategy?

---

the chargeStep is for player who is think the result on the chain is wrong.

So he need to challenge the smart contract to arbitration.

As you can see the we put he all game rule in the charge step.

So in the normal situation, the chargeStep will not use.

Because when the player charge successful, dealer will be punish.

Let dealer will carefully handle the upload record.

---

**tomclose** (2018-06-15):

After having another look, I think you might have another potential problem in the setup above: currently a bet can be generated without using the dealer’s private key, which means that anyone can impersonate the dealer, and therefore the dealer doesn’t have any control over the bets they have to accept. In state channels, to change the state you need complete consent of the parties involved in the channel - i.e. you need a digital signature from everyone involved - otherwise the logic breaks down.

When pointing you towards the commit-reveal strategy, I was shamelessly pointing you towards a state channel framework that my team has just released, which would be perfect for building a game like this. We’ve spent a lot of time trying to think through all the edge cases - and will be releasing a paper early next week which explains how it works. By running your game in this framework, you wouldn’t have the problem that your players would need you to trust you to upload the state - if you didn’t, they could claim their winnings on-chain. The framework is released open-source under the MIT license, which allows you to use it for commercial purposes (for free ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) ). (Note that the code hasn’t yet been audited, so you would need to audit any parts you plan to use yourself.)

If this is a path you wanted to follow, we’d be happy to assist you in getting started - just send me an email at [research@magmo.com](mailto:research@magmo.com) and we can set up a call or something. We built this framework for the community to use and would love to see if it would be useful for you in its current form!

---

Regarding the `chargeStep` part of your contract - I can see how it’s meant to be used, for a player to challenge a dishonest dealer. My concern is that it can also be abused by anyone. Take the following example:

```auto
let x = keccak256("some random value - it doesn't matter");
// x is a random bytes32 value, which doesn't correspond to any bet
// send x to the chargeTicketSteps methods
chargeTicketStep1([x])
chargeTicketStep2([x])
chargeTicketStep3([x])
```

My questions are: (1) Is there anything to stop anyone from doing the above? (2) What is the outcome of that sequence of operations? My concern was the the answers are “no” and “the dealer loses 10000000000” - but I could easily be wrong. Just wanted to highlight it as an edge-case for you to check! (Edit: I think in that particular example it might happen to be ok - the wider problem is that your code seems to assume that `sendSimpleTicket` is called before `chargeTicketStep1`, but it doesn’t check this.)

---

**superdcc** (2018-06-24):

In the PC channels first stage, player only play with us(Pig world is dealer)

so, you can see the dice.sol

line 50

> require(msg.sender == Dealer);

**only the dealer can upload the game record.**

and dealer can’t counterfeit a fake game record, because the player need to sign with private key and send to use with api.

because we upload the all parameter which used in the pg channels creating.

so if the player think the result is wrong, he can go to chargeTicketStep1, chargeTicketStep2, chargeTicketStep3

---

One more thing, we want to “sendSimpleTicket” as lower gas as possible.(because dealer need send every game record through this function).

so we separate the game rule(sic bo game rule) to the challenge function.

This mechanism is just like state channels’s instant leave.

---

Thank you tomclose deep & kindly response every time,

I saw your white paper, and we think we can try build a game on the FMG.

And we can learn something when we do this.

