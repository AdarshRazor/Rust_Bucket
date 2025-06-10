const puppeteer = require('puppeteer');
const fs = require('fs');

// URLs
const linkedinURL = 'https://www.linkedin.com/jobs/search/?keywords=frontend%20developer&location=India&f_TPR=r86400&sortBy=DD';
const naukriURL = 'https://www.naukri.com/frontend-developer-jobs-in-delhi?k=frontend%20developer&l=delhi%2C%20gurugram&experience=2';

// Launch Puppeteer Browser
const launchBrowser = async () => {
  return puppeteer.launch({ headless: true });
};

// Scroll Page
const slowScroll = async (page, scrollCount = 30) => {
  for (let i = 0; i < scrollCount; i++) {
    await page.evaluate(() => window.scrollBy(0, 500));
    await new Promise(r => setTimeout(r, 1000));
  }
};

// Scrape LinkedIn Jobs
const scrapeLinkedIn = async () => {
  const browser = await launchBrowser();
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36');
  await page.setViewport({ width: 1280, height: 800 });

  await page.goto(linkedinURL, { waitUntil: 'networkidle2' });
  await page.waitForSelector('a.base-card__full-link', { timeout: 30000 });

  await slowScroll(page);

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

  const jobLinks = await page.$$eval('a.base-card__full-link', links => links.map(link => link.href));
  fs.writeFileSync('linkedin_links.txt', jobLinks.map((link, i) => `${i + 1}. ${link}`).join('\n'));

  console.log('✅ LinkedIn job links saved to linkedin_links.txt');
  await browser.close();
};

// Scrape Naukri Jobs
const scrapeNaukri = async () => {
  const browser = await launchBrowser();
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36');
  await page.setViewport({ width: 1280, height: 800 });

  await page.goto(naukriURL, { waitUntil: 'networkidle2' });
  await page.waitForSelector('.jobTuple', { timeout: 30000 });

  await slowScroll(page);

  const jobLinks = await page.$$eval('.jobTuple a.title', links => links.map(link => link.href));
  fs.writeFileSync('naukri_links.txt', jobLinks.map((link, i) => `${i + 1}. ${link}`).join('\n'));

  console.log('✅ Naukri job links saved to naukri_links.txt');
  await browser.close();
};

// 📌 Choose which to run:
(async () => {
  // await scrapeLinkedIn(); // Uncomment to run LinkedIn
  await scrapeNaukri();      // Uncomment to run Naukri
})();
