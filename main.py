# main.py
from core.data_manager import DataManager
from core.user_interface import UserInterface

class ArticleManagerApp:
    """极简主应用（无标签管理菜单）"""
    
    def __init__(self, data_file: str = "article_data.json"):
        self.data_manager = DataManager(data_file)
        self.ui = UserInterface(self.data_manager)
    
    def run(self):
        self.main_menu()
    
    def main_menu(self):
        while True:
            print("\n" + "="*40)
            print("     📚 文章关键句标签管理系统")
            print("="*40)
            print("1. 文章管理")
            print("2. 按标签搜索")
            print("3. 按标题搜索")
            print("4. 查看零标签文章")
            print("0. 退出并保存")
            print("-"*40)
            
            choice = input("请选择: ").strip()
            
            if choice == '0':
                print("💾 正在保存数据...")
                self.data_manager.save_data()
                print("👋 程序已退出。")
                break
            elif choice == '1':
                self.article_menu()
            elif choice == '2':
                self.ui.search_by_tags_interactive()
            elif choice == '3':
                self.ui.search_by_title_interactive()
            elif choice == '4':
                self.ui.handle_zero_tag_articles_interactive()
            else:
                print("❌ 无效选项，请重新输入。")
    
    def article_menu(self):
        while True:
            print("\n" + "-"*30)
            print("    📄 文章管理")
            print("-"*30)
            print("1. 查看所有文章")
            print("2. 添加新文章")
            print("3. 修改文章")
            print("4. 删除文章")
            print("0. 返回主菜单")
            print("-"*30)
            
            choice = input("请选择: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.ui.display_articles()
            elif choice == '2':
                self.ui.add_article_interactive()
            elif choice == '3':
                self.ui.modify_article_interactive()
            elif choice == '4':
                self.ui.delete_article_interactive()
            else:
                print("❌ 无效选项。")

def main():
    app = ArticleManagerApp()
    app.run()

if __name__ == "__main__":
    main()