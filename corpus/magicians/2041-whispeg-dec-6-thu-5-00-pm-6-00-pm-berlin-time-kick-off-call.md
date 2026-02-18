---
source: magicians
topic_id: 2041
title: "[WhiSpeG]: Dec 6 THU 5:00 PM - 6:00 PM (Berlin Time) - kick-off call Whisper Specification Group"
author: Ethernian
date: "2018-11-27"
category: Working Groups
tags: [whisper]
url: https://ethereum-magicians.org/t/whispeg-dec-6-thu-5-00-pm-6-00-pm-berlin-time-kick-off-call-whisper-specification-group/2041
views: 1016
likes: 13
posts_count: 13
---

# [WhiSpeG]: Dec 6 THU 5:00 PM - 6:00 PM (Berlin Time) - kick-off call Whisper Specification Group

Hello all!

We are planning our first kick-off hangout call of WhiSpeG - Whisper Specification Group.

**Agenda:**

- Broader look over messaging solutions. Is whisper deprecated? (I think - it is NOT)
- Review whisper specification efforts already made by others.
- What do we have about whisper besides the code?
- What do we expect from whisper specification.
- Move from Telegram to Riot?
- ToDos & Roadmap.

**Please share your thoughts before the meeting here:**


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/RerjC_3aRtKToGJEi0sJKw)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###










[Here is doodle](https://doodle.com/poll/i9genenvw4p5zccc#calendar) to find the time slot.

===> UPDATE:

Doodle is closed. The Call time is on

** When:

Dec 6 2018 - Thursday

5:00 pm - 6:00 pm (Berlin Time)**

**8:00 am - 9:00 am (San Francisco Time)**

**Where:

===> UPDATE 2:

~~Hangout (deprecated)~~   => Zoom

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atoulme/48/1323_2.png) atoulme:

> Antoine Toulme is inviting you to a scheduled Zoom meeting.
>
>
> Topic: Whisper spec meeting
> Time: Dec 6, 2018 8:00 AM Pacific Time (US and Canada)
>
>
> Join Zoom Meeting
> Launch Meeting - Zoom
>
>
> One tap mobile
> +16699006833,521536173# US (San Jose)
> +16468769923,521536173# US (New York)
>
>
> Dial by your location
> +1 669 900 6833 US (San Jose)
> +1 646 876 9923 US (New York)
> +1 877 853 5257 US Toll-free
> +1 855 880 1246 US Toll-free
> Meeting ID: 521 536 173
> Find your local number: https://zoom.us/u/akNlpXV7h

===>

Currently we are 13 person from different corps and projects.

If you are interested to get in touch, let me know.

## Replies

**boris** (2018-11-28):

It looks like more effort into Whisper is going to be eclipsed by some Web3 Foundation work https://github.com/w3f/messaging/blob/master/README.md

---

**Ethernian** (2018-11-28):

> It looks like more effort into Whisper is going to be eclipsed by some Web3 Foundation work

Yes, we are currently talking exact about it. If you are interested, I could add you into Telegram group.

---

**ligi** (2018-11-28):

> I could add you into Telegram group.

can we please stop using a closed source apps for communication inside this space? There are alternatives like [matrix]

---

**Ethernian** (2018-11-28):

ok. valid concern, will take it in account next time.

The problem is, that some discussions start from ad-hoc conversation of two people.

---

**5chdn** (2018-11-28):

Use Wire for ad-hoc conversations. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

Re: whisper, from what I understand it’s not only the Web3 Foundation but also Status IM interested in that research “beyond” whisper.

*Edit: Just realized how funny this is, we are discussing messengers in the whisper thread.*

---

**Ethernian** (2018-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5chdn/48/1242_2.png) 5chdn:

> Re: whisper, from what I understand it’s not only the Web3 Foundation but also Status IM interested in that research “beyond” whisper.

we have Status & ConsenSys people in chat (and one big corp more - possibly they will reveal their name later. Unsure how official their participation is now). Plus authors from other messaging protocols.

Possibly it will make sense to merge the chat into some other existing one.

---

**Ethernian** (2018-12-01):

The call time is fix now.

** When:**

Dec 6 2018 - Thursday

5:00 pm - 6:00 pm (Berlin Time)

8:00 am - 9:00 am (San Francisco Time)

**Where:**

Hangout.

The link will be posted here and in TG group ~1 day before the call.

Here is the link to (already closed) [doodle poll](https://doodle.com/poll/i9genenvw4p5zccc#calendar).

**Agenda:**

- Broader look over messaging solutions. Is whisper deprecated?
- Review whisper specification efforts already made by others.
- What do we have about whisper besides the code?
- What do we expect from whisper specification.
- Move from Telegram to Riot?
- ToDos & Roadmap.

Do you have suggestions and more agenda topics? - Let me know.

---

**wschwab** (2018-12-03):

[@Ethernian](/u/ethernian) Do you want this to be just for folks seriously involved in Whisper development, or is it also intended for sideline spectators?

---

**Ethernian** (2018-12-03):

[@wschwab](/u/wschwab),

The call is free to join, and we need need both:

- people who need whisper specification (users)
- people who develop whisper and other messaging protocols (developers)

---

**andytudhope** (2018-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Is whisper deprecated?

This makes me sad. Status uses it in production, as does [Bloom](https://blog.hellobloom.io/introducing-bloom-payment-channels-enabled-by-ethereum-whisper-1fec8ba10a03) for something entirely different, as do some other [interesting](https://www.resbank.co.za/Lists/News%20and%20Publications/Attachments/8491/SARB_ProjectKhokha%2020180605.pdf) and technically advanced projects. I would like to see that removed from the agenda so the focus is on more useful topics like “what we expect from the whisper specification”. That is,

1. Is whisper intended really just for DApps, as Gav and Parity have always said, or should/can we use it for broader communications? If it is just for DApps, is it not already sufficient?
2. If we can’t use it for broader comms, then do we need another spec (i.e. what is starting to be discussed between Status, the W3F and others) for secure person-to-person messaging and, if so,
3. What should the properties of this new spec ideally be such that it meets our needs as an ecosystem/community?

I have already suggested we use the [#whisper](https://get.status.im/public/chat/whisper) topic to discuss this, but got told off for doing so. I still maintain that actually using the protocol is the best way to:

1. Ask better questions.
2. Understand what the current capabilities really are so as to drive informed dicussion about further development.

---

**Ethernian** (2018-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/andytudhope/48/45_2.png) andytudhope:

> Is whisper deprecated?
> This makes me sad

Hey, this is a question! There is a “?” at the end of the sentence!

I personally think, it is NOT deprecated!

---

**Ethernian** (2018-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atoulme/48/1323_2.png) atoulme:

> Antoine Toulme is inviting you to a scheduled Zoom meeting.
>
>
> Topic: Whisper spec meeting
> Time: Dec 6, 2018 8:00 AM Pacific Time (US and Canada)
>
>
> Join Zoom Meeting
> Launch Meeting - Zoom
>
>
> One tap mobile
> +16699006833,521536173# US (San Jose)
> +16468769923,521536173# US (New York)
>
>
> Dial by your location
> +1 669 900 6833 US (San Jose)
> +1 646 876 9923 US (New York)
> +1 877 853 5257 US Toll-free
> +1 855 880 1246 US Toll-free
> Meeting ID: 521 536 173
> Find your local number: https://zoom.us/u/akNlpXV7h

Guys, it is Zoom instead of hangout.

**Please share your thoughts before the meeting here:**


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/RerjC_3aRtKToGJEi0sJKw)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###










cc [@ligi](/u/ligi)

