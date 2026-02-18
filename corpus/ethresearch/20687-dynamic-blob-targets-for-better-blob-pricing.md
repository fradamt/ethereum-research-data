---
source: ethresearch
topic_id: 20687
title: Dynamic Blob Targets for Better Blob Pricing
author: keyneom
date: "2024-10-17"
category: Economics
tags: [data-availability, rollup]
url: https://ethresear.ch/t/dynamic-blob-targets-for-better-blob-pricing/20687
views: 772
likes: 7
posts_count: 9
---

# Dynamic Blob Targets for Better Blob Pricing

# Dynamic Blob Targets for Better Blob Pricing

## Abstract

This proposal introduces a dynamic pricing mechanism for blobs in Ethereum, using a PID (Proportional-Integral-Derivative) controller to adjust the target number of blobs. The goal is to maintain baseline security and assumes Data Availability Sampling (DAS) while optimizing blob usage and burn rates, ensuring economic stability and predictability for network participants.

## Key Concepts

1. PID-Controlled Blob Target: Adjust the target number of blobs based on network usage over time.
2. Bounded Pricing Mechanism: Implement different pricing behaviors within and outside target bounds.
3. Existing Pricing Mechanism at Limits: Use existing blob pricing mechanisms at the bounds.
4. Burn Rate Optimization: Balance per-blob pricing with overall burn amounts.

## Detailed Mechanism

### Blob Target Adjustment

- -A PID controller algorithm adjusts the target number of blobs based on consistent deviations from the current target.
- -The target blob count floats between predetermined lower and upper bounds, the upper bound is set based on security considerations and the lower bound is assumed to be 1.

### Pricing Mechanism

1. Within Target Bounds:

-Price adjusts linearly as actual blob count varies from the target.
2. -Increases when above target, decreases when below.
3. Outside Target Bounds:

-Existing blob pricing mechanisms take over, causing exponential price changes.
4. -This continues until actual blob count returns within the target bounds.
5. Blob Target Adjustment Effects:

-When target increases: Price per blob decreases, but overall burn amount increases.
6. -When target decreases: Price per blob increases, but overall burn amount decreases.

### Security and Economic Considerations

- -Upper bound for blob target is determined by validator count and DAS security requirements assuming a given bandwidth per validator (i.e. we know in advance when validators are withdrawing and it is rate limited as well so we should be safe and able to account for those with enough time to start adjusting the upper blob target limit if needed). We can assume 33% or something similar of validators online in determine how many samples can be completed, etc. to determine a conservative upper limit.
- -The system aims to maintain predictable pricing within the target range while ensuring security at the limits.
- -Economic stability is prioritized by making gradual adjustments to the target, avoiding sudden price shocks.

## Benefits

1. More predictable and stable pricing within the target range.
2. Adaptive to long-term changes in network conditions.
3. Maintains crucial security guarantees through existing mechanisms at the bounds.
4. Optimizes network usage and burn rates over time. The current system always aims to underutilize available bandwidth while still requiring higher bandwidth be available to support blocks where max blobs is reached. This proposal aims to make more consistent use of available bandwidth without exceeding validator minimum bandwidth requirements (assuming we actually get those).

## Challenges and Considerations

1. Tuning the PID controller parameters for optimal responsiveness without introducing instability.
2. Ensuring the mechanism remains economically sound under various network conditions.
3. Balancing short-term price stability with long-term adaptability to network changes.

## Implementation Considerations

- -Thorough economic modeling and simulation are necessary to validate the mechanism’s stability and effectiveness.
- -At the lower and upper target blob bound you can define a target burn as a percentage of issuance rates as well. e.g. lower target burn of 1% of issuance and upper target burn of 33% of issuance before we are considered to have re-entered the target blob bounds and start making blob target adjustments. What these targets should be should have modeling and simulations and should be discussed thoroughly as well. As indicated above, a smooth curve where price per blob drops but overall burn increases would be reasonable.

This proposal aims to create a more dynamic and responsive blob pricing system for Ethereum, enhancing network efficiency and economic stability while maintaining crucial security guarantees. The use of a PID controller for target adjustment provides a well-established control mechanism, potentially offering more predictable, sustainable, and stable long-term behavior compared to other algorithmic approaches. It is my belief that a pricing mechanism with similar behavior to what I’ve described would better match the inelastic demand common to L2s utilizing blobs for DA.

## Replies

**keyneom** (2024-10-24):

Someone shared with me this morning that comments were made on reddit here:

https://www.reddit.com/r/ethfinance/comments/1g71lyc/comment/lsoccvt/

I think people might be getting confused as to what is getting modified when. Here’s a rough POC of how target blobs could be set using a PID controller. We could use a variety of things as a setpoint but as an example here I use the average of the count of the actual blobs for the current block and the previous block’s actual blob count as our setpoint (obviously this is a moving setpoint but that’s fine, we are trying to reduce error between the actual blobs used and the predicted/target blobs used).

Obviously all parameters here are just examples and would need to be reviewed.

```python
import numpy as np
import matplotlib.pyplot as plt

# PID controller function with control signal bounds and a proportional error deadband
def pid_controller(Kp, Ki, Kd, prev_target_blobs, set_point, integral, previous_error, dt, lower_bound, upper_bound, deadband):
    # Error is the difference between the previous control signal (x_prev) and the current input (y_current)
    error = set_point - prev_target_blobs
    p_error = error

    if abs(error) < deadband:
        p_error = 0

    integral += error * dt  # Integral of error
    derivative = (error - previous_error) / dt  # Derivative of error

    # Bounded Control signal
    new_target_blobs = Kp * p_error + Ki * integral + Kd * derivative
    new_target_blobs = int(np.clip(new_target_blobs, lower_bound, upper_bound))

    # Return the new control signal (x), and the updated integral and error for next step
    return new_target_blobs, integral, error

# Parameters for the PID controller
Kp = 0.1  # Proportional gain
Ki = 0.25  # Integral gain
Kd = 0.05  # Derivative gain
dt = 1   # Time step
lower_bound = 1  # Lower bound
upper_bound = 21  # Upper bound
deadband = 1

# Input signal (array of whole numbers representing system input at each time step)
# actual_blobs_for_block = [5, 3, 2, 6, 4, 1, 6, 4, 2, 5, 3, 6]  # Example input array
# actual_blobs_for_block = [3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4]
# actual_blobs_for_block = [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]
# actual_blobs_for_block = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
# actual_blobs_for_block = [0, 0, 0, 0, 0, 0, 0, 0, 24, 24, 24, 24, 24, 24, 24, 24, 10, 10, 10, 10, 10, 10, 10, 10]
# actual_blobs_for_block = [5, 3, 2, 6, 4, 1, 6, 0, 0, 4, 2, 5, 3, 6, 5, 3, 2, 6, 4, 1, 6, 0, 0, 4]
# actual_blobs_for_block = [7,9,7,9,7,9,7,9,7,9,7,9,7,9,7,9,7,9,7,9,7,9,7,9]
actual_blobs_for_block = [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Initial conditions
prev_actual_blobs = 0
prev_target_blobs = 1  # Initial previous control signal
integral = 0.0
previous_error = 0.0

# Arrays to store the control signals and error for plotting
blob_targets_for_block = []
errors = []

# Simulation loop
for actual_blobs_for_current_block in actual_blobs_for_block:
    # Calculate the new control signal
    target_blobs_for_next_block, integral, previous_error = pid_controller(
        Kp, Ki, Kd, prev_target_blobs, (actual_blobs_for_current_block+prev_actual_blobs)/2, integral, previous_error, dt, lower_bound, upper_bound, deadband
    )

    # Store control signal and error for plotting
    blob_targets_for_block.append(target_blobs_for_next_block)
    errors.append(actual_blobs_for_current_block - prev_target_blobs)

    # Update for the next iteration
    prev_target_blobs = target_blobs_for_next_block
    prev_actual_blobs = actual_blobs_for_current_block

# Plotting input signal and control signal
time_steps = np.arange(len(actual_blobs_for_block)) * dt
plt.figure(figsize=(10, 5))

# Plot input signal
plt.plot(time_steps, actual_blobs_for_block, label='Input Signal', marker='o')

# Plot control signal
plt.plot(time_steps, blob_targets_for_block, label='Control Signal', marker='x')

plt.xlabel('Time (s)')
plt.ylabel('Signal Value')
plt.title('PID Control Signal vs Input Signal')
plt.legend()
plt.grid(True)
plt.savefig('pid_simulation_plot.png')
# plt.show()

# Print the average error
average_error = np.mean(np.abs(errors))
print(f"Average Error:    {average_error:.3f}")
print("input_signal:    ", actual_blobs_for_block)
print("control_signals: ", blob_targets_for_block)

```

Target blobs is completely separate from the price of the blobs as you can see no price is used as input. I’m recommending that the price per blob (assuming in the simple case that the actual blob count is always equal to the target blob count) be determined by a curve. The higher the target blob count the lower the base price per blob but the higher the overall burn as a percentage of issuance.

i.e. When we use fewer blobs the blobs become more expensive per blob but we burn the basefee of fewer blobs overall (basefee=10, target_blob_count=3, target_total_burn=30). When we use more blobs the blobs become cheaper per blob but we burn the basefee of more blobs overall (basefee=5, target_blob_count=10, target_total_burn=50). Target total burn can be set as a percentage of total issuance (so variable depending on the target blob count and depending on the number of validators since that impacts issuance).

This incentivizes using more blobs overall as long as the blob is profitable, it becomes easier to have profitable blobs the more you use them. The downside of this is that when the blob target is low you need a blob that will make a lot of money to offset the cost. We need to find a point that feels reasonable here.

When the lower and upper bounds on the target blob count are hit the pricing per blob reverts to the existing mechanism, i.e. an exponential adjustment until they hit the target burn price at which point the target blob count kicks in again and its pricing mechanism takes over.

**Optional: The last portion of the pricing mechanism–that may be unnecessary and overcomplicated but maybe has a useful property–is to adjust the *actual* basefee from the *target* basefee (what we defined two paragraphs back) given the target burn for the target blob count on our curve. We move this price linearly up or down from the target price per blob every time the current target blob count equals the prior blocks target blob count and the actual blob count is higher or lower than it was last time. This is intended to be another stabilizing force to avoid the target blob count moving too much this time though instead of the PID controller adjusting our target supply of blobs we are using an economic force to adjust demand. When we first start seeing more blobs than what we are targeting we charge a higher basefee. Ideally this helps to create a system that gives more predictable demand, more predictable and sustainable prices for blobs, and encourages full use of network capacity while remaining secure (max blob count is specified by the number of validators on the network and other variables for peerdas including how many columns are custodied, how many subnets exist, and how many peers each node needs to connect to without breaking our desired bandwidth limitations).

This was written mostly as a stream of consciousness so please forgive me if I still haven’t done a very good job of making the concept clear. I’d be happy to respond to any questions. I don’t know that this is the optimal solution to blob pricing but I’m hoping it can start a conversation regarding how blob pricing can be improved.

Right now I think blob prices are likely to be overly volatile. Since demand for blobs is more inelastic than with regular user txs, you are more likely to see prices sit at 0 for a long time, have a bunch of L2s build on blobs assuming prices remain at 0 and then as more onboarding occurs, we reach “price discovery” and a bunch of the smaller L2s get priced out of being able to leverage blobs. This is less than ideal for them and their users. Reducing costs of blobs as more blobs are used should enable these L2s to have a more predictable sense of the long term economics of relying on blobs for DA. Having a slower moving blob target adjustment that keeps prices more predictable is preferable in my opinion and creates for more sustainable economics for network validators when blob usage is low.

---

**ben-lilly** (2024-11-04):

Nice note here keyneom.

Apologies for the seemingly adjacent question… But I’m trying to get up to date on the conversations regarding fees in general. Seems the economics section of this forum is not very active… Is there a more active dialogue taking place elsewhere?

Once up to date I hope to be more active and take part in the conversation. Thank you!

---

**keyneom** (2024-11-05):

Hard to say if there are conversations happening elsewhere but I think this is still probably the a good place to participate. Not every post gets tagged as economics related though even if it is touching on it. Other than here some stuff on Twitter or Farcaster perhaps?

---

**timjrobinson** (2024-12-05):

I really like this idea! I recently created the Ethereum Blob Simulator ([GitHub - blue-yard/ethereum-blob-simulator: Visualize how changes to the Ethereum Blob market will affect transaction prices and ETH burn](https://github.com/blue-yard/ethereum-blob-simulator)) and when using it noticed there were a number of economic issues with blobs:

1. The pricing of blobs seems to be very all or nothing, where for a long time they are basically free, and then as the blobs fill up costs can increase rapidly for everyone. We’re seeing this now where in just a month and a small amount of growth, transactions on L2’s have gone from free to 5c - 10c on average. This does get smoother as we have more blobs.
2. Assuming the Ethereum ecosystem grows to thousands of TPS in the near future, we’re going to need to regularly increase the total blobs available. We will likely need a more reactive mechanism than just changing the total blobs with each hard fork.
3. A third problem is if TPS then drops significantly we’ll have many free blobs costing validators a lot of bandwidth and disk space / IO but without any payment. There could be months or years where validators are processing hundreds of blobs per block for no payment. Will we ever choose to reduce blob count to prevent this? or is there a better mechanism?

It seems like this proposal would solve all 3 issues? Have you done any further work on simulating how this PID mechanism would work? Perhaps it could be added to the blob simulator? I’d be happy to chat further about that and help with the implementation.

---

**keyneom** (2024-12-06):

I haven’t done any other simulations. I’d be happy to see it tested in the blob simulator. I might be able to help with adding it if you think it would be useful. I think I commented on your twitter post about the blob simulator and potentially a better pricing mechanism linking to this post but I wouldn’t be surprised if you weren’t notified about it. My dms are open on twitter so feel free to ping me there or just dm me here.

---

**keyneom** (2025-02-01):

Another couple ideas I’ve had that might be able to be mixed in here is to subsidize blobs that are proven on L1 to support use of blobspace by actual L2s. You could perhaps do this to different degrees depending on how “native” the L2 is.



      [x.com](https://x.com/keyneom/status/1881136834132295699)





####

[@keyneom](https://x.com/keyneom/status/1881136834132295699)

  @0xBreadguy You can match the blob to their respective txs and introduce local fee markets on txs to increase costs for noisy neighbors, no? I've also been thinking it could be worth it to subsidize costs for L2s that have onchain proofs, so they get lower pricing by default by being rollups

  https://x.com/keyneom/status/1881136834132295699










Or another possibility that I’ve thought might be interesting is to have blob provisioning nfts–kind of like blob futures. The idea is that you can provision a certain throughput in advance by bidding on the price of the “nft” (like provisioned throughput for DynamoDB in AWS). The nft purchase price is the number of remaining blocks before expiration multiplied by the base fee you get to pay for one blob each block (if you own two provisioned blob nfts you can buy two blobs every slot at their respective base fees). Priority fee is still pertinent to inclusion. Like ens the nft expires after a fixed period of time. It goes up for auction for all interested parties prior to expiration. Of course the current owner can sell it early if they decide to. You could dedicate half of the available blobspace to be provisioned and the other half to be on demand. Ideally this creates more predictable and spread out demand for blobs and also even gives certain protections from noisy neighbors to L2s. You could have provisioned blob nfts that always last 1 year, 6 months, 3 months, and a month. You could have fewer long term nfts and more short term ones in circulation.

---

**kustrun** (2025-02-04):

Thank you for sharing this interesting idea about **dynamic blob pricing**!

If I understand correctly, this approach would **dynamically adjust the blob target** based on **historical demand**, rather than keeping it fixed at 3 blobs per block (as it is today). This adjustment would result in **smoother and more stable fee changes**, preventing sharp spikes when demand increases and reducing overall volatility.

Most of the time, fees would **adjust more gradually**, with smaller step changes compared to the current model. However, during periods of high congestion, the existing **exponential fee increase mechanism** would still apply.

Would this dynamic blob target adjustment remove the need for hard-coded boundaries (currently 0 to 6 blobs per block)? If so, could this allow for an unconstrained upper bound, adapting flexibly to long-term demand trends?

Looking forward to seeing simulations of how this would behave on real on-chain data!

---

**keyneom** (2025-02-05):

You’ll still have upper bounds and a lower bound (0 of course) but those could be dynamic to some extent as well. Yes, the idea is more stability of fees. I don’t imagine it being implemented soon but after or with full peerdas perhaps.

