---
source: magicians
topic_id: 19305
title: "ERC-7660: A Protocol for ERC20 Tokens Which Released Based On Predefined Periods Controlled"
author: Ray
date: "2024-03-22"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7660-a-protocol-for-erc20-tokens-which-released-based-on-predefined-periods-controlled/19305
views: 1762
likes: 2
posts_count: 1
---

# ERC-7660: A Protocol for ERC20 Tokens Which Released Based On Predefined Periods Controlled

```auto
This protocol introduces improvements in the following areas:

1. ERC20 Tokens and Linear Release Functionality.
2. Online Representation of ERC20 Balances.
3. Lock-Up Functionality for ERC20 Tokens.
4. "Sorter" Algorithm.
5. Low-Cost Swap Algorithm.
6. Transaction Fee Collection Mechanism.
```

- Sorter && Low-Cost Swap Algorithm

```auto
    function _handleTokenTransfer(address from, address to, uint256 amount,uint256 toAmount) internal virtual {
        claimRelease(from);
        uint256 fromBalance = _Owned[from];
        require(fromBalance >= amount, "ERC20: transfer amount exceeds balance");
        unchecked {
            _Owned[from] = fromBalance - amount;
        }
        //update to vestInfo
        if (!_isExcludedVest[to]) {
            claimRelease(to);
            uint startTime = block.timestamp / period * period;
            uint pos = vestCursor[to];
            VestInfo storage toInfo = userVestInfo[to][pos];
            if (toInfo.startTime != startTime) {
                if (pos == 6) {
                    pos = 0;
                } else {
                    ++pos;
                }
                toInfo = userVestInfo[to][pos];
                toInfo.total = toAmount;
                toInfo.released = 0;
                toInfo.startTime = uint128(startTime);
                vestCursor[to] = pos;
            } else {
                toInfo.total += toAmount;
            }
            toInfo.updateTime = uint128(block.timestamp);
        } else {
            if(_isSwapRouter[to]){
                _Owned[to] += amount;
            }else{
                _Owned[to] += toAmount;
            }
        }
    }
```

- linear Release

```auto
    function claimRelease(address account) public {
        uint canReleaseTotal;
        for (uint i = 0; i = info.startTime + duration) {
                canRelease = info.total - info.released;
            } else {
                uint temp = info.total * (block.timestamp - info.startTime) / duration;
                canRelease = temp - info.released;
            }
            canReleaseTotal += canRelease;
            info.released += canRelease;
        }

        if (canReleaseTotal > 0) {
            _Owned[account] += canReleaseTotal;
        }
    }
```

- Linear balance

```auto
    function balanceOf(address account) public view virtual override returns (uint256) {
        (, uint256 canRelease,) = getCanReleaseInfo(account);
        return _Owned[account] + canRelease;
    }

    function getCanReleaseInfo(address account) public view returns (uint256 total, uint256 canRelease, uint256 released) {
        for (uint i = 0; i = info.startTime + duration) {
                canRelease += info.total - info.released;
            } else {
                uint temp = info.total * (block.timestamp - info.startTime) / duration;
                canRelease += temp - info.released;
            }
        }
    }

```
