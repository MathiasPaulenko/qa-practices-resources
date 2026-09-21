function fn() {
  // Karate 2.x resolves this file on the classpath or working directory.
  // Override with: java -jar karate.jar -DbaseUrl=https://staging.example.com users-api.feature
  var config = {
    baseUrl: 'https://jsonplaceholder.typicode.com'
  };
  return config;
}
