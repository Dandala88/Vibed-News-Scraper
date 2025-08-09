# 🤖 Building News Agent Android APK

Complete instructions for building the News Agent mobile app for Android.

## 📋 Prerequisites

### System Requirements
- **Linux/macOS** (recommended) or **Windows with WSL**
- **Python 3.7+**
- **Java 8** (OpenJDK recommended)
- **Git**

### Installation Steps

#### 1. Install System Dependencies (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

#### 2. Install Buildozer
```bash
pip3 install --user buildozer
```

#### 3. Install Cython (required for Kivy)
```bash
pip3 install --user cython==0.29.33
```

## 🏗️ Building the APK

### Option A: Using the Build Script (Recommended)
```bash
# Make sure you're in the project directory
cd AgentTest

# Run the build script
python build_apk.py
```

### Option B: Manual Build Process
```bash
# Install mobile dependencies
pip install -r mobile_requirements.txt

# Initialize buildozer (if first time)
buildozer init

# Build debug APK
buildozer android debug

# For release APK (requires signing)
buildozer android release
```

## 📱 Installing on Android Device

### Method 1: Direct Installation
```bash
# Enable USB debugging on your device
# Connect device via USB
buildozer android deploy
```

### Method 2: Manual Installation
1. Copy the APK from `bin/` folder to your device
2. Enable "Install from Unknown Sources" in Android settings
3. Open the APK file on your device to install

## 🔧 Configuration Options

### App Permissions (in buildozer.spec)
```ini
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
```

### App Icon and Name
- Icon: `icon.png` (72x72px minimum, 512x512px recommended)
- App name: Edit `title` in `buildozer.spec`

### Target API Levels
```ini
android.api = 31
android.minapi = 21
android.ndk = 25b
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. "Command 'buildozer' not found"
```bash
# Add pip user directory to PATH
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

#### 2. "Java 8 not found"
```bash
# Ubuntu/Debian
sudo apt install openjdk-8-jdk
sudo update-alternatives --config java
```

#### 3. "Android SDK not found"
Buildozer automatically downloads Android SDK/NDK on first build. This can take 30+ minutes.

#### 4. "Build failed with NDK error"
```bash
# Clean and rebuild
buildozer android clean
buildozer android debug
```

#### 5. "Permission denied" errors
```bash
# Fix permissions
chmod +x ~/.buildozer/android/platform/android-ndk-*/build/tools/make_standalone_toolchain.py
```

#### 6. Windows-specific issues
- Use WSL (Windows Subsystem for Linux)
- Or use a Linux virtual machine
- Native Windows builds are challenging

### Debug Build Issues
```bash
# Clean everything and start fresh
rm -rf .buildozer/
buildozer android clean
buildozer android debug -v  # Verbose output
```

## 📊 Build Artifacts

After successful build:
- **APK location**: `bin/newsagent-{version}-debug.apk`
- **App size**: ~15-25 MB (depending on dependencies)
- **Installation**: Side-load or install via ADB

## 🔒 Creating Release APK

### 1. Generate Signing Key
```bash
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
```

### 2. Configure buildozer.spec
```ini
[app]
# ... other settings ...

[buildozer]
# Path to keystore
android.keystore = my-release-key.keystore
android.keyalias = alias_name
```

### 3. Build Release
```bash
buildozer android release
```

## 📱 App Features

The mobile app includes:
- ✅ **Native Android UI** (Kivy-based)
- ✅ **Touch-optimized interface**
- ✅ **Real-time news fetching**
- ✅ **Article summarization**
- ✅ **Relevance scoring**
- ✅ **Offline-capable UI**
- ✅ **Material Design elements**

## 🔄 Development Workflow

### Testing Changes
```bash
# For quick testing (debug build)
buildozer android debug

# Install directly to connected device
buildozer android debug deploy run
```

### Updating Dependencies
```bash
# Update mobile_requirements.txt
# Then rebuild
buildozer android clean
buildozer android debug
```

## 📈 Performance Tips

1. **Optimize Images**: Use compressed PNG/WebP for icons
2. **Limit Dependencies**: Keep requirements.txt minimal
3. **Test on Multiple Devices**: Different Android versions
4. **Monitor APK Size**: Keep under 50MB for easy distribution

## 🆘 Getting Help

If you encounter issues:

1. **Check Buildozer logs** in `.buildozer/logs/`
2. **Search Kivy/Buildozer documentation**
3. **Check Android developer documentation**
4. **Verify Java/Python versions**

## 🎯 Next Steps

After building successfully:
- Test on multiple Android devices
- Optimize app performance
- Add additional features
- Consider publishing to Google Play Store

---

**Happy Android Development! 📱🚀**