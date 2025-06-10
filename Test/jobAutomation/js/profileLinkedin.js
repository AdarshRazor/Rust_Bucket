const puppeteer = require('puppeteer');
const fs = require('fs').promises;

const url = 'https://www.linkedin.com/in/khushi-sinha-813052263/';

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Set user agent and viewport to avoid bot detection
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36');
  await page.setViewport({ width: 1280, height: 800 });

  try {
    // Navigate to the profile page
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Wait for key profile elements to load
    await page.waitForSelector('.pv-top-card');

    // Extract profile details
    const profileData = await page.evaluate(() => {
      const name = document.querySelector('.pv-top-card h1')?.textContent?.trim() || 'N/A';
      const headline = document.querySelector('.pv-top-card .text-body-medium')?.textContent?.trim() || 'N/A';
      const about = document.querySelector('.pv-about-section .pv-about__summary-text')?.textContent?.trim() || 'N/A';
      
      return { name, headline, about };
    });

    // Format and save the output
    const output = `
Profile URL: ${url}
Name: ${profileData.name}
Headline: ${profileData.headline}
About: ${profileData.about}
    `.trim();

    await fs.writeFile('profile_result.txt', output);
    console.log('✅ Profile data saved to profile_result.txt');

  } catch (error) {
    console.error('Error scraping profile:', error.message);
  } finally {
    await browser.close();
  }
})();