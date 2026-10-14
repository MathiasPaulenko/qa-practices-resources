// Gatling simulation — same scenario as k6/load-test.js (ramp 20 -> sustain 50 VUs).
// Run: mvn gatling:test -Dgatling.simulationClass=ProductBrowsingSimulation  (Gatling 3.12)
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class ProductBrowsingSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl(System.getProperty("BASE_URL", "https://staging.acme-shop.dev")) // Placeholder: staging URL
    .acceptHeader("application/json")

  val scn = scenario("ProductBrowsing")
    .exec(
      http("list products")
        .get("/api/v1/products")
        .check(status.is(200))
    )
    .pause(1)

  setUp(
    scn.inject(
      rampUsers(20).during(30.seconds),   // ramp
      constantUsersPerSec(50).during(60.seconds) // sustain (approx — rate-based, not VU-based)
    )
  ).protocols(httpProtocol)
    .assertions(
      global.responseTime.percentile3.lt(500),
      global.failedRequests.percent.lt(1.0)
    )
}
