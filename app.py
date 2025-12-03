from flask import Flask, render_template, request, jsonify
import json
import re
import subprocess
import os
import requests  # 如果需要通过HTTP调用DeepSeek
app = Flask(__name__)

class JHTEProcessor:
    """JHTE 方法处理器"""
    
    @staticmethod
    def translate_text(text, target_lang):
        """JHTE 翻译方法 - 使用Ollama调用DeepSeek模型"""
        try:
            print(f"=== 开始翻译过程 ===")
            print(f"输入文本: {text}")
            print(f"目标语言: {target_lang}")
            
            # 检查输入是否有效
            if not text or not text.strip():
                error_msg = "请输入要翻译的文本"
                print(f"错误: {error_msg}")
                return {"error": error_msg}
            
            # 首先检查Ollama服务是否可用
            print("检查Ollama服务状态...")
            try:
                # 尝试运行一个简单的ollama命令来检查服务状态
                check_result = subprocess.run(
                    ['ollama', 'list'],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    timeout=10
                )
                
                if check_result.returncode != 0:
                    error_msg = "Ollama服务未正常运行，请确保已启动Ollama服务"
                    print(f"错误: {error_msg}")
                    print(f"检查命令输出: {check_result.stderr}")
                    return {"error": error_msg}
                else:
                    print("Ollama服务状态正常")
                    
            except FileNotFoundError:
                error_msg = "未找到Ollama命令，请确保已安装Ollama并添加到系统PATH"
                print(f"错误: {error_msg}")
                return {"error": error_msg}
            except subprocess.TimeoutExpired:
                error_msg = "Ollama服务检查超时，可能服务未正常启动"
                print(f"错误: {error_msg}")
                return {"error": error_msg}
            
            # 根据目标语言构建不同的提示词
            lang_mapping = {
                "英语": "英语",
                "日语": "日语", 
                "韩语": "韩语",
                "法语": "法语",
                "德语": "德语"
            }
            lang_code = lang_mapping.get(target_lang, "英语")  # 默认英语
            
            print(f"使用语言代码: {lang_code}")
            
            # 构建优化的提示词 - 基于您的调用经验
            prompt = f'下面我需要你把我需要的句子翻译为{lang_code}，需要你完全理解语义，并且不要包含任何其它符号，并且回复只有一句翻译结果，句子是"{text}"'
            
            print(f"构建的提示词: {prompt}")
            
            # 调用Ollama DeepSeek模型
            try:
                print("开始调用Ollama DeepSeek模型...")
                
                # 使用subprocess调用ollama命令，指定UTF-8编码
                result = subprocess.run(
                    ['ollama', 'run', 'deepseek-r1:7b', prompt],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore',
                    timeout=600  # 增加到60秒超时
                )
                
                print(f"Ollama调用完成，返回码: {result.returncode}")
                
                if result.returncode == 0:
                    # 成功获取响应
                    model_response = result.stdout.strip()
                    print(f"模型原始响应: {model_response}")
                    
                    # 如果响应为空，可能是模型未下载
                    if not model_response:
                        error_msg = "模型响应为空，可能是deepseek-r1:7b模型未下载，请使用 'ollama pull deepseek-r1:7b' 下载模型"
                        print(f"错误: {error_msg}")
                        return {"error": error_msg}
                    
                    # 清理响应文本 - 移除可能的思考过程
                    # 查找直接的翻译结果
                    lines = model_response.split('</think>')
                    translation = lines[1]
                    
                    # 如果找到了翻译结果
                    if translation:
                        # 按照您要求的格式返回：翻译结果 + 原文
                        result_text = f"翻译结果: {translation}\n原文: {text}"
                        print(f"最终结果: {result_text}")
                        print("=== 翻译过程完成 ===")
                        return {"success": True, "result": result_text}
                    else:
                        # 如果无法提取清晰的翻译，返回原始响应
                        print("未找到清晰的翻译结果，返回原始响应")
                        result_text = f"翻译结果: {model_response}\n原文: {text}"
                        print(f"最终结果: {result_text}")
                        print("=== 翻译过程完成 ===")
                        return {"success": True, "result": result_text}
                        
                else:
                    # ollama命令执行失败
                    error_msg = result.stderr.strip()
                    
                    # 根据错误信息提供更具体的建议
                    if "model not found" in error_msg.lower():
                        detailed_error = f"未找到模型: {error_msg}。请使用 'ollama pull deepseek-r1:7b' 下载模型"
                    elif "connection refused" in error_msg.lower():
                        detailed_error = f"连接被拒绝: {error_msg}。请确保Ollama服务正在运行"
                    else:
                        detailed_error = f"Ollama调用失败: {error_msg}"
                    
                    print(f"Ollama调用失败，错误信息: {detailed_error}")
                    return {"error": detailed_error}
                    
            except subprocess.TimeoutExpired:
                error_msg = "翻译请求超时（60秒），请稍后重试"
                print(f"错误: {error_msg}")
                return {"error": error_msg}
            except Exception as e:
                error_msg = f"调用翻译服务时出错: {str(e)}"
                print(f"错误: {error_msg}")
                return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"翻译过程中出现错误: {str(e)}"
            print(f"错误: {error_msg}")
            return {"error": error_msg}
    @staticmethod
    def analyze_sentiment(text):
        """JHTE 情感分析方法"""
        try:
            if not text or not text.strip():
                return {"error": "请输入要分析的文本"}
            
            # 模拟情感分析结果 - 替换为真实的模型调用
            # 这里返回更丰富的情感分析数据用于可视化
            if "服务" in text and "差" in text:
                mock_response = {
                    "服务": {"sentiment": "负面", "score": 0.8},
                    "环境": {"sentiment": "中性", "score": 0.5}
                }
            elif "食物" in text and "好吃" in text:
                mock_response = {
                    "食物": {"sentiment": "正面", "score": 0.9},
                    "价格": {"sentiment": "中性", "score": 0.6}
                }
            elif "价格" in text and "贵" in text:
                mock_response = {
                    "价格": {"sentiment": "负面", "score": 0.7},
                    "质量": {"sentiment": "正面", "score": 0.8}
                }
            else:
                mock_response = {
                    "整体": {"sentiment": "中性", "score": 0.5}
                }
                
            return {"success": True, "result": mock_response}
            
        except Exception as e:
            return {"error": f"情感分析过程中出现错误: {str(e)}"}

jte = JHTEProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '无效的请求数据'})
            
        text = data.get('text', '')
        target_lang = data.get('target_lang', '英语')
        
        result = jte.translate_text(text, target_lang)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '无效的请求数据'})
            
        text = data.get('text', '')
        
        result = jte.analyze_sentiment(text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'服务器错误: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)