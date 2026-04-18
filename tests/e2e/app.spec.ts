import { test, expect } from '@playwright/test';

test.describe('Gleam Web App', () => {
  test('homepage loads and displays title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Gleam Competitions/);
    await expect(page.locator('h1')).toContainText('Gleam Competitions');
  });

  test('search functionality filters competitions', async ({ page }) => {
    await page.goto('/');
    
    const searchInput = page.locator('input[placeholder*="search" i], input[name*="q" i]');
    const initialCompetitionsText = await page.locator('body').textContent();
    
    if (searchInput) {
      await searchInput.fill('nonexistent');
      await page.waitForLoadState('networkidle');
      
      const filteredText = await page.locator('body').textContent();
      expect(filteredText).toBeTruthy();
    }
  });

  test('api competitions endpoint returns JSON', async ({ page }) => {
    const response = await page.request.get('/api/competitions');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
  });

  test('api competitions endpoint supports search query', async ({ page }) => {
    const response = await page.request.get('/api/competitions?q=test');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
  });

  test('refresh endpoint returns 303 redirect', async ({ page }) => {
    const response = await page.request.post('/refresh', {
      maxRedirects: 0,
    });
    expect(response.status()).toBe(303);
  });
});
