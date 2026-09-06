// Programmatic Lighthouse 12 usage in Node.js
// Install: npm install lighthouse@12 chrome-launcher
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runLighthouse(url) {
    const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
    const options = {
        logLevel: 'info',
        output: 'json',
        onlyCategories: ['performance'],
        port: chrome.port,
    };

    const result = await lighthouse(url, options, null);

    const score = Math.round(result.lhr.categories.performance.score * 100);
    const lcp = result.lhr.audits['largest-contentful-paint'].displayValue;
    const inp = result.lhr.audits['interaction-to-next-paint'].displayValue;
    const cls = result.lhr.audits['cumulative-layout-shift'].displayValue;

    console.log(`Performance score: ${score}/100`);
    console.log(`LCP: ${lcp}`);
    console.log(`INP: ${inp}`);
    console.log(`CLS: ${cls}`);

    await chrome.kill();
    return { score, lcp, inp, cls };
}

const url = process.argv[2] || 'https://staging.qa.local';
runLighthouse(url).catch((err) => {
    console.error('Lighthouse run failed:', err);
    process.exit(1);
});
