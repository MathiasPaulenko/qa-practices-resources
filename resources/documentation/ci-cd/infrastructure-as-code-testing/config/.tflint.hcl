# tflint config — run with `tflint --config=config/.tflint.hcl`
rule "terraform_unused_declarations" {
  enabled = true
}
rule "terraform_naming_convention" {
  enabled = true
  format  = "snake_case"
}
rule "terraform_deprecated_syntax" {
  enabled = true
}
