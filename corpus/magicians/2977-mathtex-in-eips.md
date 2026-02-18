---
source: magicians
topic_id: 2977
title: MathTeX in EIPs
author: fulldecent
date: "2019-03-24"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/mathtex-in-eips/2977
views: 783
likes: 1
posts_count: 2
---

# MathTeX in EIPs

GitHub pages has partial support for using MathTeX in GitHub pages (which is the mechanism used to publish EIPs to [eips.ethereum.org](http://eips.ethereum.org)).

We can fix it so that these expressions will render properly in the browser.

Issue: https://github.com/ethereum/EIPs/issues/1860

MathTeX just lets you put math TeX expressions inline in a paragraph or as their own expression block. If you’ve used TeX it looks like this:

$$y = \sqrt(x)$$

and it renders perfectly just like in every math book you have ever read. That is because every math book you have ever read uses TeX.

## Replies

**boris** (2019-03-24):

I left a comment on the issue. It may be simpler than that.

Let’s see if this is turned on in Discourse. Edit: nope!

Anyway, should be pretty simple to do.

---

$$

\begin{align*}

& \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right)

= \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \

& (x_1, \ldots, x_n) \left( \begin{array}{ccc}

\phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \

\vdots & \ddots & \vdots \

\phi(e_n, e_1) & \cdots & \phi(e_n, e_n)

\end{array} \right)

\left( \begin{array}{c}

y_1 \

\vdots \

y_n

\end{array} \right)

\end{align*}

$$

