---
source: magicians
topic_id: 15665
title: A new proposal of Entity Component System
author: rickey
date: "2023-09-05"
category: EIPs
tags: [ecs]
url: https://ethereum-magicians.org/t/a-new-proposal-of-entity-component-system/15665
views: 1300
likes: 1
posts_count: 7
---

# A new proposal of Entity Component System

Hey guys, I’m trying to build a minimal Entity Component System(ECS) on ethereum. The ECS is an architectural pattern often used in game development. It facilitates code reusability by separating the data from the behavior. [Learn more about ECS](https://github.com/SanderMertens/ecs-faq).

If you are interested, please check out this [EthereumECS](https://github.com/HelloRickey/EthereumECS).

## Replies

**SamWilsn** (2023-09-05):

Hey! Thanks for writing up this EIP.

I have one non-editorial related topic I want to bring up. The mutating functions (i.e. `set*`), who do you expect to be calling them? I would assume they’ll mostly be used by the game developer, and not called by third-parties. Like I wouldn’t imagine my wallet needing to know how to create an entity, or associate a component, right?

I mention this because it is customary to omit functions from EIPs that are only going to be called by the owner of a contract. You’ll note that [ERC-20](https://eips.ethereum.org/EIPS/eip-20) doesn’t define a mint function.

I think this might be relevant here too. You probably don’t need to define all the functions for modifying the configuration or creating entities and such?

I could be wrong though; I’m no expert on ECS!

---

**rickey** (2023-09-05):

Hey [@SamWilsn](/u/samwilsn) , Thanks for your reply.

Do you mean set() in Component.sol?

Both game developers and players can call it.

Game developers can call it to initialize data for entities.

Players can call functions in System.sol, and these functions can call set().

For example, if a player wants to move, he will call move() of System.sol, and move() will call set() to change the player’s position data.

btw, thanks for the comments on github, they were useful and I’m making changes based on them. ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=12)

---

**SamWilsn** (2023-09-05):

My pleasure!

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/r/958977/48.png) rickey:

> Do you mean set() in Component.sol?

I’m referring to all of the functions that modify state, so pretty much the list in your Security Considerations section:

> createEntity(),
> setEntityState(),
> addComponent(),
> removeComponent(),
> registerComponent(),
> setComponentState(),
> registerSystem(),
> setSystemState()

I imagine that for the vast majority of cases these will either: be called only by the developer, or hidden behind a facade for players.

---

In fact, I should probably ask: who are the parties that need to agree on this standard to be able to interact? EIPs are only really necessary when you expect multiple independent parties to implement them.

For example, consider ERC-20 tokens. Wallets, exchanges, and block explorers all need to be able to understand arbitrary tokens. Most often, your wallet is created by Company A, while your exchange is created by Company B. Company A and B need to agree on what a token **is**, so ERC-20 is necessary.

Here, I’m not too clear on who the multiple parties would need to be. If a game wants to use an ECS to implement their game logic, it is free to do so, but who else but the game itself would need to inspect the game state?

All that to say: **do we need a standard for entity-component-systems or do we need a library?**

I don’t mean to unduly discourage you from working on an EIP, but you’ll need to justify (in your Motivation section) why we need a standard for ECS instead of a Solidity library.

---

**rickey** (2023-09-05):

I try to explain it with an example,

Now there are three characters.

World’s Owner

Developer (contributor)

player

I play the role of a world owner. I am organizing the development of a game similar to Stardew Valley. You are a developer who is very interested in this game. Because the data and behavior of ECS are separated, you want to contribute the component and system of the farm part. After you finish development, you can initiate a proposal on github to describe your component and system, and call registerComponent and registerSystem to submit your contract. As the owner of the contract, I will check it. If I think there is no problem, I will call setComponentState. setSystemState enables it. Or enable it by community vote. This is like an approve() for Component and System

Users can play the farm function through the system you contribute. Now that I want to upgrade the farm, I only need to set your system to be unavailable through setSystemState, and then re-register a new system. And if other people want to access the data of the farm, then he can directly obtain the data of each entity of the farm through IComponent.

The following functions can also be opened to players according to the design of the game, a few examples

createEntity, the player creates a game character.

setEntityState, the player’s game character died in battle

addComponent, players choose different game character professions and add different attributes.

removeComponent, the attributes of the player disappear after taking a certain potion.

setComponentState, the player is frozen after being attacked by magic ![:cold_face:](https://ethereum-magicians.org/images/emoji/twitter/cold_face.png?v=12)

---

**SamWilsn** (2023-09-06):

Would you expect the exact same farm components and system from this Stardew Valley-style game to work with other games? Like could I come along, with my Eve Online-style game, and enable your farm contracts to work with my planet entities?

---

**rickey** (2023-09-06):

There may be no guarantee that all components and entities in Stardew Valley will work with all games,

But when you want to combine Eve Online with it, it’s very simple to use ECS,

First, you need to determine what data you want to operate on.

You can first use getEntityComponents() or getComponents() to find the components you are interested in. And use getComponentState() to check whether these components are available. You can also create new Components based on IComponent.

Then, you need to get the existing systems through getSystems(), if there is no suitable system for you, you can also create a new system yourself. This system will connect your Eve Online Component to the Stardew Valley Component.

Finally, you can use registerComponent() and registerSystem() to register them, waiting for review and approval by the Stardew Valley committee.

In fact, I really expect composability between games, which is why ECS was proposed.

