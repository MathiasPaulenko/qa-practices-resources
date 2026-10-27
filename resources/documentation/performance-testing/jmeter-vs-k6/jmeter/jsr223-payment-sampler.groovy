import groovy.json.JsonBuilder
import groovy.json.JsonSlurper

// JMeter 5.6.3 — JSR223 Sampler (Groovy) for the NovaPay payment body.
// The card token comes from a CSV Data Set Config element.

def token = vars.get("cardToken")
def body = new JsonBuilder([
    amount: 99.99,
    currency: "USD",
    token: token
]).toString()

sampler.setPostBodyRaw(true)
sampler.getArguments().clear()
sampler.addNonEncodedArgument("", body, "")

// Later, in a JSR223 PostProcessor, extract transactionId for the refund step
def response = prev.getResponseDataAsString()
def json = new JsonSlurper().parseText(response)
vars.put("transactionId", json.transactionId.toString())
