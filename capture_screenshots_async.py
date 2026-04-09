#!/usr/bin/env python3
"""Capture screenshots using Playwright async API."""

import asyncio
import os
from urllib.parse import urlparse

async def capture_screenshots(url, output_dir="screenshots"):
    """Capture screenshots at desktop, tablet, and mobile viewports."""
    from playwright.async_api import async_playwright
    
    os.makedirs(output_dir, exist_ok=True)
    
    viewports = {
        "desktop_1920x1080": {"width": 1920, "height": 1080},
        "tablet_768x1024": {"width": 768, "height": 1024},
        "mobile_375x812": {"width": 375, "height": 812},
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        for viewport_name, viewport_size in viewports.items():
            print(f"Capturing {viewport_name}...")
            
            context = await browser.new_context(viewport=viewport_size)
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until='networkidle')
                
                output_path = os.path.join(output_dir, f"{viewport_name}.png")
                await page.screenshot(path=output_path, full_page=False)
                print(f"✓ Saved: {output_path}")
                
            except Exception as e:
                print(f"✗ Error capturing {viewport_name}: {e}")
            finally:
                await context.close()
        
        await browser.close()

if __name__ == "__main__":
    url = "https://art-directed.com"
    asyncio.run(capture_screenshots(url))
    print("\nScreenshots capture complete!")
