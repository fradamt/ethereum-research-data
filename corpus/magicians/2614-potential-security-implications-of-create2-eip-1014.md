---
source: magicians
topic_id: 2614
title: Potential security implications of CREATE2? (EIP-1014)
author: rajeevgopalakrishna
date: "2019-02-08"
category: EIPs
tags: [opcodes, eip-1014]
url: https://ethereum-magicians.org/t/potential-security-implications-of-create2-eip-1014/2614
views: 18682
likes: 56
posts_count: 93
---

# Potential security implications of CREATE2? (EIP-1014)

Not sure if this has been discussed elsewhere/before but I came across this topic today on AllCoreDevs gitter and thought it may be useful to start a thread here. Thanks to [@carver](/u/carver) and [@holiman](/u/holiman) for initiating this discussion.

**Summary** (per my understanding so far): `CREATE2` allows contracts to change in-place after being deployed. This is because, although `CREATE2` includes the hash of `init_code` in address generation, the same `init_code` could intentionally generate arbitrary contract code. There appear to be use cases where such behaviour is desirable but potentially leaves it open for misuse. So users interacting with a seemingly ‘benign’ contract earlier could suddenly be interacting with a newer contract (at the same address) which implements a completely different (potentially malicious) functionality.

Perhaps this is obvious to some but not to many. So it may be worthwhile to make sure this is discussed and documented. I’m copying the gitter discussion context below:

From [@carver](/u/carver):

> So, based on my social network and @holiman 's sampling, it looks like a lot of contract devs aren’t aware that (new) contracts will be able to change in-place after CREATE2 from Constantinople goes live. How about in this room, is this a broadly-understood change?
> It opens up a lot of interesting ways of tricking people into giving you their ether/tokens/etc – for example: have a user verify contract source, send a transaction to your contract, and then front-run them with a couple transactions to swap in the new contract with arbitrary source.

> I think the implication there is that any mischievous contract post-Constantinople already looks shady, pre-Constantinople. But you can construct a pretty innocuous contract pre-C, one that has two possible outcomes from a transaction: {“contract exists”: “swap tokens”, “contract self-destructs”: “waste some gas”}. Post-Constantinople, the options could now become {“contract exists”: “swap tokens”, “contract self-destructs”: “waste some gas”, “contract replaced”: “all ERC20 tokens that were pre-approved to the contract are stolen”}.
> There are mitigations for these problems, of course. We just need to educate coders and auditors, and soon. (I’ll do my part and write something up, but my reach is pretty minimal)

> For example, the init code could load bytecode from another contract and return it. So the init code doesn’t change, but returns arbitrary contract code to deploy.

From [@holiman](/u/holiman):

> And the corollary being, as previously, that if someone verified the source, he should have noticed the  SELFDESTRUCT  (without a due inactivity period) and avoid interacting with it. I would believe that most perusers of this channel are fully aware of all the effects of  CREATE2 . The general eth deveopers and auditors, less so, unfortunately.

> Yes, that’s it. I’m constantly surprised about how little known that fact is - even in this very niche channel

From [@veox](/u/veox):

> CREATE2 allows for many new funky use cases; @carver - could you explain your example?..
>
>
> CREATE2-derived contract address depends on the “init code” hash being passed as argument to the instruction, so “new contract with arbitrary source” (in actual on-chain deployment) translates to that contract being deployed to a different address (than would have been presented previously to the user).
>
>
> (This is a non-issue for the attacker if the user is to interact with the CREATE2-deployed contract through an attacker-provided delegation mechanism.)

> You mean a scheme of: in-CREATE2 init_code loads data to memory from storage of a fixed external contract, and the external contract is under an attacker’s control (allows changing payload in storage).

> Future educational material on CREATE2 could benefit from highlighting that init_code is not the code to be deployed, but the code to generate the code to be deployed. Similar to current send-to-none “contract deployment” transactions that use CREATE. Highlighting generate, that is (so dynamic!).

From [@rajeevgopalakrishna](/u/rajeevgopalakrishna):

> Doesn’t this change a major invariant assumed by users today and introduce a potentially serious attack vector with  CREATE2 ? Doesn’t this mean that any contract post-Constantinople with a  selfdestruct  is now more suspect than before? Should restrictions be considered on  init_code  used in  CREATE2  to prevent it from loading bytecode from storage of other contracts (not sure if this is possible)?

From [@veox](/u/veox):

> Not SELFDESTRUCT per-se, but non-deterministic init_code. Restricting storage access would also limit the usefulness of CREATE2, specifically in cases where one would want non-determinism. Say, a claim to ownership of a particular ENS entry in the past. Or, more broadly, a query to ENS in init_code. Or to the reverse registrar. Or even an ERC-20 balance look-up…

## Replies

**carver** (2019-02-08):

Limiting the init code to avoid these problems is almost certainly going to be ineffective. For example, even if we stop the code from invoking any external contract/storage, the init code could emit bytecode A until block number 7.5M and then bytecode B afterward.

Not to mention that there isn’t enough time to make a change to the opcode before Constantinople launches. If we decide that these in-place updates are unresolvable, then pretty much our only option would be to remove it entirely. It’s not too late to do that, but we’re getting close.

---

**rajeevgopalakrishna** (2019-02-08):

I am not aware of the design rationale here but won’t this problem be avoided if we simply prevent `CREATE2` from creating a contract at an address if one had already been created at that same address before (and `SELFDESTRUCT`-ed thereafter)? Not sure if there are valid use cases which require this behaviour.

---

**carver** (2019-02-08):

Unfortunately, that would require keeping around a flag for every contract that has ever existed, after it’s gone. That can have a significant impact on the account trie size/structure over time.

---

**rajeevgopalakrishna** (2019-02-08):

But one bit per contract (only those created using `CREATE2`) is worth it if the alternative is that such a contract might change in-place in future and it is hard (?) to verify beforehand that a contract is capable of doing so. Are there any other possible mitigations?

---

**carver** (2019-02-08):

You can actually do this with regular `CREATE` contracts too, if you layer them underneath `CREATE2` ones.

---

**rajeevgopalakrishna** (2019-02-08):

I see. So based on your analysis and prototypes (and ongoing discussion with [@Arachnid](/u/arachnid) on gitter - pasted below), this is a real exploitable concern, correct? If analysing `init_code` is hard and not sufficient, then besides keeping a flag-bit history for created contracts, are there any other options we could consider?

From [@carver](/u/carver):

> I’m not even sure if looking at the init code used is enough. I don’t have a prototype of this one, but you can theoretically deploy a malleable contract which itself calls a regular CREATE. Then when you reset the malleable deployer contract, you can do another CREATE to the same address, because you reset the nonce on the deployer contract. Now you don’t have any constraint on the init code being the same.

From [@Arachnid](/u/arachnid):

> This is a really good point. You’d have to verify everything back to the first EOA-created contract.

---

**rajeevgopalakrishna** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rajeevgopalakrishna/48/1463_2.png) rajeevgopalakrishna:

> From @carver:
>
>
>
> I’m not even sure if looking at the init code used is enough. I don’t have a prototype of this one, but you can theoretically deploy a malleable contract which itself calls a regular CREATE. Then when you reset the malleable deployer contract, you can do another CREATE to the same address, because you reset the nonce on the deployer contract. Now you don’t have any constraint on the init code being the same.

By ‘reset’, do you mean re-create the malleable deployer contract using `CREATE2` at the same address? Keeping a flag-bit for `CREATE2` only contracts would prevent this, won’t it? You won’t be able to reset the deployer contract and hence the nonce.

---

**carver** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rajeevgopalakrishna/48/1463_2.png) rajeevgopalakrishna:

> this is a real exploitable concern, correct?

It’s not an EVM exploit, exactly, but it is a way to maybe make auditors’ jobs more difficult. There are ways around each of these “social attacks”, but most of them require education. That will surely lag behind the Constantinople upgrade itself.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rajeevgopalakrishna/48/1463_2.png) rajeevgopalakrishna:

> By ‘reset’, do you mean re-create the malleable deployer contract using CREATE2 at the same address? Keeping a flag-bit for CREATE2 only contracts would prevent this, won’t it? You won’t be able to reset the deployer contract and hence the nonce.

Right, if you prevent `CREATE2` redeploys, then you prevent `CREATE` redeploys, as far as I can tell.

---

**rajeevgopalakrishna** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carver/48/846_2.png) carver:

> It’s not an EVM exploit, exactly, but it is a way to maybe make auditors’ jobs more difficult. There are ways around each of these “social attacks”, but most of them require education. That will surely lag behind the Constantinople upgrade itself.

Agree but at some level this further reduces the trust end-users expect from contracts being “immutable.” Not only can they be upgraded but now they may be redeployed as well. There is a perceptional risk here and we can’t blame the users (or the auditors).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/carver/48/846_2.png) carver:

> Right, if you prevent CREATE2 redeploys, then you prevent CREATE redeploys, as far as I can tell.

So the additional redeploy-tracking flag-bit only for `CREATE2` contracts might not add much (?) to the state assuming that most use cases will continue to use `CREATE`, correct? But as [@Arachnid](/u/arachnid) indicated, this will be a consensus change.

---

**holiman** (2019-02-08):

- Regarding the fact that CREATE2 ->A, CREATE -> B+2 x SELFDESTRUCT and then CREATE2 -> Amod, CREATE -> Bmod

I don’t think that changes things a lot. It simply further an argument against an anti-pattern: the anti-pattern of trying to establish trust through investigating history of a contract.

The pattern that should be used, is:

- Use EXTCODEHASH to verify that the code you are calling matches what you expect. This might mean that during either compilation, construction or initialization (not necessarily same as construction), you store the expected EXTCODEHASH for other contracts that you will interact with.

Example: A DEX, when enrolling new ERC20 assets, may have to store the EXTCODEHASH when the new asset is enrolled.

Bonus: When solidity does a call, today it uses EXTCODESIZE to verify that the contract exists. It could use EXTCODEHASH instead, and internalize it so the call would look maybe like theToken.verify(codehash).transfer(from, to, value).
- Alternative: when enrolling the token, it would do a safety-check, to verify once and for all that the contract is immutable.

There may arise an immutability-registry. That would simply run a check that contract `X` does not have `SELFDESTRUCT`, `DELEGATECALL`, `CALLCODE`  (that’s it right?).  EDIT TO CLARIFY: A registry of codehashes, not addresses.

That was the on-chain scenario, so how about the EOA scenario, interacting with a contract `Casino`?

- Attack vector: When user sends large amount of ether to Casino, then the operator front-runs with two transactions:

SELFDESTRUCT Casino.
- CREATE2 a new Casino which steals the funds.

**OBS:** The `SELFDESTRUCT` and recreation cannot happen within one transaction, due to how `SELFDESTRUCT` operates.

This scenario is flawed from the beginning:

1. The EOA should not send money to a contract which can SELFDESTRUCT without prior notice. That’s dangerous even today (but there is no payout for the operator, only the wreak-havoc factor).
2. If the user, despite this, wants to interact with the contract, he can do so e.g. via a personal on-chain wallet.

At the end of the day, auditors and developers *NEED* to get up to speed with these new changes. It’s been discussed ever since the suggestion of the first `CREATE2` variant, and then further discussed with the current variant.

---

**rajeevgopalakrishna** (2019-02-08):

Thanks for the detailed explanation with examples.

As [@Arachnid](/u/arachnid) explained on gitter, the “bytecode invariant” may not hold for contracts deployed with `CREATE2` or even with `CREATE` if one of its ancestors were deployed with `CREATE2`.

Therefore, it’s going to be even more critical going forward that the security pattern leverages `EXTCODEHASH` before interacting with other contracts.

So it sounds like the bottomline is that these concerns are not new, have been deliberated, no mitigations are necessary and what is needed is incorporating this guideline in the security best practises.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> There may arise an immutability-registry. That would simply run a check that contract X does not have SELFDESTRUCT , DELEGATECALL , CALLCODE (that’s it right?).

This is a very interesting idea.

---

**Arachnid** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Use EXTCODEHASH to verify that the code you are calling matches what you expect. This might mean that during either compilation, construction or initialization (not necessarily same as construction), you store the expected EXTCODEHASH for other contracts that you will interact with.

I really think this is an antipattern; for interoperability and for permissionless innovation, security models should not depend on called contracts having specific bytecode. Contracts should be designed to be secure regardless of the callee’s code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Example: A DEX, when enrolling new ERC20 assets, may have to store the EXTCODEHASH when the new asset is enrolled.

…and it won’t help here; a malicious token contract could be deleted and replaced with one with a constructor that produces the same byte code, but allocates the initial balances arbitrarily.

---

**holiman** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> …and it won’t help here; a malicious token contract could be deleted and replaced with one with a constructor that produces the same byte code, but allocates the initial balances arbitrarily.

Yes, that naturally depends on what properties you want guarantees on. I was more thinking of the scenario where you audit a potential ERC20 token before enrolling it, to ensure that it will behave in certain ways when invoked.

---

**rajeevgopalakrishna** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> …and it won’t help here; a malicious token contract could be deleted and replaced with one with a constructor that produces the same byte code, but allocates the initial balances arbitrarily.

Darn! So `EXTCODEHASH` offers no protection against this scenario. Doesn’t this alone justify a mitigation measure? [@Arachnid](/u/arachnid)’s below suggestion on gitter seems elegant:

> I honestly think the simplest solution to all of this would have been to modify self destruct to leave an account’s nonce intact. Selfdestruct is already an ineffective way to encourage freeing state, and this would solve the issues.

Does this have any other side-effects?

Some of the text at [Prevent overwriting contracts · Issue #684 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/issues/684) from [@vbuterin](/u/vbuterin) seems to perhaps raise this concern as well, but I don’t have all the insight/context and could be mistaken:

> ### Specification
>
>
>
> If a contract creation is attempted, due to either a creation transaction or the CREATE (or future CREATE2) opcode, and the destination address already has either nonzero nonce, or nonempty code, then the creation throws immediately, with exactly the same behavior as would arise if the first byte in the init code were an invalid opcode. This applies retroactively starting from genesis.
>
>
>
> ### Rationale
>
>
>
> This is the most correct approach for handling the case where a contract is created in a slot where a contract already exists, as the current behavior of overwriting contract code is highly unintuitive and dangerous.
>
>
> Currently this is not an issue because there is no way to create a contract with the same address twice without spending >2^80 computational effort to find an address collision, but with #86 this will change. Hence it is important to have correct behavior for this situation in the long term. This can be safely applied retroactively for simplicity, because currently creating a contract with the same address twice is computationally infeasible.

---

**rajeevgopalakrishna** (2019-02-08):

Is there any way to characterise the overall risk here given that `EXTCODEHASH` does not fully protect against all scenarios?

If the risk is minimal, that would justify status quo. If the risk of misuse is high and all mitigations require consensus-changes, then what is the best way forward?

---

**Arachnid** (2019-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/holiman/48/147_2.png) holiman:

> Yes, that naturally depends on what properties you want guarantees on. I was more thinking of the scenario where you audit a potential ERC20 token before enrolling it, to ensure that it will behave in certain ways when invoked.

“Can’t change the balances arbitrarily” seems like a pretty important property to preserve!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rajeevgopalakrishna/48/1463_2.png) rajeevgopalakrishna:

> Is there any way to characterise the overall risk here given that EXTCODEHASH does not fully protect against all scenarios?

Again, relying on a callee contract to have specific behaviour is a bad pattern. We should be authoring contracts to be secure regardless of what a third-party contract does.

---

**rajeevgopalakrishna** (2019-02-09):

Yes, defensive programming is something everyone should ideally practise and educate, but if there is a design flaw, it should be addressed as such without shifting that burden to the user/developer/auditor.

And this unintended/unintuitive side-effect of `CREATE2` which can be maliciously exploited in multiple ways certainly looks like a flaw in opcode semantics. Yes, it may be too late to fix/remove it now before Constantinople (assuming the cost to fix > risk of exploitation) but has to be addressed soon if we believe this is indeed a design flaw.

---

**AdamDossa** (2019-02-09):

If I’ve understood correctly then for it to be possible to mutate contract A’s byte code, contract A must somewhere call `selfdestruct`. If that’s the case, a big red warning on [etherscan.io](http://etherscan.io) for post-C contracts which contain `selfdestruct` opcode would probably make this exploit / obfuscation near useless.

I do think it would pretty much kill off use of `selfdestruct` but don’t see that as problematic as it is fairly rarely used today due to their being little incentive to include it.

---

**holiman** (2019-02-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> “Can’t change the balances arbitrarily” seems like a pretty important property to preserve!

Right, and if that’s a concern, you should not let in contracts that can `SELFDESTRUCT`.

If, however, your main concern is that it doesn’t do a  reentrancy-attack against you, then you might allow that but don’t allow change of code.

---

**adamkolar** (2019-02-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adamdossa/48/817_2.png) AdamDossa:

> If I’ve understood correctly then for it to be possible to mutate contract A’s byte code, contract A must somewhere call selfdestruct. If that’s the case, a big red warning on etherscan.io for post-C contracts which contain selfdestruct opcode would probably make this exploit / obfuscation near useless.

For this to work, you would also need to check for  `delegatecall`  and  `callcode`


*(72 more replies not shown)*
