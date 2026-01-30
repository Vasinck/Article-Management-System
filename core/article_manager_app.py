# core/article_manager_app.py
from typing import Dict, Callable
from .data_manager import DataManager
from .user_interface import UserInterface

class ArticleManagerApp:
    """主应用程序类"""
    
    def __init__(self, data_file: str = "article_data.json"):
        """
        初始化应用程序
        
        Args:
            data_file: 数据文件路径
        """
        self.data_manager = DataManager(data_file)
        self.ui = UserInterface(self.data_manager)
    
    def run(self) -> None:
        """运行主程序"""
        self.main_menu()
    
    def main_menu(self) -> None:
        menu_options: Dict[str, tuple[str, Callable]] = {
            '1': ('文章管理', self.article_menu),
            '2': ('按标签搜索文章', self.ui.search_by_tags_interactive),
            '3': ('按标题搜索文章', self.ui.search_by_title_interactive),
            '4': ('查看零标签文章', self.ui.handle_zero_tag_articles_interactive)
        }
        
        while True:
            print("\n======= 文章标签搜索工具 =======")
            for key, (text, _) in menu_options.items():
                print(f"{key}. {text}")
            print("0. 退出程序")
            print("==============================")
            
            choice = input("请输入选项: ").strip()
            
            if choice == '0':
                print("正在保存数据...")
                self.data_manager.save_data()
                print("程序已退出。")
                break
            elif choice in menu_options:
                menu_options[choice][1]()
            else:
                print("无效的选项，请重新输入。")
    
    def article_menu(self) -> None:
        """文章管理子菜单（纯文章操作）"""
        menu_options: Dict[str, Callable] = {
            '1': self.ui.display_articles,
            '2': self.ui.add_article_interactive,
            '3': self.ui.modify_article_interactive,
            '4': self.ui.delete_article_interactive,
        }
        
        while True:
            print("\n--- 文章管理 ---")
            print("1. 查看所有文章")
            print("2. 添加新文章")
            print("3. 修改文章")
            print("4. 删除文章")
            print("0. 返回主菜单")
            print("----------------")
            
            choice = input("请选择操作: ").strip()
            
            if choice == '0':
                break
                
            action = menu_options.get(choice)
            if action:
                action()
            else:
                print("无效的选项。")