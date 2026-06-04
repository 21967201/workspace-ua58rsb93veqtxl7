#!/usr/bin/env python3
"""测试GenericAgent自适应阈值"""

from ecc_compressor import ECCCompressor, CompressorType

def main():
    # 读取长文本
    with open('test_long_context.txt', 'r', encoding='utf-8') as f:
        long_text = f.read()
    
    print('=' * 60)
    print('GenericAgent - 自适应阈值测试')
    print('=' * 60)
    
    compressor = ECCCompressor()
    
    # 测试1: 使用自适应阈值 (threshold=None)
    print('\n测试1: 自适应阈值 (threshold=None)')
    result1 = compressor.compress(long_text, CompressorType.GENERIC_AGENT)
    print(f'  原始长度: {result1.original_length}')
    print(f'  压缩后长度: {result1.compressed_length}')
    print(f'  压缩比: {result1.compression_ratio:.2%}')
    
    token_count1 = result1.metadata['high_density_token_count']
    print(f'  保留Token数: {token_count1}')
    
    # 测试2: 使用固定阈值 (threshold=0.7)
    print('\n测试2: 固定阈值 (threshold=0.7)')
    result2 = compressor.compress(long_text, CompressorType.GENERIC_AGENT)
    print(f'  原始长度: {result2.original_length}')
    print(f'  压缩后长度: {result2.compressed_length}')
    print(f'  压缩比: {result2.compression_ratio:.2%}')
    
    token_count2 = result2.metadata['high_density_token_count']
    print(f'  保留Token数: {token_count2}')
    
    print('\n' + '=' * 60)
    print('自适应阈值测试完成！')
    print('=' * 60)

if __name__ == '__main__':
    main()
