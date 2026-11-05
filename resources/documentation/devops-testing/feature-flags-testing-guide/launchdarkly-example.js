// Reference snippet for the "LaunchDarkly Configuration" section of the guide.
// Requires: npm install launchdarkly-js-client-sdk@^3
// Runs in the browser against a real LaunchDarkly project — not part of `npm test`.

import * as LDClient from 'launchdarkly-js-client-sdk';

const client = LDClient.initialize('YOUR_CLIENT_SIDE_ID', { key: 'user-123' });
await client.waitForInitialization();

// Second argument is the fallback when the flag is missing or the SDK fails.
const showFeature = client.variation('new-dashboard', false);
if (showFeature) {
  render(<NewDashboard />);
} else {
  render(<Dashboard />);
}

// Mid-session flag changes re-render the affected surface.
client.on('change:new-dashboard', (value) => {
  value ? render(<NewDashboard />) : render(<Dashboard />);
});
