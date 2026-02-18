---
source: magicians
topic_id: 2389
title: Jello Paper as Canonical EVM Spec
author: expede
date: "2019-01-10"
category: Magicians > Primordial Soup
tags: [evm, yellow-paper, jello-paper]
url: https://ethereum-magicians.org/t/jello-paper-as-canonical-evm-spec/2389
views: 8418
likes: 114
posts_count: 73
---

# Jello Paper as Canonical EVM Spec

Hello all ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=15)

During Devcon 4, there was some discussion about moving the canonical EVM spec to the Jello Paper. I think that this is a *fantastic* idea. Very few people seem happy with the Yellow Paper as written, and the ambiguous state of maintenance. I am partway through an EVM implementation myself, and have found the Jello Paper to be *far* superior to the Yellow and Beige Papers. Some of the reasons include:

- Much clearer
- Fewer edge cases
- Took the time to formalize the semantics
- Executable (hooray for K!)
- Can generate various EVMs (via K backends)
- Very readable (not hard to get used to K’s output)

I will be submitting a Meta EIP shortly, but would love to hear other people’s thoughts!

# Related EM Posts

- Discussion about the technical spec of the EVM
- Yellow Paper Maintainership
- Highlighting the other standards & specs that make up Ethereum

## Replies

**boris** (2019-01-11):

Does anyone know if the [Constantinople changes](https://en.ethereum.wiki/roadmap#constantinople) have been added to the Yellow Paper or Jello Paper? [@jpitts](/u/jpitts) [@Arachnid](/u/arachnid) [@ehildenb](/u/ehildenb)

I just [filed a PR to set 1014 and 1052 to Accepted](https://github.com/ethereum/EIPs/pull/1692) – I’m not even sure if they went through Last Call (not, as far as I can tell, they just sat in Draft). I’m happy to help maintain the EIPs repo if there aren’t enough hands on deck for this basic admin stuff.

EDIT: [@axic](/u/axic) beat me to creating the same PR. I noticed this back in December, should’ve done it then.

---

**ehildenb** (2019-01-11):

We are current as of 23 days ago: LINK REDACTED FOR SOME REASON

The Jello Paper is unfortunately not automatically updated on PRs into KEVM, just occasionally manually (though the derivation process itself is 100% automatic). It’s on my todo list to have the CI server update the Jello Paper automatically on merges to master.

---

**gcolvin** (2019-01-12):

I brought this up on the AllCoreDevs channel and there was the usual criticism, but more support for the Yellow Paper than I expected.  People liked that there were formal specs, but wanted there to be one that they can read as well.

The math in the Yellow Paper is not that advanced,  (anyone with a year of so of undergraduate study can handle it) but it’s badly presented. And the English could be much better, as in the [Beige Paper](https://github.com/chronaeon/beigepaper/blob/master/beigepaper.pdf).  But with effort people who need to read it can, and without learning another language first.  And with effort it could be much more readable.

Compared to technical English and basic math very few people can read formal specification languages, and that terribly compromises many purposes of having a spec.  For one important example, a spec that an engineer can use to write a client matters.  For that purpose, for most engineers, the Yellow Paper falls short, but a K spec would be nearly useless.

To be truly useful I think our K spec would need to use a carefully designed presentation syntax, teach the reader the K they need to know, and be sure the embedding English is complete and correct without the K.  Because in the end a K spec is a reference implementation in a language that hardly anybody knows.  And reference implementations have well-known strengths and weaknesses as specs.

Still, it depends on who does the work, and how the community cares to put it to use.  A number of people volunteered to get to work on a better Yellow Paper, including how best to embrace our K and Lem formalizations.  Whether they do the work remains to be seen.

---

**gcolvin** (2019-01-12):

PS.

For what it’s worth.

- The Yellow Paper specifies the entire client in about 2600 lines of LaTex.  About half of that is the VM.
- The Jello Paper specifies the VM in about 2400 lines of K.
- py-evm implements the VM in about 2900 lines of Python.
- aleth implements the VM in about 2400 lines of C++.

---

**grosu** (2019-01-12):

Thanks, [@expede](/u/expede), for starting this discussion!  Your list of reasons is great!  I would like to add one more, which in my view is in fact the most important one in the long term (disclaimer: I am a researcher in formal methods, specification and verification, as well as PL design — so I may not see things as clearly as I should):

- Usable as is as input to a program verifier that can formally specify and verify smart contracts at the EVM bytecode level.  That is, the gap between what you verify and what you execute is zero.
That was the main reason we came up with the K semantics of EVM first place (we’ve already done that with other languages, such as C, Java, JavaScript, Python, etc., in the past).

---

**grosu** (2019-01-12):

[@gcolvin](/u/gcolvin) I share your thoughts about  formal specs being harder to read/grasp by non-experts.  And I am genuinely interested in doing something about it.  It would be really nice to have a tool that takes a formal semantics (say in K for starters) and generate human-readable documentation from it.  Note that this is research, though!  That is, I’d need one or two people to work on such a project for 6 months or so.  My company does not have any resources allocated to do this, so we either need some funding or some enthusiastic volunteers.  Such a tool would have the benefit that we can then keep using it as EVM itself evolves, not to mention that it can be used for other VMs and languages as well (WASM, IELE, maybe even higher level languages).

Anyway, I am in for this.  Our main concern so far was really to make sure that the KEVM semantics is adequate, especially because as I said above, we use it for formal verification of smart contracts.  Serving as documentation for EVM was not our original intention.  But it makes a lot of sense to pick a reference model that is rigorous and that is used as input to tools, because it avoids the problem of having to keep things in synch.  Ah, and additional advantage is that different uses of it with different tools sometimes reveal quite subtle bugs in the semantics/model, which once fixed, they are then fixed for all tools.

---

**grosu** (2019-01-12):

Thanks for these statistics, [@gcolvin](/u/gcolvin), very useful to know!  Again, the K semantics can be used for many purposes as is.  Execution is only one use.  Symbolic execution, model checking, deductive verification (verification of smart contracts), and hopefully test-case generation soon, are other possible uses.  In my view this is the main advantage of the K approach, not necessarily compactness.  I would go for these advantages even if the K semantics of the EVM were 4x larger than an implementation.  But again, I am biased here.  Heavily.

---

**boris** (2019-01-12):

Is there a tracking Github issue for this? (auto-update of Jello Paper by CI Server) Please paste it here or create it, because then it can be bountied!

---

**gcolvin** (2019-01-12):

LatTex is fairly verbose, so the Yellow Paper is already half the line count of the three implementations, and even more compact once printed.  And readable by a vastly larger audience.  And I mean vastly.  That counts a lot for me.

But in the end we will continue to have the Yellow Paper for so long as we continue to have editors, and it will continue to be used as a standard for so long as people find it useful.  We will also have implementations in various languages, including the Python reference implementation, the K and Lem specifications, and various production clients.  Some of those, especially the Python and K work, may also prove useful as standards.

In a consensus network *they all must agree.*  Any disagreement indicates a defect in at least one of them.  Which one, if any, to call *canonical* or *normative* is to some extent a matter of convenience.  But whose convenience, and for what purposes?

PS.  The K spec being no larger than programs that implement it I consider a victory.

---

**gcolvin** (2019-01-12):

So we have a small number of specifications and reference implementations. Primarily

- Python research implementation and specification
- EIPs slated for a release
- KEVM reference implementation and specification
- Yellow Paper

Each serves different purposes at difference points in the workflow. I don’t see a need (or even a way) to bless one of them as “the standard.”

---

**gcolvin** (2019-01-12):

Note.  It’s a good thing that K is code.  Mostly.

[![Strip-Les-specs-cest-du-code-650-finalenglish](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e86bb69c12175fcb823fe386536203bc8b216f9c_2_530x500.jpeg)Strip-Les-specs-cest-du-code-650-finalenglish650×613 266 KB](https://ethereum-magicians.org/uploads/default/e86bb69c12175fcb823fe386536203bc8b216f9c)

---

**ehildenb** (2019-01-12):

Hmmmmm, seems my posts are being hidden because I’m including links to repository stuffs? That seems insane.

Anyway, [@boris](/u/boris), I’ve made an issue about adding a CD job to update the Jello Paper on updates to `master`. It’s issue 239 on KEVM repository, which I can’t link to because that would be “overly promotional”. A little bit insane, because we’re literally talking about that repository.

---

**boris** (2019-01-13):

Have to stop the spammers some how!

After spending time coming back to the forum, your account gets upgraded. I don’t have admin powers to do more right now, but just PM me if it’s a problem.

Thanks for filing the issue. Here’s the link for reference: https://github.com/kframework/evm-semantics/issues/293

---

**gcolvin** (2019-01-14):

[@ehildenb](/u/ehildenb) Could summarize what we haven’t been able to read?

---

**ehildenb** (2019-01-14):

The post that remains hidden says:

Great to see other people championing this! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Feel free to open issues against the KEVM repository (at LINK REDACTED FOR SOME REASON) if you find places where it could be clearer or could use more explanation. The Jello Paper is derived from that repository directly.

---

**gcolvin** (2019-01-15):

Thanks [@ehildenb](/u/ehildenb)  To be clear, [@grosu](/u/grosu) and [@expede](/u/expede), I’m a big fan of K-EVM and the Jello Paper.  I’m also a big fan of the work to maintain and improve the Yellow Paper.  But I’m becoming convinced that given our anarchy there is nobody to declare one spec normative, only community consensus that certain specs are useful.   And given the computational consensus network we are building there is no need for a normative spec; the network itself is normative.  To mangle Heinlein, [“The blockchain is a harsh mistress.”](https://archive.org/details/TheMoonIsAHarshMistress_201701)

---

**expede** (2019-01-16):

Hmm, I’m not sure why LOC would matter here. [@gcolvin](/u/gcolvin) am I missing something here? IMO a spec should be complete and clear, without regard for length (either short or long)

Anyhow, here’s some information in a table

|  | kLOC | Language | Style | Executable | Complete | Days Since Update |
| --- | --- | --- | --- | --- | --- | --- |
| Yellow | ~1.3 | LaTeX | Prose & Equations |  | Mostly | 37 |
| Beige | 1.3 | LaTeX | Prose |  |  | 249 |
| Jello | 2.4 | K | Declarative |  |  | 7 |
| Trinity | 2.9 | Python | Imperative |  |  | 0 |
| Aleth | 2.4 | C++ | Imperative |  |  | 0 |

---

**expede** (2019-01-16):

> To be clear, @grosu and @expede, I’m a big fan of K-EVM and the Jello Paper.

![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=12)![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=12)![:tada:](https://ethereum-magicians.org/images/emoji/twitter/tada.png?v=12) ![:mage:](https://ethereum-magicians.org/images/emoji/twitter/mage.png?v=12)

> there is no need for a normative spec

![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12) Thinking out loud

Interesting. Shouldn’t the semantics of the execution engine be strongly guaranteed by the platform, lest a network split occur from differing state? AFAICT Ethereum is intended to have a logically centralized VM. Such an event would get healed, and is absolutely possible today, but also would cause some general thrash in the system (uncle rate), which should be best avoided, no?

---

**expede** (2019-01-16):

*TL;DR an impassioned defense of the Jello Paper’s notation*

I’m trying to balance facilitating discussion and being opinionated ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=9) Take the following with a grain of salt, and opposing viewpoints are *very strongly* encouraged!

While almost everyone that I speak to is immediately positive about moving to the JP, I feel like there’s two points of resistance:

1. No one seems to love the YP’s notation as-is, but some have already invested in learning it
2. Don’t want to invest in learning a new notation / assume K is for math geniuses only

K doesn’t read like the PLT literature (aside from BNF). As such, there’s no special advantage on first reading of the JP vs YP, even for people with such a background (omitting those who already know K). From an informal sample, K appears to be much easier to grok for programmers than judgements or the lambda calculus. Further, being that it’s executable (and formalized), the JP has no option but to be extremely clear about all details, which is what you want out of a spec.

The YP’s notation *also* takes some getting used to. I personally find its syntax to be unnecessarily dense (ex. “which μ subscript is which again?”). Also some details are unclear, so I found myself repeatedly referring to concrete implementations (mainly Parity and Trinity) while writing my implementation based on the YP. It’s a a small sample, but I hear this from others as well. Admittedly this could be corrected in the notation and prose, but this paper is almost 5 years old and still reads this way ![:woman_shrugging:](https://ethereum-magicians.org/images/emoji/twitter/woman_shrugging.png?v=9)

---

**expede** (2019-01-18):

I’m just going to vaguely gesture at this thread as more reason to have a formally verified spec. Explicit invariant are also very important. We can go pretty far enshrining invariants in the system



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png)
    [Immutables, invariants, and upgradability](https://ethereum-magicians.org/t/immutables-invariants-and-upgradability/2440) [EIPs](/c/eips/5)



> One of the critical meta-questions raised by Remediations for EIP-1283 reentrancy bug and the delay of the Constantinople upgrade is: Precisely what on Ethereum is immutable and what behavior should be considered invariant?
> Since irregular state transitions are outside the scope of this conversation, for sake of argument let’s all agree that code and data (storage) are immutable.
> However, we’re left with the challenge that EVM semantics can and do change during a hard fork, the most germane ex…

I personally would love if the community would take a first-principles approach on Ethereum, with only explicit invariants. The current system is loose enough to make spec change conversations difficult.


*(52 more replies not shown)*
