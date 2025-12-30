# File Download and Organization Tool

This document describes how to download and organize files from a remote URL into the appropriate directories in this Laravel application.

## Overview

Two methods are provided to download and organize files:

1. **Laravel Artisan Command** (Recommended)
2. **Shell Script** (Alternative)

## Method 1: Laravel Artisan Command

### Usage

```bash
php artisan files:download-organize <URL>
```

### Example

```bash
php artisan files:download-organize https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63
```

### Features

- Automatically downloads all files from the provided URL
- Detects file types and organizes them into appropriate directories
- Handles file conflicts by renaming duplicates
- Provides detailed progress output
- Supports various file types (images, CSS, JavaScript, fonts, SQL, PHP, etc.)

## Method 2: Shell Script

### Usage

```bash
./download-organize.sh <URL>
```

### Example

```bash
./download-organize.sh https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63
```

## File Organization Rules

The system organizes files based on their extensions as follows:

### Images
- **Extensions:** jpg, jpeg, png, gif, svg, webp
- **Target Directory:** `public/site-img/`

### Stylesheets
- **Extensions:** css
- **Target Directory:** `public/css/`

### JavaScript
- **Extensions:** js
- **Target Directory:** `public/js/`

### Fonts
- **Extensions:** ttf, otf, woff, woff2, eot
- **Target Directory:** `public/fonts/`

### Views
- **Extensions:** .blade.php
- **Target Directory:** `resources/views/`

### PHP Files
- **Extensions:** php
- **Target Directory:** 
  - Controllers: `app/Http/Controllers/`
  - Models: `app/`
  - Other: `app/`

### SQL Files
- **Extensions:** sql
- **Target Directory:** `sql/`

### Documents
- **Extensions:** pdf, doc, docx
- **Target Directory:** `storage/app/documents/`

### Data Files
- **Extensions:** json, xml, csv
- **Target Directory:** `storage/app/data/`

### Other Files
- **Default Target Directory:** `storage/app/other/`

## Requirements

### For Artisan Command
- PHP 7.x or higher
- Laravel framework
- cURL extension enabled
- DOM extension enabled

### For Shell Script
- Bash shell
- wget command
- Basic Unix utilities (grep, cut, basename)

## Troubleshooting

### URL is Inaccessible

If the URL is blocked or inaccessible:

1. Download the files manually to a temporary directory
2. Modify the script to process local files instead
3. Or use a VPN/proxy to access the URL

### Permission Issues

If you encounter permission errors:

```bash
# Ensure the script is executable
chmod +x download-organize.sh

# Ensure Laravel has proper permissions
php artisan cache:clear
chmod -R 775 storage
chmod -R 775 bootstrap/cache
```

### Existing Files

If a file already exists at the target location, the system will automatically rename the new file by appending a counter (e.g., `image_1.jpg`, `image_2.jpg`).

## Manual File Organization

If you prefer to organize files manually, follow these Laravel conventions:

1. **Public Assets** (accessible via web):
   - Place in `public/` subdirectories
   
2. **Resources** (compiled/processed):
   - Place in `resources/` subdirectories
   
3. **Application Code**:
   - Place in appropriate `app/` subdirectories
   
4. **Storage** (user-uploaded or generated):
   - Place in `storage/app/` subdirectories

## Notes

- The system creates target directories if they don't exist
- Downloaded files are temporarily stored in `storage/app/temp_downloads/` before being organized
- The temporary directory is automatically cleaned up after processing
- Both methods provide detailed console output showing the progress

## Support

For issues or questions, please refer to the Laravel documentation or contact the development team.
