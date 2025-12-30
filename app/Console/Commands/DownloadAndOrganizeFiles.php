<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;

class DownloadAndOrganizeFiles extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'files:download-organize {url : The URL to download files from}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Download files from a URL and organize them into appropriate folders';

    /**
     * File type to directory mapping
     *
     * @var array
     */
    protected $fileTypeMapping = [
        // Images
        'jpg' => 'public/site-img',
        'jpeg' => 'public/site-img',
        'png' => 'public/site-img',
        'gif' => 'public/site-img',
        'svg' => 'public/site-img',
        'webp' => 'public/site-img',
        'ico' => 'public',
        
        // Stylesheets
        'css' => 'public/css',
        'scss' => 'resources/assets/sass',
        'sass' => 'resources/assets/sass',
        'less' => 'resources/assets/less',
        
        // Scripts
        'js' => 'public/js',
        'ts' => 'resources/assets/js',
        'jsx' => 'resources/assets/js',
        'tsx' => 'resources/assets/js',
        
        // Fonts
        'ttf' => 'public/fonts',
        'otf' => 'public/fonts',
        'woff' => 'public/fonts',
        'woff2' => 'public/fonts',
        'eot' => 'public/fonts',
        
        // Views
        'blade.php' => 'resources/views',
        
        // PHP files
        'php' => 'app',
        
        // SQL files
        'sql' => 'sql',
        
        // Documents
        'pdf' => 'storage/app/documents',
        'doc' => 'storage/app/documents',
        'docx' => 'storage/app/documents',
        
        // Data files
        'json' => 'storage/app/data',
        'xml' => 'storage/app/data',
        'csv' => 'storage/app/data',
    ];

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $url = $this->argument('url');
        
        $this->info("Starting file download and organization from: {$url}");
        
        // Create temporary download directory
        $tempDir = storage_path('app/temp_downloads');
        if (!File::exists($tempDir)) {
            File::makeDirectory($tempDir, 0755, true);
        }
        
        try {
            // Download files from the URL
            $files = $this->downloadFiles($url, $tempDir);
            
            if (empty($files)) {
                $this->error('No files were downloaded.');
                return 1;
            }
            
            $this->info("Downloaded {count($files)} file(s).");
            
            // Organize each file
            foreach ($files as $file) {
                $this->organizeFile($file);
            }
            
            // Clean up temporary directory
            File::deleteDirectory($tempDir);
            
            $this->info('File organization completed successfully!');
            return 0;
            
        } catch (\Exception $e) {
            $this->error("Error: {$e->getMessage()}");
            return 1;
        }
    }

    /**
     * Download files from the given URL
     *
     * @param string $url
     * @param string $tempDir
     * @return array
     */
    protected function downloadFiles($url, $tempDir)
    {
        $files = [];
        
        // Initialize cURL for the main page
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
        
        $html = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200 || !$html) {
            $this->warn("Could not fetch the page. HTTP Code: {$httpCode}");
            return $files;
        }
        
        // Parse HTML to find file links
        $dom = new \DOMDocument();
        @$dom->loadHTML($html);
        $xpath = new \DOMXPath($dom);
        
        // Look for common download link patterns
        $links = $xpath->query('//a[@href]');
        
        foreach ($links as $link) {
            $href = $link->getAttribute('href');
            
            // Skip navigation links
            if (empty($href) || $href === '#' || strpos($href, 'javascript:') === 0) {
                continue;
            }
            
            // Convert relative URLs to absolute
            if (strpos($href, 'http') !== 0) {
                $href = $this->resolveUrl($url, $href);
            }
            
            // Try to determine if this is a file link
            if ($this->isFileLink($href)) {
                $fileName = basename(parse_url($href, PHP_URL_PATH));
                $filePath = $tempDir . '/' . $fileName;
                
                $this->info("Downloading: {$fileName}");
                
                if ($this->downloadFile($href, $filePath)) {
                    $files[] = $filePath;
                }
            }
        }
        
        return $files;
    }

    /**
     * Download a single file
     *
     * @param string $url
     * @param string $destination
     * @return bool
     */
    protected function downloadFile($url, $destination)
    {
        try {
            $ch = curl_init($url);
            $fp = fopen($destination, 'wb');
            
            curl_setopt($ch, CURLOPT_FILE, $fp);
            curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
            curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
            
            curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            
            curl_close($ch);
            fclose($fp);
            
            if ($httpCode === 200 && file_exists($destination) && filesize($destination) > 0) {
                return true;
            } else {
                @unlink($destination);
                return false;
            }
        } catch (\Exception $e) {
            $this->warn("Failed to download {$url}: {$e->getMessage()}");
            return false;
        }
    }

    /**
     * Organize a file into the appropriate directory
     *
     * @param string $filePath
     * @return void
     */
    protected function organizeFile($filePath)
    {
        $fileName = basename($filePath);
        $extension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
        
        // Special case for blade templates
        if (strpos($fileName, '.blade.php') !== false) {
            $extension = 'blade.php';
        }
        
        // Determine target directory
        $targetDir = $this->getTargetDirectory($extension, $fileName);
        
        if (!$targetDir) {
            $this->warn("Unknown file type for {$fileName}. Placing in storage/app/other");
            $targetDir = base_path('storage/app/other');
        } else {
            $targetDir = base_path($targetDir);
        }
        
        // Ensure target directory exists
        if (!File::exists($targetDir)) {
            File::makeDirectory($targetDir, 0755, true);
        }
        
        // Move file to target directory
        $targetPath = $targetDir . '/' . $fileName;
        
        // Handle file conflicts
        if (File::exists($targetPath)) {
            $this->warn("File {$fileName} already exists. Renaming...");
            $targetPath = $this->getUniqueFilePath($targetDir, $fileName);
        }
        
        if (File::move($filePath, $targetPath)) {
            $this->line("✓ Moved {$fileName} to " . str_replace(base_path(), '', $targetDir));
        } else {
            $this->error("✗ Failed to move {$fileName}");
        }
    }

    /**
     * Get target directory for a file based on its extension
     *
     * @param string $extension
     * @param string $fileName
     * @return string|null
     */
    protected function getTargetDirectory($extension, $fileName)
    {
        // Special logic for PHP files (before general mapping)
        if ($extension === 'php') {
            if (strpos($fileName, 'Controller') !== false) {
                return 'app/Http/Controllers';
            } elseif (strpos($fileName, 'Migration') !== false) {
                return 'database/migrations';
            } elseif (strpos($fileName, 'Seeder') !== false) {
                return 'database/seeds';
            } elseif (strpos($fileName, 'Model') !== false || preg_match('/^[A-Z][a-z]+\.php$/', $fileName)) {
                return 'app';
            } else {
                return 'app';
            }
        }
        
        // Check direct mapping
        if (isset($this->fileTypeMapping[$extension])) {
            return $this->fileTypeMapping[$extension];
        }
        
        return null;
    }

    /**
     * Get a unique file path to avoid conflicts
     *
     * @param string $directory
     * @param string $fileName
     * @return string
     */
    protected function getUniqueFilePath($directory, $fileName)
    {
        $info = pathinfo($fileName);
        $name = $info['filename'];
        $extension = isset($info['extension']) ? '.' . $info['extension'] : '';
        
        $counter = 1;
        do {
            $newFileName = $name . '_' . $counter . $extension;
            $newPath = $directory . '/' . $newFileName;
            $counter++;
        } while (File::exists($newPath));
        
        return $newPath;
    }

    /**
     * Resolve a relative URL to absolute
     *
     * @param string $base
     * @param string $rel
     * @return string
     */
    protected function resolveUrl($base, $rel)
    {
        // Return if already absolute URL
        if (parse_url($rel, PHP_URL_SCHEME) != '') {
            return $rel;
        }
        
        // Queries and anchors
        if ($rel[0] == '#' || $rel[0] == '?') {
            return $base . $rel;
        }
        
        // Parse base URL and convert to local variables: $scheme, $host, $path
        extract(parse_url($base));
        
        // Remove non-directory element from path
        $path = isset($path) ? preg_replace('#/[^/]*$#', '', $path) : '';
        
        // Destroy path if relative url points to root
        if ($rel[0] == '/') {
            $path = '';
        }
        
        // Dirty absolute URL
        $abs = "$host$path/$rel";
        
        // Replace '//' or '/./' or '/foo/../' with '/'
        $re = ['#(/\.?/)#', '#/(?!\.\.)[^/]+/\.\./#'];
        for ($n = 1; $n > 0; $abs = preg_replace($re, '/', $abs, -1, $n)) {
        }
        
        // Absolute URL is ready!
        return $scheme . '://' . $abs;
    }

    /**
     * Check if a URL appears to be a file link
     *
     * @param string $url
     * @return bool
     */
    protected function isFileLink($url)
    {
        $path = parse_url($url, PHP_URL_PATH);
        
        if (!$path) {
            return false;
        }
        
        // Check if path has a file extension
        $extension = pathinfo($path, PATHINFO_EXTENSION);
        
        return !empty($extension) && strlen($extension) <= 5;
    }
}
