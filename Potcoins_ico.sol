// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract potcoin_ico {

    // Introducing the maximum number of Potcoins available for sale
    uint public max_potcoins = 1000000;

    // Introducing the AUD to Potcoins conversion rate
    uint public aud_to_potcoins = 1000;

    // Introducing the total number of Potcoins that have been purchased by investors
    uint public total_potcoins_bought = 0;

    // Mapping from the investor address to its equity in Potcoins and AUD
    mapping(address => uint) equity_potcoins;
    mapping(address => uint) equity_aud;

    //Checking if an investor can buy Potcoin
    modifier can_buy_potcoins(uint aud_invested) {
        require(aud_invested * aud_to_potcoins + total_potcoins_bought <= max_potcoins);
        _;
    }

    //Getting the equity in Potcoins of an investor
    function equity_in_potcoins(address investor) external view returns (uint) {    
        return equity_potcoins[investor];
    }   

    //Getting the equity in AUD of an investor
    function equity_in_aud(address investor) external view returns (uint) {     
        return equity_aud[investor];
    }

    //Buying Potcoins
    function buy_potcoins(address investor, uint aud_invested) external 
    can_buy_potcoins(aud_invested) {
        uint potcoins_bought = aud_invested * aud_to_potcoins;
        equity_potcoins[investor] += potcoins_bought;
        equity_aud[investor] = equity_potcoins[investor] / 1000;
        total_potcoins_bought += potcoins_bought;
    }

    //Selling Potcoins
    function sell_potcoins(address investor, uint potcoins_sold) external {
        equity_potcoins[investor] += potcoins_sold;
        equity_aud[investor] = equity_potcoins[investor] / 1000;
        total_potcoins_bought -= potcoins_sold;
    }
}
