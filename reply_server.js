// We'll use Puppeteer is our browser automation framework.
const puppeteer = require('puppeteer');

const pluginStealth = require('puppeteer-extra-plugin-stealth') 
const {executablePath} = require('puppeteer'); 

//const exec = require('child_process').exec;

//exec('taskkill /F /IM chrome.exe', () => {})

//const express = require('express');
//const app = express();
//app.use(express.json()) 
 
// Use stealth 
//puppeteer.use(pluginStealth()) 

// This is where we'll put the code to get around the tests.

(async () => {
  // Launch the browser in headless mode and set up a page.
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--use-fake-ui-for-media-stream'],
    headless: false,
  });
  const page = await browser.newPage();

  await page.goto('https://character.ai')

  //await preparePageForTests(page);

  await page.waitForSelector('#mobile-app-modal-close')
  await page.click('#mobile-app-modal-close')

  await page.waitForTimeout(3000)

  await page.evaluate(() => {
    document.getElementById("#AcceptButton").click()
  })

  await page.waitForTimeout(2000)

  await page.waitForSelector('#header-row > div:nth-child(5) > div:nth-child(1) > button')
  await page.click('#header-row > div:nth-child(5) > div:nth-child(1) > button')

  await page.waitForNavigation()

  userInput = await page.waitForSelector('#username')
  await userInput.type('botmusic79@gmail.com')

  await page.waitForTimeout(3000)

  passInput = await page.waitForSelector('#password')
  await passInput.type('HilliHelfer123')

  await page.waitForSelector('body > div > main > section > div > div > div > form > div.c22fea258 > button')
  await page.click('body > div > main > section > div > div > div > form > div.c22fea258 > button')

  await page.waitForNavigation()

    await page.waitForTimeout(3000)

  //await preparePageForTests(page)

  await page.waitForSelector('#discover-page > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > div > div')
  await page.click('#discover-page > div > div > div > div:nth-child(1) > div:nth-child(2) > div > div > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > div > div')

  //await page.goto('https://beta.character.ai/chat2?char=a9Pdcl24K0VDknXiPbsCle2TLApwaupblK23KM-GHtg')

  //await page.waitForTimeout(100000)
  // Prepare for the tests (not yet implemented).
  
  // Navigate to the page that will perform the tests.

  //await page.setRequestInterception(true);

  
  await page.waitForTimeout(5000)

  await page.setRequestInterception(true);

  input_field = await page.waitForSelector('#user-input')
  await input_field.type('Was machst du beruflich?')

  await page.waitForSelector('#send-btn-icon')
  await page.click('#send-btn-icon')

  app.post('/get_reply', async (req, res) => {
    query = req.body



    await page.evaluate(textToEnter => {
      document.querySelector("#user-input").innerHTML = textToEnter
    }, query)
  })

  await page.waitForTimeout(3000)


  console.log("accepted")

  await page.waitForTimeout(100000);
})();