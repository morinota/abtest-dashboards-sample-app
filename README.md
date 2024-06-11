# ローカル環境でのapp起動方法

```shell
cd path/to/abtest-dashboards-sample-app
export PYTHONPATH=$(pwd)
streamlit run app/main.py
```

# sqliteテーブルデータの初期化方法

```shell
cd path/to/abtest-dashboards-sample-app
python sqlite/initialize_database.py
```
