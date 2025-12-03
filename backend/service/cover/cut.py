from PIL import Image
import os

class ImageCutter:
    def __init__(self):
        self.data_dir = "d:/PythonWorkspace/contentCreatorHelper/data"
        self.input_image_path = os.path.join(self.data_dir, "1.jpg")
        self.output_dir = self.data_dir
    
    def open_image(self, image_path):
        """打开图片"""
        try:
            return Image.open(image_path)
        except Exception as e:
            print(f"打开图片失败: {str(e)}")
            return None
    
    def calculate_crop_box(self, image_width, image_height, target_ratio):
        """计算裁剪区域
        
        Args:
            image_width: 原始图片宽度
            image_height: 原始图片高度
            target_ratio: 目标宽高比 (width/height)
            
        Returns:
            裁剪区域坐标 (left, top, right, bottom)
        """
        # 计算原始图片的宽高比
        original_ratio = image_width / image_height
        
        if original_ratio > target_ratio:
            # 原始图片更宽，需要裁剪宽度
            new_width = int(image_height * target_ratio)
            left = (image_width - new_width) // 2
            top = 0
            right = left + new_width
            bottom = image_height
        else:
            # 原始图片更高，需要裁剪高度
            new_height = int(image_width / target_ratio)
            left = 0
            top = (image_height - new_height) // 2
            right = image_width
            bottom = top + new_height
        
        return (left, top, right, bottom)
    
    def crop_image(self, image, target_ratio, output_filename):
        """裁剪图片
        
        Args:
            image: 原始图片
            target_ratio: 目标宽高比
            output_filename: 输出文件名
            
        Returns:
            裁剪后的图片
        """
        # 计算裁剪区域
        crop_box = self.calculate_crop_box(image.width, image.height, target_ratio)
        
        # 裁剪图片
        cropped_image = image.crop(crop_box)
        
        # 保存裁剪后的图片
        output_path = os.path.join(self.output_dir, output_filename)
        try:
            cropped_image.save(output_path)
            print(f"裁剪后的图片已保存到: {output_path}")
            return cropped_image
        except Exception as e:
            print(f"保存裁剪后的图片失败: {str(e)}")
            return None
    
    def cut_to_3_4(self):
        """将图片裁剪为3:4比例"""
        image = self.open_image(self.input_image_path)
        if not image:
            return None
        
        # 3:4比例的宽高比为0.75 (3/4)
        return self.crop_image(image, 3/4, "1_3_4.jpg")
    
    def cut_to_3_2(self):
        """将图片裁剪为3:2比例"""
        image = self.open_image(self.input_image_path)
        if not image:
            return None
        
        # 3:2比例的宽高比为1.5 (3/2)
        return self.crop_image(image, 3/2, "1_3_2.jpg")
    
    def cut_to_all_ratios(self):
        """裁剪为所有需要的比例"""
        # 裁剪为3:4比例
        self.cut_to_3_4()
        
        # 裁剪为3:2比例
        self.cut_to_3_2()

# 测试代码
if __name__ == "__main__":
    cutter = ImageCutter()
    
    # 将图片裁剪为3:4和3:2比例
    print("正在裁剪图片...")
    cutter.cut_to_all_ratios()