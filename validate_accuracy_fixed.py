#!/usr/bin/env python3
"""ECC压缩器 - 准确性验证 (BLEU/ROUGE分数) - 修复Unicode错误"""

from ecc_compressor import ECCCompressor, CompressorType

def calculate_bleu(reference, hypothesis):
    """简化的BLEU分数计算 (实际应使用nltk或sacrebleu)"""
    # 这里使用简化的token重叠率作为近似
    ref_tokens = set(reference.split())
    hyp_tokens = set(hypothesis.split())
    
    if not ref_tokens or not hyp_tokens:
        return 0.0
    
    overlap = ref_tokens & hyp_tokens
    bleu = len(overlap) / len(ref_tokens)
    return bleu

def calculate_rouge_l(reference, hypothesis):
    """简化的ROUGE-L分数计算 (实际应使用rouge-score库)"""
    # 这里使用最长的公共子序列(LCS)长度 / 参考长度
    ref_len = len(reference)
    hyp_len = len(hypothesis)
    
    # 简化：使用字符级重叠率
    common_chars = sum(1 for c in reference if c in hypothesis)
    rouge_l = common_chars / ref_len if ref_len > 0 else 0.0
    return rouge_l

def main():
    print('=' * 60)
    print('ECC压缩器 - 准确性验证 (BLEU/ROUGE)')
    print('=' * 60)
    
    # 读取测试数据
    with open('test_long_context.txt', 'r', encoding='utf-8') as f:
        original_text = f.read()
    
    compressor = ECCCompressor()
    
    # 测试LightThinker++
    print('\n测试1: LightThinker++ 准确性')
    print('-' * 60)
    
    result_lt = compressor.compress(original_text, CompressorType.LIGHT_THINKER)
    
    # 获取压缩后的文本
    compressed_content_lt = result_lt.compressed_content
    if isinstance(compressed_content_lt, dict):
        compressed_text_lt = compressed_content_lt.get('concise_summary', '')
    else:
        compressed_text_lt = str(compressed_content_lt)
    
    # 计算BLEU和ROUGE-L
    bleu_lt = calculate_bleu(original_text, compressed_text_lt)
    rouge_l_lt = calculate_rouge_l(original_text, compressed_text_lt)
    
    print(f'  压缩比: {result_lt.compression_ratio:.2%}')
    print(f'  BLEU分数: {bleu_lt:.2%}')
    print(f'  ROUGE-L分数: {rouge_l_lt:.2%}')
    print(f'  综合准确性: {(bleu_lt + rouge_l_lt) / 2:.2%}')
    
    # 测试GenericAgent
    print('\n测试2: GenericAgent 准确性')
    print('-' * 60)
    
    result_ga = compressor.compress(original_text, CompressorType.GENERIC_AGENT)
    
    compressed_content_ga = result_ga.compressed_content
    if isinstance(compressed_content_ga, dict):
        compressed_text_ga = compressed_content_ga.get('summary', '')
    else:
        compressed_text_ga = str(compressed_content_ga)
    
    bleu_ga = calculate_bleu(original_text, compressed_text_ga)
    rouge_l_ga = calculate_rouge_l(original_text, compressed_text_ga)
    
    print(f'  压缩比: {result_ga.compression_ratio:.2%}')
    print(f'  BLEU分数: {bleu_ga:.2%}')
    print(f'  ROUGE-L分数: {rouge_l_ga:.2%}')
    print(f'  综合准确性: {(bleu_ga + rouge_l_ga) / 2:.2%}')
    
    # 对比预设准确性
    print('\n' + '=' * 60)
    print('准确性对比 (预设 vs 实测)')
    print('=' * 60)
    print(f'LightThinker++: 预设92% vs 实测{(bleu_lt + rouge_l_lt) / 2:.2%}')
    print(f'GenericAgent: 预设88% vs 实测{(bleu_ga + rouge_l_ga) / 2:.2%}')
    
    # 评估是否达标
    print('\n' + '=' * 60)
    print('准确性评估 (目标: 85-95%)')
    print('=' * 60)
    
    lt_accuracy = (bleu_lt + rouge_l_lt) / 2
    ga_accuracy = (bleu_ga + rouge_l_ga) / 2
    
    if lt_accuracy >= 0.85:
        print(f'LightThinker++: {lt_accuracy:.2%} - [通过] 达到目标')
    else:
        print(f'LightThinker++: {lt_accuracy:.2%} - [未通过] 低于目标(85%)')
    
    if ga_accuracy >= 0.85:
        print(f'GenericAgent: {ga_accuracy:.2%} - [通过] 达到目标')
    else:
        print(f'GenericAgent: {ga_accuracy:.2%} - [未通过] 低于目标(85%)')
    
    print('\n' + '=' * 60)
    print('准确性验证完成！')
    print('=' * 60)

if __name__ == '__main__':
    main()
