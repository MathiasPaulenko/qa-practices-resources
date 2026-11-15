// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {SimpleVault} from "../src/SimpleVault.sol";

contract SimpleVaultTest is Test {
    SimpleVault vault;
    address alice = makeAddr("alice");
    address bob   = makeAddr("bob");

    function setUp() public {
        vault = new SimpleVault();
        vm.deal(alice, 10 ether);
        vm.deal(bob, 10 ether);
    }

    function testDepositUpdatesBalance() public {
        vm.prank(alice);
        vault.deposit{value: 1 ether}();
        assertEq(vault.balances(alice), 1 ether);
        assertEq(vault.totalHoldings(), 1 ether);
    }

    function testWithdrawReturnsFunds() public {
        vm.prank(alice);
        vault.deposit{value: 2 ether}();
        vm.prank(alice);
        vault.withdraw(2 ether);
        assertEq(vault.balances(alice), 0);
        assertEq(alice.balance, 10 ether);
    }

    function testWithdrawInsufficientBalanceReverts() public {
        vm.prank(bob);
        vm.expectRevert("insufficient balance");
        vault.withdraw(1 ether);
    }

    function testZeroDepositReverts() public {
        vm.prank(alice);
        vm.expectRevert("zero deposit");
        vault.deposit{value: 0}();
    }

    function testDepositEmitsEvent() public {
        vm.prank(alice);
        vm.expectEmit(true, false, false, true);
        emit SimpleVault.Deposit(alice, 1 ether);
        vault.deposit{value: 1 ether}();
    }

    function testFuzz_DepositWithinBalance(uint96 amount) public {
        vm.assume(amount > 0 && amount <= 10 ether);
        vm.prank(alice);
        vault.deposit{value: amount}();
        assertEq(vault.balances(alice), amount);
    }

    function testFuzz_WithdrawNeverExceedsDeposit(uint96 depositAmt, uint96 withdrawAmt) public {
        vm.assume(depositAmt > 0 && depositAmt <= 10 ether);
        vm.prank(alice);
        vault.deposit{value: depositAmt}();
        if (withdrawAmt > depositAmt) {
            vm.prank(alice);
            vm.expectRevert("insufficient balance");
            vault.withdraw(withdrawAmt);
        }
    }
}
