#!/usr/bin/env python3
"""
Check Git Files for Render Deployment
Shows which files will be included/excluded from your GitHub repository
"""

import os
import subprocess
from pathlib import Path

def get_git_status():
    """Get list of files that will be tracked by Git"""
    try:
        # Get all files in the directory
        all_files = []
        for root, dirs, files in os.walk('.'):
            # Skip .git directory
            if '.git' in root:
                continue
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        
        # Check which files Git will track
        tracked_files = []
        untracked_files = []
        
        for file_path in all_files:
            try:
                result = subprocess.run(
                    ['git', 'check-ignore', file_path], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode == 0:
                    # File is ignored
                    untracked_files.append(file_path)
                else:
                    # File will be tracked
                    tracked_files.append(file_path)
            except:
                # If git check-ignore fails, assume file will be tracked
                tracked_files.append(file_path)
        
        return tracked_files, untracked_files
    except Exception as e:
        print(f"Error checking Git status: {e}")
        return [], []

def categorize_files(files):
    """Categorize files by importance for Render deployment"""
    essential = []
    useful = []
    optional = []
    
    essential_patterns = [
        'main.py',
        'requirements.txt',
        'Dockerfile',
        'render.yaml',
        'study_time_model.pkl',
        'study_api_client.py',
        'README.md',
        'DEPLOYMENT.md',
        'RENDER_DEPLOYMENT_GUIDE.md'
    ]
    
    useful_patterns = [
        '.github/',
        'test_',
        'setup_',
        'deploy.py',
        'docker-compose.yml',
        'Procfile'
    ]
    
    for file_path in files:
        file_name = os.path.basename(file_path)
        is_essential = any(pattern in file_path for pattern in essential_patterns)
        is_useful = any(pattern in file_path for pattern in useful_patterns)
        
        if is_essential:
            essential.append(file_path)
        elif is_useful:
            useful.append(file_path)
        else:
            optional.append(file_path)
    
    return essential, useful, optional

def main():
    print("🔍 Git Files Check for Render Deployment")
    print("=" * 50)
    
    # Check if this is a Git repository
    try:
        subprocess.run(['git', 'status'], capture_output=True, check=True)
        print("✅ Git repository found")
    except:
        print("❌ Not a Git repository. Run 'git init' first.")
        return
    
    # Get file lists
    tracked_files, untracked_files = get_git_status()
    
    if not tracked_files:
        print("❌ No files will be tracked. Check your .gitignore file.")
        return
    
    # Categorize files
    essential, useful, optional = categorize_files(tracked_files)
    
    print(f"\n📁 Files that will be uploaded to GitHub ({len(tracked_files)} total):")
    print("=" * 60)
    
    print(f"\n🎯 ESSENTIAL for Render deployment ({len(essential)} files):")
    print("-" * 40)
    for file_path in sorted(essential):
        print(f"✅ {file_path}")
    
    print(f"\n📚 USEFUL for development ({len(useful)} files):")
    print("-" * 40)
    for file_path in sorted(useful):
        print(f"📖 {file_path}")
    
    print(f"\n📝 OPTIONAL files ({len(optional)} files):")
    print("-" * 40)
    for file_path in sorted(optional):
        print(f"📄 {file_path}")
    
    print(f"\n🚫 Files excluded by .gitignore ({len(untracked_files)} files):")
    print("-" * 40)
    for file_path in sorted(untracked_files)[:10]:  # Show first 10
        print(f"❌ {file_path}")
    if len(untracked_files) > 10:
        print(f"... and {len(untracked_files) - 10} more files")
    
    # Check for critical missing files
    critical_files = [
        'main.py',
        'requirements.txt',
        'Dockerfile',
        'study_time_model.pkl'
    ]
    
    missing_critical = []
    for file in critical_files:
        if not any(file in f for f in tracked_files):
            missing_critical.append(file)
    
    print(f"\n🔍 Deployment Readiness Check:")
    print("=" * 40)
    
    if missing_critical:
        print("❌ CRITICAL FILES MISSING:")
        for file in missing_critical:
            print(f"   - {file}")
        print("\n⚠️  These files are required for Render deployment!")
    else:
        print("✅ All critical files will be included")
    
    # Repository size estimate
    total_size = 0
    for file_path in tracked_files:
        try:
            total_size += os.path.getsize(file_path)
        except:
            pass
    
    size_mb = total_size / (1024 * 1024)
    print(f"\n📊 Estimated repository size: {size_mb:.2f} MB")
    
    if size_mb > 100:
        print("⚠️  Large repository size. Consider excluding more files.")
    elif size_mb > 50:
        print("📈 Medium repository size. Acceptable for deployment.")
    else:
        print("✅ Good repository size for deployment.")
    
    print(f"\n🎉 Your repository is ready for Render deployment!")
    print("📖 Next steps:")
    print("   1. Run: git add .")
    print("   2. Run: git commit -m 'Initial commit'")
    print("   3. Push to GitHub")
    print("   4. Deploy to Render")

if __name__ == "__main__":
    main()
