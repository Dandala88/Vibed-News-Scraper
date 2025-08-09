#!/usr/bin/env python3
"""
Script to build the News Agent APK for Android
Requires: Buildozer, Android SDK, Android NDK
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check Python
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ required")
        return False
    print("✅ Python version OK")
    
    # Check if we're on Windows (WSL recommended for Android builds)
    if platform.system() == "Windows":
        print("⚠️  Windows detected. For Android builds, WSL or Linux is recommended.")
        print("   You can still try, but you may encounter issues.")
    
    # Check if buildozer is available
    try:
        subprocess.run(["buildozer", "--version"], capture_output=True, check=True)
        print("✅ Buildozer found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Buildozer not found. Install with: pip install buildozer")
        return False
    
    return True

def setup_environment():
    """Set up the build environment"""
    print("🔧 Setting up build environment...")
    
    # Create necessary directories
    os.makedirs(".buildozer", exist_ok=True)
    os.makedirs("bin", exist_ok=True)
    
    print("✅ Environment setup complete")

def build_apk():
    """Build the APK using Buildozer"""
    print("🏗️  Building APK...")
    print("This may take a while on first build (downloading Android SDK/NDK)...")
    
    try:
        # Initialize buildozer if needed
        if not os.path.exists("buildozer.spec"):
            print("📝 Initializing buildozer...")
            subprocess.run(["buildozer", "init"], check=True)
        
        # Build debug APK
        print("🔨 Building debug APK...")
        subprocess.run(["buildozer", "android", "debug"], check=True)
        
        print("✅ APK build successful!")
        
        # Find the APK file
        apk_path = find_apk()
        if apk_path:
            print(f"📱 APK location: {apk_path}")
            print(f"📁 APK size: {get_file_size(apk_path):.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error: {e}")
        print("\n💡 Common solutions:")
        print("   - Ensure Android SDK/NDK are properly installed")
        print("   - Check buildozer.spec configuration")
        print("   - Try: buildozer android clean")
        return False

def find_apk():
    """Find the generated APK file"""
    bin_dir = Path("bin")
    if bin_dir.exists():
        apk_files = list(bin_dir.glob("*.apk"))
        if apk_files:
            return apk_files[0]
    return None

def get_file_size(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def install_dependencies():
    """Install Python dependencies for mobile app"""
    print("📦 Installing mobile dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "mobile_requirements.txt"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    """Main build process"""
    print("🤖 News Agent Android Build Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Run this script from the project root.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Install Python dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Set up environment
    setup_environment()
    
    # Build APK
    if build_apk():
        print("\n🎉 Build completed successfully!")
        print("\n📱 To install on your Android device:")
        print("   1. Enable 'Developer Options' and 'USB Debugging'")
        print("   2. Connect your device via USB")
        print("   3. Run: buildozer android deploy")
        print("   Or manually transfer the APK and install it")
    else:
        print("\n❌ Build failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()