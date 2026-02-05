# JCF Compressor - Custom File Compression Format

## 🎯 Overview

**JCF (JSON Compressed Format)** is a custom file compression format that can compress any file type including:
- Images (PNG, JPG, GIF, etc.)
- JSON files
- Text files
- Media files
- Game resources (like in Minecraft Java Edition)
- Any other file type!

The format uses **zlib compression** for efficient file size reduction and includes metadata preservation.

---

## 📦 Package Contents

This package includes:

1. **jcf_compressor.py** - Core Python library for compression/decompression
2. **jcf_gui.py** - Windows GUI application
3. **jcf_compressor.html** - Web-based compression tool
4. **README.md** - This file
5. **requirements.txt** - Python dependencies

---

## 🚀 Quick Start

### Option 1: Command Line Interface (CLI)

#### Compress a file:
```bash
python jcf_compressor.py compress myfile.png
```

#### Decompress a file:
```bash
python jcf_compressor.py decompress myfile.png.jcf
```

#### Get file info:
```bash
python jcf_compressor.py info myfile.png.jcf
```

#### Specify output filename:
```bash
python jcf_compressor.py compress myfile.png compressed.jcf
```

---

### Option 2: Windows GUI Application

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the GUI:**
   ```bash
   python jcf_gui.py
   ```

3. **Use the interface:**
   - Select "Compress File" or "Decompress File"
   - Click "Browse Files" to select your file
   - Click the action button to compress/decompress
   - Choose where to save the output file

---

### Option 3: Web Application

1. **Open the HTML file:**
   - Double-click `jcf_compressor.html`
   - Or open it in any modern web browser

2. **Use the web interface:**
   - **Compress Tab:** Drag & drop or click to select any file
   - **Decompress Tab:** Drag & drop or click to select a .jcf file
   - Click the action button
   - File automatically downloads

**Features:**
- No installation required
- Works offline
- Drag & drop support
- Real-time compression statistics
- Beautiful, modern UI

---

## 🎮 Using JCF in Games (Minecraft Java Edition)

JCF files can be used similarly to ZIP files in Minecraft Java Edition:

### For Resource Packs:
1. Compress your resource pack folder:
   ```bash
   python jcf_compressor.py compress my_resource_pack.zip my_resource_pack.jcf
   ```

2. You can extract it when needed:
   ```bash
   python jcf_compressor.py decompress my_resource_pack.jcf
   ```

### For Mod Assets:
- Compress texture files
- Compress JSON configuration files
- Compress sound files
- Reduce overall mod file size

**Note:** While JCF can compress game files, Minecraft specifically requires ZIP format for resource packs and mods. Use JCF for:
- Distributing custom content
- Backing up game files
- Reducing storage space
- Transferring files faster

---

## 📊 JCF File Format Specification

### File Structure:

```
+------------------+
| Magic Number     | 4 bytes: "JCF1"
+------------------+
| Version          | 1 byte: 0x01
+------------------+
| Filename Length  | 2 bytes: unsigned short
+------------------+
| Original Name    | Variable: UTF-8 encoded
+------------------+
| Original Size    | 8 bytes: unsigned long long
+------------------+
| Compressed Size  | 8 bytes: unsigned long long
+------------------+
| Compressed Data  | Variable: zlib compressed
+------------------+
```

### Format Features:
- **Magic Number:** Identifies JCF files (JCF1)
- **Version:** Format version for future compatibility
- **Metadata:** Preserves original filename and sizes
- **Compression:** Industry-standard zlib (RFC 1950)
- **Integrity:** Size verification on decompression

---

## 💻 Python Library Usage

### In Your Own Code:

```python
from jcf_compressor import JCFCompressor, JCFError

# Compress a file
try:
    output_path = JCFCompressor.compress_file('image.png', 'image.jcf')
    print(f"Compressed to: {output_path}")
except JCFError as e:
    print(f"Error: {e}")

# Decompress a file
try:
    output_path = JCFCompressor.decompress_file('image.jcf', 'restored.png')
    print(f"Decompressed to: {output_path}")
except JCFError as e:
    print(f"Error: {e}")

# Get file information
try:
    info = JCFCompressor.get_info('image.jcf')
    print(f"Original filename: {info['filename']}")
    print(f"Compression ratio: {info['compression_ratio']:.2f}%")
except JCFError as e:
    print(f"Error: {e}")
```

---

## 📋 Requirements

### For CLI and GUI:
- Python 3.7 or higher
- No external dependencies for CLI
- tkinter (included with Python) for GUI

### For Web Application:
- Any modern web browser (Chrome, Firefox, Edge, Safari)
- No installation required
- Works offline

---

## 🔧 Installation

### Clone or Download:
Download all files to a folder on your computer.

### Install Python Dependencies (Optional):
```bash
pip install -r requirements.txt
```

Note: The core library has no external dependencies!

---

## 📈 Compression Performance

Typical compression ratios by file type:

| File Type | Compression Ratio |
|-----------|------------------|
| Text files | 60-80% |
| JSON files | 70-90% |
| PNG images | 5-15% (already compressed) |
| JPG images | 0-5% (already compressed) |
| Log files | 80-95% |
| Source code | 60-75% |

**Note:** Already-compressed formats (PNG, JPG, MP3, ZIP) show minimal compression because they're already optimized.

---

## 🛠️ Building Standalone Executable (Windows)

To create a standalone .exe file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico jcf_gui.py
```

The executable will be in the `dist` folder.

---

## 🌟 Features

### ✅ Core Features:
- Compress any file type
- Decompress .jcf files
- Preserve original filenames
- Verify data integrity
- Cross-platform support

### ✅ GUI Features:
- Beautiful, modern interface
- Real-time file information
- Progress indicators
- Easy file browsing
- Compression statistics

### ✅ Web Features:
- No installation required
- Drag & drop support
- Works offline
- Mobile responsive
- Real-time statistics

---

## 🔒 Security Notes

- JCF files are NOT encrypted
- Use for compression, not security
- Original filename is stored in plaintext
- Data integrity is verified during decompression

---

## 🤝 Contributing

This is a custom compression format demonstration. Feel free to:
- Modify the code for your needs
- Add encryption features
- Implement additional compression algorithms
- Create versions for other programming languages

---

## 📝 License

This project is provided as-is for educational and practical use.

---

## 💡 Tips

1. **Best results:** Text files, logs, JSON, XML, CSV
2. **Moderate results:** BMP images, uncompressed audio
3. **Minimal results:** Already compressed formats (PNG, JPG, MP3, ZIP)
4. **Compression level:** Default is 9 (maximum). Lower values are faster but compress less.

---

## 🐛 Troubleshooting

### "Module not found" error:
```bash
pip install -r requirements.txt
```

### GUI won't start:
Make sure tkinter is installed:
```bash
python -m tkinter
```

### Web app doesn't work:
Use a modern browser (Chrome, Firefox, Edge). Some very old browsers may not support required features.

---

## 📞 Support

For issues or questions:
1. Check this README
2. Verify Python version (3.7+)
3. Ensure all files are in the same directory
4. Try the web version if CLI/GUI has issues

---

## 🎉 Examples

### Compress an image:
```bash
python jcf_compressor.py compress photo.jpg
# Creates: photo.jpg.jcf
```

### Compress a JSON file:
```bash
python jcf_compressor.py compress config.json settings.jcf
# Creates: settings.jcf
```

### Batch compress multiple files:
```bash
for file in *.txt; do python jcf_compressor.py compress "$file"; done
```

### Get info about a compressed file:
```bash
python jcf_compressor.py info document.jcf
```

---

## 🚀 Advanced Usage

### Custom compression level (in code):
```python
JCFCompressor.compress_file('large_file.txt', compression_level=6)
```

### Batch processing:
```python
import os
from jcf_compressor import JCFCompressor

for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        JCFCompressor.compress_file(filename)
```

---

**Enjoy using JCF Compressor! 🎊**
