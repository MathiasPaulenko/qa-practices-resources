// Groovy assertion for SoapUI
// Add as a Groovy Script assertion on your AuthorizePayment test step
// Uses XmlSlurper for XPath-based checks instead of raw contains

def response = context.expand('${AuthorizePayment#Response}')
def xml = new XmlSlurper().parseText(response)

// Assert Status is APPROVED
assert xml.Body.AuthorizePaymentResponse.Status == 'APPROVED' : "Expected APPROVED, got ${xml.Body.AuthorizePaymentResponse.Status}"

// Assert TransactionId is 10 digits
assert xml.Body.AuthorizePaymentResponse.TransactionId =~ /^\d{10}$/ : "TransactionId does not match 10-digit pattern"

// Assert Timestamp is present
assert xml.Body.AuthorizePaymentResponse.Timestamp != null : "Timestamp is missing from response"

log.info "All SOAP response assertions passed"
