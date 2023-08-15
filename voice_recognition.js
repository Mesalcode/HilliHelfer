// We'll use Puppeteer is our browser automation framework.
const puppeteer = require('puppeteer-extra');

const pluginStealth = require('puppeteer-extra-plugin-stealth') 
const {executablePath} = require('puppeteer'); 
 
// Use stealth 
puppeteer.use(pluginStealth()) 

// This is where we'll put the code to get around the tests.
const preparePageForTests = async (page) => {
  // Pass the User-Agent Test.
  const userAgent = 'Mozilla/5.0 (X11; Linux x86_64)' +
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.39 Safari/537.36';
  await page.setUserAgent(userAgent);

  // Pass the Webdriver Test.
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', {
      get: () => false,
    });
  });

  // Pass the Chrome Test.
  await page.evaluateOnNewDocument(() => {
    // We can mock this in as much depth as we need for the test.
    window.navigator.chrome = {
      runtime: {},
      // etc.
    };
  });

  // Pass the Permissions Test.
  await page.evaluateOnNewDocument(() => {
    const originalQuery = window.navigator.permissions.query;
    return window.navigator.permissions.query = (parameters) => (
      parameters.name === 'notifications' ?
        Promise.resolve({ state: Notification.permission }) :
        originalQuery(parameters)
    );
  });

  // Pass the Plugins Length Test.
  await page.evaluateOnNewDocument(() => {
    // Overwrite the `plugins` property to use a custom getter.
    Object.defineProperty(navigator, 'plugins', {
      // This just needs to have `length > 0` for the current test,
      // but we could mock the plugins too if necessary.
      get: () => [1, 2, 3, 4, 5],
    });
  });

  // Pass the Languages Test.
  await page.evaluateOnNewDocument(() => {
    // Overwrite the `plugins` property to use a custom getter.
    Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en'],
    });
  });
}

(async () => {
  // Launch the browser in headless mode and set up a page.
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--use-fake-ui-for-media-stream'],
    headless: false,
  });
  const page = await browser.newPage();

  // Prepare for the tests (not yet implemented).
  

  // Navigate to the page that will perform the tests.
  const testUrl = 'https://translate.google.com/?sl=de&tl=es&op=translate';
  await page.goto(testUrl);

  await preparePageForTests(page);

  await page.waitForSelector('#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.AIC7ge > div.CxJub > div.VtwTSb > form:nth-child(2) > div > div > button > span')
  await page.click('#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.AIC7ge > div.CxJub > div.VtwTSb > form:nth-child(2) > div > div > button > span')

  await page.waitForNavigation()

  await preparePageForTests(page);

  await page.waitForTimeout(2000)

  await page.waitForSelector('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-RLmnJb')
  await page.click('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-RLmnJb')

  await page.waitForTimeout(1000000)

  // Clean up.
  await browser.close()
})();

