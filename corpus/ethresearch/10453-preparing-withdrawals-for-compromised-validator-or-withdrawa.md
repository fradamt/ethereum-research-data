---
source: ethresearch
topic_id: 10453
title: Preparing withdrawals for compromised validator or withdrawal keys. FAO Zilm
author: TobesVibration
date: "2021-08-31"
category: The Merge
tags: []
url: https://ethresear.ch/t/preparing-withdrawals-for-compromised-validator-or-withdrawal-keys-fao-zilm/10453
views: 13905
likes: 37
posts_count: 60
---

# Preparing withdrawals for compromised validator or withdrawal keys. FAO Zilm

Dear Zilm & ETH Devs,

Apologies in advance if my post is deemed inappropriate for https://ethresear.ch the purpose of my post is to help find a solution for all ETH 2 nodes which may have had their validator or withdrawal keys breached.

It is pointless getting into the details of how it happened to me, what I think is important is trying to find a solution. I will make this attempt to share my thoughts in a manner which hopefully doesn’t get me immediately banned.

The purpose of a system breach may not only be for financial purposes it may be to undermine the network and the Ethereum Foundation, so being extra prudent for when withdrawals are enabled is what I would like to discuss.

For a large number of nodes there will be two operators, the host (server side) who holds the validator key and the Staker (client side) who holds the withdrawal key. Below I will write a list of steps which would mean the two parties would need to work together to authorise each other to request a withdrawal, thus making it much harder for a hacker/bad-actor to use a compromised withdrawal key.

Note: This proposal is a little labor intensive and may not be for everyone, it could be **optional** but for extra security and peace of mind it could be worth the effort and may be worth the client paying the host a fee for example $50-$100 for each withdrawal.

1. Maybe not popular, but with such large sums of money involved Host’s should use KYC type security protocols.
2. Not everyone will want to withdraw funds when we reach phase 1.5 so could there be an option to “lock/unlock” the node withdrawal service, by default all nodes should be set to “locked” this way withdrawals will be impossible until the Staker chooses he/she/they is ready for a withdrawal.
3. Similar to a 3 way handshake a withdrawal could have multiple steps to protect the misuse of a key using the (server side) node key and the (client side) withdrawal key/request.
4. After a users ID has been fully verified by the host the Staker makes a request to the host for a withdrawal/skim.
5. Using the node validator Key the host (server side) would need to send a request to the network for a withdrawal/skim.
6. Each (server side) withdrawal request will trigger a unique forthcoming Epoch or Slot number to be sent to the node/host, for the purpose of this discussion we can think of an Epoch or Slot number as a type of PIN number similar to that used with a credit card (CC).
7. The PIN number could be sent to the client after full ID verification has taken place, the PIN could be sent using email, SMS, phone call or maybe even sent in the post similar to a CC PIN number?
8. The client now has their withdrawal key and a PIN, by rights the hacker only has the withdrawal key (we hope) rendering it useless without the PIN.
9. This PIN must be unique for each withdrawal request and can only be used once.
10. The client starts the withdrawal request using the PIN, withdrawal key, amount to withdraw and a wallet address to send the funds.
11. The withdrawal request will trigger an unlock request with the host (server side) and the host can confirm the withdrawal request was made by the client before unlocking the node.
12. Client verifies the wallet withdrawal address and confirms the withdrawal request was initiated by the client and the node is unlocked by the host.
13. The client will have only one chance with each request, should the PIN be input incorrectly the node would stay locked the host informed of a failed withdrawal request and if it was the client who made a mistake the withdrawal process would have to be started again. This with luck should make it very hard for a validator or withdrawal Key to be misused.
14. Client waits for Epoch or Slot number to be processed and with luck at this point in time a successful withdrawal/skim has taken place.
15. Node goes back to default state of being “locked”.

It may seem laborious but by the time we get to phase 1.5 each node could have a value well in excess of $250,000 so in my view it is worth making the withdrawal process as secure as possible, which in effect renders the key useless without a PIN.

Of course this is just a rough idea and I am by no means an expert in blockchain, however I hope there are some steps that could be helpful to anyone like myself who sadly had an ETH 2 withdrawal key breached, a similar process could also be used for withdrawal key rotation, should a Staker wish to change the withdrawal key!

Thanks kindly for reading my post, I am ever so grateful for all your efforts and time.

Tobes

## Replies

**zilm** (2021-08-31):

I definitely don’t understand why loss of withdrawal key should be considered as the usual case. It’s not used during validator duties, so it’s cold-stored. It’s absolutely the same case when you lose the private key of your Mainnet account. The other question is: in the PoW network we could make multi-sig wallets etc, so, could we provide the same level of security for validator withdrawals? Yes, you will be able withdraw to any predefined Mainnet address (see [PR#2149](https://github.com/ethereum/consensus-specs/pull/2149)), so the receiver could be a contract with any security considerations implemented.

---

**TobesVibration** (2021-08-31):

“I definitely don’t understand why loss of withdrawal key should be considered as the usual case.”

Hi Zilm, thanks kindly for your reply, sorry to have posted here I was trying to find a way to contact you.

I completely understand what you are saying about considering the loss of the key a usual case, I am just desperate to find a solution for myself and others who sadly have had their private keys compromised.

If what I suggested above is not plausible, would it be possible to lock the node and only allow withdrawals to be made only from the server itself thereby refusing any external connection to make the withdrawal? I would happily trust the host to make the withdrawal and then transfer the funds back to me so I could reinvest into a new validator node, I do not wish to withdraw the funds but sadly am in a daunting situation.

I am sick to my stomach at the thought a thief is waiting for withdrawals to be activated and am desperate to find a solution, my wallet key was compromised at the same time as the withdrawal key ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=9)

I don’t know what the number of compromised keys is, but I know for sure it is not just me, and I think it would be devastating if our funds were stolen.

Is there a chance I could talk to you privately for a few minutes? I would pay for your time if needed, I just want to find a solution so I can put my mind at rest, the investment of the nodes was meant as an investment for my daughter, so I am terrified of the worst case scenario.

Thanks kindly for your time.

Tobes

---

**zilm** (2021-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/tobesvibration/48/7018_2.png) TobesVibration:

> If what I suggested above is not plausible, would it be possible to lock the node and only allow withdrawals to be made only from the server itself thereby refusing any external connection to make the withdrawal?

If ever made (though it’s really difficult to make something like this), it would play against thousands of users who are going to participate in shared pools and other forms of validator/investor separation, which should be at first place for wide adoption, less centralization and less number of big whales.

I would recommend you to join #withdrawal-methods channel in Eth R&D Discord for further discussions.

---

**TobesVibration** (2021-09-01):

Hi Zilm, Thats the best news I have heard for a while, it means there is hope, I would happily pay towards this development, it could be optional so if needed the lock could be enabled, if 100 people needed this and were prepared to pay 10k each towards this, we could raise $1m towards this mod?

I will go to #withdrawal-methods and with luck discuss this more, I will also talk to my host who may also be very interested in this who may me able to talk further with their contacts.

Thanks for giving me hope Zilm, sending you good vibes, peace & love xx

---

**benjaminchodroff** (2021-12-13):

I am happy to help fund this.

The #withdrawal-methods [@jgm](/u/jgm) has discussed the option of a social mechanism where validators could optionally provide a text file to request what withdrawal address to allow. My eth2 validator key is compromised (I took notes, and forgot I took them… I am very ashamed) and I would strongly prefer requesting that the only allowed withdrawal address should be my eth1 deposit address (which is not compromised).

I can still sign messages with both my eth1 deposit key and eth2 key. The attacker cannot.

---

**TobesVibration** (2021-12-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminchodroff/48/8085_2.png) benjaminchodroff:

> @jgm has discussed the option of a social mechanism where validators could optionally provide a text file to request what withdrawal address to allow.

Sorry to hear that Ben, I know how you feel but sadly its more common than you think, mistakes happen in all walks of life, don’t beat yourself up, let’s just pray ETH devs come to our rescue.

If what JGM suggested can be done server side, that sounds pretty cool, we just need to be able to block the hacker. I like that idea if its a .txt file that is included server side, previous discussions have suggested giving power to host’s could be problematic, but I still think its a better option than allowing a breached key to be used, and if a host did abuse such powers which I personally think would be commercial suicide for them, they could be held legally accountable if they abused such power and could be held accountable & outted publicly so others know they are not a trustworthy host. I know for sure my host would never screw their customers and want to help! I am guessing 99.9% would not risk their reputation.

Good luck! wagmi

---

**benjaminchodroff** (2021-12-13):

Thanks [@TobesVibration](/u/tobesvibration). I came into blockchain to learn, and I still am. I am a solo hoster for 10 validators, and happy to put any mechanism to work on my beacon nodes and validators, and help fund the effort to build this for the community. I need help, but want to help too.

Was your eth1 deposit address keys AND the key associated your eth2 validator address also hacked? If not, it seems a proposed idea could be to create a “validator_address.txt” file that contains something like this (I am not an expert, but just trying to help)

{

“eth1deposit_address”: “0x06f2e9ce84d5e686428d361d91b437dc589a5163”,

“eth1deposit_msg”: “0x455448322052657475726e20546f2053656e646572”,

“eth1deposit_sig”: “e1e393e6dd403e05b2f7d8e234d0dc226551b21f61fe9b655d7b1792d4bc2e955aeb04c3de876d044ac7d6b9bed505fb6bde47f83ea3dce96aae13067e7c519e1c”,

“eth2validator_address”: “0xa03c5ea17b017cfad22b6030575c4452f20a4737393de16a616fb0a8b0555fe66472765720abec97e8922680204d3866”,

“eth2validator_msg”: "0x5f24e819400c6a8ee2bfc014343cd971b7eb707320025a7bcd83e621e26c35b7 ",

“eth2validator_sig”: “0xa2965dfd099dd0e44535c443d90c3b38016e43283a5aec5c0c7c04e94af89c0878bbc18b9f3f1bd5428ddd319c5d296717f741ce0e24fbbce1ae8fa77ba4a9f015a611bddf58f713e9a7aff022b87964a66cc26c3e8388c3707b10cc2ced4974”

}

If you can prove both eth1 and eth2 custody, you should be the rightful owner AND the only allowed withdrawal address should be set to the ETH1 deposit signature - this makes a “return to sender” feature. We could then ask clients to support importing these text files, optionally. It may help prevent attackers from being successful in withdrawing when enough beacon nodes start rejecting fraudulent withdrawals or change address to other address.

---

**jgm** (2021-12-13):

Worth expanding a little on the Discord post, and explaining what this suggestion is and what it is not.

The idea is to allow some way to provide a social consensus system that restricts the “change withdrawal credentials” operation for a given set of source withdrawal credentials to only be considered valid if they have a specific target withdrawal credential.

The change withdrawal credentials operation is not yet fully specified, but is likely to have at least the following fields:

- validator index
- current withdrawal public key
- proposed (execution layer) withdrawal address
- signature by withdrawal private key over prior fields

In a situation where multiple users have access to the withdrawal private key it is impossible for the network to differentiate the “legitimate” holder of the key from the “illegitimate”.  However, there are signals that could be considered in a wider sense.  The most commonly cited one is that the legitimate holder is also in control of the execution layer deposit address, in which case the suggestion is to require the proposed withdrawal address to match the deposit address.  This is not something that can be enforced in-protocol, partly due to lack of information on the beacon chain about the deposit address and partly due to the fact that this was never listed as a requirement so it is possible that deposit addresses will no longer be under the control of the legitimate holder of the withdrawal private key.  But it may be possible for individual nodes to locally restrict the changes they wish to include in blocks they propose, and which they propagate around the network.

The proposal is as follows: beacon nodes take an additional parameter pointing to a file.  That file contains multiple lines of the format `withdrawal credentials,withdrawal address` where each line is a restriction on the contents of withdrawal change operations.  Specifically:

- if a node is presented with a withdrawal change operation via the REST API it will reject it if there is a line in the file that contains a matching withdrawal credentials and the related withdrawal address does not match that in the operation
- if a node is presented with a withdrawal change operation via P2P it will drop it if there is a line in the file that contains a matching withdrawal credentials and the related withdrawal address does not match that in the operation

Note that these restrictions do *not* apply to withdrawal credential change operations in blocks.  If an operation has been included on-chain it is by definition valid regardless of its contents.

It is critical to understand that this is not a consensus change.  Nothing in this proposal restricts the validity of withdrawal credential change operations within the protocol.  It is a voluntary change by client teams to build this functionality in to their beacon nodes, and a voluntary change by node operators to accept any or all of the restrictions suggested by end users.

Because of the above, even fully implemented it will be down to chance as to which validators propose blocks, and which voluntary restrictions those validators’ beacon nodes are running.  Node operators can do what they will to help, but there are no guarantees of success.  Those who wish to put time and resources in to building this or any similar proposal should be remain aware of this fact at all times.

I hope that I have made it clear that this is very much a voluntary effort on the part of all involved.  I don’t see this being driven by anyone in the core dev team, as their focus will rightly be elsewhere.  Those that are affected by this situation will need to organize and at the least get together a plan for doing the following:

- formalize the above in to a clear proposal of exactly what they want from client teams and node operators
- approach the client teams regarding the feasibility of them doing the required work
- approach the major node operators (i.e. staking services) regarding their requirements for adding entries to the list
- build a list, with relevant proofs as required by the major node operators

The good news here is that the community as a whole will want to help those who have genuinely lost control of their withdrawal keys.  But there will no doubt be contentious issues along the way, not least the general premise of what I am suggesting above.  Again, at this point I suggest that those affected organize early and so are ready to present their best case to the client teams once they start to look at the capella hard fork.

(And for the record: I am not in the situation described above.  I’m outlining this because it is the result of various conversations had on Discord and elsewhere with affected parties, and as an attempt to help them find a resolution.  Equally, I am not championing or endorsing this proposal; that is up to those affected.)

---

**TobesVibration** (2021-12-13):

Hi Jim, I am super grateful for your input and that also of Ben.

Ben, I am willing to do whatever I can to help, sadly I am not a coder, I have worked in Web for years HTML, CSS, SEO etc and have dabbled with Object-oriented Java programming and a tiny bit of PHP, but in fairness am a bit lost with blockchain, but will still do anything I can to help. I will pass this link to a friend later who has some underlying knowledge of building on Ethereum so he may be useful and may be able to help, would it be worth opening a private chat on Telegram?

I must confess that I fell for a scam on Telegram so since then I have been super wary of using the app, but somewhere to talk might make sense, or maybe we could start a new thread somewhere here where devs won’t get pinged all day long? I have access to a server so could setup a forum if that helped?

Let me know what you think Ben, I myself would be eternally indebted to you if your able to help find a solution, I am grateful that Jim has given some guidance as my efforts to find a solution did not go far as Jim has said Core Devs are too busy to get involved with this, and sadly to implement this fix we would need the community to agree I believe?

Let me know what I can do to help and I will do everything I can.

Tobes

---

**pietjepuk** (2021-12-13):

If I understand [@jgm](/u/jgm) 's proposal correctly, the file should *only* contain entries of people known to have been targeted.

I would instead propose that the file contains *all* `withdrawal credentials, (first) deposit address` combinations [0]. This would prevent:

- what I think will be a difficult process of targeted validators signing up to some centralized list [1]
- the “withdrawal address” of this centralized list not actually being the deposit address. [2]

With the assumption that clients locally cache 0x00 → 0x01 messages they see, and can/will have an eviction policy for conflicting one, my proposed process is something like:

- run a script against your local EL to generate the txt, or download it through some centralized service
- (indifferent to REST API. Could be no special action, could be to enforce a match with the txt file [3])
- only rebroadcast P2P messages if it’s a credential change message for a validator that (1) is not yet in your storage or (2) already in your storage, but the message is different from the one you stored and its 0x01 credentials match those of the json/txt file. Of course in case 2 also overwrite whatever you have in storage.

The same “this is not part of consensus” restrictions/disclaimers apply as in [@jgm](/u/jgm) 's proposal.

Also note that this proposal can be complementary to that of jgm, e.g. usable as a fallback method.

[0] Or only for 0x00 withdrawal credentials, as it doesn’t make much sense for 0x01. But them being in there as well doesn’t hurt.

[1] There’s also the thing of them maybe not wanting to announce they have been compromised, or think they have been compromised. Although the former case will come out eventually of course.

[2] If we can let people generate or verify a txt/json file locally against their own EL, that would address this particular issue.

[3] Enforcing a match is good for people that are somewhat uncertain they will correctly enter their withdrawal address to be their original deposit address I guess. Not sure it offers much over double-triple-quadruple checking it though, and it hinders those who want a different withdrawal address.

---

**benjaminchodroff** (2021-12-13):

Greatly appreciate [@jgm](/u/jgm) guidance

[@TobesVibration](/u/tobesvibration) Contact me on telegram - my name is violinvivaldi. Let’s discuss ideas, and make a plan. What we need most is a simple document of the plan, and then allow submitters to upload their evidence to a repository such as github. We then need to contact the clients and staking pools to support this plan and show verifiable evidence and convince them to use it.

This isn’t just a feature for compromised users. If anyone used eth2cli before v1.2, we didn’t get an option to set --eth1_withdrawal_address. This feature may provide users one last chance for any reason to try to set a correct address (I would have definitely used this feature if I had it), and beg the validators to accept the facts before it is immutably recorded to the chain.

---

**jgm** (2021-12-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminchodroff/48/8085_2.png) benjaminchodroff:

> This isn’t just a feature for compromised users. If anyone used eth2cli before v1.2, we didn’t get an option to set --eth1_withdrawal_address. This feature may provide users one last chance for any reason to try to set a correct address (I would have definitely used this feature if I had it), and beg the validators to accept the facts before it is immutably recorded to the chain.

The normal (proposed) operation of the change credentials operation will cover the above situation (and indeed is its whole purpose).

---

**benjaminchodroff** (2021-12-14):

Are you suggesting the (proposed) operation that to do a withdrawal change it would require BOTH the original eth1 credentials (which I am *certain* my eth1 key has not been compromised) AND my eth2 mnemonic (which I am *certain* my eth2 seed phrase and 10 keys have all been compromised)?

Will we be allowed withdrawal address changes before withdrawals are allowed? This would give me ample time to fix the problem before any attacker withdraws by setting my 0x00 withdrawal addresses to a new 0x01 address.

If the withdrawal address change only requires ETH2 signature, or if the withdrawal change can only happen after withdrawals are also allowed, then I am afraid I am going to have to compete in the race against a very sophisticated attacker group. It appears the group came from a compromised GPU mining program I recently installed which used a command control malware to find its way into my NAS where the note and keys were accidentally stored (the mnemonic was never meant to be saved on a computer).

---

**jgm** (2021-12-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminchodroff/48/8085_2.png) benjaminchodroff:

> Are you suggesting the (proposed) operation that to do a withdrawal change it would require BOTH the original eth1 credentials (which I am certain my eth1 key has not been compromised) AND my eth2 mnemonic (which I am certain my eth2 seed phrase and 10 keys have all been compromised)?

The operation will only require the withdrawal private key, which is derived from the mnemonic.

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminchodroff/48/8085_2.png) benjaminchodroff:

> Will we be allowed withdrawal address changes before withdrawals are allowed? This would give me ample time to fix the problem before any attacker withdraws by setting my 0x00 withdrawal addresses to a new 0x01 address.

As it stands, credentials will have to be changed before a withdrawal can take place.  But this doesn’t buy you any time, as the attacker can change the at the same point in time as you.

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminchodroff/48/8085_2.png) benjaminchodroff:

> …I am afraid I am going to have to compete in the race…

Yes, you are.  As mentioned above, there is no way that the protocol can differentiate between you and the entity that took your mnemonic.  This is the reason why I’m proposing a social consensus system where you could can do the work in advance.

---

**benjaminchodroff** (2021-12-14):

Got it. Let the race begin. Thank you, again. I will start documenting the social mechanisms outlined for those of us impacted/suspected impacted to plea for validator help to consider in a github project. The list will be manually moderated, but independently verifiable. I don’t think I can help anyone who lost their keys or seed, but for those of us compromised or concerned they may be, it may help give an edge.

---

**3eph1r0th** (2022-01-11):

Hi. I am the founder of Allnodes. We host a lot of Ethereum 2.0 nodes and I have met a lot of people who exposed their keys to scammers and even who completely lost access to their withdrawal keys. I am sure that we should help these people.

Solution that I propose:

You can execute transaction to change withdrawal credentials from these wallets:

1. Initial deposit address (this transaction can be reverted using current withdrawal address and withdrawal key can be changed only to initial deposit address).
2. Current withdrawal address (this transaction cannot be reverted, but withdrawal key can be changed only to initial deposit address).

Because of possible revert option these transactions should be possible to execute long before withdrawals are enabled.

Whom this solution will help:

1. Those who lost access to their withdrawal keys.
2. Those who’s withdrawal keys were breached.

Thank you for your time.

---

**TobesVibration** (2022-01-12):

Hi Seph and Allnodes team,

It is wonderful of you to have joined the discussion. Many thanks. However I am thinking you may have scrolled back in our chat at [allnodes.com](http://allnodes.com) and clicked an old link, I did send you a link via email to a GitHub proposal where this topic has been worked on significantly since this thread. I have sent you the link again via the [allnodes.com](http://allnodes.com) chat. I hope you can find the time to check it out as it will probably answer many questions you may have, and with luck the Devs and yourself can continue the discussion on the Discord group which I will ask [@benjaminchodroff](/u/benjaminchodroff) to pass you/me an invite that I can pass to you.

I am super grateful you made the effort to chime into the discussion, when you read the GitHub proposal I think you will see the Devs have come up with something quite special. Consensus Layer Withdrawal Protection.

My understanding is the EIP needs to be reviewed and there is still chance for some changes. It is a very important proposal, and sounds like you agree it could potentially save hundreds of millions of $ of ETH.

Thanks kindly for taking a look and your help.

Tobes

---

**benjaminchodroff** (2022-01-13):

[@3eph1r0th](/u/3eph1r0th) Really appreciate your support from Allnodes. I fully agree that there are many users who are either aware or even unaware their validator mnemonic has been compromised.

I have documented the suggestions from the developers into a draft proposal, which covers your suggestions. None of the proposal changes consensus. Instead, we have suggested mechanisms which favors (not guarantees) legitimate users can likely win through voluntary node operator behavior. This includes using Initial Deposit Address as a tiebreaker for any race conditions, asking clients to voluntarily delay rebroadcasting change addresses which do not match the deposit address, filter rebroadcasting messages which do not match the intended signed change withdrawal address, and providing a mechanism to broadcast signed change address messages to any address on the first available block.

Draft Proposal:



      [github.com](https://github.com/benjaminchodroff/ConsensusLayerWithdrawalProtection/)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/8/8/882ac597a9c8e3a5e7bac7e30f3a57c9608b2170_2_690x344.png)



###



Contribute to benjaminchodroff/ConsensusLayerWithdrawalProtection development by creating an account on GitHub.










I am now working to rework this proposal into the EIP template, review with Ethereum Cat Herders for feedback, and get more developer feedback. I hope to eventually create a client which demonstrates these ideas in action. If anyone can point me to a client codebase which already supports the change withdrawal address operation, I will try to make a pull request against it.

Anyone can reach out to me via github, or my discord is [@benjaminchodroff](/u/benjaminchodroff)#5260. I appreciate any feedback and help.

---

**benjaminchodroff** (2022-02-04):

I have submitted an EIP pull request: https://github.com/ethereum/EIPs/pull/4736

Ongoing EIP discussion will happen here: [Consensus Layer Withdrawal Protection - EIPs - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/consensus-layer-withdrawal-protection/8161)

I appreciate any help or feedback.

---

**Tex419** (2022-11-30):

Hey [@benjaminchodroff](/u/benjaminchodroff), it’s almost a full year after you posted this reply and I’m stuck in a similar situation as both my eth1 Deposit address keys and the eth2 validator address are compromised. I have messaged you on your website and on LinkedIn as well so please excuse my persistence as I’m very stressed out over the threat of losing my 32eth stake. I’m doing the best I can to educate myself on EIP-4736 and any other related topic but I’m not really sure how to proceed. I want to ensure I beat the hackers to the withdraw when they are finally enabled. I may be at a disadvantage because I have no prior coding experience (I’m using a Plug & Play validator). Is there anything I can do now to prepare myself in the race for my staked eth?


*(39 more replies not shown)*
