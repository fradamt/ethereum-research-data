---
source: ethresearch
topic_id: 8
title: Read this before posting
author: system
date: "2017-08-17"
category: Administrivia
tags: []
url: https://ethresear.ch/t/read-this-before-posting/8
views: 59173
likes: 62
posts_count: 9
---

# Read this before posting

This is a semi-public forum for participating in Ethereum’s research efforts, including but not limited to:

- Proof-of-Stake
- Scaling solutions
- EVM improvements
- Low-level protocol improvements
- Economics

protocol economics
- Resource pricing economics

Other second-level features

This is **not** the place for:

- generic ethereum discussion.  For that visit r/ethereum.
- discussing specific EIPs.  For that visit the Ethereum Magicians forum.
- technical questions and ELI5s. For that visit the StackExchange.

If your signal-to-noise ratio gets too low, **you will be banned from ethresear.ch**.  So please keep discussions information-rich.  Posting on this site is accepting releasing your submitted content into the **public domain** ([CC0](https://creativecommons.org/publicdomain/zero/1.0/)).

# Forum Features!

## 1. LaTeX Equations

This forum supports \LaTeX equations between $dollar signs$.  The default LaTeX style is the “inline” style which looks like \sum_{k=0}^n {n \choose k} = 2^n , in text this is

```auto
$ \sum_{k=0}^n {n \choose k} = 2^n $
```

However, if you start your equation with $$ on it’s own beginning and teminating line like,

```auto
$$
\sum_{k=0}^n {n \choose k} = 2^n
$$
```

it looks like this

\sum_{k=0}^n {n \choose k} = 2^n

---

## 2. Graphviz diagrams

See the documentation for a [list of examples](https://graphs.grevian.org/example) to build your graph.

```auto
[graphviz engine=dot]
digraph {
  concentrate=true;
  a[color=red, style=filled, fillcolor=pink];
  b[shape=diamond];
  a -> b;
  b -> c;
  c -> a;
  d -> c;
  e -> c;
  e -> a;
  a -> e;
}
[/graphviz]
```

a

a

b

b

a->b

e

e

a->e

c

c

b->c

c->a

d

d

d->c

e->c

---

## 3. YUML diagrams

[YUML diagrams](https://yuml.me/diagram/scruffy/class/samples) allow making nice little graphs within your posts.

They have an idiosyncratic but fairly simple markup language.

Example:

![image](https://ethresear.ch/uploads/default/original/2X/6/6cda7a2b39ec24a1fcf8d534194440e424283c23.svg)

```auto
[yuml]
[foo{bg:cornsilk}]--[baz]
[foo]->[bar{bg:orange}]
[baz]-.->[qux]
[qux]--label>[bar]
[/yuml]
```

![image](https://ethresear.ch/uploads/default/original/2X/8/8e9d3cc9e5fad5a46d35977caf02bf17fe5447f8.svg)

```auto
[yuml]
[Vote Message|+Source hash;-Source height;+Target hash;-Target height|+Withdraw();+Last_commit]
[/yuml]
```

---

## 4. Images!

Unsurprisingly, we also support images.

[![u1](https://ethresear.ch/uploads/default/original/1X/f155892dd1d8921e9afeb4407aa241d16a6a0c84.jpg)u1614×800 57.9 KB](https://ethresear.ch/uploads/default/f155892dd1d8921e9afeb4407aa241d16a6a0c84)

---

## Useful sites

- Ethereum dot org - https://ethereum.org/
- Upgrading Ethereum by Ben Edgington - https://eth2book.info/

## Replies

**captnbli** (2026-01-04):

My issue is I can’t post a new topic, having just joined, which is what I want to do, And how I achieve that is not explained, or available to me on FF/Linux.

Thanks, Pete

---

**abcoathup** (2026-01-04):

Hey Pete, In Discourse forums you can’t create a new topic until you have done spent some time reading.

Recommend that you read multiple topics first, you should then automatically earn a Basic badge.   https://ethresear.ch/u/captnbli/badges

So far you have spent 9 minutes reading: https://ethresear.ch/u/captnbli/summary

---

**captnbli** (2026-01-05):

Well, I understand your policy. I t must be difficult to keep things focused.

but looking forward to posting my saved post. I think there is a time limit. Is it “as well” or “either”?

---

**abcoathup** (2026-01-05):

I don’t know what settings Eth Research uses, I am just a regular user like everyone else.

Default Discourse is time spent reading and reading X posts: [Understanding Discourse Trust Levels](https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/)

---

**ngrawlings** (2026-02-02):

I have some research I would like to post. I did reply to a previous post as I can not post new topics. The research is related to Post Quantum. It is credible. The maths works, so hardly crack pot stuff and it does at very least raise a perspective to consider.

That reply was removed, probably for not being relevant to the post it was under.

How do I do about posting this research?

---

**abcoathup** (2026-02-03):

[@ngrawlings](/u/ngrawlings) in Discourse forums (such as Eth Research) you can’t create a new topic until you have spent time reading multiple topics.

Recommend you read the [post-quantum](/tag/post-quantum) topics and the replies.  I’m not a mod/admin here, so don’t know the specific settings.

---

**brighammurdoch-byte** (2026-02-04):

Hey! I’m an Economics/Data student who is interested in working in blockchain based tokennomics and incentives design! I’m wondering if I could get some information on the best places to start. If anyone has some suggestions plese let me know!

Also, if someone could point me to the biggest topics and proposals being discussed right now that would be verry helpful! I have a good high level understaning of Ethereum but don’t know much of the nitty gritty.

---

**umamimi** (2026-02-05):

nonce classic has published their guide to understand the tokenomics. It would be your good start and you can find more resources based on this basic. I hope you would find this interesting.

Google “Tokenomics Design 101 for Early Stage Crypto Startups” then find it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

