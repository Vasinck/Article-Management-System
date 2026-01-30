# core/user_interface.py
import json
import os
from datetime import datetime
from typing import List, Optional

from .article import Article
from .data_manager import DataManager


class UserInterface:
    """用户界面类（支持模糊搜索 + 结果保存）"""

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def display_articles(self, articles: List[Article] = None) -> bool:
        target_articles = articles if articles is not None else self.data_manager.articles
        print("\n--- 📄 文章列表 ---")
        if not target_articles:
            print("📭 当前没有任何文章。")
            return False

        for i, article in enumerate(target_articles):
            print(f"\n{i + 1}. {article}")
            print("-" * 30)
        print("-" * 30)
        return True

    def add_article_interactive(self) -> None:
        """🔄 循环添加文章，标题为空时退出（支持重复标签提示 + 跨文章重复检测）"""
        print("\n" + "="*50)
        print("🔄 批量添加文章模式（输入空标题退出）")
        print("="*50)

        while True:
            title = input("\n📝 请输入文章标题（直接回车退出）: ").strip()
            
            if title == "":
                print("✅ 退出添加模式，返回上级菜单。")
                break

            print("\n📌 请输入标签（关键句，每行一个，输入空行结束）:")
            tags = []
            seen_tags = set()
            
            while True:
                tag = input("🏷️  > ").strip()
                if tag == "":
                    break
                if tag:
                    if tag in seen_tags:
                        print(f"⚠️  重复标签 '{tag}'，已忽略。")
                    else:
                        seen_tags.add(tag)
                        tags.append(tag)

            # ✅ 新增：跨文章重复检测
            duplicate_found = False
            similar_articles = []
            
            for existing_article in self.data_manager.articles:
                if existing_article.title == title:  # 只比对标题！
                    similar_articles.append(existing_article)
                    duplicate_found = True

            if duplicate_found:
                print(f"\n🚨 警告：发现 {len(similar_articles)} 篇标题重复的文章！")
                for art in similar_articles:
                    print(f"   ID: {art.id}")
                    print(f"   标题: {art.title}")
                    if art.tags:
                        print("   标签:")
                        for t in art.tags:
                            print(f"      {t}")
                    else:
                        print("   标签: 无")
                    print("   " + "-"*20)
                
                confirm = input("\n⚠️  是否仍要添加此重复标题文章？(y/N, 默认 N): ").strip().lower()
                if confirm != 'y':
                    print("↩️  已取消添加。")
                    continue  # 跳过本次添加，继续下一轮

            article = Article(title, tags)
            self.data_manager.add_article(article)
            
            print(f"\n🎉 文章 '{title}' (ID: {article.id}) 添加成功！")
            if tags:
                print("🏷️  标签:")
                for tag in tags:
                    print(f"      {tag}")
            else:
                print("🏷️  （未添加标签）")
            
            print("\n" + "-"*30)
            print("➡️  准备添加下一篇...")

    def modify_article_interactive(self) -> None:
        if not self.display_articles():
            return

        while True:
            article_id = input("🔍 请输入要修改的文章 ID (输入 'q' 退出): ").strip()
            if article_id.lower() == 'q':
                break

            article = self.data_manager.find_article_by_id(article_id)
            if not article:
                print(f"❌ 未找到 ID 为 '{article_id}' 的文章。")
                continue

            print(f"\n📄 找到文章:\n{article}")
            print("\n🛠️  选择要修改的内容:\n1. 修改标题\n2. 修改标签\nq. 返回")
            choice = input("请选择: ").strip()

            if choice == '1':
                new_title = input("✏️  新标题: ").strip()
                if not new_title:
                    print("⛔ 标题不能为空。")
                else:
                    old_title = article.title
                    article.title = new_title
                    print(f"✅ 标题已从 '{old_title}' 修改为 '{new_title}'。")
                    self.data_manager.save_data()
                    break

            elif choice == '2':
                self._modify_article_tags(article)
                break

            elif choice.lower() == 'q':
                break
            else:
                print("❌ 无效选择。")

    def _modify_article_tags(self, article: Article) -> None:
        print(f"\n📄 当前文章标签:")
        if article.tags:
            for tag in article.tags:
                print(f"      {tag}")
        else:
            print("      （无）")

        print("\n📌 请输入新标签（关键句，每行一个，空行结束）:")
        new_tags = []
        seen_tags = set()
        
        while True:
            tag = input("🏷️  > ").strip()
            if tag == "":
                break
            if tag:
                if tag in seen_tags:
                    print(f"⚠️  重复标签 '{tag}'，已忽略。")
                else:
                    seen_tags.add(tag)
                    new_tags.append(tag)

        article.tags = new_tags  # Article 构造函数内去重已无必要，但保留兼容
        print("✅ 标签已更新:")
        if article.tags:
            for tag in article.tags:
                print(f"      {tag}")
        else:
            print("      （已清空）")
        self.data_manager.save_data()

    def delete_article_interactive(self) -> None:
        if not self.display_articles():
            return

        while True:
            article_id = input("🗑️  请输入要删除的文章 ID (输入 'q' 退出): ").strip()
            if article_id.lower() == 'q':
                break

            article = self.data_manager.find_article_by_id(article_id)
            if not article:
                print(f"❌ 未找到 ID 为 '{article_id}' 的文章。")
                continue

            confirm = input(f"⚠️  确认删除文章 '{article.title}' (ID: {article_id})？ (y/n): ").strip().lower()
            if confirm == 'y':
                if self.data_manager.remove_article(article_id):
                    print(f"✅ 文章 '{article.title}' 已删除。")
                break
            else:
                print("↩️  操作已取消。")
                break

    def _save_search_results(self, search_type: str, keywords: List[str], results: List[Article]) -> None:
        """保存搜索结果到 JSON 文件"""
        if not results:
            print("📭 无结果可保存。")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"search_result_{timestamp}.json"

        data = {
            "search_type": search_type,
            "keywords": keywords,
            "search_time": datetime.now().isoformat(),
            "results": [article.to_dict() for article in results]
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"💾 搜索结果已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")

    def search_by_tags_interactive(self) -> None:
        if not self.data_manager.articles:
            print("📭 当前没有文章可供搜索。")
            return

        print("\n🔎 按标签模糊搜索（每行输入一个关键词，空行结束）:")
        search_keywords = []
        while True:
            keyword = input("🔍 > ").strip()
            if keyword == "":
                break
            if keyword:
                search_keywords.append(keyword)

        if not search_keywords:
            print("⛔ 未输入任何搜索关键词。")
            return

        # 模糊 AND 匹配：每篇文章必须满足每个关键词至少在一个标签中出现
        found_articles = []
        for article in self.data_manager.articles:
            # 检查是否满足所有关键词
            all_keywords_matched = True
            for kw in search_keywords:
                keyword_matched = False
                for tag in article.tags:
                    if kw in tag:  # 模糊匹配
                        keyword_matched = True
                        break
                if not keyword_matched:
                    all_keywords_matched = False
                    break

            if all_keywords_matched:
                found_articles.append(article)

        print(f"\n--- 📌 标签模糊搜索结果 (必须包含: {', '.join(search_keywords)}) ---")
        if found_articles:
            self.display_articles(found_articles)
        else:
            print("📭 未找到匹配的文章。")
        print("-" * 50)

        # 询问是否保存
        save_choice = input("是否保存此次搜索结果？(y/n, 默认 n): ").strip().lower()
        if save_choice == 'y':
            self._save_search_results("tag_search", search_keywords, found_articles)

    def search_by_title_interactive(self) -> None:
        if not self.data_manager.articles:
            print("📭 当前没有任何文章。")
            return

        print("\n🔎 按标题模糊搜索（每行输入一个关键词，空行结束）:")
        search_keywords = []
        while True:
            keyword = input("🔍 > ").strip()
            if keyword == "":
                break
            if keyword:
                search_keywords.append(keyword)

        if not search_keywords:
            print("⛔ 未输入任何搜索关键词。")
            return

        # 模糊 AND 匹配：标题必须包含所有关键词
        found_articles = []
        for article in self.data_manager.articles:
            all_matched = True
            for kw in search_keywords:
                if kw not in article.title:  # 模糊匹配
                    all_matched = False
                    break
            if all_matched:
                found_articles.append(article)

        print(f"\n--- 📌 标题模糊搜索结果 (必须包含: {', '.join(search_keywords)}) ---")
        if found_articles:
            self.display_articles(found_articles)
        else:
            print("📭 未找到匹配的文章。")
        print("-" * 50)

        # 询问是否保存
        save_choice = input("是否保存此次搜索结果？(y/n, 默认 n): ").strip().lower()
        if save_choice == 'y':
            self._save_search_results("title_search", search_keywords, found_articles)

    def handle_zero_tag_articles_interactive(self) -> None:
        zero_tag_articles = self.data_manager.get_zero_tag_articles()
        print("\n--- 🆘 零标签文章 ---")

        if not zero_tag_articles:
            print("🎉 没有发现零标签的文章。")
            return

        self.display_articles(zero_tag_articles)

        while True:
            article_id = input("🆔 请输入要添加标签的文章 ID ('q' 退出): ").strip()
            if article_id.lower() == 'q':
                break

            article = self.data_manager.find_article_by_id(article_id)
            is_zero_tag = any(z.id == article_id for z in zero_tag_articles)

            if not article or not is_zero_tag:
                print(f"❌ 未在零标签列表中找到 ID '{article_id}'。")
                continue

            print(f"\n📌 为文章 '{article.title}' 添加标签（关键句，每行一个，空行结束）:")
            tags = []
            seen_tags = set()
            
            while True:
                tag = input("🏷️  > ").strip()
                if tag == "":
                    break
                if tag:
                    if tag in seen_tags:
                        print(f"⚠️  重复标签 '{tag}'，已忽略。")
                    else:
                        seen_tags.add(tag)
                        tags.append(tag)

            article.tags = tags
            print("✅ 已添加标签:")
            if article.tags:
                for tag in article.tags:
                    print(f"      {tag}")
            else:
                print("      （无）")
            self.data_manager.save_data()
            break