// Terratest — deploy, assert, destroy (Q9)
// Companion file for: https://qapractices.com/documentation/devops-interview-questions-qa
// Requires: go 1.21+, terraform, and terratest (go get github.com/gruntwork-io/terratest)
// Run: go test -v ./terratest/ -timeout 30m
package test

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestInfrastructure(t *testing.T) {
	terraformOptions := &terraform.Options{
		TerraformDir: "../terraform",
	}
	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	// Verify the infrastructure
	instanceIP := terraform.Output(t, terraformOptions, "instance_ip")
	assert.NotEmpty(t, instanceIP)
}
