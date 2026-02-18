---
source: magicians
topic_id: 6523
title: Installed "Discourse Math Plugin" for using LaTeX in comments
author: jpitts
date: "2021-06-22"
category: Protocol Calls & happenings > Announcements
tags: []
url: https://ethereum-magicians.org/t/installed-discourse-math-plugin-for-using-latex-in-comments/6523
views: 1043
likes: 2
posts_count: 4
---

# Installed "Discourse Math Plugin" for using LaTeX in comments

This is to announce that with the latest upgrade we have installed the Discourse Math Plugin. Thanks [@hwwang](/u/hwwang) for the suggestion!


      ![](https://ethereum-magicians.org/uploads/default/original/2X/1/1b0984d7ee08bce90572f46a1950e1ced436d028.png)

      [Discourse Meta – 16 Jul 25](https://meta.discourse.org/t/discourse-math/65770)



    ![image](https://d11a6trkgmumsb.cloudfront.net/optimized/4X/0/7/8/0783e5858f4219b6624393a8e9ffad5ecdfec133_2_1024x62.png)



###





          Plugin






            official
            math
            included-in-core







:discourse2: Summary Discourse Math uses MathJax (default) or KaTeX to render maths in your Discourse forum.   📖 Install Guide This plugin is  bundled with Discourse core. There is no need to install the plugin separately.     Enabling Math The...



    Reading time: 10 mins 🕑
      Likes: 129 ❤

## Replies

**xinbenlv** (2022-11-28):

Thank you for doing this. But it seems not working right now

I missing be something here, could you help me out or check if this Math plugin is working?



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png)

      [EIP-5982 Role-based Access Control](https://ethereum-magicians.org/t/eip-5982-role-based-access-control/11759/7) [EIPs](/c/eips/5)




> We are definitely happy to add these events into IERC_ACL_CORE if getting your support, but if I may take sometime to clarify and make sure we are on the same page about the implications.
> We want this new EIP to be compatible to OpenZeppelin, more specifically we are looking at IAccessControl.sol between OZ v4.4.1 - v.4.8.0
> Therefore the methods and events of IERC_ACL_CORE needs to be a subset of AccessControl.sol
> $$
> S_{IERC_ACL_CORE} \subset S_{OZAcessControl.sol}
> $$
> The events of questio…

```auto
$$
S_{IERC_ACL_CORE} \subset S_{OZAcessControl.sol}
$$
```

Yields unrendered as shown

[![2022-11-28_08-46-30](https://ethereum-magicians.org/uploads/default/original/2X/2/203473a9ff244ff1304133bffb9f6b329e88cbda.png)2022-11-28_08-46-30772×138 6.38 KB](https://ethereum-magicians.org/uploads/default/203473a9ff244ff1304133bffb9f6b329e88cbda)

---

**Pandapip1** (2022-11-28):

Test:

$hello_{world}$

EDIT: Can confirm that the tex doesn’t work.

---

**anett** (2022-12-06):

[@jpitts](/u/jpitts) can we update the plugin ?

