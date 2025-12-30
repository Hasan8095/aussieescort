#!/bin/bash

# Script to download and organize files from a URL
# Usage: ./download-organize.sh <URL>

URL="${1:-https://os5.mycloud.com/action/share/725a3af7-32b7-4498-9db3-335c19d7ac63}"
BASE_DIR="/home/runner/work/aussieescort/aussieescort"
TEMP_DIR="/tmp/file_downloads_$$"

echo "=========================================="
echo "File Download and Organization Script"
echo "=========================================="
echo "URL: $URL"
echo ""

# Create temporary directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR" || exit 1

echo "Downloading files from URL..."

# Try to download the page and extract file links
wget -q -O index.html "$URL" 2>/dev/null

if [ ! -f index.html ] || [ ! -s index.html ]; then
    echo "Error: Could not download the page. The URL might be inaccessible."
    echo ""
    echo "Alternative: If you have files locally, you can manually run:"
    echo "  php artisan files:download-organize <URL>"
    echo ""
    echo "Or place files in the temp directory and run this script in manual mode."
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Extract file links from HTML (basic approach)
# This looks for href attributes that appear to be file downloads
grep -oP 'href="[^"]*\.(jpg|jpeg|png|gif|svg|css|js|ttf|woff|woff2|pdf|sql|php)"' index.html | \
    cut -d'"' -f2 > file_links.txt

# Download each file
while IFS= read -r file_url; do
    # Convert relative URLs to absolute if needed
    if [[ ! "$file_url" =~ ^https?:// ]]; then
        file_url="${URL}/${file_url}"
    fi
    
    filename=$(basename "$file_url")
    echo "Downloading: $filename"
    wget -q "$file_url" -O "$filename" 2>/dev/null
    
    if [ -f "$filename" ] && [ -s "$filename" ]; then
        echo "  ✓ Downloaded successfully"
    else
        echo "  ✗ Download failed"
        rm -f "$filename"
    fi
done < file_links.txt

# Function to organize files
organize_file() {
    local file="$1"
    local filename=$(basename "$file")
    local extension="${filename##*.}"
    local target_dir=""
    
    # Determine target directory based on file extension
    case "${extension,,}" in
        jpg|jpeg|png|gif|svg|webp)
            target_dir="$BASE_DIR/public/site-img"
            ;;
        ico)
            target_dir="$BASE_DIR/public"
            ;;
        css)
            target_dir="$BASE_DIR/public/css"
            ;;
        js)
            target_dir="$BASE_DIR/public/js"
            ;;
        ttf|otf|woff|woff2|eot)
            target_dir="$BASE_DIR/public/fonts"
            ;;
        sql)
            target_dir="$BASE_DIR/sql"
            ;;
        pdf|doc|docx)
            target_dir="$BASE_DIR/storage/app/documents"
            ;;
        json|xml|csv)
            target_dir="$BASE_DIR/storage/app/data"
            ;;
        php)
            if [[ $filename == *"Controller"* ]]; then
                target_dir="$BASE_DIR/app/Http/Controllers"
            elif [[ $filename == *".blade.php" ]]; then
                target_dir="$BASE_DIR/resources/views"
            else
                target_dir="$BASE_DIR/app"
            fi
            ;;
        *)
            target_dir="$BASE_DIR/storage/app/other"
            ;;
    esac
    
    # Create target directory if it doesn't exist
    mkdir -p "$target_dir"
    
    # Handle file conflicts
    target_path="$target_dir/$filename"
    if [ -f "$target_path" ]; then
        echo "  ⚠ File already exists, renaming..."
        local base="${filename%.*}"
        local ext="${filename##*.}"
        local counter=1
        while [ -f "$target_dir/${base}_${counter}.${ext}" ]; do
            counter=$((counter + 1))
        done
        target_path="$target_dir/${base}_${counter}.${ext}"
    fi
    
    # Move file
    cp "$file" "$target_path"
    local relative_path="${target_path#$BASE_DIR/}"
    echo "  ✓ Moved to: $relative_path"
}

echo ""
echo "Organizing downloaded files..."
echo ""

# Process all downloaded files
for file in *; do
    if [ -f "$file" ] && [ "$file" != "index.html" ] && [ "$file" != "file_links.txt" ]; then
        echo "Processing: $file"
        organize_file "$file"
    fi
done

# Cleanup
cd /
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "File organization completed!"
echo "=========================================="
