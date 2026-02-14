[app]

title = Palacharak POS
package.name = palacharak
package.domain = org.rawley

android.release_artifact = apk
android.debug_artifact = apk



source.dir = .
source.include_exts = py,kv,png,jpg,ttf,db,json

version = 0.1

requirements = python3==3.10.11,kivy==2.2.1,pyjnius==1.5.0,sqlite3,pillow==10.0.0,qrcode,python-docx


p4a.python_version = 3.10
p4a.branch = release-2024.01.21



orientation = portrait

fullscreen = 0

android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA

android.archs = arm64-v8a, armeabi-v7a


log_level = 2

warn_on_root = 0

