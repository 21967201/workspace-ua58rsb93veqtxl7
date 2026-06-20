#!/usr/bin/env python3
"""
Skill Tree Manager Enhanced: 增强版技能树管理器 (修复版)

使用向量特征 + 余弦相似度。
"""

import json
import argparse
import math
from typing import List, Dict, Any
from datetime import datetime


class SkillTreeEnhanced:
    """增强版技能树管理器 (修复相似度计算bug)"""
    
    def __init__(self, embedding_model: str = "simplified", similarity_threshold: float = 0.5):
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        self.skill_tree = {"nodes": {}, "edges": []}
        
        print(f"[INFO] Skill Tree Enhanced (fixed) initialized")
        print(f"[INFO]   Embedding model: {embedding_model}")
        print(f"[INFO]   Similarity threshold: {similarity_threshold}")
    
    def _extract_feature_vector(self, skill: Dict[str, Any]) -> List[float]:
        """
        提取技能特征向量（修复版：返回数值向量）
        
        Args:
            skill: 技能数据
            
        Returns:
            vector: 特征向量（21维）
        """
        skill_data = skill.get("skill", {})
        vector = []
        
        # 特征1：名称关键词（7维 one-hot）
        name = skill_data.get("name", "").lower()
        vector.append(1.0 if "pdf" in name else 0.0)
        vector.append(1.0 if "reader" in name else 0.0)
        vector.append(1.0 if "basic" in name else 0.0)
        vector.append(1.0 if "advanced" in name else 0.0)
        vector.append(1.0 if "ocr" in name else 0.0)
        vector.append(1.0 if "batch" in name else 0.0)
        vector.append(1.0 if "smart" in name else 0.0)
        
        # 特征2：描述关键词（8维 count-based）
        desc = skill_data.get("description", "").lower()
        vector.append(float(desc.count("basic")))
        vector.append(float(desc.count("advanced")))
        vector.append(float(desc.count("layout")))
        vector.append(float(desc.count("scanned")))
        vector.append(float(desc.count("batch")))
        vector.append(float(desc.count("detect")))
        vector.append(float(desc.count("extract")))
        vector.append(min(float(len(desc.split()) / 20), 1.0))  # 归一化描述长度
        
        # 特征3：工具使用（4维 one-hot）
        tools = [t.lower() for t in skill_data.get("tools", [])]
        vector.append(1.0 if "read" in tools else 0.0)
        vector.append(1.0 if "write" in tools else 0.0)
        vector.append(1.0 if "exec" in tools else 0.0)
        vector.append(1.0 if "web_search" in tools else 0.0)
        
        # 特征4：数值特征（3维）
        steps = skill_data.get("steps", [])
        examples = skill_data.get("examples", [])
        vector.append(float(len(steps)))
        vector.append(float(len(examples)))
        vector.append(float(sum(len(s.split()) for s in steps) / max(len(steps), 1)))
        
        # 总计：7 + 8 + 4 + 3 = 22维
        return vector
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        计算余弦相似度（修复版）
        
        Args:
            vec1: 向量1
            vec2: 向量2
            
        Returns:
            similarity: 余弦相似度（-1 to 1，处理后0-1）
        """
        if not vec1 or not vec2:
            return 0.0
        
        # 确保向量长度相同
        max_len = max(len(vec1), len(vec2))
        vec1 = vec1 + [0.0] * (max_len - len(vec1))
        vec2 = vec2 + [0.0] * (max_len - len(vec2))
        
        # 计算点积
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # 计算模
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        
        cosine = dot_product / (norm1 * norm2)
        
        # 归一化到0-1范围
        similarity = (cosine + 1.0) / 2.0
        
        return similarity
    
    def build_skill_tree(self, assessed_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """构建技能树"""
        print(f"\n[INFO] Building skill tree from {len(assessed_candidates)} candidates...")
        
        self.skill_tree = {"nodes": {}, "edges": []}
        
        # 添加根节点
        root_id = "root"
        self.skill_tree["nodes"][root_id] = {
            "skill_data": {"skill": {"name": "Root", "description": "Root node"}},
            "feature_vector": [0.0] * 22,
            "assessment": {"final_score": 1.0}
        }
        
        # 添加所有候选技能
        for i, candidate in enumerate(assessed_candidates):
            node_id = f"node_{i}"
            
            # 提取特征向量
            feature_vector = self._extract_feature_vector(candidate)
            
            self.skill_tree["nodes"][node_id] = {
                "skill_data": candidate,
                "feature_vector": feature_vector,
                "assessment": candidate.get("assessment", {})
            }
            
            self.skill_tree["edges"].append({
                "source": root_id,
                "target": node_id,
                "weight": candidate.get("assessment", {}).get("final_score", 0.5)
            })
            
            print(f"[INFO]   Added node {node_id}: {candidate.get('skill', {}).get('name', 'Unknown')}")
        
        print(f"[INFO] Skill tree built: {len(self.skill_tree['nodes'])} nodes, {len(self.skill_tree['edges'])} edges")
        return self.skill_tree
    
    def retrieve_skills(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        检索技能树中的相关技能（修复版）
        """
        print(f"\n[INFO] Retrieving top-{top_k} skills for query: {query[:50]}...")
        
        # 构建查询特征向量
        query_skill = {
            "skill": {
                "name": query,
                "description": query,
                "tools": [],
                "steps": [query],
                "examples": []
            }
        }
        query_vector = self._extract_feature_vector(query_skill)
        
        # 计算相似度
        similarities = []
        for node_id, node_data in self.skill_tree["nodes"].items():
            if node_id == "root":
                continue
            
            vector = node_data.get("feature_vector", [])
            similarity = self._cosine_similarity(query_vector, vector)
            
            similarities.append({
                "node_id": node_id,
                "skill_data": node_data["skill_data"],
                "similarity": similarity,
                "assessment": node_data.get("assessment", {})
            })
        
        # 按相似度排序
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # 返回Top-K
        retrieved = similarities[:top_k]
        
        print(f"[INFO] Retrieved {len(retrieved)} skills:")
        for i, item in enumerate(retrieved):
            name = item["skill_data"].get("skill", {}).get("name", "Unknown")
            print(f"[INFO]   {i+1}. {name} (similarity={item['similarity']:.3f})")
        
        return retrieved
    
    def save_skill_tree(self, output_file: str):
        """保存技能树到文件"""
        print(f"\n[INFO] Saving skill tree to: {output_file}")
        
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "embedding_model": self.embedding_model,
            "similarity_threshold": self.similarity_threshold,
            "num_nodes": len(self.skill_tree["nodes"]),
            "num_edges": len(self.skill_tree["edges"]),
            "skill_tree": self.skill_tree
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Skill tree saved successfully")
    
    def load_skill_tree(self, input_file: str):
        """从文件加载技能树"""
        print(f"\n[INFO] Loading skill tree from: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.embedding_model = data.get("embedding_model", "simplified")
        self.similarity_threshold = data.get("similarity_threshold", 0.7)
        self.skill_tree = data.get("skill_tree", {"nodes": {}, "edges": []})
        
        print(f"[INFO] Skill tree loaded: {len(self.skill_tree['nodes'])} nodes")


def main():
    parser = argparse.ArgumentParser(description="Skill Tree Enhanced: Build and manage skill tree (fixed)")
    parser.add_argument("--assessed", type=str, help="Assessed candidates JSON file")
    parser.add_argument("--output", type=str, default="skill-tree-enhanced-fixed.json", help="Output skill tree file")
    parser.add_argument("--load", type=str, help="Load existing skill tree")
    parser.add_argument("--retrieve", type=str, help="Retrieve skills with query")
    parser.add_argument("--top-k", type=int, default=3, help="Number of skills to retrieve")
    
    args = parser.parse_args()
    
    print("[INFO] Skill Tree Enhanced: Structured Skill Tree Manager (Fixed Version)")
    print("[INFO]   With vector features + cosine similarity\n")
    
    tree_manager = SkillTreeEnhanced(
        embedding_model="simplified",
        similarity_threshold=0.5
    )
    
    if args.load:
        tree_manager.load_skill_tree(args.load)
    
    if args.assessed:
        with open(args.assessed, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assessed_candidates = data.get("candidates", [])
        
        tree_manager.build_skill_tree(assessed_candidates)
        tree_manager.save_skill_tree(output_file=args.output)
    
    if args.retrieve:
        if not args.load:
            print("[WARN] No skill tree loaded, cannot retrieve. Use --load first.")
            return
        
        retrieved = tree_manager.retrieve_skills(args.retrieve, top_k=args.top_k)
        
        print(f"\n[INFO] Retrieval results:")
        for i, item in enumerate(retrieved):
            print(f"  {i+1}. {item['skill_data'].get('skill', {}).get('name', 'Unknown')} (similarity={item['similarity']:.3f})")
    
    if not args.assessed and not args.retrieve:
        print("[INFO] No action specified. Use --assessed to build tree or --retrieve to search.")


if __name__ == "__main__":
    main()
