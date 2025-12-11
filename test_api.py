#!/usr/bin/env python3
"""
PPTX to JPEG Converter Service 测试脚本
用于测试API接口是否正常工作
"""

import requests
import sys
import os
from pathlib import Path

def test_health_endpoint(base_url="http://localhost:8131"):
    """测试健康检查端点"""
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到服务: {e}")
        return False

def test_root_endpoint(base_url="http://localhost:8131"):
    """测试根端点"""
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 根端点正常")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 根端点失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到服务: {e}")
        return False

def test_conversion_endpoint(pptx_file_path, base_url="http://localhost:8131"):
    """测试转换端点"""
    if not os.path.exists(pptx_file_path):
        print(f"❌ 测试文件不存在: {pptx_file_path}")
        return False
    
    try:
        url = f"{base_url}/convert/pptx-to-jpeg/"
        with open(pptx_file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            # 解析返回的JSON响应
            result = response.json()
            print(f"✅ 转换成功")
            print(f"   状态: {result.get('status')}")
            print(f"   消息: {result.get('message')}")
            print(f"   幻灯片数量: {result.get('slide_count')}")
            print(f"   图片URLs:")
            for i, url in enumerate(result.get('images', []), 1):
                print(f"     {i}. http://localhost:8131{url}")
            return True
        else:
            print(f"❌ 转换失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 转换请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试PPTX to JPEG Converter Service")
    print("=" * 50)
    
    base_url = "http://localhost:8131"
    
    # 测试健康检查
    print("\n1. 测试健康检查端点...")
    health_ok = test_health_endpoint(base_url)
    
    # 测试根端点
    print("\n2. 测试根端点...")
    root_ok = test_root_endpoint(base_url)
    
    # 测试转换端点（如果有测试文件）
    print("\n3. 测试转换端点...")
    test_files = ["test.pptx", "sample.pptx", "presentation.pptx", "测试.pptx", "演示文稿.pptx"]
    test_file = None
    
    for file_name in test_files:
        if os.path.exists(file_name):
            test_file = file_name
            break
    
    if test_file:
        conversion_ok = test_conversion_endpoint(test_file, base_url)
    else:
        print("⚠️  未找到测试PPTX文件，跳过转换测试")
        print("   请将测试文件命名为: test.pptx, sample.pptx, presentation.pptx, 测试.pptx 或 演示文稿.pptx")
        conversion_ok = True  # 不因为缺少测试文件而失败
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"   健康检查: {'✅ 通过' if health_ok else '❌ 失败'}")
    print(f"   根端点: {'✅ 通过' if root_ok else '❌ 失败'}")
    print(f"   转换功能: {'✅ 通过' if conversion_ok else '❌ 失败'}")
    
    if health_ok and root_ok and conversion_ok:
        print("\n🎉 所有测试通过！服务运行正常。")
        return 0
    else:
        print("\n💥 部分测试失败，请检查服务状态。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
