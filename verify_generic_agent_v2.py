#!/usr/bin/env python3
"""验证GenericAgent压缩质量 (threshold=0.85) - 简化版"""

from ecc_compressor import ECCCompressor, CompressorType

def main():
    # 读取长文本
    with open('test_long_context.txt', 'r', encoding='utf-8') as f:
        long_text = f.read()
    
    print('=' * 60)
    print('GenericAgent 压缩质量验证 (threshold=0.85)')
    print('=' * 60)
    
    compressor = ECCCompressor()
    result = compressor.compress(long_text, CompressorType.GENERIC_AGENT)
    
    print(f'\n原始长度: {result.original_length} 字符')
    print(f'压缩后长度: {result.compressed_length} 字符')
    print(f'压缩比: {result.compression_ratio:.2%}')
    print(f'准确性: {result.accuracy_score:.2%}')
    
    # 显示metadata的所有key
    print(f'\n=== Metadata ===')
    for key, value in result.metadata.items():
        if isinstance(value, (list, dict)):
            print(f'  {key}: {type(value).__name__} (len={len(value)})')
        else:
            print(f'  {key}: {value}')
    
    # 显示压缩内容
    print(f'\n=== 压缩内容 (前300字符) ===')
    content = result.compressed_content
    
    if isinstance(content, str):
        print(content[:300])
    elif isinstance(content, dict):
        # 显示所有key
        print(f'Dict keys: {list(content.keys())}')
        # 显示第一个value
        if content:
            first_key = list(content.keys())[0]
            first_value = str(content[first_key])
            print(f'\n{first_key} (前300字符):')
            print(first_value[:300])
    
    # 验证关键信息
    print('\n=== 关键信息验证 ===')
    key_info = ['人工智能', '机器学习', '深度学习', 'LLM', 'ECC', 'LightThinker']
    
    missing = []
    content_str = str(content)
    for info in key_info:
        if info in long_text and info not in content_str:
            missing.append(info)
    
    if missing:
        print('[Warning] 缺失关键信息: {}'.format(missing))
    else:
        print('[Success] 所有关键信息保留！')
    
    print('\n' + '=' * 60)
    print('质量验证完成！')
    print('=' * 60)

if __name__ == '__main__':
    main()
