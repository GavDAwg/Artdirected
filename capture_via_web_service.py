#!/usr/bin/env python3
"""Capture screenshots using web-based screenshot service."""

import urllib.request
import urllib.error
import os
import time

def capture_screenshot_from_service(url, viewport_width, viewport_height, output_path, service="screenshot"):
    """Capture screenshot using web snapshot service."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        if service == "screenshot":
            # Using screenshot.rocks API
            api_url = f"https://api.screenshot.rocks/screenshot?url={urllib.parse.quote(url)}&type=png&width={viewport_width}&height={viewport_height}"
        else:
            raise ValueError(f"Unknown service: {service}")
        
        print(f"Downloading from: {api_url[:60]}...")
        
        with urllib.request.urlopen(api_url, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"✓ Saved {output_path} ({file_size:.1f} KB)")
        return True
        
    except urllib.error.URLError as e:
        print(f"✗ Network error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

import urllib.parse

if __name__ == "__main__":
    url = "https://art-directed.com"
    base_output_dir = "screenshots"
    
    viewports = [
        ("desktop_1920x1080", 1920, 1080),
        ("tablet_768x1024", 768, 1024),
        ("mobile_375x812", 375, 812),
    ]
    
    print(f"Capturing screenshots of {url}\n")
    
    for name, width, height in viewports:
        output_path = os.path.join(base_output_dir, f"{name}.png")
        print(f"Capturing {name}...")
        capture_screenshot_from_service(url, width, height, output_path)
        time.sleep(0.5)  # Rate limiting
    
    print(f"\nScreenshots saved to {base_output_dir}/")
