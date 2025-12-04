import os
import re

class MaterialLoader:
    """
    素材加载器，用于加载material目录下的文本文件，并按1.、2.等格式分块
    """
    
    def __init__(self):
        self.base_path = os.path.join(os.path.dirname(__file__), '../../../data/material')
    
    def load_material(self, material_id):
        """
        加载指定ID的素材文件
        
        Args:
            material_id: 素材ID，对应material目录下的文件名（不带.txt后缀）
            
        Returns:
            list: 按1.、2.等格式分块后的内容数组
        """
        file_path = os.path.join(self.base_path, f'{material_id}.txt')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正则表达式按1.、2.等格式分块
            blocks = self._split_content(content)
            return blocks
        except FileNotFoundError:
            raise FileNotFoundError(f"素材文件 {file_path} 不存在")
        except Exception as e:
            raise Exception(f"加载素材文件时出错: {str(e)}")
    
    def _split_content(self, content):
        """
        将内容按#符号分块
        
        Args:
            content: 原始文本内容
            
        Returns:
            list: 分块后的内容数组
        """
        # 使用正则表达式匹配以#开头的行作为分块标记
        # 使用捕获组保留#符号和空格，以便后续拼接
        parts = re.split(r'(#\s+)', content)
        
        # 整理结果，确保每个块都包含正确的标记和内容
        blocks = []
        
        # 如果parts长度为1，说明没有找到#符号，返回整个内容作为一个块
        if len(parts) == 1:
            blocks.append(parts[0].strip())
            return blocks
        
        # 从第二个元素开始处理（第一个元素可能是空字符串）
        for i in range(1, len(parts), 2):
            # 确保有内容部分
            if i+1 < len(parts):
                # 拼接#符号标记和内容
                block = parts[i] + parts[i+1]
                blocks.append(block.strip())
            else:
                # 如果只剩下#符号标记，也添加到结果中
                blocks.append(parts[i].strip())
        
        return blocks

# 测试代码
if __name__ == "__main__":
    loader = MaterialLoader()
    try:
        blocks = loader.load_material('1')
        print(f"加载成功，共 {len(blocks)} 个块：")
        for i, block in enumerate(blocks):
            print(f"\n块 {i+1}：")
            print(block)
    except Exception as e:
        print(f"加载失败：{str(e)}")