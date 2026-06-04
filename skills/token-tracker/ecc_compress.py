#!/usr/bin/env python3
"""
ECC压缩器命令行工具
基于ECC混合压缩器，提供命令行接口进行Token压缩
"""

import argparse
import json
import sys
import os

# 添加父目录到sys.path (以便导入ecc_compressor)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ecc_compressor import ECCCompressor, CompressorType


def main():
    parser = argparse.ArgumentParser(
        description='ECC混合压缩器 - Token优化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 压缩JSON数据
  python ecc_compress.py --type json --input data.json
  
  # 压缩推理链
  python ecc_compress.py --type reasoning --input chain.txt
  
  # 压缩上下文
  python ecc_compress.py --type context --input context.txt
  
  # 自动检测类型
  python ecc_compress.py --auto --input input.txt
  
  # 指定压缩器
  python ecc_compress.py --compressor LightThinker++ --input text.txt
        """
    )
    
    parser.add_argument('--type', type=str, choices=['json', 'code', 'reasoning', 'context', 'auto'],
                        help='内容类型')
    parser.add_argument('--auto', action='store_true',
                        help='自动检测内容类型')
    parser.add_argument('--compressor', type=str,
                        choices=['SmartCrusher', 'LightThinker++', 'GenericAgent', 'Auto'],
                        default='Auto',
                        help='指定压缩器类型 (默认: Auto)')
    parser.add_argument('--input', type=str, required=True,
                        help='输入文件')
    parser.add_argument('--output', type=str,
                        help='输出文件 (默认: stdout)')
    parser.add_argument('--format', type=str, choices=['text', 'json'],
                        default='json',
                        help='输出格式 (默认: json)')
    
    args = parser.parse_args()
    
    # 读取输入文件
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error: 无法读取文件 {args.input}: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 确定压缩器类型
    if args.auto or args.type == 'auto':
        compressor_type = CompressorType.AUTO
    elif args.type:
        type_map = {
            'json': CompressorType.SMART_CRUSHER,
            'code': CompressorType.CODE_COMPRESSOR,
            'reasoning': CompressorType.LIGHT_THINKER,
            'context': CompressorType.GENERIC_AGENT,
        }
        compressor_type = type_map[args.type]
    else:
        # 根据--compressor参数
        compressor_map = {
            'SmartCrusher': CompressorType.SMART_CRUSHER,
            'LightThinker++': CompressorType.LIGHT_THINKER,
            'GenericAgent': CompressorType.GENERIC_AGENT,
            'Auto': CompressorType.AUTO,
        }
        compressor_type = compressor_map[args.compressor]
    
    # 执行压缩
    try:
        compressor = ECCCompressor()
        
        # 根据内容类型选择输入格式
        if compressor_type == CompressorType.SMART_CRUSHER:
            # 尝试解析JSON
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                print("Warning: 输入不是有效的JSON，将作为普通文本处理", file=sys.stderr)
                compressor_type = CompressorType.GENERIC_AGENT
        
        result = compressor.compress(content, compressor_type)
        
    except Exception as e:
        print(f"Error: 压缩失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 格式化输出
    if args.format == 'json':
        output = {
            'original_length': result.original_length,
            'compressed_length': result.compressed_length,
            'compression_ratio': round(result.compression_ratio, 4),
            'accuracy_score': result.accuracy_score,
            'compressor_used': result.compressor_used,
            'compressed_content': result.compressed_content,
            'metadata': result.metadata
        }
        output_str = json.dumps(output, ensure_ascii=False, indent=2)
    else:
        # text格式：只输出压缩后的文本
        if isinstance(result.compressed_content, str):
            output_str = result.compressed_content
        elif isinstance(result.compressed_content, dict):
            # 如果是dict，尝试提取摘要
            if 'concise_summary' in result.compressed_content:
                output_str = result.compressed_content['concise_summary']
            elif 'summary' in result.compressed_content:
                output_str = result.compressed_content['summary']
            else:
                output_str = json.dumps(result.compressed_content, ensure_ascii=False, indent=2)
        else:
            output_str = str(result.compressed_content)
    
    # 输出结果
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_str)
            print(f"压缩完成！结果已保存到 {args.output}")
            print(f"原始长度: {result.original_length}")
            print(f"压缩后长度: {result.compressed_length}")
            print(f"压缩比: {result.compression_ratio:.2%}")
            print(f"压缩器: {result.compressor_used}")
        except Exception as e:
            print(f"Error: 无法写入文件 {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_str)


if __name__ == '__main__':
    main()
