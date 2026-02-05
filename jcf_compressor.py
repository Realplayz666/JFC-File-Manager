"""
JCF (JSON Compressed Format) - Custom Compression Format
Supports images, JSON, text, and binary files with zlib compression
"""

import zlib
import json
import os
import struct
from pathlib import Path
from typing import Union

# Magic number for .jcf files
MAGIC_NUMBER = b'JCF1'
VERSION = 1

class JCFError(Exception):
    pass

class JCFCompressor:
    """Handles compression and decompression of files to .jcf format"""
    
    @staticmethod
    def compress_file(input_path: str, output_path: str = None, compression_level: int = 9) -> str:
        """
        Compress a file to .jcf format
        
        Args:
            input_path: Path to input file
            output_path: Path to output .jcf file (optional)
            compression_level: Compression level 1-9 (default: 9)
            
        Returns:
            Path to compressed file
        """
        if not os.path.exists(input_path):
            raise JCFError(f"Input file not found: {input_path}")
        
        # Read original file
        with open(input_path, 'rb') as f:
            original_data = f.read()
        
        # Get file metadata
        original_size = len(original_data)
        filename = os.path.basename(input_path)
        
        # Compress data
        compressed_data = zlib.compress(original_data, level=compression_level)
        compressed_size = len(compressed_data)
        
        # Prepare output path
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.jcf'))
        
        # Write JCF file
        with open(output_path, 'wb') as f:
            # Write header
            f.write(MAGIC_NUMBER)  # Magic number (4 bytes)
            f.write(struct.pack('B', VERSION))  # Version (1 byte)
            
            # Write metadata
            filename_bytes = filename.encode('utf-8')
            f.write(struct.pack('H', len(filename_bytes)))  # Filename length (2 bytes)
            f.write(filename_bytes)  # Filename
            
            f.write(struct.pack('Q', original_size))  # Original size (8 bytes)
            f.write(struct.pack('Q', compressed_size))  # Compressed size (8 bytes)
            
            # Write compressed data
            f.write(compressed_data)
        
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        print(f"Compressed: {filename}")
        print(f"Original size: {original_size:,} bytes")
        print(f"Compressed size: {compressed_size:,} bytes")
        print(f"Compression ratio: {compression_ratio:.2f}%")
        
        return output_path
    
    @staticmethod
    def decompress_file(input_path: str, output_path: str = None) -> str:
        """
        Decompress a .jcf file
        
        Args:
            input_path: Path to .jcf file
            output_path: Path to output file (optional)
            
        Returns:
            Path to decompressed file
        """
        if not os.path.exists(input_path):
            raise JCFError(f"Input file not found: {input_path}")
        
        with open(input_path, 'rb') as f:
            # Read and verify header
            magic = f.read(4)
            if magic != MAGIC_NUMBER:
                raise JCFError("Invalid JCF file: incorrect magic number")
            
            version = struct.unpack('B', f.read(1))[0]
            if version != VERSION:
                raise JCFError(f"Unsupported JCF version: {version}")
            
            # Read metadata
            filename_length = struct.unpack('H', f.read(2))[0]
            original_filename = f.read(filename_length).decode('utf-8')
            
            original_size = struct.unpack('Q', f.read(8))[0]
            compressed_size = struct.unpack('Q', f.read(8))[0]
            
            # Read compressed data
            compressed_data = f.read(compressed_size)
        
        # Decompress data
        try:
            decompressed_data = zlib.decompress(compressed_data)
        except zlib.error as e:
            raise JCFError(f"Decompression failed: {e}")
        
        # Verify decompressed size
        if len(decompressed_data) != original_size:
            raise JCFError("Decompressed size mismatch")
        
        # Prepare output path
        if output_path is None:
            output_dir = os.path.dirname(input_path)
            output_path = os.path.join(output_dir, original_filename)
        
        # Write decompressed file
        with open(output_path, 'wb') as f:
            f.write(decompressed_data)
        
        print(f"Decompressed: {original_filename}")
        print(f"Output: {output_path}")
        
        return output_path
    
    @staticmethod
    def get_info(jcf_path: str) -> dict:
        """Get information about a .jcf file without decompressing"""
        if not os.path.exists(jcf_path):
            raise JCFError(f"File not found: {jcf_path}")
        
        with open(jcf_path, 'rb') as f:
            magic = f.read(4)
            if magic != MAGIC_NUMBER:
                raise JCFError("Invalid JCF file")
            
            version = struct.unpack('B', f.read(1))[0]
            filename_length = struct.unpack('H', f.read(2))[0]
            filename = f.read(filename_length).decode('utf-8')
            original_size = struct.unpack('Q', f.read(8))[0]
            compressed_size = struct.unpack('Q', f.read(8))[0]
        
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        return {
            'version': version,
            'filename': filename,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio
        }


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("JCF Compressor - Custom File Compression Format")
        print("\nUsage:")
        print("  Compress:   python jcf_compressor.py compress <input_file> [output_file]")
        print("  Decompress: python jcf_compressor.py decompress <input_file> [output_file]")
        print("  Info:       python jcf_compressor.py info <jcf_file>")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "compress":
            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            JCFCompressor.compress_file(input_file, output_file)
        
        elif command == "decompress":
            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            JCFCompressor.decompress_file(input_file, output_file)
        
        elif command == "info":
            jcf_file = sys.argv[2]
            info = JCFCompressor.get_info(jcf_file)
            print(f"\nJCF File Information:")
            print(f"  Version: {info['version']}")
            print(f"  Original filename: {info['filename']}")
            print(f"  Original size: {info['original_size']:,} bytes")
            print(f"  Compressed size: {info['compressed_size']:,} bytes")
            print(f"  Compression ratio: {info['compression_ratio']:.2f}%")
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    
    except JCFError as e:
        print(f"Error: {e}")
        sys.exit(1)
