// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title SimpleVault — minimal ETH deposit/withdraw vault for testing demos.
/// @notice Withdrawals follow the checks-effects-interactions pattern:
///         the balance is updated BEFORE the external call, so a re-entrant
///         call hits a zeroed balance and reverts.
contract SimpleVault {
    mapping(address => uint256) public balances;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);

    function deposit() external payable {
        require(msg.value > 0, "zero deposit");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient balance");
        balances[msg.sender] -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
        emit Withdrawal(msg.sender, amount);
    }

    function totalHoldings() external view returns (uint256) {
        return address(this).balance;
    }
}
