---
source: magicians
topic_id: 11907
title: Deprecate SELFDESTRUCT
author: fulldecent
date: "2022-11-27"
category: EIPs > EIPs core
tags: [opcodes]
url: https://ethereum-magicians.org/t/deprecate-selfdestruct/11907
views: 4163
likes: 25
posts_count: 12
---

# Deprecate SELFDESTRUCT

I feel like we have already deprecated SELFDESTRUCT. But it was never officially announced in the Yellow Paper or on the Ethereum Blog. This EIP fixes that.

---

We can implement this EIP now. It’s the first core EIP that does not require any client change, I think?

However, by implementing this we are putting customers on notice of a big upcoming change. And that is something that good software projects do.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6049/files#diff-7d56564329c475a6f37f3383fbb3e0e8bb5c892c868b58ba320b609b1fad6b78)














####


      `master` ← `fulldecent:patch-102`




          opened 10:34PM - 27 Nov 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2cad68a075cd871ff315dd9c9b9cf549c32d1209.jpeg)
            fulldecent](https://github.com/fulldecent)



          [+41
            -0](https://github.com/ethereum/EIPs/pull/6049/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6049)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**dankrad** (2022-11-28):

Yeah I agree that this is a good idea. Anyone still deploying code with `SELFDESTRUCT` has been warned.

---

**Pandapip1** (2022-11-28):

This should be a Meta-type EIP.

---

**fulldecent** (2022-11-29):

Here is some language in support of a meta EIP:

> they are more than recommendations, and users are typically not free to ignore them

Changed to meta at [Update eip-6049.md by fulldecent · Pull Request #6064 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6064)

---

**xinbenlv** (2022-11-29):

Thanks for this EIP, Will [@fulldecent](/u/fulldecent) , I am curious could you elaborate the relationship this EIP vs [EIP-4758: Deactivate SELFDESTRUCT](https://eips.ethereum.org/EIPS/eip-4758)

---

**abcoathup** (2022-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I am curious could you elaborate the relationship this EIP vs EIP-4758: Deactivate SELFDESTRUCT

[EIP6049](https://eips.ethereum.org/EIPS/eip-6049) formally states that SELFDESTRUCT is deprecated, to tell devs not to create contracts that depend on it.  As a meta EIP it can be quickly finalized.  The sooner devs stop creating contracts depending on SELFDESTRUCT the easier it is to change the functionality.

[EIP4758](https://eips.ethereum.org/EIPS/eip-4758) is how SELFDESTRUCT can be deprecated by changing/removing functionality and will require an upgrade.  It is not yet CFI’d, so at this rate might not be included in Shanghai upgrade and would have to wait for Cancun.

---

**xinbenlv** (2022-12-01):

Oh, got it. If the purpose is to “call it out”, I guess it would be helpful to also mention the EIP-4578 and

EIP-4760 as context as “If you ignore, here are the consequence scheduled at Shanghai”?

Overall I am still debating myself with existence of EIP-4578 and EIP-4760, how much more value does a third Meta EIP brings to the table.

The pros I can think of having this third Meta EIP is (1) it can finalize faster (2) it record and signal an existing community consensus.

---

**yoavw** (2022-12-03):

Would be nice if compilers (e.g. solc) will warn the user when violating a meta-EIP, or even consider it a compilation error unless an override flag is used.

---

**timbeiko** (2023-01-05):

I think it might be worth considering this for Shanghai, yes. Even though it’s just “symbolic”, getting a commitment from client teams that we are going down this route, and having a clear signal to users that “It’s happening ![:soon:](https://ethereum-magicians.org/images/emoji/twitter/soon.png?v=12) !” is valuable, even without EIP-4758 or similar making it into Shanghai.

Anyone want to discuss this on the next ACD ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) ? [Execution Layer Meeting 153 · Issue #704 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/704)

---

**Pandapip1** (2023-01-05):

Any reason this can’t be asynchronously proposed?

---

**timbeiko** (2023-01-06):

Oh, it can, but people just pay more attention through that (but mostly, via fork announcements). At the very least, we can post about this in the R&D discord and gauge people’s reaction.

---

**poojaranjan** (2023-03-15):

PEEPanEIP #102: [EIP-6049: Deprecate SELFDESTRUCT](https://youtu.be/Mgld_3JjFXQ) with [@fulldecent](/u/fulldecent)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/1/1efcd8fc48e070518cb6b7bae0dfb3d31816eee2.jpeg)](https://www.youtube.com/watch?v=Mgld_3JjFXQ)

