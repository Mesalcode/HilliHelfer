import asyncio
from pyppeteer import launch

async def main():
    print("main evoked")

    browser = await launch({'headless': False, 'args': [ '--use-fake-ui-for-media-stream' ]})
    page = await browser.newPage()
    await page.goto('https://translate.google.com')

    await page.waitFor(10000)

asyncio.get_event_loop().run_until_complete(main())