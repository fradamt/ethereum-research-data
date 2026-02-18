---
source: magicians
topic_id: 8896
title: CFT - Collaborative Fungible Token
author: mukas
date: "2022-04-11"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/cft-collaborative-fungible-token/8896
views: 787
likes: 1
posts_count: 3
---

# CFT - Collaborative Fungible Token

**I propose a new type of token, CFT - Collaborative Fungible Token**

It consists of a token that is created between different members of the community, each one will contribute a grain of sand or portion of the token and together a whole will be formed.

There are 2 types of owners:

1. The owner or owners of the CFT, who will have the power to decide what to do with it, for example put it up for sale or exchange it.
2. The monetary owners of the pixels/percentage/shares that will be able to exchange them individually and receive the royalties that correspond to them.

I give you an example based on the mural [r/place of Reddit](https://www.reddit.com/r/place/), imagine a mural of 1000 by 1000 pixels, each user or address will have permission to paint one or more pixels in one color, once they are all painted the mural or Token will be complete and it will belong to all the users who participated in its creation, each user will own a percentage that will depend on their involvement, that is, if you painted 2 pixels, you own twice as much as whoever painted 1.

I am currently working on a simple demo version of how to form a CFT, it is deployed on the BSC Testnet.

If you’re interested in me being on other testnets, let me know.

[TokenizedPixel](https://autotoken.tech/TokenizedPixel/index.php)

I present to you the draft of a CFT, I have treated the portions of the CFT as pixels, I hope you find it interesting and help me improve it

```auto
// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 = prices[coordX][coordY] && prices[coordX][coordY] != 0, "Very low quantity or is it not for sale");
        payable(owners[coordX][coordY]).transfer(msg.value);
        owners[coordX][coordY] = msg.sender;
        prices[coordX][coordY] = 0;
    }

    function sellPixel(uint price, uint coordX, uint coordY) external
        //  Sell Pixel
    {
        require(owners[coordX][coordY] == msg.sender, "You are not the owner");
        prices[coordX][coordY] = price*100000;
    }

    function cancelSellPixel(uint coordX, uint coordY) external
        // Cancel the sale of a pixel
    {
        require(owners[coordX][coordY] == msg.sender && prices[coordX][coordY] >= 1, "You are not the owner");
        prices[coordX][coordY] = 0;
    }

    function setNewColor(string memory color, uint coordX, uint coordY) external
        //  The owner can change the color of his pixel
    {
        require(owners[coordX][coordY] == msg.sender, "You are not the owner");
        colors[coordX][coordY] = color;
    }

    function drawPixel(string memory color, uint coordX, uint coordY) external
        //  Color a pixel, and save data like the owner, and the color
    {
        require(checkPixel(coordX, coordY) == false && coordX < 30 && coordY < 30, "Token Complete");
        owners[coordX][coordY] = msg.sender;
        colors[coordX][coordY] = color;

    }

    function checkPixel(uint coordX, uint coordY) private view returns(bool)
        //  Check if there is any pixel without owner, if not, block the modifications
        //  This way of ending the CFT can be changed to a time limit for example
    {
        if(owners[coordX][coordY]==address(0)){
            return false;
        }
        return true;
    }

    function checkIsComplete() external view returns(bool)
        //  Check if there is any pixel without owner, if not, block the modifications
        //  This way of ending the CFT can be changed to a time limit for example
    {
        for(uint i=0; i<30; i++){
            for(uint j=0; j<30; j++){
                if(owners[i][j]==address(0)){
                    return false;
                }
            }
        }
        return true;
    }

    // Getters

    function getOwners() external view returns(address[30][30] memory)
        // Returns the array of pixel owners
    {
        return owners;
    }

    function getColors() external view returns(string[30][30] memory)
        // Returns the color matrix of the CFT
        // This is the function that should be called to build the CFT
    {
        return colors;
    }

    function getPrices() external view returns(uint[30][30] memory)
        // Returns the prices matrix of the CFT
    {
        return prices;
    }

    function getOwnPixels(address owner) external view returns(uint)
        // Returns the number of pixels that msg.sender has
    {
        uint cont=0;
        for(uint i=0; i<30; i++){
            for(uint j=0; j<30; j++){
                if(owners[i][j]==owner){
                    cont++;
                }
            }
        }
        return cont;
    }

}
```

## Replies

**Luomoneros** (2022-04-21):

This could be an interesting development, however it’s a bit like tokenizing a token…

I think that with a fungible token it is not possible: how do you identify that 10 pixels are mine?

---

**mukas** (2022-04-21):

Exactly, it is like a tokenized token, but more like a shared NFT, the difference is in being able to treat it as a whole.

There are 2 types of owners:

1. The owner or owners of the CFT, who will have the power to decide what to do with it, for example put it up for sale or exchange it.
2. The monetary owners of the pixels/percentage/shares that will be able to exchange them individually and receive the royalties that correspond to them.

The owner is known by the coordinates (as well as the price), owners[i][j] = pixels[i][j] = prices[i][j], also now reading your comment I realize that this surely it can be improved.

I hope to finish the smart contract as soon as possible to be able to make everything much clearer, thanks for your comment, greetings

