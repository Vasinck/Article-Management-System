# core/article.py
import uuid
from typing import List, Dict, Optional

class Article:
    """文章实体类（支持关键句标签，保持输入顺序）"""
    
    def __init__(self, title: str, tags: List[str] = None, article_id: str = None):
        """
        初始化文章对象，标签保持输入顺序，仅去重
        """
        self.id = article_id or str(uuid.uuid4())[:8]
        self.title = title
        
        # 保持顺序的去重
        self.tags = []
        seen = set()
        for tag in (tags or []):
            if tag and tag not in seen:  # 忽略空字符串
                seen.add(tag)
                self.tags.append(tag)
    
    def add_tag(self, tag: str) -> None:
        """添加标签（保持顺序，仅去重）"""
        if tag and tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> bool:
        """移除标签"""
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False
    
    def has_tag(self, tag: str) -> bool:
        """检查是否包含指定标签（精确匹配）"""
        return tag in self.tags
    
    def has_all_tags(self, tags: List[str]) -> bool:
        """检查是否包含所有指定标签（精确匹配 AND）"""
        return all(tag in self.tags for tag in tags)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Article':
        return cls(
            title=data.get("title", ""),
            tags=data.get("tags", []),
            article_id=data.get("id")
        )
    
    def __str__(self) -> str:
        if self.tags:
            tags_display = "\n      ".join(self.tags)  # 每个标签缩进显示
            return f"ID: {self.id}\n   标题: {self.title}\n   标签:\n      {tags_display}"
        else:
            return f"ID: {self.id}\n   标题: {self.title}\n   标签: 无"