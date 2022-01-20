# raspberry pi init

## 環境構築
### windows
```
> python -m venv venv
> venv\Script\activate.bat
```

## 単一実行ファイル化
### windows
```
> pyinstaller generate.py --onefile --add-data "wpa.json;wpa.json"
```

### linux
```
# linux用実行ファイル
$ pyinstaller generate.py --onefile --add-data "wpa.json:wpa.json"
# windows用実行ファイル
$ pyinstaller generate.py --onefile --windowed --add-data "wpa.json:wpa.json"
```
