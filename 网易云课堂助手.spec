# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

SETUP_DIR = 'D:\\Downloads\\netease project\\'
a = Analysis(['main.py'],
             pathex=['D:\\Downloads\\netease project'],
             binaries=[],
             datas=[(SETUP_DIR+'category','category'),(SETUP_DIR+'data','data'),(SETUP_DIR+'dist','dist'),(SETUP_DIR+'picture','picture'),(SETUP_DIR+'prediction_model','prediction_model'),(SETUP_DIR+'report','report'),(SETUP_DIR+'word','word')],
             hiddenimports=['xgboost','numpy','pandas','jieba','astropy','scipy','lxml','cssselect','QtAwesome','requests','snownlp','phik','matplotlib','confuse','wordcloud','Pillow','PyQt5','python_dateutil','scikit_learn','sip','pandas_profiling'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='网易云课堂助手',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='网易云课堂助手')
