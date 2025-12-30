# Usage Examples

This document provides practical examples of using the file download and organization system.

## Example 1: Using the Python Script (Recommended)

```bash
# Basic usage with default URL
cd /home/runner/work/aussieescort/aussieescort
python3 download-organize.py

# Or with a custom URL
python3 download-organize.py https://example.com/shared-folder
```

**Expected Output:**
```
==================================================
File Download and Organization Script
==================================================
URL: https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63

Fetching page...
Found 15 potential file link(s).

Downloading: logo.png
  ✓ Downloaded successfully
Downloading: styles.css
  ✓ Downloaded successfully
...

Organizing 15 file(s)...

Processing: logo.png
  ✓ Moved to: public/site-img/logo.png
Processing: styles.css
  ✓ Moved to: public/css/styles.css
...

==================================================
File organization completed!
==================================================
```

## Example 2: Using the Shell Script

```bash
cd /home/runner/work/aussieescort/aussieescort
./download-organize.sh
```

## Example 3: Using Laravel Artisan Command

```bash
cd /home/runner/work/aussieescort/aussieescort

# Install dependencies if not already done
composer install --ignore-platform-reqs

# Run the command
php artisan files:download-organize https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63
```

## Example 4: Testing the Organization System

Run the test script to see how files are organized:

```bash
cd /home/runner/work/aussieescort/aussieescort
python3 test_organization.py
```

This creates sample files and demonstrates the organization logic without downloading from the internet.

**Test Output:**
```
============================================================
File Organization System Test
============================================================

Step 1: Creating sample files...
------------------------------------------------------------
Created: logo.png
Created: background.jpg
...

Step 2: Testing target directory detection...
------------------------------------------------------------
logo.png                  → public/site-img
background.jpg            → public/site-img
UserController.php        → app/Http/Controllers
...

Step 3: Organizing files...
------------------------------------------------------------
Processing: logo.png
  ✓ Moved to: public/site-img/logo.png
...

============================================================
✓ All files organized successfully!
============================================================
```

## Example 5: Verifying Organized Files

After running any of the above methods, verify the files were placed correctly:

```bash
# Check images
ls -la public/site-img/

# Check stylesheets
ls -la public/css/

# Check JavaScript
ls -la public/js/

# Check fonts
ls -la public/fonts/

# Check PHP controllers
ls -la app/Http/Controllers/

# Check SQL files
ls -la sql/

# Check documents
ls -la storage/app/documents/

# Check data files
ls -la storage/app/data/
```

## Example 6: Handling Network Issues

If you encounter network issues:

```bash
# The script will show an error message
python3 download-organize.py

# Output:
# Error: Could not fetch the page: <urlopen error [Errno -5] No address...
# 
# The URL might be inaccessible from this environment.
# 
# Alternative: You can run this script with a different URL or
# use the provided artisan command or shell script.
```

**Solution:**
1. Try from a different network
2. Use a VPN or proxy
3. Download files manually and place them in a temp directory, then modify the script to process local files

## Example 7: Processing Local Files

If you have files downloaded locally, you can modify the Python script:

```python
# Create temp directory with your files
mkdir /tmp/my_files
cp ~/Downloads/*.png /tmp/my_files/
cp ~/Downloads/*.css /tmp/my_files/

# Then run a modified version that processes local files
# Or manually move files following the organization rules
```

## File Organization Mapping Reference

| File Type | Extensions | Destination |
|-----------|-----------|-------------|
| Images | .jpg, .jpeg, .png, .gif, .svg, .webp | `public/site-img/` |
| Icons | .ico | `public/` |
| Stylesheets | .css | `public/css/` |
| JavaScript | .js | `public/js/` |
| Fonts | .ttf, .otf, .woff, .woff2, .eot | `public/fonts/` |
| Views | .blade.php | `resources/views/` |
| PHP Controllers | *Controller.php | `app/Http/Controllers/` |
| PHP Models | [A-Z]*.php | `app/` |
| Migrations | *Migration*.php | `database/migrations/` |
| Seeders | *Seeder*.php | `database/seeds/` |
| SQL Files | .sql | `sql/` |
| Documents | .pdf, .doc, .docx | `storage/app/documents/` |
| Data Files | .json, .xml, .csv | `storage/app/data/` |
| Other | * | `storage/app/other/` |

## Troubleshooting Examples

### Problem: Permission Denied
```bash
chmod +x download-organize.sh download-organize.py test_organization.py
```

### Problem: PHP Version Conflict
```bash
composer install --ignore-platform-reqs
```

### Problem: Missing Dependencies
```bash
# For Python
python3 --version  # Ensure Python 3 is installed

# For PHP
php --version  # Ensure PHP is installed
composer install --ignore-platform-reqs
```

### Problem: File Already Exists
The system automatically handles this by renaming:
- Original: `logo.png`
- If exists: `logo_1.png`
- If that exists: `logo_2.png`
- And so on...

## Integration Examples

### Example: After Organization, Update References

```bash
# After files are organized, you might need to update references in your code

# Check which files were added
git status

# Update blade templates if needed
# For example, if logo.png was added to public/site-img/
# Update your view files to reference it:
# <img src="{{ asset('site-img/logo.png') }}" alt="Logo">
```

### Example: Clearing Laravel Cache After Organization

```bash
# After organizing new files, clear Laravel caches
php artisan cache:clear
php artisan config:clear
php artisan view:clear
```

## Advanced Usage

### Custom File Type Mapping

To add support for additional file types, edit the `FILE_TYPE_MAPPING` in:
- `download-organize.py` (line 16-56)
- `app/Console/Commands/DownloadAndOrganizeFiles.php` (line 24-65)
- `test_organization.py` (line 16-39)

Example addition:
```python
# Add to FILE_TYPE_MAPPING
'mp4': 'storage/app/videos',
'mp3': 'storage/app/audio',
```

Then create the directories:
```bash
mkdir -p storage/app/videos storage/app/audio
```

## Security Notes

All three implementations include:
- ✓ Input validation
- ✓ Safe file handling
- ✓ No execution of downloaded files
- ✓ Directory traversal protection
- ✓ File conflict handling
- ✓ Error logging

The code has been reviewed and scanned with CodeQL - no security vulnerabilities detected.
