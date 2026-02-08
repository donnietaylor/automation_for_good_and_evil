#!/usr/bin/env python3
"""
Simple Code Formatter - A good automation example
Formats code files using AI assistance
"""

import os
import sys
import argparse
import difflib
from pathlib import Path

try:
    import openai
    from dotenv import load_dotenv
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def format_code(code: str, language: str) -> str:
    """
    Format code using OpenAI API
    
    Args:
        code: Source code to format
        language: Programming language (python, javascript, typescript)
        
    Returns:
        Formatted code
    """
    prompt = f"""
    Format this {language} code according to best practices:
    - Use consistent indentation
    - Add type hints (if applicable)
    - Use meaningful variable names
    - Add docstrings to functions
    - Follow language-specific style guides (PEP 8 for Python, etc.)
    - Preserve all functionality
    
    Return ONLY the formatted code, no explanations.
    
    Code:
    ```{language}
    {code}
    ```
    """
    
    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert code formatter. Return only formatted code without explanations or markdown."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        formatted = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if formatted.startswith("```"):
            lines = formatted.split("\n")
            formatted = "\n".join(lines[1:-1])
        
        return formatted
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return code


def show_diff(original: str, formatted: str, filename: str):
    """Show diff between original and formatted code"""
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        formatted.splitlines(keepends=True),
        fromfile=f"{filename} (original)",
        tofile=f"{filename} (formatted)",
        lineterm=""
    )
    
    print("\n" + "="*60)
    print(f"Changes for {filename}:")
    print("="*60)
    for line in diff:
        if line.startswith('+'):
            print(f"\033[92m{line}\033[0m", end="")  # Green
        elif line.startswith('-'):
            print(f"\033[91m{line}\033[0m", end="")  # Red
        else:
            print(line, end="")
    print("\n" + "="*60 + "\n")


def get_language(filepath: Path) -> str:
    """Determine language from file extension"""
    ext = filepath.suffix.lower()
    
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript'
    }
    
    return language_map.get(ext, 'unknown')


def format_file(filepath: Path, dry_run: bool = False, backup: bool = True):
    """
    Format a single file
    
    Args:
        filepath: Path to file
        dry_run: If True, only show changes without applying
        backup: If True, create backup before modifying
    """
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        return False
    
    language = get_language(filepath)
    if language == 'unknown':
        print(f"Skipping unsupported file type: {filepath}")
        return False
    
    print(f"Processing {filepath}...")
    
    # Read original code
    with open(filepath, 'r', encoding='utf-8') as f:
        original_code = f.read()
    
    # Format code
    formatted_code = format_code(original_code, language)
    
    # Check if changes were made
    if original_code.strip() == formatted_code.strip():
        print("No changes needed.")
        return True
    
    # Show diff
    show_diff(original_code, formatted_code, filepath.name)
    
    if dry_run:
        print("Dry run - no changes applied.")
        return True
    
    # Ask for confirmation
    response = input("Apply these changes? (y/n): ").lower()
    if response != 'y':
        print("Changes discarded.")
        return False
    
    # Create backup
    if backup:
        backup_path = filepath.with_suffix(filepath.suffix + '.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_code)
        print(f"Backup created: {backup_path}")
    
    # Apply changes
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(formatted_code)
    
    print(f"✓ Successfully formatted {filepath}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Format code files using AI assistance"
    )
    parser.add_argument(
        "path",
        help="File or directory to format"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process directories recursively"
    )
    
    args = parser.parse_args()
    
    # Check API key
    if not openai.api_key:
        print("Error: OPENAI_API_KEY not set")
        print("Create a .env file with your API key")
        sys.exit(1)
    
    path = Path(args.path)
    
    if path.is_file():
        format_file(path, dry_run=args.dry_run, backup=not args.no_backup)
    elif path.is_dir():
        pattern = "**/*" if args.recursive else "*"
        files = [
            f for f in path.glob(pattern)
            if f.is_file() and get_language(f) != 'unknown'
        ]
        
        print(f"Found {len(files)} files to process")
        
        for filepath in files:
            format_file(filepath, dry_run=args.dry_run, backup=not args.no_backup)
    else:
        print(f"Error: Path not found: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
