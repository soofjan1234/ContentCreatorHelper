from backend.service.content.content_generate import ContentCreatorService

class ContentController:
    def __init__(self):
        self.service = ContentCreatorService()
    
    def generate_content(self, material_content=None, generate_type="both"):
        """
        生成内容（标题和钩子）
        
        Args:
            material_content: 素材内容字符串
            generate_type: 生成类型，可选值："both"（生成标题和钩子）、"title"（只生成标题）、"hook"（只生成钩子）
            
        Returns:
            tuple: (成功标志, 数据/错误信息)
        """
        try:
            # 不再传递 tips 参数，由 service 内部自动读取
            result = self.service.create_content(material_content, generate_type=generate_type)
            if result:
                return True, {
                    'success': True,
                    'data': result
                }
            else:
                return False, {
                    'success': False,
                    'error': '生成内容失败'
                }
        except Exception as e:
            return False, {
                'success': False,
                'error': str(e)
            }