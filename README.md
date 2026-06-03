# 第九章 不相交集合線上測驗系統 Django 版

本專案為資料結構第九章「不相交集合 Union-Find」線上測驗系統。

## 主要功能

- Django Admin 題庫後台管理
- 題目與選項新增、修改、刪除
- 測驗題數選擇：5 題、10 題、全部 15 題
- 隨機出題順序
- 隨機選項排列
- 作答後顯示正確答案與解析
- 錯題複習模式
- 以 Session 紀錄錯題，答對後會從錯題本移除
- 題目難易度欄位：易、中、難

## 安裝與執行

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_questions
python manage.py createsuperuser
python manage.py runserver
```

開啟網站：

```txt
http://127.0.0.1:8000/
```

Django Admin 後台：

```txt
http://127.0.0.1:8000/admin/
```

## 測試流程

1. 先執行 `python manage.py seed_questions` 匯入 15 題題庫
2. 開啟 `/admin/` 登入後台
3. 可以新增、修改、刪除題目與選項
4. 回到首頁選擇 5 題或 10 題開始測驗
5. 提交後可查看正確答案與解析
6. 答錯題目會加入錯題本
7. 回首頁可進入錯題複習模式
