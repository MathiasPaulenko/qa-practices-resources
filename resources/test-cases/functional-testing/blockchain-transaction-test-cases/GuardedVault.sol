// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// Minimal contract used by the transaction test suite:
/// onlyOwner withdraw + receive ETH to exercise authorization reverts.
contract GuardedVault {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    receive() external payable {}

    function withdraw() external {
        require(msg.sender == owner, "not owner");
        payable(owner).transfer(address(this).balance);
    }
}
