"""
知识库管理器
负责管理广府非遗文化知识库
"""

import json
import os
from typing import Dict, List, Any, Optional
import sqlite3
from datetime import datetime

class KnowledgeBase:
    def __init__(self, db_path: str = "knowledge_base.db"):
        self.db_path = db_path
        self._init_database()
        self._load_cultural_knowledge()
    
    def _init_database(self):
        """初始化知识库数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建知识条目表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                tags TEXT,
                source TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建分类表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                parent_category TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_cultural_knowledge(self):
        """加载广府文化知识"""
        cultural_data = {
            "粤剧文化": {
                "历史发展": "粤剧起源于明代，是广东地方戏曲，融合了南音、粤讴、木鱼歌等民间艺术形式。经过数百年的发展，形成了独特的艺术风格。",
                "表演艺术": "粤剧表演包括唱、念、做、打四大基本功，注重身段和表情的细腻表现。演员通过精湛的技艺和细腻的表演，将故事情节和人物情感生动地呈现在观众面前。",
                "唱腔特点": "粤剧唱腔以梆子、二黄为主，还有南音、粤讴等，音韵优美，富有地方特色。唱腔丰富多样，既有激昂慷慨的梆子，也有婉转悠扬的二黄。",
                "经典剧目": "《帝女花》、《紫钗记》、《牡丹亭惊梦》、《西厢记》等都是粤剧经典剧目，深受观众喜爱。",
                "著名演员": "著名粤剧演员有红线女、马师曾、薛觉先、白驹荣等，他们为粤剧艺术发展做出重要贡献。"
            },
            "广府建筑": {
                "骑楼文化": "骑楼是广府建筑的重要特色，一楼为商铺，二楼以上为住宅，形成独特的商业街景。这种建筑形式既实用又美观，体现了广府人民的智慧。",
                "岭南园林": "岭南园林以小巧精致著称，如余荫山房、清晖园等，体现了岭南文化的特色。布局紧凑、装饰精美、意境深远。",
                "传统民居": "广府传统民居以三间两廊、四点金等格局为主，注重通风采光和防潮，体现了广府人民对居住环境的智慧设计。",
                "建筑装饰": "广府建筑装饰丰富，有木雕、石雕、砖雕、灰塑等，工艺精湛，寓意深刻，是广府文化的重要载体。"
            },
            "岭南美食": {
                "广府菜系": "广府菜是粤菜的重要组成部分，以清淡鲜美、原汁原味著称，注重食材的新鲜和烹饪的精细。",
                "茶楼文化": "广府茶楼文化历史悠久，早茶、下午茶是广府人重要的社交方式，体现了悠闲的生活态度。",
                "传统小吃": "广府传统小吃丰富多样，如肠粉、虾饺、烧卖、叉烧包等，制作精细，口味独特。",
                "饮食习俗": "广府饮食习俗体现了岭南文化的特色，如煲汤文化、糖水文化等，注重养生和美味。"
            },
            "节庆民俗": {
                "春节习俗": "广府春节习俗丰富，有贴春联、放鞭炮、拜年、舞狮等，体现了浓厚的节日氛围。",
                "端午节": "广府端午节有赛龙舟、吃粽子、挂艾草等习俗，龙舟竞渡是重要的民俗活动。",
                "中秋节": "广府中秋节有赏月、吃月饼、玩花灯等习俗，体现了团圆和思乡之情。",
                "重阳节": "广府重阳节有登高、赏菊、吃重阳糕等习俗，体现了敬老和祈福的寓意。"
            }
        }
        
        # 将文化知识存储到数据库
        self._store_cultural_data(cultural_data)
    
    def _store_cultural_data(self, cultural_data: Dict[str, Dict[str, str]]):
        """存储文化数据到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for category, items in cultural_data.items():
            # 插入分类
            cursor.execute("""
                INSERT OR IGNORE INTO categories (name, description)
                VALUES (?, ?)
            """, (category, f"{category}相关知识"))
            
            # 插入知识条目
            for title, content in items.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO knowledge_items (title, content, category, tags)
                    VALUES (?, ?, ?, ?)
                """, (title, content, category, f"{category},{title}"))
        
        conn.commit()
        conn.close()
    
    async def search_knowledge(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """搜索知识库"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category:
                cursor.execute("""
                    SELECT title, content, category, tags
                    FROM knowledge_items
                    WHERE category = ? AND (title LIKE ? OR content LIKE ?)
                    ORDER BY updated_at DESC
                """, (category, f"%{query}%", f"%{query}%"))
            else:
                cursor.execute("""
                    SELECT title, content, category, tags
                    FROM knowledge_items
                    WHERE title LIKE ? OR content LIKE ?
                    ORDER BY updated_at DESC
                """, (f"%{query}%", f"%{query}%"))
            
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                results.append({
                    "title": row[0],
                    "content": row[1],
                    "category": row[2],
                    "tags": row[3].split(",") if row[3] else []
                })
            
            return results
            
        except Exception as e:
            print(f"搜索知识库失败: {e}")
            return []
    
    async def get_knowledge_by_category(self, category: str) -> List[Dict[str, Any]]:
        """根据分类获取知识"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT title, content, tags
                FROM knowledge_items
                WHERE category = ?
                ORDER BY title
            """, (category,))
            
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                results.append({
                    "title": row[0],
                    "content": row[1],
                    "tags": row[2].split(",") if row[2] else []
                })
            
            return results
            
        except Exception as e:
            print(f"获取分类知识失败: {e}")
            return []
    
    async def add_knowledge(self, title: str, content: str, category: str, tags: List[str] = None) -> bool:
        """添加知识条目"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tags_str = ",".join(tags) if tags else ""
            
            cursor.execute("""
                INSERT INTO knowledge_items (title, content, category, tags)
                VALUES (?, ?, ?, ?)
            """, (title, content, category, tags_str))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"添加知识条目失败: {e}")
            return False
    
    async def get_categories(self) -> List[Dict[str, Any]]:
        """获取所有分类"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, description, COUNT(k.id) as item_count
                FROM categories c
                LEFT JOIN knowledge_items k ON c.name = k.category
                GROUP BY c.name, c.description
                ORDER BY c.name
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            categories = []
            for row in rows:
                categories.append({
                    "name": row[0],
                    "description": row[1],
                    "item_count": row[2]
                })
            
            return categories
            
        except Exception as e:
            print(f"获取分类失败: {e}")
            return []
    
    async def get_related_knowledge(self, title: str, limit: int = 5) -> List[Dict[str, Any]]:
        """获取相关知识"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 先获取当前条目的分类
            cursor.execute("SELECT category FROM knowledge_items WHERE title = ?", (title,))
            row = cursor.fetchone()
            
            if not row:
                return []
            
            category = row[0]
            
            # 获取同分类的其他条目
            cursor.execute("""
                SELECT title, content, tags
                FROM knowledge_items
                WHERE category = ? AND title != ?
                ORDER BY updated_at DESC
                LIMIT ?
            """, (category, title, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                results.append({
                    "title": row[0],
                    "content": row[1],
                    "tags": row[2].split(",") if row[2] else []
                })
            
            return results
            
        except Exception as e:
            print(f"获取相关知识失败: {e}")
            return []

