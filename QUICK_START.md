# Quick Start Guide: File Download and Organization

## Important Note
The URL `https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63` provided in the requirement may be inaccessible from certain environments due to network restrictions. Three methods have been implemented to handle file downloads and organization when the URL becomes accessible.

## Available Methods

### Method 1: Python Script (Recommended)
The Python script provides the most robust solution with better HTML parsing and error handling.

```bash
# Run with default URL
python3 download-organize.py

# Or specify a custom URL
python3 download-organize.py https://example.com/files
```

### Method 2: Bash Shell Script
A lightweight alternative that uses standard Unix tools.

```bash
# Run with default URL
./download-organize.sh

# Or specify a custom URL
./download-organize.sh https://example.com/files
```

### Method 3: Laravel Artisan Command
Integrated with the Laravel framework.

```bash
# First, ensure dependencies are installed
composer install --ignore-platform-reqs

# Run the command
php artisan files:download-organize https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63
```

## What These Tools Do

1. **Download Files**: Fetch all files from the provided URL
2. **Detect File Types**: Automatically identify file types based on extensions
3. **Organize**: Place files in appropriate Laravel directories based on their type
4. **Handle Conflicts**: Rename files if they already exist (e.g., `file_1.jpg`, `file_2.jpg`)
5. **Report Progress**: Show detailed output of what's happening

## File Organization Rules

| File Type | Extensions | Destination Directory |
|-----------|-----------|----------------------|
| Images | jpg, jpeg, png, gif, svg, webp | `public/site-img/` |
| Icons | ico | `public/` |
| Stylesheets | css | `public/css/` |
| JavaScript | js | `public/js/` |
| Fonts | ttf, otf, woff, woff2, eot | `public/fonts/` |
| Views | .blade.php | `resources/views/` |
| PHP Files | php | `app/` or `app/Http/Controllers/` |
| SQL Files | sql | `sql/` |
| Documents | pdf, doc, docx | `storage/app/documents/` |
| Data Files | json, xml, csv | `storage/app/data/` |
| Other | * | `storage/app/other/` |

## When URL is Accessible

Once you have access to the URL (e.g., through VPN or from a different network), run any of the three methods:

```bash
# Simplest approach
python3 download-organize.py
```

The script will:
1. Connect to the URL
2. Parse the HTML page
3. Find all downloadable file links
4. Download each file to a temporary directory
5. Analyze each file's type
6. Move it to the appropriate Laravel directory
7. Clean up temporary files

## Manual Alternative

If automated download is not possible, you can manually:

1. Download files from the URL to your local machine
2. Copy them to the server
3. Place them in appropriate directories following the table above
4. Or use the scripts to organize locally downloaded files

## Troubleshooting

### Network Issues
```
Error: Could not fetch the page
```
**Solution**: The URL is blocked. Try from a different network or use a VPN.

### Permission Issues
```bash
chmod +x download-organize.sh download-organize.py
```

### PHP Version Conflicts
The Laravel project uses PHP 7.x but the server has PHP 8.3. Use:
```bash
composer install --ignore-platform-reqs
```

## Example Output

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

## Next Steps

After files are organized:
1. Verify files are in correct locations: `ls -la public/site-img/`
2. Update references in your code if needed
3. Clear Laravel cache: `php artisan cache:clear`
4. Test your application

## Need More Help?

See `FILE_ORGANIZATION.md` for detailed documentation about:
- File type mappings
- Directory structure
- Laravel conventions
- Advanced usage scenarios
