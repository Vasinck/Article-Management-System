# core/data_manager.py
import json
import os
from typing import List, Dict, Optional

from .article import Article

class DataManager:
    """数据管理类（无全局标签池，完全动态）"""
    
    def __init__(self, data_file: str = "article_data.json"):
        self.data_file = data_file
        self.articles: List[Article] = []
        self.load_data()
    
    def load_data(self) -> None:
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.articles = [Article.from_dict(article_data) 
                                   for article_data in data.get("articles", [])]
                    print(f"成功从 {self.data_file} 加载数据。")
            except json.JSONDecodeError:
                print(f"错误：{self.data_file} 文件格式错误，将使用空数据启动。")
                self.articles = []
            except Exception as e:
                print(f"加载数据时发生未知错误：{e}，将使用空数据启动。")
                self.articles = []
        else:
            print(f"未找到数据文件 {self.data_file}，将创建新文件。")
            self.articles = []
    
    def save_data(self) -> None:
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = {
                    "articles": [article.to_dict() for article in self.articles]
                }
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存数据到 {self.data_file} 时出错: {e}")
    
    def add_article(self, article: Article) -> None:
        self.articles.append(article)
        self.save_data()
    
    def remove_article(self, article_id: str) -> bool:
        for i, article in enumerate(self.articles):
            if article.id == article_id:
                self.articles.pop(i)
                self.save_data()
                return True
        return False
    
    def find_article_by_id(self, article_id: str) -> Optional[Article]:
        for article in self.articles:
            if article.id == article_id:
                return article
        return None
    
    def search_articles_by_tags(self, search_tags: List[str]) -> List[Article]:
        """根据标签列表搜索（AND 精确匹配）"""
        return [article for article in self.articles 
                if article.has_all_tags(search_tags)]
    
    def search_articles_by_title(self, keyword: str) -> List[Article]:
        keyword_lower = keyword.lower()
        return [article for article in self.articles 
                if keyword_lower in article.title.lower()]
    
    def get_zero_tag_articles(self) -> List[Article]:
        return [article for article in self.articles if not article.tags]
    
