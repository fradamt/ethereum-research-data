---
source: magicians
topic_id: 7366
title: EIP proposal Micropayments Standard for NFTs and Multi Tokens
author: julesl23
date: "2021-10-29"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-proposal-micropayments-standard-for-nfts-and-multi-tokens/7366
views: 3283
likes: 0
posts_count: 13
---

# EIP proposal Micropayments Standard for NFTs and Multi Tokens

Hi,

I have implemented a tipping system for NFTs (ERC-721) and mult tokens (ERC-1155) that I feel is very general purpose and can fit many use cases as NFTs evolve. So, I made a submission for an EIP.

In my own system, I am using it as a way for users to easily tip content creators with ERC20 rewards, whilst keeping gas costs as low as possible. Tips can be sent in batches to save on gas costs.

Tipping allows a user to show appreciation for an NFT that monetary rewards the NFT’s holder.

The interface specification without events and comments for brevity…

```auto
interface ITipToken {

    function setApprovalForNFT(address holder, address nft, uint256 id, bool approved) external;

    function isApprovalForNFT(address holder, address nft, uint256 id) external returns (bool);

    function tip(address nft, uint256 id, uint256 amount) external;

    function tipBatch(address[] memory users, address[] memory nfts, uint256[] memory ids, uint256[] memory amounts) external;

    function deposit(address user, uint256 amount) external payable;

    function withdraw(uint256 amount) external payable;

    function balanceOf(address user) external view returns (uint256);

    function balanceDepositOf(address user) external view returns (uint256);

    function rewardPendingOf(address holder) external view returns (uint256);

}

```

`setApprovalForNFT` registers an NFT for tipping, provided that the NFT has approved the tip token contract. It checks that the holder account is the NFT holder and reverts if not. There is no limit to how many NFTs that can be registered. When a tip is sent, the deposited ERC20 that backs the tip is sent pending to the NFT holder and the tip itself is burnt. tipBatch allows a provider who wishes to save gas costs, to send batches of tips from many users for the NFTs to the NFT holders in one transaction.

`deposit` function allows a user to buy tip tokens with ERC20 compatible tokens. The deposited ERC20 can be held in the tip token contract account or an external escrow account, to be used later for when a holder decides to withdraw.

`balanceDepositOf` returns the deposited balance of a user. This divided by the value returned from the tip token contract `balanceOf` function, can be used to calculate the cost of each tip.

`rewardPendingOf` allows the holder to find out how much money they are owed, and can choose to withdraw, for example, when there is enough accumulated that it is worth the gas costs to do so.

Tip tokens can also be transferred directly to other users as they are ERC20.  Each NFT that can be registered to receive tips, can be an ERC-721 or an NFT/fungible token in an ERC-1155.

A tip token contract can implement ERC20 to allow for transfer of tips directly between users.

I am excited to create a topic here and see what the wider community thinks of it.

## Replies

**julesl23** (2021-11-01):

Some use cases I think this proposal can be used for include:

```
In game purchases and other virtual goods

Tipping messages, posts, music and video content

Donations/crowdfunding

Distribution of royalties

Pay per click advertising

Incentivising use of services

Reward cards and coupons
```

And I think a lot more.

If you foresee any issues, know of other use cases or have any other queries/suggestions, let me know.

---

**julesl23** (2021-11-02):

I’ve added support for shared holders of ERC-1155 multi tokens.

Imagine a scenario where an article is represented by an NFT (in this case an ERC-1155 fungible token) and was written by multiple contributors (holders). A reader likes the article and sends a tip to its NFT. The tip rewards will be sent pending to each of the holders in the proportion of their balance of the ERC-1155 token.

So, for two holders A and B of ERC-1155 token 1, if holder A’s balance is 25 and holder B’s is 75 then any tip sent to token 1 would distribute 25% of the reward pending to holder A and the remaining 75% pending to holder B.

Here is the full interface specification with comments:

```auto
interface ITipToken {
    /// @dev This emits when the tip token implementation approves the address
    /// of an NFT for tipping.
    /// The holders of the 'nft' are approved to receive rewards.
    /// When an NFT Transfer event emits, this also indicates that the approved
    /// addresses for that NFT (if any) is reset to none.
    event ApprovalForNFT(
        address[] holders,
        address indexed nft,
        uint256 indexed id,
        bool approved
    );

    /// @dev This emits when a user has deposited an ERC20 compatible token to
    /// the tip token's contract address or to an external address.
    /// This also indicates that the deposit has been exchanged for an
    /// amount of tip tokens
    event Deposit(
        address indexed user,
        address indexed rewardToken,
        uint256 amount,
        uint256 tipTokenAmount
    );

    /// @dev This emits when a holder withdraws an amount of ERC20 compatible
    /// reward. This reward comes from the tip token's contract address or from
    /// an external address, depending on the tip token implementation
    event Withdraw(
        address indexed holder,
        address indexed rewardToken,
        uint256 amount
    );

    /// @dev This emits when the tip token constructor or initialize method is
    /// executed. The 'rewardToken_' address is passed to the ERC20 constructor or
    /// initialize method.
    /// Importantly the ERC20 compatible token 'rewardToken_' to use as reward
    /// to NFT holders is set at this time and remains the same throughout the
    /// lifetime of the tip token contract.
    event InitializeTipToken(
        address indexed tipToken_,
        address indexed rewardToken_,
        address owner_
    );

    /// @dev This emits everytime a user tips an NFT holder.
    /// Also includes the reward token address and the reward token amount that
    /// will be held pending until the holder withdraws the reward tokens.
    event Tip(
        address indexed user,
        address[] holder,
        address indexed nft,
        uint256 id,
        uint256 amount,
        address rewardToken,
        uint256[] rewardTokenAmount
    );

    /// @notice Enable or disable approval for tipping for a single NFT held
    /// by a holder or a multi token shared by holders
    /// @dev MUST revert if calling nft's supportsInterface does not return
    /// true for either IERC721 or IERC1155.
    /// MUST revert if any of the 'holders' is the zero address.
    /// MUST revert if 'nft' has not approved the tip token contract address.
    /// MUST emit the 'ApprovalForNFT' event to reflect approval or not approval
    /// @param holders The holders of the NFT (NFT controllers)
    /// @param nft The NFT contract address
    /// @param id The NFT token id
    /// @param approved True if the 'holder' is approved, false to revoke approval
    function setApprovalForNFT(
        address[] memory holders,
        address nft,
        uint256 id,
        bool approved
    ) external;

    /// @notice Checks if 'holder' and 'nft' with token 'id' have been approved
    /// by setApprovalForNFT
    /// @dev This does not check that the holder of the NFT has changed. That is
    /// left to the implementer to detect events for change of ownership and to
    /// take appropriate action
    /// @param holder The holder of the NFT (NFT controller)
    /// @param nft The NFT contract address
    /// @param id The NFT token id
    /// @return True if 'holder' and 'nft' with token 'id' have previously been
    /// approved by the tip token contract
    function isApprovalForNFT(
        address holder,
        address nft,
        uint256 id
    ) external returns (bool);

    /// @notice Sends tip from msg.sender to holder of a single NFT or
    /// to shared holders of a multi token
    /// @dev If 'nft' has not been approved for tipping, MUST revert
    /// MUST revert if 'nft' is zero address.
    /// MUST burn the tip 'amount' to the 'holder' and send the reward to
    /// an account pending for the holder(s).
    /// If 'nft' is a multi token that has multiple holders then each holder
    /// MUST receive tip amount in proportion of their balance of multi tokens
    /// MUST emit the 'Tip' event to reflect the amounts that msg.sender tipped
    /// to holder(s) of 'nft'.
    /// @param nft The NFT contract address
    /// @param id The NFT token id
    /// @param amount Amount of tip tokens to send to the holder of the NFT
    function tip(
        address nft,
        uint256 id,
        uint256 amount
    ) external;

    /// @notice Sends a batch of tips to holders of 'nfts' for gas efficiency
    /// @dev If NFT has not been approved for tipping, revert
    /// MUST revert if the input arguments lengths are not all the same
    /// MUST revert if any of the user addresses are zero
    /// MUST revert the whole batch if there are any errors
    /// MUST emit the 'Tip' events so that the state of the amounts sent to
    /// each holder and for which nft and from whom, can be reconstructed.
    /// @param users User accounts to tip from
    /// @param nfts The NFT contract addresses whose holders to tip to
    /// @param ids The NFT token ids that uniquely identifies the 'nfts'
    /// @param amounts Amount of tip tokens to send to the holders of the NFTs
    function tipBatch(
        address[] memory users,
        address[] memory nfts,
        uint256[] memory ids,
        uint256[] memory amounts
    ) external;

    /// @notice Deposit an ERC20 compatible token in exchange for tip tokens
    /// @dev The price of tip tokens can be different for each deposit as
    /// the amount of reward token sent ultimately is a ratio of the
    /// amount of tip tokens to tip over the user's tip tokens balance available
    /// multiplied by the user's deposit balance.
    /// The deposited tokens can be held in the tip tokens contract account or
    /// in an external escrow. This will depend on the tip token implementation.
    /// Each tip token contract MUST handle only one type of ERC20 compatible
    /// reward for deposits.
    /// This token address SHOULD be passed in to the tip token constructor or
    /// initialize method. SHOULD revert if ERC20 reward for deposits is
    /// zero address.
    /// MUST emit the 'Deposit' event that shows the user, deposited token details
    /// and amount of tip tokens minted in exchange
    /// @param user The user account
    /// @param amount Amount of ERC20 token to deposit in exchange for tip tokens.
    /// This deposit is to be used later as the reward token
    function deposit(address user, uint256 amount) external payable;

    /// @notice An NFT holder can withdraw their tips as an ERC20 compatible
    /// reward at a time of their choosing
    /// @dev MUST revert if not enough balance pending available to withdraw.
    /// MUST send 'amount' to msg.sender account (the holder)
    /// MUST reduce the balance of reward tokens pending by the 'amount' withdrawn.
    /// MUST emit the 'Withdraw' event to show the holder who withdrew, the reward
    /// token address and 'amount'
    /// @param amount Amount of ERC20 token to withdraw as a reward
    function withdraw(uint256 amount) external payable;

    /// @notice MUST have identical behaviour to ERC20 balanceOf and is the amount
    /// of tip tokens held by 'user'
    /// @param user The user account
    /// @return The balance of tip tokens held by user
    function balanceOf(address user) external view returns (uint256);

    /// @notice The balance of deposit available to become rewards when
    /// user sends the tips
    /// @param user The user account
    /// @return The remaining balance of the ERC20 compatible token deposited
    function balanceDepositOf(address user) external view returns (uint256);

    /// @notice The amount of reward token owed to 'holder'
    /// @dev The pending tokens can come from the tip token contract account
    /// or from an external escrow, depending on tip token implementation
    /// @param holder The holder of NFT(s) (NFT controller)
    /// @return The amount of reward tokens owed to the holder from tipping
    function rewardPendingOf(address holder) external view returns (uint256);
}
```

---

**julesl23** (2021-11-05):

Something not immediately obvious is how tip tokens can help set a level playing field between creators from different geographical regions…

By setting fixed conversion rates with the amount of tip tokens that are bought from ERC-20 tokens per geographical region, users from poorer countries are able to send the same amount of tips as richer nations for the same level of appreciation for content/assets etc. Hence, not skewed by average wealth when it comes to using analytics to discover which NFTs are actually popular.

---

**wschwab** (2021-12-21):

Hi! Thanks for your submission. I’m trying to understand your EIP a bit more, I hope you won’t mind if I ask you a few questions.

Please correct me if I’m wrong, but I *think* the flow from your EIP would be that if I would want to tip an NFT (or owner of an NFT?) I could:

- send to the tipping contract
- receive “tipping tokens” against the deposit
- tips could be batched together, and sent to the NFT

(I very well may have misunderstood, though.)

If this is the case, I’m having a hard time understanding the need. Why can’t I lookup the `owner` of a ERC721 NFT on the NFT contract and send directly? That would only be one ERC20 transfer, whereas this implementation would have 3 over the whole process - I deposit tokens, receive tokens, and then the recipient pulls their tokens.

This is compounded imho by the price of gas on mainnet. Even one ERC20 transfer at current gas is generally more than the amounts we generally refer to as tipping or microtransactions, and while I think this EIP tries to address this issue by introducing a batching system, I didn’t understand how it gets around a user paying full ERC20 transfer gas in order to make a tip.

Thanks again for submitting!

---

**julesl23** (2021-12-21):

Hi, Thanks, sure. The flow is correct. Thanks for your questions.

One reason is to have a truth on-chain of what the tip was for, listening to events will tell that, as it includes the NFT address. This wouldn’t be the case if an ERC20 was sent directly to the owner, that information would be lost.

For an example social media use case, a reader can send a tip to an NFT of a blog post that shows their appreciation for the post content. The content creator gets feedback that their post is liked.

I envision that future decentralised social media platforms will not have such walled gardens as current centralised ones. So alternative platforms can make use of this shared data on-chain and the content creator wouldn’t have to build separate communities and content on each platform that gets lost if a platform owner decides so.

Another point is to help level the playing field with creators from poorer countries. Decoupling the tip from the ERC20 tokens means someone from a poorer country can purchase tips at a cheaper rate, but still send the same amount of tip tokens for same levels of appreciation compared to that sent from someone from a wealthy nation.

I also believe a more fluid experience can be presented to the user if there is an easy way to not have to sign with a wallet every time someone wishes to send a tip. Sure, could have a large ‘allowance’ set but with tips this is not needed. This part can be left to the implementer.

For the use case of social media, I would not imagine many would be on L1 currently. So, the cost is probably a moot point for a lot of use cases, it would be the cost on L2. For that, the batching system helps.

---

**wschwab** (2021-12-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/julesl23/48/4796_2.png) julesl23:

> Decoupling the tip from the ERC20 tokens means someone from a poorer country can purchase tips at a cheaper rate

I think this touches on something I’m not understanding: how is this system decoupled from ERC20, and how does it lead to a cheaper rate for any part of the flow?

---

**julesl23** (2021-12-22):

Okay, I will use same use case to explain. It’s optional if an implementer wants to implement something like this or not at all for their tip token contract:

Say if an implementer uses tips and doesn’t use ‘likes’ as analytics to determine what NFT content is popular. Someone from the USA called Bob would have more purchasing power on average than someone from say Peru called Xavier to purchase tips to send. Say that Xavier loves a particular content just as much as Bob does, shouldn’t they be able to easily tip roughly the same number of tip tokens?

Using a simple example, purchasing power index, Peru ‘s PPI is 33.95 and USA 109.52. PPI could be used like an exchange rate proxy to determine how much tips Xavier could afford to purchase that would be the same number of tips that Bob could afford to purchase on average. In this case it would need to be in a ratio of 33.95/109.52 cheaper for Xavier than Bob to purchase the same number of tip tokens.

They both could then send the same number of tips to show the same level of appreciation that they can afford, maybe just by clicking from a set choice of tip token amounts to send. The implementer (or whoever) can get a fairer view to how popular all the contents are.

This I believe presents an alternative way for local content to bubble up to become worldwide popular on merit, rather than traditional gatekeepers and marketing budgets. I believe this could benefit a new wave of content creators (who can then afford to do more content).

I hope explaining this scenario helped.

---

**mayt** (2022-01-13):

Hi julesl23,

I’m trying to understand the need for this interface to require a tip token. I wonder if the a new tip token requirement better fits in the implementation detail?  Is there a reason this should be part of the interface beyond the supporting the geographical regions?

Also  this interface, looks like there’s no way to liquidate the deposit. (Technically, you can transfer the tip tokens to some exchange to cash out.) Is this expected?

---

**julesl23** (2022-01-13):

Hi,

For my particular use case in social media, I was looking at ways to save gas for the many transactions; by batching and also implementing a pull request system. The latter, the receiver of rewards would be able to withdraw at their leisure when the amount was worth it compared to the gas cost. The EIP I believe achieves both.

The geographical incentive is optional but came out as a bonus.

I was also thinking of the user experience. How would they send tips at a whim without having to involve a wallet and signing every transaction? Tip tokens don’t have to be ERC20 so can easily achieve this in a lighter manner. The user can top up at their leisure too. This workflow is a different approach that exists in the offline world, that the EIP tries to capture.

Refunds currently not explicitly defined in the interface spec. The user can send the tip balance back to the service provider to receive refunds but that’s left to the implementation of the tip contract. I’ll think on this.

I believe you are correct, it doesn’t have to be a tip per say, the event InitializeTipToken allows for the tip token and deposit token to be the same ERC20. This enables it to work for e.g. royalties. Perhaps using ‘reward’ more often as a terminology would be a possibility?

---

**ethanj.eth** (2022-01-31):

Why do we not just use the normal “send” as the tip functionality?

---

**julesl23** (2022-01-31):

Hi,

I’m not understanding the question, please elaborate. Are you talking about the “send” method in ERC-777?

---

**julesl23** (2022-02-08):

Perhaps this is the answer to your question…

If you “send” ERC-777 tokens to an NFT address, assuming the NFT hasn’t implemented the token hooks, the transaction will be reverted.

If you “transfer” ERC-20 tokens to an NFT address, it most likely will be lost.

If you “tip” ERC-4393 tip tokens to an NFT address, then the tip value will be distributed among the holder(s) of the NFT.

