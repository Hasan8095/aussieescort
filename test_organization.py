#!/usr/bin/env python3
"""
Test script to demonstrate file organization functionality
This creates sample files and organizes them to show how the system works
"""

import os
import sys
import re
from pathlib import Path

# Base directory for the Laravel project
BASE_DIR = Path('/home/runner/work/aussieescort/aussieescort')

# File type to directory mapping (same as in download_organize.py)
FILE_TYPE_MAPPING = {
    'jpg': 'public/site-img',
    'jpeg': 'public/site-img',
    'png': 'public/site-img',
    'gif': 'public/site-img',
    'svg': 'public/site-img',
    'webp': 'public/site-img',
    'ico': 'public',
    'css': 'public/css',
    'js': 'public/js',
    'ttf': 'public/fonts',
    'otf': 'public/fonts',
    'woff': 'public/fonts',
    'woff2': 'public/fonts',
    'eot': 'public/fonts',
    'php': 'app',
    'sql': 'sql',
    'pdf': 'storage/app/documents',
    'doc': 'storage/app/documents',
    'docx': 'storage/app/documents',
    'json': 'storage/app/data',
    'xml': 'storage/app/data',
    'csv': 'storage/app/data',
}


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


def create_sample_files(temp_dir):
    """Create sample files to test organization"""
    sample_files = [
        'logo.png',
        'background.jpg',
        'icon.svg',
        'styles.css',
        'app.css',
        'script.js',
        'main.js',
        'font.ttf',
        'font.woff2',
        'UserController.php',
        'User.php',
        'home.blade.php',
        'database.sql',
        'document.pdf',
        'data.json',
        'config.xml',
        'favicon.ico',
    ]
    
    created_files = []
    
    for filename in sample_files:
        filepath = temp_dir / filename
        
        # Create file with some content
        with open(filepath, 'w') as f:
            f.write(f"Sample content for {filename}\n")
        
        created_files.append(filepath)
        print(f"Created: {filename}")
    
    return created_files


def test_file_organization():
    """Test the file organization system"""
    print("=" * 60)
    print("File Organization System Test")
    print("=" * 60)
    print()
    
    # Create temporary directory
    temp_dir = Path('/tmp') / f'test_organization_{os.getpid()}'
    temp_dir.mkdir(exist_ok=True)
    
    try:
        print("Step 1: Creating sample files...")
        print("-" * 60)
        sample_files = create_sample_files(temp_dir)
        print(f"\nCreated {len(sample_files)} sample files.\n")
        
        print("Step 2: Testing target directory detection...")
        print("-" * 60)
        for filepath in sample_files:
            filename = filepath.name
            target_dir = get_target_directory(filename)
            relative_target = target_dir.relative_to(BASE_DIR)
            print(f"{filename:25} → {relative_target}")
        print()
        
        print("Step 3: Organizing files...")
        print("-" * 60)
        for filepath in sample_files:
            print(f"Processing: {filepath.name}")
            organize_file(filepath)
        print()
        
        print("Step 4: Verifying organized files...")
        print("-" * 60)
        
        # Check each expected location
        expected_locations = {
            'public/site-img': ['logo.png', 'background.jpg', 'icon.svg'],
            'public/css': ['styles.css', 'app.css'],
            'public/js': ['script.js', 'main.js'],
            'public/fonts': ['font.ttf', 'font.woff2'],
            'app/Http/Controllers': ['UserController.php'],
            'app': ['User.php'],
            'resources/views': ['home.blade.php'],
            'sql': ['database.sql'],
            'storage/app/documents': ['document.pdf'],
            'storage/app/data': ['data.json', 'config.xml'],
            'public': ['favicon.ico'],
        }
        
        all_good = True
        for directory, files in expected_locations.items():
            dir_path = BASE_DIR / directory
            print(f"\nChecking: {directory}/")
            
            for filename in files:
                file_path = dir_path / filename
                
                if file_path.exists():
                    print(f"  ✓ {filename} - FOUND")
                else:
                    print(f"  ✗ {filename} - MISSING")
                    all_good = False
        
        print()
        print("=" * 60)
        if all_good:
            print("✓ All files organized successfully!")
        else:
            print("✗ Some files were not organized correctly")
        print("=" * 60)
        
        return all_good
        
    finally:
        # Cleanup temporary directory
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
            pass


if __name__ == '__main__':
    success = test_file_organization()
    sys.exit(0 if success else 1)
