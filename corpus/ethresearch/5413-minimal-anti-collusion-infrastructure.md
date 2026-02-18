---
source: ethresearch
topic_id: 5413
title: Minimal anti-collusion infrastructure
author: vbuterin
date: "2019-05-04"
category: Applications
tags: []
url: https://ethresear.ch/t/minimal-anti-collusion-infrastructure/5413
views: 34268
likes: 66
posts_count: 26
---

# Minimal anti-collusion infrastructure

For background see https://vitalik.ca/general/2019/04/03/collusion.html

Suppose that we have an application where we need collusion resistance, but we also need the blockchain’s guarantees (mainly correct execution and censorship resistance). Voting is a prime candidate for this use case: collusion resistance is essential for the reasons discussed in the linked article, guarantees of correct execution is needed to guard against attacks on the vote tallying mechanism, and preventing censorship of votes is needed to prevent attacks involving blocking votes from voters. We can make a system that provides the collusion resistance guarantee with a centralized trust model (if Bob is honest we have collusion resistance, if Bob is dishonest we don’t), and also provides the blockchain’s guarantees unconditionally (ie. Bob can’t cause the other guarantees to break by being dishonest).

## Setup

We assume that we have a **registry** R that contains a **list of public keys** K_1 ... K_n. It’s assumed that R is a smart contract that has some procedure for admitting keys into this registry, with the social norm that participants in the mechanism should only act to support admitting keys if they verify two things:

1. The account belongs to a legitimate participant (eg. is a unique human, is a member of some community as measured in some formalized way such as citizenship of a country or a sufficiently high score on a forum, holds some minimum balance of tokens…)
2. The account holder personally controls the key (ie. they have the ability to print it out on demand if they really wanted to)

Each user is also expected to put down a deposit; if anyone publishes a signature of their own address with the private key, they can steal the deposit and cause the account to be removed from the list (this feature is there to heavily discourage giving any third party access to the key).

We assume that there is an **operator** with a private key k_{\omega} and a corresponding public key K_{\omega}.

We assume that there is a **mechanism** M, which we define as a function action^n \rightarrow Outputs, where the input is the action taken by each of the n participants and the output is some output as defined by the mechanism. For example, a simple voting mechanism would be the function that returns the action that appears the most times in the input.

### Execution

At time T_{start}, the operator begins with an internal state S_{start} = \{i: (key=K_i, action=\emptyset)\} for i \in 1...n. Anyone can compute this internal state; the registry contract itself could do this.

Between times T_{start} and T_{end}, anyone has the right to publish messages into an on-chain registry (eg. set the `to` address to be a smart contract that saves them into a linked hash list) that are encrypted with the key k. There are two types of messages:

1. Actions: the intended behavior for a user is to send the encryption enc(msg=(i, sign(msg=action, key=k_i)), pubkey=K_{\omega}) where k_i is the user’s current private key and i is the user’s index in R.
2. Key changes: the intended behavior for a user is to send the encryption enc(msg=(i, sign(msg=NewK_i, key=k_i)), pubkey=K_{\omega}), where NewK_i is the user’s desired new public key and k_i is the user’s current private key.

We assume an encryption function where the user can provide a salt to make an arbitrarily large number of possible encryptions for any given value.

The operator’s job is to process each message in the order the messages appear on chain as follows:

- Decrypt the message. If decryption fails, or if the resulting object fails to deserialize into one of the two categories, skip over it and do nothing.
- Verify the internal signature using state[i].key
- If the message is an action, set state[i].action = action, if the message is a new-key, set state[i].key = NewK_i

After time T_{end}, the operator must publish the output M(state[1].action .... state[n].action), and a ZK-SNARK proving that the given output is the correct result of doing the above processing on the messages that were published.

### Collusion resistance argument

Suppose a user wants to prove that they took some action A. They can always simply point to the transaction enc(msg=(i, sign(msg=A, key=k_i)), pubkey=K_{\omega}) on chain, and provide a zero-knowledge-proof that the transaction is the encrypted version of the data containing A. However, they have no way of proving that they did not send an *earlier* transaction that switched the key to some NewK_i, thereby turning this action into a no-op. The new key then could have been used to take some other action.

The user could give someone else access to the key, and thereby give them the ability to race the user to get a new-key message in first. However, this (i) only has a 50% success rate, and (ii) would allow the other user the ability to take away their deposit.

### Problems this does not solve

- A key-selling attack where the recipient is inside trusted hardware or a trustworthy multisig
- An attack where the original key is inside trusted hardware that prevents key changes except to keys known by an attacker

The former could be mitigated by deliberately complicated signature schemes that are not trusted hardware / multisig friendly, though the verification of such a scheme would need to be succinct enough to be ZKP-friendly. The latter could be solved with an “in-person zero knowledge proof protocol”, eg. the user derives x and y where x+y=k_i, publishes X = x * G and Y = y * G, and shows the verifier two envelopes containing x and y; the verifier opens one, checks that the published Y is correct, and checks that X + Y = K_i.

### Future work

- See if there are ways to turn the trust guarantee for collusion resistance into an M of N guarantee without requiring full-on multi-party computation of signature verification, key replacement and the mechanism function
- MPC and trusted hardware-resistant signing functions.

## Replies

**barryWhiteHat** (2019-05-04):

So just after T_{start}  the first user (user_0) is able to publish their vote and get bribed because it is impossible that she created an older transaction to changed her key.  However I understnad the arugment as that this user can still after the fact update their vote again and there is no way for them to prove they did not do this.

However if user_0 can add the first two actions to the list then can

1. user_0 Make their vote
2. user_0 Update their public key to 0x0 (One where no public key exists)

So now user_0 can sell their vote. As the current state for the briber is

1. user_0 vote
2. user_0 invalidate key

If user_1 wants to sell her vote she can also do it by voting and burning her key. The current state for the briber becomes after user_0 shares her key with briber.

1. user_0 vote
2. user_0 invalidate key
3. user_1 vote
4. user_1 invalidate key

Even are honest voters interacting with the system the bribery can continue Imagine that user_2 takes an action and does not publish it. Our current briber state becomes

1. user_0 vote
2. user_0 invalidate key
3. user_1 vote
4. user_1 invalidate key
5. ???

So if all the users from user_3 to user_4 wants to see their vote they cannot right because we are not sure that that user did not invalidate their key at step 5. But what we can do is have them all vote and invalidate in series and then publish the data afterwards. The briber current state is

1. user_0 vote
2. user_0 invalidate key
3. user_1 vote
4. user_1 invalidate key
5. ???
6. user_3 vote
7. user_3 invalidate key
8. user_4 vote
9. user_4 invalidate key

Now we don’t know if user_4 or user_5 invalided their key. So the argument says we cannot bribe them. But we can bribe both of them half the amount we bribed user_0 and be sure that we paid and bought one vote. Because we know for one of them did vote the way that we wanted them to.

This think this can be a serious attack. Especially that a briber can reward users for participating early in the epoch. Let me know thoughts. I can further analyze this if there is contention about its impact.

---

**vbuterin** (2019-05-05):

That’s assuming an ability to add the first two actions to the list. One could easily make it default software for every user to switch their key to some other key and publish that message immediately after T_{start}, making it very hard for any specific user to get that position of being first.

The operator themselves could even have the first right to publish messages, allowing them to receive key switch messages from the participants through some other channel and include them before the “official” period starts.

---

**vbuterin** (2019-05-06):

Thinking a bit about doing the computation in MPC. It seems fundamentally not too hard. Note particularly that there’s nothing wrong with it being public whether a message is a key change or an action. You want something like:

### Key change

For all `j`: `k[j] = newKey * verifySig(newKey, k[j]) + k[j] * (1 - verifySig(newKey, k[j]))`

### Actions

For all `j`: `a[j] = action * verifySig(newKey, k[j]) + a[j] * (1 - verifySig(newKey, k[j]))`

Making a ZK-SNARK over the individual MPC transcripts should be harder, but seems fundamentally doable.

---

**ryanreich** (2019-05-07):

If I understand the problem correctly: you are proposing a scheme where users, identified cryptographically, can vote on something, but are disincentivized from selling their votes to each other (“collusion resistance”).

If I understand the solution correctly: users are to be indexed, in exchange for a deposit, in a centralized registry operated by a trusted third party, and may update their identity there by providing proof of it.  Both updates and votes are sent signed and encrypted to the operator, so no one can enumerate the full history of a user’s actions, even though the user can prove any individual update or vote by producing the corresponding signed message that encrypts to one that has been put on-chain.  Therefore, no one can really trust another user they are trying to buy a vote from, who may be hiding the fact that what they are selling is no longer in the registry.

I may be missing some design criterion here, but why not just require a user to cast a vote, secretly, at the time they make the deposit?  If the trusted operator can be so omniscient as to enforce setup rule 1, they can be equally certain that the vote is genuinely by the person casting it, and the secret ballot works just as it does in real life to prevent selling one’s vote.

Actually, rule 1 is the big problem that consensus mechanisms need to solve (who gets to participate), and I think it deserves a little more respect *as* a big problem here, because without it, there’s nothing stopping a sockpuppet army or plutocracy from taking over.

Rule 2, in my experience, has no teeth: unless you want people to turn up in their physical person to vote, they are anonymized enough that the most secure way to identify them is actually with the key they are submitting.  You may as well just say that a user *is* their key.  I suppose you could argue that the user could be globally identified by one master key, but submit a secondary key signed by the first one to this particular contest, but that just kicks the problem up to verifying the master key (the analogue of showing up in person) as well as introducing another layer of trusted centralization.

Okay, but let’s say the voters really need to be able to change their minds, and that the system for selecting them is satisfactory, and that we even manage to do this decentrally.  Then I think that the argument for collusion-resistance is similar to the common internet security pattern, “After creating an account, you must immediately change your password through the encrypted connection.”  At that point, an attacker has no idea “who” you really are, even if they knew your account creation data.

However, the two have the same vulnerability to shoulder-surfing (as it were).  In fact, a conspiracy dedicated to buying the election could make monetary offers *in advance* and in exchange for installing a monitor on the various sellers’ computers in order to see what their actual messages really were.  This might even satisfy the sellers as to personal security if the monitor is unable to access their authentication data or private keys (say, by literally being a camera pointed over their shoulder at the voting app).

So although I agree that this scheme severely demoralizes attempts to fix the election by *soliciting* bribes, it seems to have a real-world vulnerability to a prepared adversary due to its dependence on the secrecy of the message history.

---

**vbuterin** (2019-05-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/ryanreich/48/3479_2.png) ryanreich:

> I may be missing some design criterion here, but why not just require a user to cast a vote, secretly, at the time they make the deposit?

The goal of the scheme is to make it so that the setup needs to only be done once, and from that point it on the key be used for many different mechanisms. So the marginal cost of running a mechanism drops greatly. The intention is to help bring about a world where mechanisms (like quadratic voting etc) could be used for all sorts of use cases, and this requires the marginal cost of spinning up such a vote, and making it work reasonably securely, to be low.

I don’t think a scheme of this type needs to be secure against all sorts of fancy attacks involving shoulder surfing and cameras to be very useful; you get the bulk of the benefit by being secure against attacks that could be done purely online (like smart contract bribes). And actually installing a monitor on people’s computers seems like something that would require a high cost for people to be willing to put up with, and cheatable in many ways (how do you know I’m not going to vote with a *different* computer?)

---

**ryanreich** (2019-05-10):

I see, so the [T_\text{start}, T_\text{end}] period is repeatable: the registry is maintained, only the tally is performed at the end of each period.  This is much less of a surveillance risk, because the window for accumulating a complete history ends once the setup is complete.

It still bugs me that this is centralized.  Obviously you can’t make it decentralized in exactly the form given, because the private key k_\omega would need to be public.  Instead, let’s say that each voter has two private keys, k_i and k_i', and submits \text{enc}(K_i, k_i') when a new election begins.  All messages are sent in the clear:

\text{msg} = (i, \text{sign}(\text{action or enc(new }K_i, k_i'), k_i)),

but of course, the signature can’t be verified because no one knows the actual public key…yet.  At the end of the election, voters sacrifice their k_i' and reveal it publicly, and the entire stream of messages is verified all at once before the tally is taken.  For the next round of elections, the voter can make their old k_i into their new k_i' and pick another k_i, so that the key that is private in one election is revealed in the next one.

Until the reveal, it is impossible to know whether a given message has any effect, just as in the centralized scheme.  So this is still collusion-resistant.  One failing is that eventually, any potential briber knows that they were cheated, which is not possible in the centralized scheme, and invites possible retaliation even if the election is not affected.

Although anyone looking back through the history can (of course) figure out what all the messages mean, no one *living* the history can do this until the reveal.  So the transactions are not truly private, but they stay secret long enough to have the intended effect.

---

**vbuterin** (2019-05-10):

Yeah, I’ve thought about schemes that involve not revealing info until later, and they all run into the issue that if the briber is a little more patient they’re no good.

I agree the centralization is unfortunate! The nice thing though is that the centralization is only for the collusion-resistance guarantee, the centralized party can’t break anything else. Note that some meatspace verification being done by someone somewhere is indispensable because any scheme that requires anti-collusion infrastructure also requires unique-identity verification (or else someone can just gather up many identities and collude with themselves).

If we want to mitigate the centralization, the best that I can come up with is turning it from 1-of-1 into M-of-N via multi-party computation. We can potentially make the security even higher than 1/2 if we have a scheme that favors safety over liveness, and in the case where liveness fails detect it on-chain and automatically remove the non-live parties from the committee and restart.

---

**barryWhiteHat** (2019-05-11):

How does the withdraw of hte deposit works?

If I start with key x and update it to key y do I withdraw with key y ? Is the withdraw public in the smart contract ? Is the withdraw protected with the same coersion resistance mechanisim ?

My specific concern is something like this. I deposit eth and participate in a vote. Afterwards I withdraw my ETH deposit. If this is public I can use my withdrawal transaction from public key x as evidence to a briber that I did not update my key at any time during the Vote.

Its still possible here that I voted twice with the same public key. But I can run the probabilistic bribe attack above but this time at the end of the epoch. So I would reveal my vote that is close to the end of hte epoch and get bribed.

Let formalize the bribe amount. The operator creates a batch of transactions that overlap the end of the epoch and bribes each reveeler

`cost_per_vote * (no_transparent_actions_in_batch / no_hidden_actions_in_batch)`

The cost_per_vote is how valuable their votes are to them. In the quadratic voting analysis even if `no_transparent_actions_in_batch < no_hidden_actions_in_batch` this attack can still be more efficient.

---

**marckr** (2019-05-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> ### Future work
>
>
>
> See if there are ways to turn the trust guarantee for collusion resistance into an M of N guarantee without requiring full-on multi-party computation of signature verification, key replacement and the mechanism function
> MPC and trusted hardware-resistant signing functions.

Key selling would be a case of transitive trust. If trust is reliant upon repeated interactions from a single individual, could that not also then be packaged and sold? How does that interact with incentive compatibility wrt mechanisms?

I have been a bit wary on sMPC, but not through code tests which I should perhaps engage in. How could we decouple trust from engaging with a key signing process? This of course assumes that individuals have varying collusive tendencies. It should be clear that the risk is through a break down of trust. Keys however might be distributed widely to ensure non-collusion without discretion, but that is a shaky argument.

Believe I have mentioned before, but ring signatures and threshold signatures are essentially dual, former requiring minimal endorsement, latter requiring maximal endorsement, ie collaboration in decryption as opposed to signing. It comes down to the manner in which the keys are served to people then and for what ideally limited purpose. ZK-SNARKs have opened us back to solutions from verifiable computation, but that does not address the trust issue in repeated execution of the protocol via any given party. We’d have to think in a multilinear way with trust levels so to speak, or it all falls back to 1-2 oblivious transfer. This appears to be the gold standard of any MPC as it is transitive on the single operation of a protocol.

Have to reread the collusion post, but those are my 200 wei for now.

---

**ryanreich** (2019-05-14):

Coming back to the centralized version, I wonder if the following simpler scheme wouldn’t work better.

The idea is that, if you want to prevent bribery, you want a secret ballot; that’s what they were introduced for, in fact.  I assume there is a good reason for us to assume messages are public (if only because they will be transmitted over the internet and not a secure private network), so why not just do as we do already with online secrecy and open an encrypted channel?

So, when a voter registers with the operator, rather than giving it her public key, they do a key exchange (as in, a handshake encrypted by public key crypto that results in each of them agreeing on a symmetric key).  Now the operator is storing a separate totally secret key for each voter, and each voter can cast a ballot consisting of their voter number (in the clear) and the encrypted vote.

It is impossible to determine anything more than that a vote *was* cast, and even if a briber wants the voter to reveal a ballot as proof, the the voter would have to reveal *both* the ballot and their individual secret key in order for the briber to match it with an observed message.  (This is different from the public/private key situation you worked with, because there, the briber does know how to encrypt a message to match it with an observed one.)

Note that even though each voter gets their own secret key, the operator isn’t storing any more information than in your scheme, which keeps track of an individual public key for each voter.  The voters, in turn, are not responsible for any harder a task than when they had to hold a private key.  Finally, the messages are secure against tampering since the key encrypting the vote has to be the one stored by the operator for the numbered voter, and if that key stays secret, only the voter can accomplish this.

Unless there is a need for the votes to be public (and I don’t see why that is at all desirable as a default), or there is some aspect of the operator’s workings that precludes a key exchange, wouldn’t this work?

---

**vbuterin** (2019-05-14):

There is a need for encrypted votes to be public, which is that we don’t want to trust the operator for correctness, so we need the operator to be able to zero-knowledge prove that they counted all of the votes correctly and particularly did not “censor” any votes. The only thing a malicious operator should be able to break is the collusion resistance guarantee, not any safety or liveness guarantees.

---

**ryanreich** (2019-05-15):

In both schemes, the votes are “public” in the sense that they appear, encrypted, on-chain.  I meant that the secret-key scheme does not make it possible *ever* to prove (to the public, not the operator) how someone voted, unless they give up their secret key.  Whereas of course, the public-key scheme does allow a claimed vote to be checked against the record by encrypting it.

Is there something about the public-key setup that makes a ZK proof possible where it is not possible for the secret-key setup?  That is, given the stream of encrypted messages that are handled as you describe by the operator, there is a zero-knowledge proof that *some* correctly-signed votes and key-changes exist that make the alleged output and encrypt to the given messages; but given the stream of encrypted messages that I described, there is not a proof that some votes and some set of secret keys exist with that property?  They both sound like the same kind of problem (and also that the proofs would be exceedingly long and hard to compute; however, in both cases, the circuit only needs to be constructed once when the contract is written).

(As an aside, in order for the ZK proof for the secret-key scheme to show that the votes were cast by the users and not made up by the operator, I would have to say that each user *does* have a public key, which is initially placed into the contract, and with which they also sign the votes that they encrypt onto the chain.  Then the problem would contain an additional predicate that the same key was used for both.  Only the operator sees the signature, but that is enough for the ZK proof to reflect the fact that it is valid, like in the public-key setup.)

---

**vbuterin** (2019-05-15):

There’s also the possibility of a player agreeing with the operator on a key `k1`, but then using a different key `k2` to encrypt the message, or that of a malicious operator *claiming* that another player did such a thing. Unless the exchanged key is somehow committed to on chain in a way that the player can verify, this seems unavoidable, and if the exchanged key *is* committed to on chain in a way that the player can verify then they could prove how they voted.

So I think the ability to specifically cancel a key is important.

---

**ryanreich** (2019-05-15):

I see the problem here: the public has no means to verify an operator’s claim that some vote is invalid due to encryption with the wrong key, or that some invalid vote is valid because it’s encrypted with a key that the operator knows but isn’t the one that particular voter should use.  Fair enough: this violates the requirement that an operator failure shouldn’t affect the outcome of the vote.

Let’s modify my previous aside, which suggested that each user’s public key be kept on-chain for identity verification, to *also* keep the operator’s public-key encryption of the secret key of each user (the user as well as the ZKP can verify this because both would also have the operator’s public key and the user’s own secret key; no one else can learn anything from it).  The operator (and, correspondingly, the ZKP), is required to use *that* secret key to decrypt votes.  This ensures that a malicious operator can’t pretend that a vote is invalid, or that a vote encrypted with someone else’s secret key is valid, since the means to validate is visible, if not usable, to the public.

In general, it seems to me that by encrypting with the operator’s public key, any internal state maintained by the operator can be manifested in public, indecipherably, but still visibly enough to figure in a zero-knowledge proof that it was used correctly by the operator.

---

**vbuterin** (2019-05-17):

But then wouldn’t a user be able to prove what their secret key is, if they’re the ones to encrypt it to the operator? I suppose you could get around that if the operator encrypts, but then that seems like it would put a lot of load on the operator to make many more proofs.

---

**ryanreich** (2019-05-18):

I don’t think this reveals anything that the people who can find out don’t already know.  Maybe I should make explicit the structure that’s been coming together in pieces here.

The contract contains the following data object, annotated in some made-up, suggestive type system:

```auto
{
  registry : Map PublicKey (PubKeyEnc SymKey, SymKeyEnc (Signed Vote)),
  operatorPubKey : PublicKey
}
```

Each voter also has a data object:

```auto
{
  myVote : Vote,
  myPrivKey : PrivateKey,
  mySymKey : SymKey
}
```

The operator has a very simple data object:

```auto
{
  myPrivKey : PrivateKey
}
```

The voter and operator data are, of course, known only to the respective parties, while the contract data is public.  For each voter, there is an entry in `registry` (with pseudocode crypto API):

```auto
registry[pubKeyOf(voter.myPrivateKey)] =
  (
    pubKeyEnc(voter.mySymKey, contract.operatorPubKey),
    symKeyEnc(pubKeySign(voter.myVote, voter.myPrivKey))
  )
```

This can be constructed entirely by the voter, since it uses only data visible to them (their own and the contract’s).

Conversely, the operator can read each vote, including validating the voter:

```auto
votes =
  symKeyDec
    (
      encSignedVote,
      pubKeyDec(encSymKey, operator.myPrivKey)
    ).unsign(voterPubKey)
    for voterPubKey, (encSymKey, encSignedVote) in contract.registry.items()
```

Therefore, the operator can construct a proof that `M(votes) == outcome`, for whatever outcome.  The proof is of the existence *only* of `operator.myPrivKey`, and because of the expression above, includes proofs of the validity of each vote.  It shows that the various nonsense blobs in the contract are actually encryptions of correct data.

As you can see, only each voter knows their own symmetric key; it is stored as a message encrypted to the operator alone, and its correctness is established by the proof that the equation holds with the definition of `votes` given.

---

**ryanreich** (2019-05-18):

Of course, only after posting that long thing did I understand what you were asking.  I’ll leave it there since it seems useful, but I’ll answer your actual question here.

It does seem true that a voter could choose to reveal their own secret (symmetric) key in a way that someone else could verify, since it’s encrypted with the operator’s public key.  And I do agree that this could be fixed if the operator actually kept their “public” key private, and placed that encrypted value themselves.

Would this actually require more zero-knowledge proofs?  I think the voter could actually be sure their correct vote was used, if the expression for `votes` I gave in the long post is the one that goes into the overall proof: it requires checking the signature on their vote.  The operator should be unable to produce *any* valid voter-signed message, particularly not in the way that this exploit we’re talking about would require: the operator would have to place the wrong symmetric key in the registry, which would result in the vote being censored just because it doesn’t decrypt correctly (but then break the proof because the signature is also not validated); to actually place a *fake* vote, the operator would have to somehow come up with a fake symmetric key that causes this bad decryption to be a correctly-signed vote.  This is just not feasible.

The voter could of course give up their private key to a dishonest operator.  However, the operator would *still* have to figure out an alternate symmetric key that would decrypt the actual encrypted vote to a signed, fake vote of their choice.  I don’t think this is feasible either, though that depends on the encryption method and seems similar to actually cracking the encryption entirely.

---

**vbuterin** (2019-05-18):

My proposal was that the operator put the voter’s symmetric key on-chain encrypted with the operator’s own public key. The voter would have no way of verifying that this was actually done, unless the encryption scheme is deterministic, and in the latter case the voter could prove to others what their key is.

I feel like any scheme that doesn’t involve a key revocation game is going to keep having these kinds of issues…

---

**ryanreich** (2019-05-20):

After some thought, I have to agree that without the game it seems almost necessarily the case that a voter would be able to prove their vote.  Essentially, the voter can prove their vote to a briber (thus soliciting a bribe) if they can supply a probabilistic algorithm computing their set of messages.  In your scheme, they can enumerate it but not its complement.  My scheme definitely has a deterministic proof of vote; actually, it shows up a lot earlier in the conversation, since the voter can always just reveal their “secret” key.  Any voting scheme where the ultimate vote depends on a single message would have this problem; it has to be possible, no matter what the voter reveals, that they have omitted something important.  Which is a game.

This has been very educational.  I hope I wasn’t too obnoxious in the process.

---

**barryWhiteHat** (2019-07-11):

We are staring to implment this http://github.com/barryWhiteHat/maci

If anyone wants to join this effort please join https://t.me/joinchat/LUgOpE7J2gstRcZqdERyvw


*(5 more replies not shown)*
