// We'll use Puppeteer is our browser automation framework.
const puppeteer = require('puppeteer-extra');

//const exec = require('child_process').exec;

//exec('taskkill /F /IM chrome.exe', () => {})

const pluginStealth = require('puppeteer-extra-plugin-stealth') 
const {executablePath} = require('puppeteer'); 

const express = require('express');
const app = express();
 
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
    headless: 'new',
  });
  const page = await browser.newPage();
  

  // Prepare for the tests (not yet implemented).
  
  console.log("hier -1")
  // Navigate to the page that will perform the tests.
  const testUrl = 'https://translate.google.com/?sl=de&tl=es&op=translate';
  await page.goto(testUrl);
  //await page.setBypassCSP(true);

  //await preparePageForTests(page);

  await page.waitForSelector('#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.AIC7ge > div.CxJub > div.VtwTSb > form:nth-child(2) > div > div > button > div.VfPpkd-RLmnJb')
  await page.click('#yDmH0d > c-wiz > div > div > div > div.NIoIEf > div.G4njw > div.AIC7ge > div.CxJub > div.VtwTSb > form:nth-child(2) > div > div > button > div.VfPpkd-RLmnJb')

  console.log("hier 0")

  await page.waitForNavigation()
  await page.setBypassCSP(true);

  await preparePageForTests(page)

  await page.waitForTimeout(2000)

  console.log("hier 1")

  await page.waitForSelector('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-RLmnJb')
  await page.click('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-RLmnJb')

  await page.waitForTimeout(3000)

  console.log("Sprachserver online. Warte auf Interaktion..")

  app.get('/status', (req, res) => res.send('Up!'))

  let previousText = '';
  let iterationsSinceLastChange = 0;

  let recognizedSentence = null;
  let paused = false;

  let temperature = 0;
  let humidity = 0;

  app.get('/sentence', (req, res) => {
    res.send(recognizedSentence)
    recognizedSentence = null;
  }
  )

  app.get('/pause', async (req, res) => {
    paused = true;

    await page.evaluate(() => {

      let main_button_element = document.querySelector('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-RLmnJb') 

      main_button_element.click()
    })

    res.send('')
  })

  app.get('/unpause', (req, res) => {
    paused = false;

    res.send('')
  })

  app.get('/set_env', (req, res) => {
    console.log(req.query)

    temperature = Number(req.query.temp)
    humidity = Number(req.query.humid)

    res.send('')
  })

  app.get('/get_env', (req, res) => {
    res.send({
      'temperature': temperature,
      'humidity': humidity
    })
  })

  app.listen(3000, () => {})

  while(true) {
    if (paused) {
      console.log("Ich mache Pause.")
      await page.waitForTimeout(500)
      continue;
    }

    const {text, reenabled} = await page.evaluate(async () => {
      let activate_button = document.querySelector('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > span > svg')
      let main_button_element = document.querySelector('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-RLmnJb')

      let reenabled = false;

      if (!(activate_button?.getAttribute('enable-background'))) {
        main_button_element.click()
        reenabled = true;
      }

      if (reenabled) {
        await new Promise(resolve => setTimeout(resolve, 350))
      }

      let content = null

      while(true) {    
        content = document.querySelector('[aria-label="Source text"]').nextElementSibling.innerHTML;

        if (content == null) {
          await new Promise(resolve => setTimeout(resolve, 100))
        } else {
          break;
        }
      }

      return {
        'text': content,
        'reenabled': reenabled
      }
    })

    if (reenabled){
      console.log("neu aktiviert")
    }


    await page.waitForTimeout(100)

    const textChanged = text !== previousText
    previousText = text

    if (textChanged) {
      iterationsSinceLastChange = 0;

      continue;
    }

    if (iterationsSinceLastChange >= 20 && text.length > 0) {
      console.log(text)

      await page.evaluate(() => {

        let main_button_element = document.querySelector('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-RLmnJb')
        
        //console.log(main_button_element)  

        main_button_element.click()

        const escapeHTMLPolicy = trustedTypes.createPolicy("forceInner", {createHTML: (to_escape) => to_escape})

        document.querySelector('[aria-label="Source text"]').nextElementSibling.innerHTML = escapeHTMLPolicy.createHTML("");

      })

      iterationsSinceLastChange = 0
      previousText = '';
      recognizedSentence = text

      continue
    }

    iterationsSinceLastChange += 1

    console.log(iterationsSinceLastChange)
  }

  // Clean up.
  await browser.close()
})();

