---
source: magicians
topic_id: 3113
title: Auto-rotatation Setting in PWA
author: fubuloubu
date: "2019-04-10"
category: Magicians > Site Feedback
tags: [bug]
url: https://ethereum-magicians.org/t/auto-rotatation-setting-in-pwa/3113
views: 2195
likes: 1
posts_count: 2
---

# Auto-rotatation Setting in PWA

I use this forum (and ethresear.ch) as PWAs on my Android device. For whatever reason, ethresearch PWA respects my chosen OS option for autorotation, whereas this forum’s PWA does not. Seems like some sort of configuration issue to me, but other people have had problems in general. Here is a discourse bug report:


      ![](https://d11a6trkgmumsb.cloudfront.net/optimized/3X/b/3/b33be9538df3547fcf9d1a51a4637d77392ac6f9_2_32x32.png)

      [Discourse Meta – 12 Oct 18](https://meta.discourse.org/t/android-auto-rotate-disabled-not-respected-with-discourse-pwa/99396)



    ![image](https://d11a6trkgmumsb.cloudfront.net/original/4X/4/2/7/42734728531d1b8d4906ac646d5cc06c9ddd52c9.jpeg)



###





          Bug






This only happens with Discourse after you “add to homepage” (creating a Progressive Web App), once added, they don’t respect Auto-Rotate settings and keep rotating even when the setting is disabled on Android.  It’s incredibly frustrating since I...



    Reading time: 1 mins 🕑
      Likes: 17 ❤

## Replies

**fubuloubu** (2019-05-04):

Solve the bug. Ensure you don’t have auto-rotate turned on when you save the app to your screen and it will respect the OS option.

