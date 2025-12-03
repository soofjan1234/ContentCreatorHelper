import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

class ContentCreatorService:
    def __init__(self):
        # 初始化OpenAI客户端（使用火山方舟API）
        self.client = OpenAI(
            api_key=os.getenv("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        self.model_name = "deepseek-v3-1-terminus"
        
        # 文件路径
        self.data_dir = "d:/PythonWorkspace/contentCreatorHelper/data"
        self.material_file = os.path.join(self.data_dir, "material", "xx.txt")
        self.title_tips_file = os.path.join(self.data_dir, "tip", "title.txt")
        self.hook_tips_file = os.path.join(self.data_dir, "tip", "hook.txt")
    
    def read_file(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件 {file_path} 失败: {str(e)}")
            return None
    
    def generate_title(self, material_content, title_tips):
        """根据素材和标题技巧生成标题"""
        try:
            prompt = f"""作为一名专业的内容创作者，请根据以下素材和标题创作技巧，为健身相关内容生成3-5个吸引人的标题：

                    【素材内容】
                    {material_content}

                    【标题创作技巧】
                    {title_tips}

                    请确保生成的标题：
                    1. 符合提供的技巧
                    2. 吸引人且有情绪痛点
                    3. 与健身内容相关
                    4. 不要说教，要有价值
                    5. 问题提问必须是反认知或痛点场景

                    请以JSON格式返回结果，只需要包含titles数组，不要包含其他内容。
                    """
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一名专业的内容创作者，擅长根据素材和技巧生成吸引人的标题。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # 解析响应
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # 检查返回结果类型
            if isinstance(result, list):
                return result
            return result.get("titles", [])
            
        except Exception as e:
            print(f"生成标题失败: {str(e)}")
            return []
    
    def generate_hook(self, material_content, hook_tips):
        """根据素材和钩子技巧生成钩子"""
        try:
            prompt = f"""作为一名专业的内容创作者，请根据以下素材和钩子创作技巧，为健身相关内容生成3-5个吸引人的开头钩子：

                        【素材内容】
                        {material_content}

                        【钩子创作技巧】
                        {hook_tips}

                        请确保生成的钩子：
                        1. 符合提供的技巧
                        2. 开场不要讲道理，要戳痛点
                        3. 与健身内容相关
                        4. 能够吸引观众继续观看

                        请以JSON格式返回结果，只需要包含hooks数组，不要包含其他内容。
                        """
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "你是一名专业的内容创作者，擅长根据素材和技巧生成吸引人的开头钩子。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # 解析响应
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # 检查返回结果类型
            if isinstance(result, list):
                return result
            return result.get("hooks", [])
            
        except Exception as e:
            print(f"生成钩子失败: {str(e)}")
            return []
    
    def create_content(self):
        """主函数：读取素材和技巧，生成标题和钩子"""
        # 读取素材和技巧
        material_content = self.read_file(self.material_file)
        title_tips = self.read_file(self.title_tips_file)
        hook_tips = self.read_file(self.hook_tips_file)
        
        if not all([material_content, title_tips, hook_tips]):
            print("无法读取必要的文件，生成内容失败")
            return None
        
        # 生成标题和钩子
        titles = self.generate_title(material_content, title_tips)
        hooks = self.generate_hook(material_content, hook_tips)
        
        return {
            "titles": titles,
            "hooks": hooks
        }

# 测试代码
if __name__ == "__main__":
    service = ContentCreatorService()
    result = service.create_content()
    if result:
        print("生成的标题：")
        for i, title in enumerate(result["titles"]):
            print(f"{i+1}. {title}")
        
        print("\n生成的钩子：")
        for i, hook in enumerate(result["hooks"]):
            print(f"{i+1}. {hook}")