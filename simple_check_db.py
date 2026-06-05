"""
简单检查 chroma_db 中的文档
直接读取 SQLite 数据库
"""

import sqlite3
import os

db_path = "chroma_db"

# 找到 sqlite 文件
for root, dirs, files in os.walk(db_path):
    for file in files:
        if file.endswith('.sqlite3'):
            sqlite_file = os.path.join(root, file)
            print(f"找到 SQLite 文件：{sqlite_file}")
            
            # 连接数据库
            conn = sqlite3.connect(sqlite_file)
            cursor = conn.cursor()
            
            # 查看所有表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"\n数据库表：{[t[0] for t in tables]}")
            
            # 查看 embeddings 表结构
            if ('embeddings',) in tables:
                cursor.execute("PRAGMA table_info(embeddings);")
                columns = cursor.fetchall()
                print(f"\nembeddings 表结构：")
                for col in columns:
                    print(f"  - {col[1]} ({col[2]})")
                            
                # 查看前 5 条记录
                cursor.execute("SELECT id, document, metadata FROM embeddings LIMIT 5;")
                rows = cursor.fetchall()
                print(f"\n\u524d 5 条文档：")
                for i, row in enumerate(rows):
                    print(f"\n文档 {i+1}:")
                    print(f"  ID: {row[0]}")
                    if row[1]:
                        content = str(row[1])[:100]
                        print(f"  内容：{content}...")
                    if row[2]:
                        print(f"  元数据：{row[2]}")
            
            conn.close()
            break
