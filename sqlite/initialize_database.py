import sqlite3
import polars as pl
from pathlib import Path
import sqlite3

DB_FILE_PATH = Path("./sqlite/sample_database.db")
TABLE_DEFINE_QUERIES_DIR = Path("./sqlite/table_define_queries")


def main() -> None:
    # dbファイル達を全て削除
    _clean_db_file()

    # テーブル定義クエリを取得して順番に実行していく
    _init_db_file()


def _clean_db_file() -> None:
    # DB_FILE_PATHを削除
    if DB_FILE_PATH.exists():
        DB_FILE_PATH.unlink()


def _init_db_file() -> None:
    """テーブル定義クエリを取得して順番に実行していく
    - .dbファイルの名前は、.sqlの名前を使用する
    """
    # DBに接続
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()

    for sql_file in TABLE_DEFINE_QUERIES_DIR.iterdir():
        if sql_file.suffix != ".sql":
            raise Exception(f"Invalid file type: {sql_file.name}")
        with open(sql_file, "r") as sql_file:
            sql_str = sql_file.read()
        cursor.executescript(sql_str)
        print(f"SQL script executed successfully: {sql_file.name}")

    # transactionをcommitしてDBを閉じる
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

    # 動作確認
    ## users_eventsテーブルから全件取得するクエリを実行
    conn = sqlite3.connect(DB_FILE_PATH)
    cursor = conn.cursor()
    ## 結果をpl.DataFrameとして取得
    results = cursor.execute("SELECT * FROM users_events")
    column_names = [description[0] for description in cursor.description]
    df = pl.DataFrame(data=results.fetchall(), schema=column_names)
    print(df)
