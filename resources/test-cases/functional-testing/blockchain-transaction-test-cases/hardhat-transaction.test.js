// Hardhat 2.22 + ethers 6.x — executable versions of the transaction test cases.
// Run: npx hardhat test hardhat-transaction.test.js
import { expect } from "chai";
import hre from "hardhat";
const { ethers } = hre;

describe("Blockchain transaction test cases", function () {
  it("TC-01: simple value transfer moves balance", async function () {
    const [sender, receiver] = await ethers.getSigners();
    const tx = await sender.sendTransaction({
      to: receiver.address,
      value: ethers.parseEther("1")
    });
    await expect(tx).to.changeEtherBalance(receiver, ethers.parseEther("1"));
  });

  it("TC-02: receipt exposes status, gas and block", async function () {
    const [sender, receiver] = await ethers.getSigners();
    const tx = await sender.sendTransaction({
      to: receiver.address,
      value: ethers.parseEther("0.1")
    });
    const receipt = await tx.wait();
    expect(receipt.status).to.equal(1);
    expect(receipt.blockNumber).to.be.greaterThan(0);
    expect(receipt.gasUsed).to.equal(21000n);
  });

  it("TC-06: sequential nonces mine in order", async function () {
    const [sender, r1, r2] = await ethers.getSigners();
    const n0 = await sender.getNonce();
    const txA = await sender.sendTransaction({ to: r1.address, value: 1n, nonce: n0 });
    const txB = await sender.sendTransaction({ to: r2.address, value: 1n, nonce: n0 + 1 });
    const [rA, rB] = await Promise.all([txA.wait(), txB.wait()]);
    expect(rA.blockNumber).to.be.lessThanOrEqual(rB.blockNumber);
  });

  it("TC-12: zero-balance account cannot send", async function () {
    const fresh = ethers.Wallet.createRandom().connect(ethers.provider);
    const [funder] = await ethers.getSigners();
    await expect(
      fresh.sendTransaction({ to: funder.address, value: 1n })
    ).to.be.rejected;
  });

  it("TC-19: non-owner call to onlyOwner reverts", async function () {
    const [owner, stranger] = await ethers.getSigners();
    const Guarded = await ethers.getContractFactory("GuardedVault", owner);
    const vault = await Guarded.deploy();
    await vault.waitForDeployment();
    await expect(vault.connect(stranger).withdraw()).to.be.reverted;
  });
});
