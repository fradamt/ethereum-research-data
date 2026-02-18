---
source: ethresearch
topic_id: 18918
title: Promoting Ethereum Research to facilitate interdisciplinary collaboration and academic user engagement
author: Mirror
date: "2024-03-10"
category: Administrivia
tags: []
url: https://ethresear.ch/t/promoting-ethereum-research-to-facilitate-interdisciplinary-collaboration-and-academic-user-engagement/18918
views: 5831
likes: 75
posts_count: 18
---

# Promoting Ethereum Research to facilitate interdisciplinary collaboration and academic user engagement

It’s delightful to see our community thriving, with an increasing number of lengthy research papers and constructive technical insights being published on this forum. Ethereum Research has become the main battlefield for Ethereum innovators to delve into research. I take pride in the growth of the community and express gratitude to those who share their research insights on this forum.

As a researcher in Ethereum technology, I would like to discuss the challenges I have encountered. When I publish articles on Ethereum Research, they are not easily searchable on Google Scholar, and I have to manually add them to my Google Scholar profile. This has led me to ponder: how can we ensure that the research and creativity on this forum are discovered, discussed, and cited by more enthusiasts more effectively and efficiently?

A prime example is a twitter bot [@ethreserchbot](https://x.com/ethresearchbot?s=11)

It effectively extends the research of this forum to the user community on Twitter, and uses AI to summarize complex studies, making them more accessible to other researchers.

I want to emphasize that this is crucial! Since the establishment of the scientific research system, a large amount of research progress has been generated through interdisciplinary collaboration. Speaking of which, we need to mention blockchain again. Today’s blockchain discipline is a hybrid discipline composed of computer science, cryptography, statistics, finance, social sciences, and various game theories. Blockchain was born from the collision of finance and computer science, becoming a gem of this era against political authority and financial hegemony.

How to facilitate interdisciplinary research? It’s quite simple: make it more visible. By providing academic grants, collaborating with universities, and extensively recruiting researchers, Ethereum has established a vast knowledge network. However, for traditional researchers, it may not be very user-friendly, primarily due to the challenge of knowledge discovery. So, how can this be improved?

One straightforward approach is to periodically compile forum content into paper collections similar to preprints for publication. Assigning a DOI number to each article would enable quick retrieval in various academic search engines, facilitating easier citation and dissemination.

I look forward to seeing more ideas for promoting research on this forum. If you believe there are any mistakes in what I have said, I welcome criticism and corrections, as well as any valuable suggestions for improvement.

## Replies

**nicszerman** (2024-03-10):

Right on. Only minor point where I disagree on format: compile knowledge into indexable posts, not into papers.

---

**Val** (2024-03-10):

Hi Mirror I completely agree with you regarding the distribution of research and the following questions and statements:

> how can we ensure that the research and creativity on this forum are discovered, discussed, and cited by more enthusiasts more effectively and efficiently?

> It’s quite simple: make it more visible

> However, for traditional researchers, it may not be very user-friendly, primarily due to the challenge of knowledge discovery. So, how can this be improved?

> more ideas for promoting research on this forum.

which all inscribe well in the perspective of the project I created thanks to the large support provided by Flashbots:  [mev.fyi](https://www.mev.fyi), the open-source MEV research chatbot announced [here](https://twitter.com/unlock_VALue/status/1763270581116432733). I indexed all the content from mevfyi’s vector database which the chatbot can access.

This database is displayed on the [MEV Research Hub](https://data.mev.fyi) and the underlying code indexing this content is available in this set of [repos](https://repos.mev.fyi) (the data repo more specifically).

mevfyi has a [Twitter bot](https://twitter.com/unlock_VALue/status/1763270591627346084) that users can directly tag in-thread to ask questions while having the thread as context, further helping the distribution of that *vast knowledge network* as you coined it.

What would be helpful at our stage of both mev.fyi and likely [ethresearchbot](https://twitter.com/ethresearchbot), are the following elements:

- even greater discovery, sharing, namely:

among our first target group namely blockchain research hobbyists and connoisseurs,  where I expect Twitter and Discord channels to have the largest expected impact
- and cascading groups of traditional academic networks and universities (including student organisations). I do not have a large network there though I expect a sales approach with dozens of cold emails to have an impact
- leverage SEO expertise (which I do not have)
- should anybody have other channels and go-to-market strategies in mind please suggest them on that same post. I expanded a bit on the topic here about mevfyi

grants to fund both maintenance and future development of such open-source public goods

- from a feature perspective
- from a reach/marketing perspective
- and more that could provide a better reach per dollar/eth funded

---

**0xdestroyr** (2024-03-10):

I’m so glad you’ve found @ethresearchbot to be helpful, we’ve had such a great time building it and watching it gain traction. If anyone has any features they would like to see added please let me know!

---

**KMontag42** (2024-03-10):

@ethresearchbot has been an awesome project to work on and share with the community. Thanks for the shout out!

As someone who has lurked on these boards for many years I’m happy to be able to give back ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**ziyinlox-purple** (2024-03-11):

Agree with you. I think many researches can be compiled into indexable posts, such as threads, which means whether you’re a particularly advanced researcher or not, you can quickly get the general idea.

---

**bowaggoner** (2024-03-11):

Great to see this post. I’m in academia. I think the challenge here is the life cycle of an idea. First it is exploratory. Then it becomes more fully fleshed out. Then it is rigorously tested and turns from an idea into “knowledge”. In academia, at that final point it’s written up in a paper designed to communicate a unit of digestible knowledge (and it’s peer-reviewed, etc). Normally when we cite something or see it pop up somewhere like Google scholar, we’d expect it to be at that final stage.

Ethresearch posts are usually somewhere earlier in the lifecycle. If a researcher wants to engage with the development of an idea, just like discussing at a workshop, ethresearch posts are fantastic. But if it were framed as a repository of “knowledge” like a journal full of papers that one can cite, I think that would create a mismatch of expectations as far as academics are concerned. I think it’s better to frame ethresearch as a community where interesting ideas are discussed and developed. Hope this feedback is helpful.

(Added) And to help with the goal of disseminating the research of the community, I’d love to see the conclusions from productive threads written up into papers of their own and published somewhere as a self-contained paper instead of spread out among a conversation that is going to be hard for someone to read and digest in the future. That could be an approach to what you’re getting at in the first post on this thread!

---

**barnabe** (2024-03-11):

Thank you Bo for this perspective, and thank you [@Mirror](/u/mirror) for starting this thread! From a pragmatic point of view, I had looked into the requirements for this (Discourse) forum to be indexed by Google Scholar, and I don’t think the requirements can be satisfied so easily, but the documentation is also [pretty sparse](https://scholar.google.com/intl/en/scholar/inclusion.html#crawl). At a higher level, it may not be valuable to default to indexing all posts on the forum. Notwithstanding the (generally high!) quality of the posts, I agree with Bo that even some of the most important new ideas which were posted here in the first place might not have reached “final form” stage.

Generally, there are two problems we may want to consider:

- Discovery: How do we ensure that the right audiences read the posts that are relevant to them.
- Attribution: How do we ensure that the ideas are rightfully attributed to their originators.

I’ll deal with attribution first. Many people who post on ethresear.ch do not really care for citation counts and are driven by sharing early ideas to elicit feedback and “checkpoint” their work. Despite this, I sometimes worry that improper attribution (e.g., a research paper is written by a different set of authors mining ideas from the forum) may lead to discouragement or protectionism: Researchers will be less inclined to share early ideas or communicate on ethresear.ch. This is more of an issue especially for ideas that are closer to “final form”, where the ethresear.ch post is almost like a “mini-paper”. In this case, I think it would be good to have a way to standardise and index these posts such that they are available on Scholar and other databases for easy citation in research works. This doesn’t prevent idea mining entirely, but it may create a stronger moat by making the research artefact visible to the protocols that academics use. We could look into ways to obtain e.g., a DOI and offer this approach to authors whose work is fleshed out enough (or this could also be permissionless), I know of [Zenodo](https://zenodo.org/) for instance but also keen to hear if anyone here has experience with different registries.

The question of discovery is also important. Here the process is more diffuse, authors will hopefully champion their own ideas, take them forward into papers or conference talks, but there may also be good ideas for which the authors are unsure how to cross the chasm. I like the idea of a periodic “review” of ethresear.ch, which could collect significant works published during some period of time. The angle could be “here are promising ideas that we think deserve more eyeballs”, but the question as always is who is the “we” in there (there is always the “objective” solution to use likes or views but in this airdrop economy that seems ill-fated ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)). As Bo writes, it would also be optimal in certain cases to have a paper written out of some productive discussion, though that’s not always possible for the original authors due to time constraints or unfamiliarity with the format. I’ll note here that grants may help to create bandwidth for the author and match them with useful resources, and having a strong early work published on ethresear.ch is probably one of the highest quality signals.

(note that I am a mod since recently but these are my personal opinions)

Edit: Also wanted to acknowledge the great work of the ethresearchbot, and mev.fyi ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**Julian** (2024-03-11):

The bot is really great! Are you considering building a bot for Farcaster as well?

---

**Mirror** (2024-03-11):

It makes sense, I agree with your first two responses. I hold a different opinion on the third point because the creativity in research and discussions on this forum has far surpassed that of most journals or conferences. At the same time, knowledge from diverse fields of Ethereum converges on this forum while journals and conferences usually only showcase one specific field, which is neither conducive to innovation nor to reading. Additionally, I have also considered the issue of research cycle delays brought about by peer review, and I believe a form similar to preprints is appropriate.Encourage interdisciplinary integration rather than further subdivision.

---

**Mirror** (2024-03-11):

Thank you for your response, your perspective is much better than my initial rough idea. The premise of my proposal is also based on the increasing number of ‘mini-papers’ close to final papers in the forum, which can prevent plagiarism and facilitate citation through DOIs. However, it is really difficult to make an objective evaluation of which article is a significant work. Building on your response, I would like to make a suggestion: anyone can consider their work as significant (being indexed), as long as they write it in a standardized format to meet certain requirements, similar to preprints.

---

**bowaggoner** (2024-03-11):

Hi Mirror, I strongly agree that the creativity and potential value of discussions on ethresearch is very high. And I think preprints are great. I like your idea of letting people opt-in to their work being considered an official preprint and being indexed. Although, I’m not sure if the first post of an ethresearch thread is the best format for that, or if it should be posted as a stand-alone document or page or post in some way.

---

**Mirror** (2024-03-12):

I am also not sure what kind of format would be more appropriate, it seems we need more people to join the discussion.

---

**0xemperor** (2024-03-12):

The most natural bucket forum posts might fall under is if they are rewritten as blogs with some responses from others and then rebuttals by authors. A good rule to attribution is always “be generous in attribution, and critical in order (if you wish to be)”, I am not sure how it works in crypto research but if the order of author matters then the one who wrote the post should be first, and then perhaps some randomized or order by likes received. The only issue when it comes to forum posts being indexed is noise, not all posts pass scrutiny to pass as “work” and are blog posts to gather or collect thoughts sometimes.

For starters, for those who are interested in such attribution, posts could be ended with, some indexers also allow @blog, but @misc is the best. I think *beginning* somewhere for those interested and iterating towards a final format is better than being very pedantic in trying to index these. Ultimately an author of a post on forums like ethresearch is well aware of the quality of work they’ve put forth and can be trusted to know if a post should be attributed or not.

```auto
@misc{,
    title={

},
    author={

},
    year={2023},
    eprint={<>},
    archivePrefix={<>},
    primaryClass={<>}
}
```

---

**ed** (2024-03-12):

Hi!  I run the [ethrd Farcaster](https://warpcast.com/~/channel/ethrd) channel, and I’d love to integrate @ethresearchbot into a frame on the channel.  I’m happy to do the work myself if you could point me to the code.  (Sorry in advance if the code is obviously public; I searched for a repo but couldn’t find one.)

---

**0xdestroyr** (2024-03-12):

[@KMontag42](/u/kmontag42) and I will get the bot set up on Farcaster this week, I’ll shoot you a message when it’s live.

---

**DonMartin3z** (2024-04-19):

This is a solid appointment sir, but i guess that just using your answers are not enough. For my perspective, you’re trying to “pierce a bubble” i Guess that there is a solid way to do that: add universitie’s profiles and student’s users officially on ethereum by the use of .eth domains and solid endorsement from ethereum foundation. This could enhance the productivy and presence of vibrant energy on the forum, as well leading to the solve of many challenges.

---

**Pfed-prog** (2024-05-07):

I can not find a better place to ask Ethereum related questions, but unfortunately the banning is getting out of hand. I would really appreciate an opportunity to create threads on the governance forum without the fear of getting banned.

For example, right now I am building an alternative to Etherscan with Blockscout, can I create a thread asking for features that I should include on this forum?

