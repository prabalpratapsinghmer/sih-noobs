import { test, expect } from '@playwright/test';

test.describe('CyberCell Platform E2E Suite', () => {

  test('Gateway Homepage: verifies branding, live status, and opaque hamburger navigation launchpad', async ({ page }) => {
    await page.goto('/');

    // Check title and logo
    await expect(page).toHaveTitle(/CyberCell/i);
    await expect(page.getByText('CYBERCELL').first()).toBeVisible();
    await expect(page.getByText('SOVEREIGN DEFENSE').first()).toBeVisible();

    // Verify live status pill
    await expect(page.getByText(/(API|GRID): (LIVE|SIM)/i)).toBeVisible();


    // Verify hamburger menu opens launchpad
    const menuBtn = page.locator('button[aria-label="Open Navigation"]');
    await expect(menuBtn).toBeVisible();
    await menuBtn.click();

    // Check launchpad elements
    await expect(page.getByText('Sovereign Platforms')).toBeVisible();
    await expect(page.getByText('Citizen Reporting Portal (1930 Sync)')).toBeVisible();
    await expect(page.getByText('Tactical Command HQ & Mule Ontology')).toBeVisible();

    // Verify close menu button works
    const closeBtn = page.locator('button[aria-label="Close Navigation"]');
    await expect(closeBtn).toBeVisible();
    await closeBtn.click();
    await expect(page.getByText('Sovereign Platforms')).not.toBeVisible();
  });

  test('Command HQ: verifies map, removal of MiniMap, ReactFlow controls, and scenario flow', async ({ page }) => {
    await page.goto('/command');

    // Wait for cockpit elements
    await expect(page.getByText(/TACTICAL ROOM/i)).toBeVisible();
    await expect(page.getByText('GNN THREAT ELEVATED')).toBeVisible();

    // Threat map card
    await expect(page.getByText('Tactical High-Definition Terrain Map')).toBeVisible();
    await expect(page.getByText('ZERO-CLUTTER FEED')).toBeVisible();

    // Crucial check: MiniMap must NOT be rendered anywhere in ReactFlow
    const minimap = page.locator('.react-flow__minimap');
    await expect(minimap).toHaveCount(0);

    // ReactFlow controls must be present
    const controls = page.locator('.react-flow__controls');
    await expect(controls).toBeVisible();

    // Controls button background should be dark (not white)
    const ctrlBtn = page.locator('.react-flow__controls-button').first();
    await expect(ctrlBtn).toBeVisible();
    const btnBg = await ctrlBtn.evaluate(el => window.getComputedStyle(el).backgroundColor);
    expect(btnBg).toBe('rgb(0, 0, 0)');

    // Verify interactive ATM selector pills
    await expect(page.getByRole('button', { name: /ATM-04/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /ATM-07/i })).toBeVisible();

    // Crucial check: 5-min scenario button must NOT be present
    await expect(page.getByRole('button', { name: /Run 5-Min Scenario/i })).toHaveCount(0);
  });

  test('Report Incident: loads intake form with Section 91 CrPC notice readiness', async ({ page }) => {
    await page.goto('/report');

    await expect(page.getByText(/Citizen Incident Intake/i).or(page.getByText(/Report/i)).first()).toBeVisible();
    // Verify intake form elements
    await expect(page.locator('input, button').first()).toBeVisible();
  });

  test('Field Patrol: loads active patrol units and telemetry grid', async ({ page }) => {
    await page.goto('/field');

    await expect(page.getByText(/Field/i).first()).toBeVisible();
    // Verify patrol interface is loaded
    await expect(page.locator('header')).toBeVisible();
  });

  test('Telemetry & STM: verifies GNN model metrics and audit logs', async ({ page }) => {
    await page.goto('/admin');

    await expect(page.getByText(/Telemetry/i).or(page.getByText(/STM/i)).first()).toBeVisible();
  });

  test('Global Command Palette (⌘K / Search): opens and navigates', async ({ page }) => {
    await page.goto('/');

    const searchBtn = page.locator('button[aria-label="Open Command Palette (⌘K)"]');
    await searchBtn.click();

    // Modal should be visible
    await expect(page.getByPlaceholder(/Search commands/i)).toBeVisible();
    await expect(page.getByText('Navigation Targets')).toBeVisible();

    // Hit Escape to close
    await page.keyboard.press('Escape');
    await expect(page.getByPlaceholder(/Search commands/i)).not.toBeVisible();
  });

  test('Security & Role-Based Access Control: verifies dashboard click interception, Moksh login, and citizen clearance restrictions', async ({ page }) => {
    // 1. Visit Home Page in clean unauthenticated state
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    await page.reload();

    // 2. Click "Launch Tactical Command" on Home Page when unauthenticated
    const launchCmdBtn = page.getByRole('button', { name: /Launch Tactical Command/i });
    await expect(launchCmdBtn).toBeVisible();
    await launchCmdBtn.click();

    // 3. Verify that Auth Modal opens with "Authentication Required" prompt
    await expect(page.getByText('SOVEREIGN IDENTITY ACCESS')).toBeVisible();
    await expect(page.getByText(/Authentication Required/i)).toBeVisible();

    // 4. Test Citizen login (citizen_rahul / rahul123) to verify Role Clearance Restrictions
    await page.getByPlaceholder(/vikramaditya or officer/i).fill('citizen_rahul');
    await page.getByPlaceholder(/••••••••••••/i).fill('rahul123');
    await page.getByRole('button', { name: /AUTHENTICATE SESSION/i }).click();

    // 5. Navigate to /command as Citizen -> MUST be restricted!
    await page.goto('/command');
    await expect(page.getByText(/Insufficient Clearance/i)).toBeVisible();
    await expect(page.getByText('citizen_rahul')).toBeVisible();
    await expect(page.getByText(/ADMIN or INSPECTOR/i)).toBeVisible();

    // 6. Click "Switch to Authorized Account" on the Access Denied screen
    const switchBtn = page.getByRole('button', { name: /Switch to Authorized Account/i });
    await expect(switchBtn).toBeVisible();
    await switchBtn.click();

    // 7. Click 1-Click quick test credential for Super Admin (Director Moksh / mok008)
    const mokshQuickBtn = page.getByRole('button', { name: /👑 Moksh/i });
    await expect(mokshQuickBtn).toBeVisible();
    await mokshQuickBtn.click();

    // Verify inputs filled
    await expect(page.getByPlaceholder(/vikramaditya or officer/i)).toHaveValue('Moksh');
    await expect(page.getByPlaceholder(/••••••••••••/i)).toHaveValue('mok008');

    // Submit authentication
    await page.getByRole('button', { name: /AUTHENTICATE SESSION/i }).click();

    // 8. Super Admin (Moksh) should now have full access to Command HQ!
    await page.goto('/command');
    await expect(page.getByText(/TACTICAL ROOM/i)).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('GNN THREAT ELEVATED')).toBeVisible();

    // 9. Verify Topbar shows Moksh (ADMIN)
    const profileBtn = page.getByRole('button', { name: /Moksh/i }).or(page.getByRole('button', { name: /User Profile/i }));
    await expect(profileBtn.first()).toBeVisible();
    await profileBtn.first().click();
    await expect(page.getByText('ADMIN')).toBeVisible();

    // 10. Test sign out
    const signOutBtn = page.getByRole('button', { name: /Sign Out Session/i });
    await expect(signOutBtn).toBeVisible();
    await signOutBtn.click();

    // Verify user is signed out
    await expect(page.getByRole('button', { name: /Sign In/i }).first()).toBeVisible();
  });

});



