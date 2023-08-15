import asyncio
from pyppeteer import launch

async def main():
    print("main evoked")

    browser = await launch({'headless': False, 'args': [ '--use-fake-ui-for-media-stream' ]})
    page = await browser.newPage()
    await page.goto('https://translate.google.com')

    cookie_btn = await page.Jx('//button[contains(text(), "Alle akzeptieren")]')

    await page.waitForNavigation()
    await page.waitForSelector('#i9 > span.VfPpkd-YVzG2b')
    await page.click('#i9 > span.VfPpkd-YVzG2b')
    await page.waitForSelector('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-Jh9lGc')
    await page.click('#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div > div.AxqVh > div.OPPzxe > c-wiz.rm1UF.UnxENd > div.FFpbKc > div:nth-child(1) > c-wiz > span.jNeWz > div:nth-child(2) > div:nth-child(1) > span > button > div.VfPpkd-Bz112c-Jh9lGc')
    await page.waitFor(100000)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())