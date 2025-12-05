from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from backend.controller.load import MaterialLoadController
from backend.controller.content.content_controller import ContentController

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
    material_id = request.args.get('id', default='1', type=str)
    controller = MaterialLoadController()
    success, data = controller.load_material(material_id)
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
    print(f"素材内容: {material_contents}")
    
    # 循环处理每个素材内容
    for i, material_content in enumerate(material_contents):
        print(f"处理素材 {i+1}")
        print(f"素材内容: {material_content[:50]}...")
        
        success, data = controller.generate_content(material_content, title_tips, hook_tips)
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


if __name__ == '__main__':
    print("Starting Instagram Robot Service...")
    print("\n服务启动在 http://localhost:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)