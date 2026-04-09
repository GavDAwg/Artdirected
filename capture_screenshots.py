#!/usr/bin/env python3
"""Capture screenshots of a website at different viewport sizes."""

from playwright.sync_api import sync_playwright
import os

def capture_screenshots(url, output_dir="screenshots"):
    """Capture screenshots at desktop, tablet, and mobile viewports."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define viewports
    viewports = {
        "desktop_1920x1080": {"width": 1920, "height": 1080},
        "tablet_768x1024": {"width": 768, "height": 1024},
        "mobile_375x812": {"width": 375, "height": 812},
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for viewport_name, viewport_size in viewports.items():
            print(f"Capturing {viewport_name}...")
            
            page = browser.new_page(viewport=viewport_size)
            
            try:
                # Navigate to the URL and wait for network to be idle
                page.goto(url, wait_until='networkidle')
                
                # Take screenshot
                output_path = os.path.join(output_dir, f"{viewport_name}.png")
                page.screenshot(path=output_path, full_page=False)
                print(f"✓ Saved: {output_path}")
                
            except Exception as e:
                print(f"✗ Error capturing {viewport_name}: {e}")
            finally:
                page.close()
        
        browser.close()

if __name__ == "__main__":
    url = "https://art-directed.com"
    capture_screenshots(url)
    print("\nScreenshots capture complete!")
