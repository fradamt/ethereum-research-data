---
source: ethresearch
topic_id: 18614
title: "[Space Program] [Update] Launch Ethereum nodes into GSO （Geosynchronous orbit ）"
author: Mirror
date: "2024-02-08"
category: Networking
tags: []
url: https://ethresear.ch/t/space-program-update-launch-ethereum-nodes-into-gso-geosynchronous-orbit/18614
views: 2418
likes: 9
posts_count: 10
---

# [Space Program] [Update] Launch Ethereum nodes into GSO （Geosynchronous orbit ）

Considering launching an Ethereum node into space, any suggestions?

**Functional objectives:**

Direct communication with ground computer

Running Ethereum Light Nodes

Long running time (over 10 years)

Has certain computer experimental performance

**Plan update:**

1.We need to launch the satellite into geostationary orbit to ensure that it has good communication performance and lifespan.

*Regarding the geostationary orbit:*

*Geosynchronous orbit satellites refer to artificial satellites that operate from west to east in geostationary orbit. Its orbital period is the same as the Earth’s rotation period, which is one stellar day, which is 23 hours, 56 minutes, and 4 seconds; Approximately 35786 km from the ground and 42164 km from the center of the earth. Geosynchronous satellites are commonly used for communication, meteorology, navigation, and military intelligence gathering.*

**Why not launch into lower cost near Earth orbit?**

If launched into LEO orbit, it orbits the Earth in a period of approximately 90 minutes. When entering orbit, there will be a switch on the satellite kit that will be turned on, and the Arduino inside will start running. The LEO orbit is not actually particularly “space”, for example, it is still in the ionosphere, so the radiation received is relatively small. This is also why the International Space Station is at this altitude (high radiation can cause death). However, this can also bring some problems. For example, the atmosphere here still has an impact, so satellites will continue to fall into orbit. Due to various limitations in weight, volume, and payload types (such as the prohibition of high-pressure containers and toxic chemicals), it is difficult to install effective orbit maintenance devices for this type of miniature satellite. Therefore, within 3-16 weeks, the satellite will generally crash into the dense atmosphere and burn down. The specific time depends on the initial altitude of the orbit and the strength of solar activity.

**Regarding satellite production:**

The things satellites can do in space are also limited, in addition to weight limitations, there is also an issue of attitude maintenance. When entering orbit and scattering other small satellites together, the satellite would have entered a rotating state due to collisions or disturbances. How to maintain a stable posture also requires attention. The general method is to install one or more inertial flywheels to balance angular momentum, but once the rotational speed of the flywheels reaches the upper limit, it is completely impossible to maintain balance. So there is also the installation of a small coil to slowly adjust using the geomagnetic field. Another problem that needs to be solved here is how to know where I am pointing and where I need to point, even if I have the ability to adjust my posture. The simpler method here is to use Earth+Sun recognition, while the more complex method is to use starry sky for navigation (it feels like plate solving, which is said to be how ballistic missiles in the 1950s did).

**What are the risks of launching to GSO?**

Although electromagnetic radiation is not a significant issue for GSO in the ionosphere, and vacuum has little impact on most electronic devices, extreme problems in space still need to be addressed. When the sun is directly shining, the surface temperature of the satellite can reach over 200 degrees above zero, and when it reaches the far side of the Earth, the surface temperature of the satellite can reach over 100 degrees below zero. It is necessary to find a way to prevent components, including batteries, from BOOM. The traditional method is to add an insulation layer and add a heating circuit to the battery. This may require specialized learning. I have read some books online that introduce how to build a small microsatellite that can work in space from civilian grade DIY components. I think it is a good introductory reading material.

2.Regarding the selection of launch vehicles.

*The reusable Falcon 9 rocket is relatively inexpensive, and the publicly offered launch services for low Earth orbit and geostationary transfer orbit are approximately 3000U/kg and 10000U/kg, respectively*

[![1707410994604](https://ethresear.ch/uploads/default/optimized/2X/2/26d1569c34e481245928f759fa2b2a3e30aa79c3_2_690x445.png)17074109946042607×1683 211 KB](https://ethresear.ch/uploads/default/26d1569c34e481245928f759fa2b2a3e30aa79c3)

**Current plan:**

1U CubeSat

- 10x10x10 cm chassis: constructed from laser-cut square aluminum bands and PCBs
- Printed circuit boards (PCBs)
- Electronic components, 2x4 Mbits FRAM Memory, Atmega 2560 microcontroller, integrated micro-USB port
- 9-degree-of-freedom inertial module (with magnetometer)
- Extra solar power: 4 durable 1.37W solar cells
- 4 Lithium Ion batteries (with holding clips and temperature sensors); longer life
- Improved power-management and charging control
- 1.5W high-efficiency radio transceiver with built-in amplifier
- α β γ radiation sensor
- Real-time Clock
- Dipole communications antenna
- Compatibility with Arduino IDE
- 2 sub-miniature deployment switches

**Service contractor:** isilaunch

**Target launch vehicle:** Falcon 9（Cheap）

**Target launch schedule:** September 2025

**Drawing:**

[![image](https://ethresear.ch/uploads/default/optimized/2X/8/841ab2906a8c988c2cad23689a7430332da4bf84_2_613x500.jpeg)image1920×1565 99.6 KB](https://ethresear.ch/uploads/default/841ab2906a8c988c2cad23689a7430332da4bf84)

[![1707389167102](https://ethresear.ch/uploads/default/optimized/2X/1/122becbcfd0e8f27e5eb961ea79780aba56497b2_2_690x488.png)17073891671022251×1595 358 KB](https://ethresear.ch/uploads/default/122becbcfd0e8f27e5eb961ea79780aba56497b2)

More alternative satellite solutions are being conceived…

**Additional**

I am currently applying to the US Department of Defense and NASA for satellite radio frequency usage permits, space business radio station licenses, and satellite launch permits.

Current estimated satellite production and launch costs:

Less than 50000 US dollar

Join the discussion:


      ![](https://ethresear.ch/uploads/default/original/2X/6/60a0dd1195aa91677b6f00e7a4eb29555e45506b.svg)

      [Telegram](https://t.me/eth_pn)



    ![](https://ethresear.ch/uploads/default/original/2X/c/cb2a74c9a798d98fa1be31302fd320595a175a59.jpeg)

###



Let us become immortal stars✨

## Replies

**alexhook** (2024-02-08):

very interesting, but as someone who has no clue how these launches work i’d like to read more details from smarter people

how will it be connected to the internet? will it be possible to upgrade node software from the earth? how come light node? how to deal with increasing hardware requirements? who will sponsor it?

---

**Mirror** (2024-02-08):

Haha, there are still many difficult questions for me to answer. But I have updated more details in the main text.

---

**mratsim** (2024-02-11):

What light client have you tried on an Arduino? How long does it take to verify a block?

---

**Mirror** (2024-02-12):

How about broadcasting validated node data on Earth in the universe using radio frequency signals?

---

**XofEE** (2024-02-12):

Perhaps Cryptosat could offer their help and expertise? They were involved in securing the KZG ceremony from one of their satellites.

https://docs.cryptosat.io/cryptosat/cryptosat/contribution-to-the-ethereum-kzg-ceremony

---

**Mirror** (2024-02-12):

Thank you, in fact, it is very helpful to generate randomness with the assistance of space satellites. This provides good evidence that this study can be helpful for Ethereum in practical scenarios. When we have our own satellite, we can provide more extensive assistance to Ethereum.

---

**kladkogex** (2024-02-12):

Whats the intended purpose ? If the purpose is censorship resistance, then a simple blockchain with totally settled code (like Bitcoin) makes more sense - the moment you introduce a possibility for updates, it can be an attack vector.

If the purpose is providing global access to ETH, then a way lower orbit (like the one starlink uses or even statosphere baloons) would be a cheaper and more effective solution

Or we want do to an ETH airdrop on aliens?

---

**Mirror** (2024-02-13):

Response to you:

Both 1 and 2 are my goals.

Why not enhance Bitcoin?

I am an Ethereum enthusiast and I provide support for my ecosystem.

Why use satellites?

It has a unique feature in resisting censorship, for example, it won’t fall from the sky just because of a ban.

Why is it running on LEO like Starlink?

Bro, this is mainly due to maintenance costs. Due to the effect of gravity, satellites operating in LEO will continuously descend until they fall into the atmosphere and burn out. As a self funded project, I do not have enough funds to invest in satellite attitude adjustment and the installation of boosters.

Why not use hot air balloons?

Difficult to sustain and will be shot down by the Coast Guard.

I’m glad you raised so many questions at once.My answer may not be correct, I am still learning for that goal. I hope you can join in and make this matter better.

---

**kladkogex** (2024-02-13):

Well - it seems it is a vague idea then, not a logically complete proposal. Good luck!

