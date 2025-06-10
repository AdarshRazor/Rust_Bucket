const puppeteer = require('puppeteer');
const fs = require('fs');

const url = 'https://www.linkedin.com/jobs/search/?keywords=frontend%20developer&location=India&f_TPR=r86400&sortBy=DD';

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Set user agent + viewport to avoid bot detection
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36');
  await page.setViewport({ width: 1280, height: 800 });

  await page.goto(url, { waitUntil: 'networkidle2' });

  await page.waitForSelector('a.base-card__full-link');

  // Slow scroll in increments
  for (let i = 0; i < 30; i++) {
    await page.evaluate(() => {
      window.scrollBy(0, 500);
    });
    await new Promise(r => setTimeout(r, 1000));
  }

  // Try clicking "Load more" button if exists
  while (true) {
    try {
      const loadMoreBtn = await page.$('button.infinite-scroller__show-more-button');
      if (!loadMoreBtn) break;
      await loadMoreBtn.click();
      await new Promise(r => setTimeout(r, 2000));
    } catch {
      break;
    }
  }

  // Get job links - try alternate selector if needed
  const jobLinks = await page.$$eval('a.base-card__full-link', links => links.map(link => link.href));

  const output = `✅ Found ${jobLinks.length} job links:\n` + jobLinks.map((link, i) => `${i + 1}. ${link}`).join('\n');
  fs.writeFileSync('result.txt', output);

  console.log('✅ Job links saved to result.txt');

  await browser.close();
})();
