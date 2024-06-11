import sqlite3
import polars as pl
from pathlib import Path
import sqlite3

DB_FILE_DIR = Path("./sqlite/db_files")
TABLE_DEFINE_QUERIES_DIR = Path("./sqlite/table_define_queries")


def main() -> None:
    # dbファイル達を全て削除
    _clean_db_files()

    # テーブル定義クエリを取得して順番に実行していく
    _init_db_files()


def _clean_db_files() -> None:
    for file in DB_FILE_DIR.iterdir():
        file.unlink()


def _init_db_files() -> list[Path]:
    """テーブル定義クエリを取得して順番に実行していく
    - .dbファイルの名前は、.sqlの名前を使用する
    """
    db_files = []
    for file in TABLE_DEFINE_QUERIES_DIR.iterdir():
        if file.suffix == ".sql":
            db_file = DB_FILE_DIR / (file.stem + ".db")
            db_files.append(db_file)
            _execute_sql_query(file, db_file)
    return db_files


def _execute_sql_query(sql_file: Path, db_file: Path) -> None:
    # SQLのクエリを文字列として取得
    with open(sql_file, "r") as file:
        sql = file.read()

    # DBに接続してクエリを実行
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executescript(sql)
    conn.commit()
    conn.close()

    print(f"SQL script executed successfully: {sql_file}")


if __name__ == "__main__":
    main()

    # 動作確認
    ## users_eventsテーブルから全件取得するクエリを実行
    db_file = DB_FILE_DIR / "users_events.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    ## 結果をpl.DataFrameとして取得
    results = cursor.execute("SELECT * FROM users_events")
    column_names = [description[0] for description in cursor.description]
    df = pl.DataFrame(data=results.fetchall(), schema=column_names)
    print(df)
