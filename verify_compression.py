#!/usr/bin/env python3
"""验证ECC压缩器结果"""

from ecc_compressor import ECCCompressor, CompressorType

def main():
    # 读取长文本
    with open('test_long_context.txt', 'r', encoding='utf-8') as f:
        long_text = f.read()
    
    print('=' * 60)
    print('LightThinker++ 压缩结果验证')
    print('=' * 60)
    
    compressor = ECCCompressor()
    result = compressor.compress(long_text, CompressorType.LIGHT_THINKER)
    
    print(f'\n原始长度: {result.original_length} 字符')
    print(f'压缩后长度: {result.compressed_length} 字符')
    print(f'压缩比: {result.compression_ratio:.2%}')
    print(f'准确性: {result.accuracy_score:.2%}')
    print(f'\n关键步骤数: {result.metadata["key_steps_count"]}')
    
    print(f'\n=== 关键步骤 ===')
    for i, step in enumerate(result.compressed_content['key_steps'], 1):
        if len(step) > 80:
            print(f'  {i}. {step[:80]}...')
        else:
            print(f'  {i}. {step}')
    
    print(f'\n=== 极简摘要 ===')
    print(result.compressed_content['concise_summary'])
    
    print(f'\n=== 详细摘要 ===')
    print(result.compressed_content['detailed_summary'][:200])
    if len(result.compressed_content['detailed_summary']) > 200:
        print('...')
    
    print('\n' + '=' * 60)
    print('验证完成！')
    print('=' * 60)

if __name__ == '__main__':
    main()
