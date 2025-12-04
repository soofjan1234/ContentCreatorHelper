from backend.service.load import MaterialLoader

class MaterialLoadController:
    def __init__(self):
        self.loader = MaterialLoader()
    
    def load_material(self, material_id):
        """
        加载指定ID的素材文件并分块返回
        
        Args:
            material_id (str): 素材文件ID
            
        Returns:
            tuple: (成功标志, 数据/错误信息)
        """
        try:
            blocks = self.loader.load_material(material_id)
            return True, {
                'success': True,
                'material_id': material_id,
                'blocks': blocks,
                'total_blocks': len(blocks)
            }
        except FileNotFoundError:
            return False, {
                'success': False,
                'error': f'素材文件 {material_id}.txt 不存在'
            }
        except Exception as e:
            return False, {
                'success': False,
                'error': str(e)
            }