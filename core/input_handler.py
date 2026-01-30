# core/input_handler.py
import sys
import readchar
from typing import List

class InputHandler:
    """输入处理类，提供带自动补全功能的输入（支持任意标签/关键词）"""
    
    @staticmethod
    def get_input_with_suggestions(prompt: str, suggestions_list: List[str]) -> str:
        """
        带建议和Tab补全的输入函数（支持关键词/长短语）
        
        Args:
            prompt: 提示信息
            suggestions_list: 建议列表（动态从 DataManager.get_all_tags() 获取）
            
        Returns:
            用户输入的字符串（可包含任意字符，如空格、标点）
        """
        input_str = ""
        selected_suggestion_index = 0
        while True:
            current_tag_fragment = input_str.split(',')[-1].strip()
            suggestions = []
            if current_tag_fragment:
                suggestions = [tag for tag in suggestions_list 
                             if tag.startswith(current_tag_fragment)]
                if selected_suggestion_index >= len(suggestions):
                    selected_suggestion_index = 0

            CLEAR_LINE = "\x1b[2K"
            CARRIAGE_RETURN = "\r"

            suggestion_text = ""
            if suggestions:
                highlighted_suggestions = []
                for i, suggestion in enumerate(suggestions[:4]):
                    if i == selected_suggestion_index:
                        highlighted_suggestions.append(f"[{suggestion}]")
                    else:
                        highlighted_suggestions.append(suggestion)
                suggestion_text = f" [建议: {', '.join(highlighted_suggestions)} (Tab/↑↓选择)]"

            full_line = f"{prompt}{input_str}{suggestion_text}"
            sys.stdout.write(f"{CARRIAGE_RETURN}{CLEAR_LINE}{full_line}")
            sys.stdout.flush()

            key = readchar.readkey()

            if key in (readchar.key.ENTER, readchar.key.CR):
                sys.stdout.write('\n')
                return input_str
            elif key in (readchar.key.BACKSPACE, '\x7f'):
                input_str = input_str[:-1]
            elif key == readchar.key.TAB:
                if suggestions:
                    selected_suggestion = suggestions[selected_suggestion_index]
                    last_comma_pos = input_str.rfind(',')
                    if last_comma_pos != -1:
                        base_str = input_str[:last_comma_pos + 1].rstrip() + " "
                        current_fragment = input_str[last_comma_pos + 1:].strip()
                        if current_fragment == selected_suggestion:
                            input_str += ", "
                            selected_suggestion_index = 0
                        else:
                            input_str = base_str + selected_suggestion
                    else:
                        if input_str.strip() == selected_suggestion:
                            input_str += ", "
                            selected_suggestion_index = 0
                        else:
                            input_str = selected_suggestion
            elif key == readchar.key.UP:
                if suggestions and selected_suggestion_index > 0:
                    selected_suggestion_index -= 1
            elif key == readchar.key.DOWN:
                if suggestions and selected_suggestion_index < len(suggestions) - 1:
                    selected_suggestion_index += 1
            elif key == ',':
                input_str += key + " "
            else:
                if key.isprintable():
                    input_str += key
                    selected_suggestion_index = 0