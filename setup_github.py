#!/usr/bin/env python3
"""
GitHub Setup Script for Render Deployment
Helps configure Git and prepare for GitHub upload
"""

import os
import subprocess
import sys

def configure_git():
    """Configure Git identity"""
    print("🔧 Configuring Git Identity")
    print("=" * 40)
    
    # Get user input
    name = input("Enter your name (for Git commits): ").strip()
    email = input("Enter your email (for Git commits): ").strip()
    
    if not name or not email:
        print("❌ Name and email are required!")
        return False
    
    try:
        # Configure Git
        subprocess.run(['git', 'config', '--global', 'user.name', name], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
        
        print("✅ Git identity configured successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configuring Git: {e}")
        return False

def check_git_status():
    """Check current Git status"""
    print("\n📊 Git Status Check")
    print("=" * 30)
    
    try:
        # Check if files are staged
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        
        if result.stdout.strip():
            print("📁 Files ready to commit:")
            for line in result.stdout.strip().split('\n'):
                if line:
                    status = line[:2]
                    filename = line[3:]
                    print(f"   {status} {filename}")
        else:
            print("📁 No files staged for commit")
            
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking Git status: {e}")
        return False

def stage_files():
    """Stage all files for commit"""
    print("\n📦 Staging Files")
    print("=" * 20)
    
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ All files staged successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error staging files: {e}")
        return False

def commit_files():
    """Commit staged files"""
    print("\n💾 Committing Files")
    print("=" * 25)
    
    try:
        commit_message = "Initial commit - Study Time Prediction API for Render deployment"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print("✅ Files committed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error committing files: {e}")
        return False

def setup_branch():
    """Set up main branch"""
    print("\n🌿 Setting up Main Branch")
    print("=" * 30)
    
    try:
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        print("✅ Main branch set up successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error setting up branch: {e}")
        return False

def get_github_url():
    """Get GitHub repository URL from user"""
    print("\n🔗 GitHub Repository Setup")
    print("=" * 35)
    
    print("📝 Steps to create GitHub repository:")
    print("1. Go to https://github.com/")
    print("2. Click 'New repository'")
    print("3. Name: study-time-prediction-api")
    print("4. Make it PUBLIC (required for Render free tier)")
    print("5. Don't initialize with README (you already have files)")
    print("6. Click 'Create repository'")
    print()
    
    github_url = input("Enter your GitHub repository URL (e.g., https://github.com/username/study-time-prediction-api.git): ").strip()
    
    if not github_url:
        print("❌ GitHub URL is required!")
        return None
    
    if not github_url.startswith('https://github.com/'):
        print("❌ Please enter a valid GitHub URL!")
        return None
    
    return github_url

def add_remote(github_url):
    """Add GitHub remote"""
    print("\n🔗 Adding GitHub Remote")
    print("=" * 25)
    
    try:
        subprocess.run(['git', 'remote', 'add', 'origin', github_url], check=True)
        print("✅ GitHub remote added successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error adding remote: {e}")
        return False

def push_to_github():
    """Push to GitHub"""
    print("\n🚀 Pushing to GitHub")
    print("=" * 20)
    
    try:
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("✅ Successfully pushed to GitHub!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")
        print("💡 Make sure you have:")
        print("   - Created the GitHub repository")
        print("   - Have proper authentication set up")
        return False

def show_next_steps():
    """Show next steps for Render deployment"""
    print("\n🎉 GitHub Setup Complete!")
    print("=" * 30)
    print("📖 Next steps for Render deployment:")
    print()
    print("1. 🎨 Go to https://render.com/")
    print("2. 📝 Sign up with GitHub account")
    print("3. 🚀 Click 'New' → 'Web Service'")
    print("4. 🔗 Connect your GitHub repository")
    print("5. ⚙️  Configure:")
    print("   - Name: study-time-api")
    print("   - Environment: Docker")
    print("   - Branch: main")
    print("   - Build Command: (leave empty)")
    print("   - Start Command: (leave empty)")
    print("6. 🎯 Click 'Create Web Service'")
    print("7. ⏳ Wait for deployment (5-10 minutes)")
    print("8. 🧪 Test your API at: https://your-app-name.onrender.com")
    print()
    print("📚 For detailed instructions, see: RENDER_DEPLOYMENT_GUIDE.md")

def main():
    print("🚀 GitHub Setup for Render Deployment")
    print("=" * 50)
    
    # Step 1: Configure Git
    if not configure_git():
        return
    
    # Step 2: Check status
    check_git_status()
    
    # Step 3: Stage files
    if not stage_files():
        return
    
    # Step 4: Commit files
    if not commit_files():
        return
    
    # Step 5: Setup branch
    if not setup_branch():
        return
    
    # Step 6: Get GitHub URL
    github_url = get_github_url()
    if not github_url:
        return
    
    # Step 7: Add remote
    if not add_remote(github_url):
        return
    
    # Step 8: Push to GitHub
    if not push_to_github():
        return
    
    # Step 9: Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
