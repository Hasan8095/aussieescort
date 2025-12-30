#!/usr/bin/env python3
"""
File Download and Organization Script for Laravel Project
This script downloads files from a URL and organizes them into appropriate directories
based on Laravel conventions and file types.
"""

import os
import sys
import re
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
from urllib.error import URLError, HTTPError

# Base directory for the Laravel project
BASE_DIR = Path('/home/runner/work/aussieescort/aussieescort')

# File type to directory mapping
FILE_TYPE_MAPPING = {
    # Images
    'jpg': 'public/site-img',
    'jpeg': 'public/site-img',
    'png': 'public/site-img',
    'gif': 'public/site-img',
    'svg': 'public/site-img',
    'webp': 'public/site-img',
    'ico': 'public',
    
    # Stylesheets
    'css': 'public/css',
    'scss': 'resources/assets/sass',
    'sass': 'resources/assets/sass',
    
    # Scripts
    'js': 'public/js',
    
    # Fonts
    'ttf': 'public/fonts',
    'otf': 'public/fonts',
    'woff': 'public/fonts',
    'woff2': 'public/fonts',
    'eot': 'public/fonts',
    
    # PHP files
    'php': 'app',
    
    # SQL files
    'sql': 'sql',
    
    # Documents
    'pdf': 'storage/app/documents',
    'doc': 'storage/app/documents',
    'docx': 'storage/app/documents',
    
    # Data files
    'json': 'storage/app/data',
    'xml': 'storage/app/data',
    'csv': 'storage/app/data',
}


class LinkExtractor(HTMLParser):
    """HTML parser to extract file links from a page"""
    
    def __init__(self):
        super().__init__()
        self.links = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href' and value:
                    # Check if this looks like a file link
                    if self.is_file_link(value):
                        self.links.append(value)
    
    def is_file_link(self, url):
        """Check if URL appears to be a file link"""
        if not url or url.startswith('#') or url.startswith('javascript:'):
            return False
        
        # Check if URL has a file extension
        path = urllib.parse.urlparse(url).path
        ext = os.path.splitext(path)[1].lower().lstrip('.')
        
        return ext in FILE_TYPE_MAPPING or ext in ['json', 'xml', 'csv']


def download_file(url, destination):
    """Download a file from URL to destination"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            
        with open(destination, 'wb') as f:
            f.write(content)
        
        return os.path.exists(destination) and os.path.getsize(destination) > 0
    
    except (URLError, HTTPError) as e:
        print(f"  ✗ Failed to download: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def get_target_directory(filename):
    """Determine the target directory for a file based on its extension"""
    # Handle .blade.php files
    if filename.endswith('.blade.php'):
        return BASE_DIR / 'resources/views'
    
    # Get file extension
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    
    # Special logic for PHP files (before general mapping)
    if ext == 'php':
        if 'Controller' in filename:
            return BASE_DIR / 'app/Http/Controllers'
        elif 'Migration' in filename:
            return BASE_DIR / 'database/migrations'
        elif 'Seeder' in filename:
            return BASE_DIR / 'database/seeds'
        elif re.match(r'^[A-Z][a-z]+\.php$', filename):
            return BASE_DIR / 'app'
        else:
            return BASE_DIR / 'app'
    
    # Check direct mapping
    if ext in FILE_TYPE_MAPPING:
        return BASE_DIR / FILE_TYPE_MAPPING[ext]
    
    # Default location for unknown types
    return BASE_DIR / 'storage/app/other'


def get_unique_filepath(directory, filename):
    """Get a unique file path to avoid conflicts"""
    base_path = directory / filename
    
    if not base_path.exists():
        return base_path
    
    name, ext = os.path.splitext(filename)
    counter = 1
    
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_path = directory / new_filename
        
        if not new_path.exists():
            return new_path
        
        counter += 1


def organize_file(filepath):
    """Move a file to its appropriate directory"""
    filename = os.path.basename(filepath)
    target_dir = get_target_directory(filename)
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Get unique target path to avoid conflicts
    target_path = get_unique_filepath(target_dir, filename)
    
    # Move file
    try:
        if filepath != target_path:
            os.rename(filepath, target_path)
        
        relative_path = target_path.relative_to(BASE_DIR)
        print(f"  ✓ Moved to: {relative_path}")
        return True
    
    except Exception as e:
        print(f"  ✗ Failed to move: {e}")
        return False


def download_and_organize(url):
    """Main function to download and organize files from URL"""
    print("=" * 50)
    print("File Download and Organization Script")
    print("=" * 50)
    print(f"URL: {url}\n")
    
    # Create temporary directory
    temp_dir = Path('/tmp') / f'file_downloads_{os.getpid()}'
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Download the main page
        print("Fetching page...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
        except (URLError, HTTPError) as e:
            print(f"Error: Could not fetch the page: {e}")
            print("\nThe URL might be inaccessible from this environment.")
            print("\nAlternative: You can run this script with a different URL or")
            print("use the provided artisan command or shell script.")
            return False
        
        # Extract file links
        parser = LinkExtractor()
        parser.feed(html_content)
        
        if not parser.links:
            print("No file links found on the page.")
            return False
        
        print(f"Found {len(parser.links)} potential file link(s).\n")
        
        # Download each file
        downloaded_files = []
        
        for link in parser.links:
            # Convert relative URLs to absolute
            file_url = urllib.parse.urljoin(url, link)
            filename = os.path.basename(urllib.parse.urlparse(file_url).path)
            
            print(f"Downloading: {filename}")
            
            file_path = temp_dir / filename
            if download_file(file_url, file_path):
                downloaded_files.append(file_path)
                print(f"  ✓ Downloaded successfully")
            else:
                print(f"  ✗ Download failed")
        
        if not downloaded_files:
            print("\nNo files were successfully downloaded.")
            return False
        
        print(f"\nOrganizing {len(downloaded_files)} file(s)...\n")
        
        # Organize each downloaded file
        for filepath in downloaded_files:
            print(f"Processing: {filepath.name}")
            organize_file(filepath)
        
        print("\n" + "=" * 50)
        print("File organization completed!")
        print("=" * 50)
        
        return True
    
    finally:
        # Cleanup temporary directory
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
            pass


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63'
    
    success = download_and_organize(url)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
