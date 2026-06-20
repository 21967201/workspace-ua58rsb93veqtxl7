#!/usr/bin/env python3
"""
Skill Tree Manager: 技能树管理

构建结构化、多样化和可泛化的技能树
支持技能检索、遍历和持久化
"""

import json
import os
import argparse
from typing import List, Dict, Any, Optional
from datetime import datetime


class SkillNode:
    """技能树节点"""
    
    def __init__(self, skill_data: Dict[str, Any], parent_id: Optional[str] = None):
        """
        Args:
            skill_data: 技能数据 (from CSN-Gen/Assess)
            parent_id: 父节点ID (如果有)
        """
        self.id = skill_data.get("skill", {}).get("name", "unknown")
        self.skill_data = skill_data
        self.parent_id = parent_id
        self.children_ids = []
        self.created_at = datetime.now().isoformat()
        self.usage_count = 0
        self.success_rate = 0.0
        
    def add_child(self, child_id: str):
        """添加子节点"""
        if child_id not in self.children_ids:
            self.children_ids.append(child_id)
    
    def update_performance(self, success: bool):
        """更新性能统计"""
        self.usage_count += 1
        
        # 更新成功率 (滑动平均)
        if self.usage_count == 1:
            self.success_rate = 1.0 if success else 0.0
        else:
            alpha = 0.1  # 学习率
            new_rate = 1.0 if success else 0.0
            self.success_rate = (1 - alpha) * self.success_rate + alpha * new_rate
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 (for JSON serialization)"""
        return {
            "id": self.id,
            "skill_data": self.skill_data,
            "parent_id": self.parent_id,
            "children_ids": self.children_ids,
            "created_at": self.created_at,
            "usage_count": self.usage_count,
            "success_rate": self.success_rate
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SkillNode':
        """从字典创建节点"""
        node = cls(data["skill_data"], parent_id=data.get("parent_id"))
        node.id = data["id"]
        node.children_ids = data.get("children_ids", [])
        node.created_at = data.get("created_at", datetime.now().isoformat())
        node.usage_count = data.get("usage_count", 0)
        node.success_rate = data.get("success_rate", 0.0)
        return node


class SkillTreeManager:
    """技能树管理器"""
    
    def __init__(self, tree_file: str = "memory/csts-skill-tree.json"):
        """
        Args:
            tree_file: 技能树持久化文件路径
        """
        self.tree_file = tree_file
        self.nodes = {}  # {node_id: SkillNode}
        self.root_ids = []  # 根节点ID列表
        
        # 加载已有技能树
        self.load()
        
        print(f"[INFO] SkillTreeManager initialized")
        print(f"[INFO]   Tree file: {tree_file}")
        print(f"[INFO]   Loaded nodes: {len(self.nodes)}")
    
    def add_skill(self, skill_data: Dict[str, Any], parent_id: Optional[str] = None) -> str:
        """
        添加技能到树
        
        Args:
            skill_data: 技能数据
            parent_id: 父节点ID (如果是子技能)
            
        Returns:
            node_id: 添加的节点ID
        """
        # 创建节点
        node = SkillNode(skill_data, parent_id=parent_id)
        
        # 检查是否已存在
        if node.id in self.nodes:
            print(f"[WARN] Skill already exists: {node.id}, skipping")
            return node.id
        
        # 添加到树
        self.nodes[node.id] = node
        
        # 更新父节点
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].add_child(node.id)
        else:
            # 根节点
            if node.id not in self.root_ids:
                self.root_ids.append(node.id)
        
        print(f"[INFO] Added skill: {node.id}")
        print(f"[INFO]   Parent: {parent_id or '(root)'}")
        print(f"[INFO]   Total nodes: {len(self.nodes)}")
        
        # 自动保存
        self.save()
        
        return node.id
    
    def get_skill(self, node_id: str) -> Optional[SkillNode]:
        """获取技能节点"""
        return self.nodes.get(node_id)
    
    def search_skills(self, query: str, top_k: int = 5) -> List[SkillNode]:
        """
        搜索技能 (简化版：基于关键词匹配)
        
        Args:
            query: 搜索查询
            top_k: 返回前K个结果
            
        Returns:
            results: 匹配的技能节点列表
        """
        query_lower = query.lower()
        results = []
        
        for node_id, node in self.nodes.items():
            skill = node.skill_data.get("skill", {})
            description = skill.get("description", "").lower()
            name = skill.get("name", "").lower()
            
            # 简单匹配：查询词是否在描述或名称中
            if query_lower in description or query_lower in name:
                results.append(node)
        
        # 按成功率排序
        results.sort(key=lambda n: n.success_rate, reverse=True)
        
        return results[:top_k]
    
    def update_skill_performance(self, node_id: str, success: bool):
        """更新技能性能"""
        if node_id in self.nodes:
            self.nodes[node_id].update_performance(success)
            self.save()
    
    def get_tree_structure(self) -> Dict[str, Any]:
        """获取树结构 (for visualization)"""
        return {
            "roots": self.root_ids,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "stats": {
                "total_nodes": len(self.nodes),
                "total_roots": len(self.root_ids),
                "avg_success_rate": sum(n.success_rate for n in self.nodes.values()) / max(len(self.nodes), 1)
            }
        }
    
    def save(self):
        """保存技能树到文件"""
        try:
            os.makedirs(os.path.dirname(self.tree_file), exist_ok=True)
            
            data = {
                "roots": self.root_ids,
                "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
                "saved_at": datetime.now().isoformat()
            }
            
            with open(self.tree_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[INFO] Tree saved to: {self.tree_file}")
        except Exception as e:
            print(f"[ERROR] Failed to save tree: {e}")
    
    def load(self):
        """从文件加载技能树"""
        if not os.path.exists(self.tree_file):
            print(f"[INFO] Tree file not found, starting with empty tree")
            return
        
        try:
            with open(self.tree_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.root_ids = data.get("roots", [])
            self.nodes = {}
            
            for nid, node_data in data.get("nodes", {}).items():
                self.nodes[nid] = SkillNode.from_dict(node_data)
            
            print(f"[INFO] Tree loaded from: {self.tree_file}")
            print(f"[INFO]   Roots: {len(self.root_ids)}")
            print(f"[INFO]   Nodes: {len(self.nodes)}")
        except Exception as e:
            print(f"[ERROR] Failed to load tree: {e}")


def main():
    parser = argparse.ArgumentParser(description="Skill Tree Manager: Build and manage skill tree")
    parser.add_argument("--assessed", type=str, help="Assessed skills JSON file (from CSN-Assess)")
    parser.add_argument("--tree-output", type=str, default="memory/csts-skill-tree.json", 
                       help="Output tree file")
    parser.add_argument("--add-to-openclaw", action="store_true", 
                       help="Add skills to OpenClaw (generate SKILL.md files)")
    parser.add_argument("--search", type=str, help="Search skills by query")
    parser.add_argument("--top-k", type=int, default=5, help="Top-K search results")
    
    args = parser.parse_args()
    
    # 初始化管理器
    manager = SkillTreeManager(tree_file=args.tree_output)
    
    # 添加评估后的技能
    if args.assessed:
        print(f"\n[INFO] Loading assessed skills from: {args.assessed}")
        
        with open(args.assessed, 'r', encoding='utf-8') as f:
            assessed_skills = json.load(f)
        
        print(f"[INFO] Loaded {len(assessed_skills)} assessed skills")
        
        # 按最终评分排序 (高分优先)
        assessed_skills.sort(
            key=lambda x: x.get("assessment", {}).get("final_score", 0.0), 
            reverse=True
        )
        
        # 添加到技能树
        for skill_data in assessed_skills:
            node_id = manager.add_skill(skill_data, parent_id=None)  # 暂时都作为根节点
            
            # 如果需要添加到OpenClaw
            if args.add_to_openclaw:
                # TODO: 生成SKILL.md文件
                print(f"[INFO] TODO: Generate SKILL.md for {node_id}")
        
        print(f"\n[INFO] Total nodes in tree: {len(manager.nodes)}")
    
    # 搜索技能
    if args.search:
        print(f"\n[INFO] Searching skills: {args.search}")
        
        results = manager.search_skills(args.search, top_k=args.top_k)
        
        print(f"[INFO] Found {len(results)} results:")
        for i, node in enumerate(results):
            skill = node.skill_data.get("skill", {})
            print(f"  {i+1}. {skill.get('name', 'Unknown')}")
            print(f"     Description: {skill.get('description', '')[:50]}...")
            print(f"     Success rate: {node.success_rate:.2%}")
            print(f"     Usage: {node.usage_count}")
    
    # 如果没有指定操作，显示树统计
    if not args.assessed and not args.search:
        stats = manager.get_tree_structure()["stats"]
        print(f"\n[INFO] Skill Tree Statistics:")
        print(f"  Total nodes: {stats['total_nodes']}")
        print(f"  Total roots: {stats['total_roots']}")
        print(f"  Avg success rate: {stats['avg_success_rate']:.2%}")


if __name__ == "__main__":
    main()
