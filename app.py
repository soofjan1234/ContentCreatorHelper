from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from backend.controller.load.load_controller import LoadController
from backend.controller.content.content_controller import ContentController
from backend.controller.cover.cover_controller import CoverController
from backend.controller.publish.publish_controller import PublishController

app = Flask(__name__)
CORS(app)

frontend_path = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'frontend')

# 主页路由
@app.route('/')
def index():
    return send_from_directory(os.path.join(frontend_path, 'html'), 'index.html')

# 静态文件路由 - 统一处理所有静态资源
@app.route('/<path:filename>')
def serve_static(filename):
    if filename.startswith('css/') or filename.startswith('js/'):
        return send_from_directory(frontend_path, filename)
    return send_from_directory(os.path.join(frontend_path, 'html'), filename)

# 数据文件路由 - 处理data文件夹下的资源
@app.route('/data/<path:filename>')
def serve_data(filename):
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    return send_from_directory(data_path, filename)

# 加载素材API接口
@app.route('/api/load-material', methods=['GET'])
def load_material():
    controller = LoadController()
    success, data = controller.load_material()
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

# 生成内容API接口
@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    # 获取请求参数
    material_contents = request.json.get('material_contents', [])
    title_tips = request.json.get('title_tips')
    hook_tips = request.json.get('hook_tips')
    generate_type = request.json.get('generate_type', 'both')  # 新增：生成类型，默认生成标题和钩子
    
    # 如果是单个素材，兼容旧格式
    if not material_contents and request.json.get('material_content'):
        material_contents = [request.json.get('material_content')]
    
    if not material_contents:
        return jsonify({
            'success': False,
            'error': '未提供素材内容'
        }), 400
    
    controller = ContentController()
    results = []
    
    print(f"收到素材数量: {len(material_contents)}")
    print(f"生成类型: {generate_type}")
    
    # 循环处理每个素材内容
    for i, material_content in enumerate(material_contents):
        print(f"处理素材 {i+1}")
        print(f"素材内容: {material_content[:50]}...")
        
        success, data = controller.generate_content(material_content, title_tips, hook_tips, generate_type)
        if success:
            print(f"素材 {i+1} 生成成功")
            print(f"生成的标题: {data['data']['titles']}")
            print(f"生成的钩子: {data['data']['hooks']}")
            
            results.append({
                'material_index': i + 1,
                'titles': data['data']['titles'],
                'hooks': data['data']['hooks']
            })
        else:
            print(f"素材 {i+1} 生成失败: {data['error']}")
            results.append({
                'material_index': i + 1,
                'error': data['error']
            })
    
    return jsonify({
        'success': True,
        'data': {
            'results': results
        }
    }), 200


# 获取toPs图片列表API接口
@app.route('/api/get_to_ps_images', methods=['GET'])
def get_to_ps_images():
    controller = LoadController()
    success, data = controller.get_to_ps_images()
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

# 获取蒙版图片列表API接口
@app.route('/api/get_mask_images', methods=['GET'])
def get_mask_images():
    controller = LoadController()
    success, data = controller.get_mask_images()
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

# 生成蒙版封面API接口
@app.route('/api/generate-mask-cover', methods=['POST'])
def generate_mask_cover():
    controller = CoverController()
    
    # 支持循环调用，根据前端需求可以传递图片列表
    images = request.json.get('images', [])
    
    # 调用controller的方法生成蒙版封面（controller内部会处理循环）
    success, data = controller.generate_cover_with_mask(images)
    
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

# 生成裁剪图片API接口
@app.route('/api/generate-cropped-image', methods=['POST'])
def generate_cropped_image():
    controller = CoverController()
    
    # 支持循环调用，根据前端需求可以传递图片列表
    images = request.json.get('images', [])
    aspect_ratio = request.json.get('aspect_ratio', 'free')
    
    # 调用controller的方法生成裁剪图片（controller内部会处理循环）
    success, data = controller.generate_cropped_image(images, aspect_ratio)
    
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

# 获取发布文件夹列表API接口
@app.route('/api/publish/folders', methods=['GET'])
def get_publish_folders():
    controller = PublishController()
    success, data = controller.get_publish_folders()
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

# 整理内容API接口
@app.route('/api/organize-content', methods=['POST'])
def organize_content():
    controller = PublishController()
    materials = request.json.get('materials', [])
    
    success, data = controller.organize_content(materials)
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

# 发布内容API接口
@app.route('/api/publish/<folder_name>', methods=['POST'])
def publish_content(folder_name):
    controller = PublishController()
    success, data = controller.publish_content(folder_name)
    if success:
        return jsonify(data), 200
    else:
        return jsonify(data), 400

if __name__ == '__main__':
    print("Starting Instagram Robot Service...")
    print("\n服务启动在 http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)