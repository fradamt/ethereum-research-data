---
source: ethresearch
topic_id: 1301
title: Conditional proof of stake hashcash
author: vbuterin
date: "2018-03-04"
category: Applications
tags: []
url: https://ethresear.ch/t/conditional-proof-of-stake-hashcash/1301
views: 24601
likes: 17
posts_count: 20
---

# Conditional proof of stake hashcash

**Updated 2018.04.04: see bottom**

This is a writeup of an idea that I introduced at the meetup in Bangkok here: https://youtu.be/OOJVpL9Nsx8?t=3h24m51s

Proof of work was proposed in the 1990s originally as a form of email spam prevention by Dwork and Naor [here](http://www.hashcash.org/papers/pvp.pdf). The idea is that a user’s email client would only show emails that come with a proof of work nonce `n` attached, such that `n` is the solution to some math problem based on the contents of the email; in Adam Back’s hashcash it could be simplified to hash(email\_message + n) < \frac{2^{256}}{D}, where D is a difficulty parameter. This requires all email senders to do a small amount of computational work to send an email that the recipient will read, with the hope that legitimate users (who have a high valuation for the ability to send an email) will be willing to do this cost but spammers (who have a low valuation) will not.

The problem is that (i) there’s an imbalance in favor of the spammers, as specialized implementations can do proof of work better than regular users (not to mention smartphones), and (ii) it turns out the happy medium that’s low enough for users and too high for spammers does not really exist.

But we can improve this approach using proof of stake! The idea here is that we set up a smart contract mechanism where along with an email the recipient gets a secret key (the preimage of a hash) that allows them to delete some specified amount (eg. $0.5) of the sender’s money, but only if he wants to; we expect the recipient to not do this for legitimate messages, and so for legitimate senders the cost of the scheme is close to zero (basically, transaction fees plus occasionally losing $0.5 to malicious receivers).

The contract code might look like this:

```python
deposits: public({withdrawn_at: timestamp, size: wei_value, creator: address}[bytes32])

@public
@payable
def make_deposit(hash: bytes32):
   assert self.deposits[hash].size == 0
   self.deposits[hash] = {withdrawn_at: 0, size: msg.value, creator: msg.sender}

@public
def delete_deposit(secret: bytes32):
   self.deposits[sha3(secret)] = None

@public
def start_withdrawal(hash: bytes32):
    assert self.deposits[hash].creator == msg.sender
    self.deposits[hash].withdrawn_at = block.timestamp

@public
def withdraw(hash: bytes32):
    assert self.deposits[hash].withdrawn_at <= block.timestamp - 3600
    send(self.deposits[hash].creator, self.deposits[hash].size)
    self.deposits[hash] = None
```

An email client would check that a deposit is active and a withdrawal attempt has not yet started. Individual recipients could also demand that the secret key they receive has some properties (eg. containing their own email address at the beginning), thereby preventing reuse of the same secret key among multiple users.

---

Optimizations:

1. If a sender needs to send multiple emails at a time (eg. a group email, or a legitimate newsletter), they could publish a Merkle root of the secret keys, and give each recipient a Merkle branch of their secret.
2. If you don’t want the sender to know if any individual recipient punished them, then you could have a game where all senders put in $0.5, by default have a 50% chance of getting $1 back, but if the recipient wishes the chance the sender will get $1 back drops to 0%. This can be done by requiring the recipient to pre-commit to a list of N values, then for each email, after some time passes and a block hash becomes available as random data, the recipient would normally see if the value they committed to for that email has the same parity (even vs odd) as the block hash, and if it is they would publish it and unlock the sender’s double-deposit gain. If a recipient has a grudge against the sender, they could simply never publish the value regardless of parity. It would be expected as a default that the committed values are deleted as soon as they are used, so that recipients could not be forced to prove how they acted.

**Update 2018.04.14**:

This could also be used for paywalled content services: a user needs to pay to access the content, but at the end the user can choose whether the funds go to the author or to charity. This removes perverse incentives in existing paywalls (eg. [yours.org](http://yours.org)) where it’s in writers’ interest to put their best content before the paywalled portion of a post begins in order to advertise it; with this scheme, unhappy writers could deny authors their revenues after being disappointed with the initially hidden portion of a piece.

Suggestion from [@danrobinson](/u/danrobinson): another option is that if a user dislikes a piece of content, the funds paid by the user go into a pool which refunds all previous users (ideally only previous users, to avoid making the content cheaper and thereby perversely more popular). This increases the scheme’s “efficiency” (users and writers don’t find it in their mutual benefit to switch to a platform that helps both keep their money more) as well as its “fairness” (if everyone finds that some piece of content sucks, then everyone gets most of their money back).

## Replies

**EazyC** (2018-03-05):

I watched your entire presentation at Bangkok and found both the email portion and the content curation very interesting. But the main portion I wanted to comment about isn’t the email implementation, but the content implementation where you talked about Twitter scammers. The idea is clearly the same pos hashcash but for social media messages than emails. The main issue in this whole situation is what happens in highly contentious situations?

Won’t the primary incentive in those situations be to stay away from voting since there is a good chance they will lose their stake? Or even worse, to vote on what they think might win rather than what they believe the common, salient reality to be? This mainly applies to situations where it is not very clear if something is a scam/spam and it is very close to 50/50 upvotes and downvotes. For example, say there is a decentralized Wikipedia where people stake up or downvotes on edits but the edit is not clearly vandalism but instead highly controversial - not necessarily false. Or let’s say a tweet that is highly controversial that is getting around 50/50 upvote and downvotes.

In those situations, it might be a complete crapshoot what the “reality” ends up being so it could highly discourage participation since people might be afraid to participate. But ironically, those situations are the most important ones for people to participate in since they are the most contentious and markets could help. What mechanisms could be implemented to solve those scenarios? Perhaps locking the voting results from being seen until a round is complete?

---

**vbuterin** (2018-03-05):

> Or even worse, to vote on what they think might win rather than what they believe the common, salient reality to be?

Yes. But remember that the prediction market is not self-referential; it’s not like a system where those who vote the majority get the coins of those who vote the minority. Rather, it’s a prediction market for what some underlying moderation DAO would vote for. This moderation DAO could for example be 20 judges elected by DPOS by the token holders of the system, or some other mechanism. If the moderation DAO is itself corrupted, then users will stop caring about what it says, and what the prediction market for it says, and everyone will switch to a different moderation DAO that is not corrupted.

---

**nootropicat** (2018-03-06):

The profit-maximizing thing to do is to demand a ‘reasonable’ sum smaller than the penalty as payment for not deleting. This could be easily automated. Even if somehow genuine receivers would never to do that, if popular, it would create a new type of ransomware in which users are encouraged to send messages to false addresses.

The problem isn’t with messages, but with accounts. If accounts were hard to get spammers would be trivial to eliminate after a while. Perhaps something like being able to send messages only from an account connected to an eth address with 1 eth that’s at least X days old. This could be done in a zk way to avoid connecting the specific account to a separate identity.

---

**vbuterin** (2018-03-06):

> The profit-maximizing thing to do is to demand a ‘reasonable’ sum smaller than the penalty as payment for not deleting. This could be easily automated.

Not convinced; acquiring a reputation for succumbing to blackmail is very risky. Standard email software would not include a “pay blackmail” feature, and it’s not worth it to individually negotiate with users over $0.25. If users *do* find even losing $0.50 uncomfortable, then the penalty could be reduced further; the intent is that only sending large quantities of undesired emails should be painful.

---

**nootropicat** (2018-03-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Standard email software would not include a “pay blackmail” feature, and it’s not worth it to individually negotiate with users over $0.25

If users can deposit money in a smart contract, even with the built-in support, they have the ability to send money for ransom.

No individual negotiation just like with most ransomware, instead picking an amount that’s expected to maximize profits. With sufficient scale it’s only a matter of binary search assuming monotonicity. It could be trustlessly automated by making a smart contract that’s only payable if the original deposit isn’t deleted.

In any case I can’t imagine many people willing to pay something to send. For one thing this eliminates all people with low confidence as they’re going to ask themselves if what they wanted to write won’t be considered spam and write nothing. What if you have to write a mail that’s likely to make the other side seriously angry? Almost guaranteed loss.

In general it’s lot of hassle for unclear benefit, in my experience spam filters are very effective as of now.

Is email spam an actual problem for you?

---

**vbuterin** (2018-03-07):

> In general it’s lot of hassle for unclear benefit, in my experience spam filters are very effective as of now.

They are, though at the high hidden cost of letting Google read your email, and making it much harder to spin up a new competitor in the email space, or even for existing providers to make their email end-to-end encrypted.

> In any case I can’t imagine many people willing to pay something to send.

People were willing to pay $1 to send mail 30 years ago. Here it’s just a usually small risk of paying something, and the payment could be much smaller. If $0.50 is too high, then it could be something like $0.10, or more generally an amount of ETH equal to what you would pay to send 10-50 transactions.

---

**MicahZoltu** (2018-03-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/nootropicat/48/258_2.png) nootropicat:

> In any case I can’t imagine many people willing to pay something to send.

I would gladly pay some number of pennies per email sent if it meant that I knew spammers had to pay the same.  The key is picking a price point that is low enough that it would never influence my decision to spend, but will always influence a spammers decision to send.  For example, at $0.01 I would never *not* send an email because of cost, but maybe that is high enough that a spammer would see it as prohibitively expensive?

The problem is that such a system doesn’t interface with the legacy email system, so I would need to get everyone who wanted to communicate with me to move over to this new system.

---

**kladkogex** (2018-03-09):

I think Vitalik is correct that the probability of people forming syndicates for blackmailing etc. will be low, and even if blackmailing starts, one could easily design a bit more complex protocol to prevent blackmailing.

Imho the real problem in this architecture is that email recipients will not have any gas to pay for the slashing call.  Even if a shard or a plasma chain is used so the amount of gas is tiny, most of email recepients will have no ETH accounts, and even if they do have ETH it will be too much hassle for them to provide access to the wallet etc.

A solution to this is to provide an ability for self-paying accounts coupled with an  ability for  user to provide PoW in lieu of gas.  This was already proposed this during the discussion of account abstraction. Essentially the user will do PoW and provide a PoW proof during the transaction submission.  The contract will have an ETH reserve for gas payments. The gas available to a particular transaction will be proportional to the PoW submitted by the transaction.

Overall, the solution, if it works, maybe a worthwhile theme for a startup …

---

**dlubarov** (2018-03-09):

[@kladkogex](/u/kladkogex) that sounds like a useful feature, as long as it’s rarely/never profitable for miners to do PoW just for the gas fees. Not a huge problem but the gas/PoW rate would be adjusted periodically.

Theoretically the problem could be solved by sharing the private key to a small separate account, right? But I realize the overhead would be substantial (around $.10 currently?).

A more radical alternative would be to introduce a PAYGAS opcode, let any account involved in a transaction to contribute to gas costs, and then not require transactions to be signed; it would be up to each account’s code to decide what signature(s) to require if any. Obviously a huge change though, and mitigating DoS attacks with invalid transactions would be extra challenging.

---

**vbuterin** (2018-03-10):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Imho the real problem in this architecture is that email recipients will not have any gas to pay for the slashing call.

We can use a layer-2 incentivization protocol to solve this; third parties can include the secret key in a transaction on chain and get paid a small amount for it to cover gas. The sender would just need to publish the secret key.

---

**AnthonyAkentiev** (2018-03-15):

Awesome. I really hope that tokenized systems will solve spam problem.

The payment-based anti-spam was suggested long above, but now we have a blockchain technology that can really solve it.

“Bill Gates announced that Microsoft is working on a solution requiring so-called “unknown senders”, i.e. senders not on the Accepted List of the recipient to post “the electronic equivalent of a” stamp whose value would be lost to the sender only if the recipient disapproves of the email.[1] Gates said that Microsoft favors other solutions in the short-term, but would rely on the contingent payment solution to solve the spam problem over the longer run. Microsoft, AOL as well as Yahoo! have recently introduced systems that allow commercial senders to avoid filters if they obtain a paid or pre-paid certificate or certification, which is lost to the sender if recipients complain.”

---

**rumkin** (2018-03-15):

This is good idea but… Companies today are ready to pay for advertisement much more money than people could pay as non-spam guarantee. When company know who you are they will pay a lot of money to buy your attention. So popular people will became victims of high payment attacks.

Also it makes communication progress more aggressive and make communication initiator an subordinate. Communications should be free and fast. This is what information era brings to us. And payment based communication can roll us back to stone age. The first thing what we should to do is to specify spam types such a mass mailing, unwanted content, fakes and other. Hashcash-like solutions can limit unwanted content with high fees.

I think the solution should not limit regular users and should to provide instruments to identify honest users and to separate them from spammers. There is existing social filter which is based on friendship, same interests, common activities, professional links and so. We can reproduce it. And It might be handshaking based algorithm with public profile (visit cards) exchange as the first level and optional hashcash.

---

**MicahZoltu** (2018-03-16):

[@rumkin](/u/rumkin) The problem being solved isn’t targeted advertising, where the conversion on marketing is high.  The problem being solved is spam advertising where the advertiser send out millions/billions of emails and get zero to one conversion off of it.

One can imagine that a company with a 100% conversion rate is actually *helping* customers it advertises to because it is making them aware of a product that they didn’t know existed but ended up wanting.  On the other extreme, a company with 0% conversion rate is just annoying everyone.  All marketing schemes are on this spectrum, and increasing the cost per impression results in companies moving towards the 100% side of this spectrum.

---

**vbuterin** (2018-04-14):

Updated today:

> This could also be used for paywalled content services: a user needs to pay to access the content, but at the end the user can choose whether the funds go to the author or to charity. This removes perverse incentives in existing paywalls (eg. yours.org) where it’s in writers’ interest to put their best content before the paywalled portion of a post begins in order to advertise it; with this scheme, unhappy writers could deny authors their revenues after being disappointed with the initially hidden portion of a piece.

> Suggestion from @danrobinson: another option is that if a user dislikes a piece of content, the funds paid by the user go into a pool which refunds all previous users (ideally only previous users, to avoid making the content cheaper and thereby perversely more popular). This increases the scheme’s “efficiency” (users and writers don’t find it in their mutual benefit to switch to a platform that helps both keep their money more) as well as its “fairness” (if everyone finds that some piece of content sucks, then everyone gets most of their money back).

---

**burrrata** (2018-10-16):

edit: replying to original post

If ANY message can have it’s stake burned, what would stop someone from abusing opt in systems like email newsletters?

- Honest Bob has an email newsletter that people like and opt in to receive
- Eve does not like Bob’s email newsletter
- Eve subscribes random people to Bob’s newsletter and they flag the incoming messages as spam causing financial loss for Bob

Potential solution: initially cooperative tit-for-tat mechanism. By default, initial cold emails are allowed without slashing (unless the user changes this to a more private account). When receiving an email from a new sender the recipient has an option to add the sender to a white list, a neutral list, or a black list. The sender is notified of the recipients choice in order to respond accordingly:

- white list (friends and contacts): everything’s good and they can communicate in the clear
- neutral list (newsletters, product purchases, etc…): messages will be evaluated on a message by message basis. This means that the recipient is open to receiving emails, but… if they don’t like a message (say I buy a product or sign up for a service but then they send me stuff about product upsells or ICOs), then the recipient can choose to slash the stake on the message. This way, if the sender plays nice and sends quality content, then the receiver will most likely also play nice, and if not then there are consequences. This also might, maybe… incentivize marketers to craft more thoughtful and less spamy emails (I doubt it, but one can dream).
- black listed (spam/bad): they will be blocked and any attempted further correspondence will result in an immediate burning of the stake for that message

This would obviously be vulnerable to an attacker keeping a (marketing/spam) list of emails/accounts and then spinning up new email addresses or new accounts on social media to take advantage of the free 1st message feature, however, people already do this whenever accounts/addresses get blocked. While this proposal is only a mild improvement upon the current situation, it has no downside for the receiver and is a step towards putting more power in the hands of the user. It also creates financial penalties for repeat spamming making it more costly (time and money) for spammers to spam.

You could also implement this more strictly as a protocol that requires an initial handshake/hello message for ANY correspondences where both sides need to opt in to continue further correspondence. This could be an additional feature on emails or social media accounts that you can enable in settings (just like you can often set an account to private/friends only or to receive messages only from people on your contacts list), but where there are additional financial consequences beyond just being blocked or having messages go to a spam/archive folder.

---

**burrrata** (2018-10-16):

edit: replying to [@vbuterin](/u/vbuterin) in regards to update regarding paywalled content

What if you had a contract that refunded customers based on the satisfaction of other customers?

- N total customers, where S are satisfied and D are dissatisfied.
- If D customers want a refund at any time they can redeem D/N * A, where A is the amount a dissatisfied customer paid for a product/service.
- If you are a satisfied customer, you can publicly state this fact in a review (verified by your purchase) and receive a discount for future purchases or some other promotion/benefit.

If you’re an early adopter or trying something new, and the product/experience sucks, you can wait until more people agree with you and then claim a higher refund. This could be programmed at the time of purchase in order to “set it and forget it”. You could also build in provisions such as: after the first X customers, if D>S, all customers get a refund proportional to D/N * A.

This also means if you’re trying to scam a great product, you’ll only receive a very small portion of your initial purchase as most people would disagree with you and D/N would be very small.

While this mechanism would incur some costs to the business, they could be rolled into the marketing/promotional budget as real reviews that are verified are 10X more valuable than crowdturfed Yelp reviews.

To attack the system an attacker would have to actually put down a payment and participate in the mechanism. This could create reputation damage via fake reviews and negative signaling, but at a financial cost to the attacker. Unfortunately, the cost of this attack is trivial for a well funded attacker who would get the majority of their money back if they can overwhelm the system and make D ~= N. Since any attack where D < ~N would be quite expensive, it’s likely that attackers would go after targets they feel confident they can overtake, or else choose to forgo the attack altogether. This at least reduces the attack surface of businesses that could be affected, although sadly this would skew attacks towards smaller/newer entities which are more vulnerable. That being said, this already happens every day because it’s hilariously cheap to attack businesses on yelp or google maps. Any step towards increasing the difficulty of crowdturfing attacks is a plus. This would also be much harder if the business only accepted payments in person like at a coffee shop, or if there was a way to verify identity in addition to verifying the purchase.

If viable, this could potentially be applied to paywalled content, kickstarter campaigns, new movies, yoga classes, coffee, dinner, anything. If the business has a great product that people love (and paid for), they can undeniably prove it, creating a positive signal and generating more sales. If it’s poor product or scam, people will find out quickly, get partially refunded, and the evidence will be undeniable. This reduces downside risk for consumers trying new things and sends strong signals about quality products/businesses.

Open Problem: creating a mechanism that completely prevents online sybil attacks from well funded attackers. I’m thinking that identity verified via a socially network of trust/believably might help, but then that introduces a chicken/egg problem where you have to do stuff to establish reputation but you also have to have reputation to create interesting mechanisms that allow you to do more interesting stuff (assuming you want a native experience that doesn’t rely on a web2/gov KYC bridge to establish web3 identities). I imagine that there are other directions with solutions that I’m unaware of too though. Did I miss anything here and what would you recommend as a direction for further research? Thanks

---

**vbuterin** (2018-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/burrrata/48/3692_2.png) burrrata:

> If ANY message can have it’s stake burned, what would stop someone from abusing opt in systems like email newsletters?

Opting into a newsletter would entail adding a filter that allows messages from that address to be seen even if they do not come with a deposit.

This is actually a really good equilibrium, as it puts the newsletter whitelist into the user’s hands and if a user removes something from their whitelist the newsletter would have no way of getting around that without risking a deposit (unlike the status quo where users hitting “unsubscribe” often just confirms to spammers that their email is still a useful one to send junk to).

> What if you had a contract that refunded customers based on the satisfaction of other customers?

That seems like an interesting approach too!

---

**burrrata** (2018-12-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What if you had a contract that refunded customers based on the satisfaction of other customers?

That seems like an interesting approach too!

Here’s another variation using public voting and reviews.

Currently, we get bombarded with marketing trying to capture our attention and make want to buy things, and this is followed by various rating and review systems that are often created by the same platforms that are trying to sell us stuff in the first place. This is noisy, heavily biased, and subject to manipulation; everyone wants to say their thing is the best thing and they have no reason to tell you otherwise. The real information comes **after** people buy, but most people don’t have that information when making the purchase decision, so they either don’t do it or often have regrets. If you want to try something new you take the risk ¯\*(ツ)*/¯

What if we had a system where the producer AND the user rate the product, and if the user’s ratings are not in line with the producer’s ratings, users get a discount for current or future purchases? It’s a win/win because then people will be incentivized to try and buy more stuff, and producers will be incentivized to produce better stuff. It also greatly increases the cost/burden of purchased reviews (positive or negative).

For example: if you’re a band who does live performances, and you think your show is great and people will love it, rate your show X out of 10 stars. If fans disagree, offer them a refund proportional to the delta between your opinion and their opinion. This would incentivize artist/brands to make the best stuff possible because that way they get rewarded more in the form of money and positive marketing, but it also incentivizes the fans/consumers to try out new things even if there’s a risk they don’t like it. Only people who purchased a product can leave reviews, and they are incentivized to do so either by social pressure if reivews are public and/or by economic incentivizes in the form of a refund if they were dissatisfied or a discount on future purchases if they were satisfied.

I currently see this in 2 flavors, basic and keynesian, but I’m sure there are many more:

- Basic: X is your self assessed star rating, if people feel like your show/thing was less than X give them a refund proportional to the difference (say 10% per star or something), and if they feel like the value received was greater than X they can leave a tip and/or get a coupon for a future purchase.
- Keynesian: X is your self assessed star rating, if people think that it was less than X they would receive a refund proportional to the other people who also thought it was less than X, and if people thought something was greater than X they would be encouraged to tip an amount proportional to the amount of people who also felt that way.

Regarding attacks to this system, it’s not perfect and would not scale to something as important as elections or health care, but neither would Yelp or Amazon reviews. This is intended to reduce the surface area of crowdturfing attacks from 24/7 online everywhere to verified users who are socially and economically incentivized to create signal rather than noise. For may usecases that would be a great improvement. The system can still be attacked, and there are many many ways to do so within and beyond the protocol described, but I think the cost of doing so would be higher than the systems in use today. Happy to talk about said attacks though, so please let me know what you think! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Inspired by ideas from these blog posts:

- Gabe The Bass Player: Show Rating
- Charity Through Marginal Price Discrimination: https://vitalik.ca/jekyll/general/2017/03/11/a_note_on_charity.html
- and of course this thread: Conditional proof of stake hashcash - #18 by vbuterin

Initial (and evolving) sketches of the system can be found here:

- https://github.com/burrrata/research

---

**vaibhavchellani** (2020-04-17):

We have started work on a variant of this.

Read more: https://hackmd.io/@n2eVNsYdRe6KIM4PhI_2AQ/rkiV79oDI

