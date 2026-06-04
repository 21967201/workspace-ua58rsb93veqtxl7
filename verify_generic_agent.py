#!/usr/bin/env python3
"""验证GenericAgent压缩质量 (threshold=0.85)"""

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
    print(f'保留Token数: {result.metadata["high_density_token_count"]}')
    print(f'总Token数: {result.metadata["total_tokens"]}')
    
    # 显示压缩后的文本
    print(f'\n=== 压缩后的文本 (前200字符) ===')
    compressed_text = result.compressed_content
    if isinstance(compressed_text, str):
        print(compressed_text[:200])
    else:
        # 如果是dict，显示摘要
        if 'summary' in compressed_text:
            print(compressed_text['summary'][:200])
        elif 'compressed' in compressed_text:
            print(compressed_text['compressed'][:200])
    
    # 验证关键信息是否保留
    print(f'\n=== 关键信息验证 ===')
    key_info = [
        '人工智能',
        '机器学习',
        '深度学习',
        'LLM',
        'Transformer',
        'ECC',
        'LightThinker',
        'GenericAgent'
    ]
    
    missing = []
    for info in key_info:
        if info in long_text and info not in str(result.compressed_content):
            missing.append(info)
    
    if missing:
        print(f'⚠️ 缺失关键信息: {missing}')
    else:
        print('✅ 所有关键信息保留！')
    
    print('\n' + '=' * 60)
    print('质量验证完成！')
    print('=' * 60)

if __name__ == '__main__':
    main()
