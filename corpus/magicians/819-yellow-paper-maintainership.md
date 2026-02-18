---
source: magicians
topic_id: 819
title: Yellow Paper Maintainership
author: ldct
date: "2018-07-20"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/yellow-paper-maintainership/819
views: 1926
likes: 18
posts_count: 14
---

# Yellow Paper Maintainership

Is anyone maintaining / reviewing PRs for the yellow paper (https://github.com/ethereum/yellowpaper)?

I’ve found it useful in the past as an authoritative source in which to look up stuff (when I couldn’t find the answer elsewhere) and would be sad to see it become unmaintained.

## Replies

**boris** (2018-07-20):

The only commits I saw were from [@pirapira](/u/pirapira) and I know he was taking a break. Regardless, having only one person do all the commits and reviews for a community resource is not ideal.

A broader discussion is if the EF can come up with a policy of adding community maintainers.

Hey [@souptacular](/u/souptacular) – any thoughts on adding maintainers to certain EF repos?

---

**jpitts** (2019-01-08):

**Important update on this topic:**

I have been in contact with researchers at the Kestrel Institute who are a part of the [ACL2 Ethereum Project](https://www.kestrel.edu/home/projects/ethereum/). This project has received a grant from the Ethereum Foundation to continue this formal verification work using [ACL2](https://www.cs.utexas.edu/users/moore/acl2/). The team has expressed interest in participating in a working group to maintain the Yellow Paper and keep it current.

Just before the end of year vacation period, I had a call with Eric McCarthy (the PI on the project), Alessandro Coglio, and Eric Smith. I will soon start posting on the Forum and elsewhere to try to find others to participate in a Yellow Paper Circle or working group.

---

**boris** (2019-01-08):

Thanks [@jpitts](/u/jpitts)

I *just* posted a Maintainers page on the Ethereum wiki — https://en.ethereum.wiki/maintainers

Currently Nick Savers is the listed YP maintainer.

---

**ChainSafe** (2019-01-08):

[@ansermino](/u/ansermino) from our team is interested in getting involved in a yellow paper working group ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**jpitts** (2019-01-09):

I’m glad to hear this!

I have taken note of [@ansermino](/u/ansermino)’s interest. Also, I have created a Google Form with which to voice interest in this group, so please add more info there if you wish.

**Yellow Paper Maintainership Interest Form**

https://goo.gl/forms/xItvS9YvIrkB5od53

---

**boris** (2019-01-09):

I don’t think we need a form. There is already the repo https://github.com/ethereum/yellowpaper – so commenting on the issues and proposing & reviewing the PRs is the work to be done.

Asking Nick Savers to be co-maintainer or repo powers might be warranted if we see that issues aren’t being replied to promptly.

---

**jpitts** (2019-01-10):

At this point I believe it is unknown who or what group is maintaining the Yellow Paper; I’ll ping Nick Savers to see what his interest level is at this point.

RE: the form, I thought it would be good to collect names of people wider than just here on the Forum and on the current GitHub repo. I am not even sure if a YP group would become a Ring adopting Magicians’ principles, or a working group on its own.

---

**boris** (2019-01-10):

Let’s ask!

I posted an issue to the repo — [Maintainer(s) for this repo · Issue #725 · ethereum/yellowpaper · GitHub](https://github.com/ethereum/yellowpaper/issues/725)

I’m also going to post another issue asking if YellowPaperDotIO is dead permanently ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=9)

---

**boris** (2019-01-10):

Got a response!  https://github.com/ethereum/yellowpaper/issues/725

---

**jpitts** (2019-01-10):

Thanks [@boris](/u/boris)! I actually hadn’t realized that he was on the repo, but this is Allessandro, who works on ACL2 Ethereum Project.

Seeing [@expede](/u/expede)’s “[Jello as the canonical EVM spec](https://ethereum-magicians.org/t/jello-paper-as-canonical-evm-spec/2389)” post, perhaps this call to action should be something more along the lines of “Maintainership of Specification of Ethereum”, and they could see to it that the YP is part of its discussions and that there are appropriate maintainers on the YP repo.

This is the ethos expressed to be by Eric McCarthy from the ACL2 Ethereum Project. He emphasized that the YP doesn’t have the be “THE spec”, rather maintained by those wishing to use its mathematics in formal verification efforts w/ K framework, ACL2, etc.

It will be interesting to see what would be the best way to represent THE specification when you have two very different but interdependent kinds of users: engineers and researchers.

---

**expede** (2019-01-10):

> YP doesn’t have the be “THE spec”, rather maintained by those wishing to use its mathematics in formal verification efforts w/ K framework, ACL2, etc.

As a counterpoint, I worry that having more than one spec could be actively dangerous. How do you make sure that they’re in sync? When they inevitably drift apart (ex. one updates first), which one should you choose? Is there an implicit “higher spec” that they’re both implementations of? One advantage of K is that it can generate text in many styles / forms.

Beyond formalization (ie: as an engineer) the YP has LOTS of ambiguities when trying to write an EVM. The JP is very explicit about how each part works. I agree that the YP is nice in that it uses notation from high school math, but it’s also not written totally straightforwardly, and you need familiarity with its specialized style.

…but that’s me ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12) I’d very much like to hear more thoughts on the topic ![:100:](https://ethereum-magicians.org/images/emoji/twitter/100.png?v=12)

---

**expede** (2019-01-10):

> I’m also going to post another issue asking if YellowPaperDotIO is dead permanently

If so, I may just buy `yellowpaper.club` for $1.70 [source: namecheap] and point it at the PDF. A niche issue for sure, but annoying to have to hunt down every time ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**jpitts** (2019-01-11):

The Twitter thread on YP maintainership referenced below is helpful to understand the greater context of the neglected YP issue, and the closely related topic of alternative, engineer-accessible forms of the Ethereum specification.

From [Christoph Jentzsch](https://twitter.com/ChrJentzsch):

> One of the strong safeguards of #Ethereum was/is one complete technical specification: The yellow paper. This virtue should be upheld and it should always be updated first . Every consensus relevant EIP should have a PR to the yellow paper including the full specification of it.
>
>
> Twitter thread on YP maintainership

