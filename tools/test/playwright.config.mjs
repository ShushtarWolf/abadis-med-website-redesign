import { defineConfig } from '@playwright/test';

const BASE = process.env.BASE || 'http://127.0.0.1:8080';

export default defineConfig({
  testDir: '.',
  testMatch: /site\.spec\.mjs$/,
  timeout: 120_000,
  expect: { timeout: 15_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [['list'], ['json', { outputFile: 'out/playwright-report.json' }]],
  use: {
    baseURL: BASE,
    headless: true,
    viewport: { width: 1440, height: 900 },
    ignoreHTTPSErrors: true,
    actionTimeout: 15_000,
  },
  outputDir: 'out/pw-artifacts',
});
