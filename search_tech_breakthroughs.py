#!/usr/bin/env python3
"""
搜索Token优化和LLM推理相关的最新技术突破
"""
import requests
import json
import time
from datetime import datetime, timedelta

def search_github_repos(query, limit=5):
    """搜索GitHub仓库"""
    url = f"https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json().get("items", [])
    except Exception as e:
        print(f"  [ERROR] GitHub API错误: {e}")
    return []

def search_arxiv_papers(query, limit=5):
    """搜索arXiv论文"""
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": limit
    }
    
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            # 简单解析XML (避免额外依赖)
            import re
            entries = re.findall(r"<entry>(.*?)</entry>", r.text, re.DOTALL)
            papers = []
            for entry in entries[:limit]:
                title = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
                summary = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
                published = re.search(r"<published>(.*?)</published>", entry, re.DOTALL)
                
                if title:
                    papers.append({
                        "title": title.group(1).strip(),
                        "summary": summary.group(1).strip()[:200] if summary else "",
                        "published": published.group(1)[:10] if published else ""
                    })
            return papers
    except Exception as e:
        print(f"  [ERROR] arXiv API错误: {e}")
    return []

def print_separator(char="=", length=70):
    """打印分隔线"""
    print(char * length)

def main():
    print("\n")
    print_separator("=")
    print("搜索Token优化和LLM推理最新技术突破")
    print_separator("=")
    print("\n")
    
    # 定义搜索关键词
    searches = [
        {
            "category": "Token优化",
            "queries": [
                "token optimization LLM",
                "prompt compression",
                "context compression"
            ]
        },
        {
            "category": "语义缓存",
            "queries": [
                "semantic cache LLM",
                "semantic search cache",
                "embedding cache"
            ]
        },
        {
            "category": "LLM推理优化",
            "queries": [
                "LLM inference optimization",
                "KV cache optimization",
                "attention optimization"
            ]
        },
        {
            "category": "上下文管理",
            "queries": [
                "context window management",
                "long context LLM",
                "context pruning"
            ]
        }
    ]
    
    results = {}
    
    for search in searches:
        category = search["category"]
        print(f"\n{'='*70}")
        print(f"类别: {category}")
        print(f"{'='*70}\n")
        
        results[category] = {
            "repos": [],
            "papers": []
        }
        
        for query in search["queries"]:
            print(f"[搜索] {query}")
            
            # GitHub仓库
            repos = search_github_repos(query, limit=3)
            if repos:
                print(f"  GitHub仓库 (Top {len(repos)}):")
                for i, repo in enumerate(repos, 1):
                    name = repo["name"]
                    desc = repo.get("description", "无描述")[:80]
                    stars = repo["stargazers_count"]
                    print(f"    {i}. {name} (Stars: {stars})")
                    print(f"       {desc}")
                    results[category]["repos"].append({
                        "name": name,
                        "stars": stars,
                        "description": desc
                    })
            
            # arXiv论文 (只搜索第一个query,避免API限制)
            if query == search["queries"][0]:
                papers = search_arxiv_papers(query.replace(" ", "+"), limit=3)
                if papers:
                    print(f"  arXiv论文 (Top {len(papers)}):")
                    for i, paper in enumerate(papers, 1):
                        title = paper["title"][:80]
                        date = paper["published"]
                        print(f"    {i}. {title}")
                        print(f"       日期: {date}")
                        results[category]["papers"].append({
                            "title": title,
                            "date": date
                        })
            
            print()
            time.sleep(1)  # 避免API限制
    
    # 生成总结报告
    print("\n")
    print_separator("=")
    print("技术突破总结报告")
    print_separator("=")
    print("\n")
    
    for category, data in results.items():
        print(f"【{category}】")
        
        if data["repos"]:
            print(f"  Top仓库:")
            for repo in data["repos"][:3]:
                print(f"    - {repo['name']} ({repo['stars']} stars)")
        
        if data["papers"]:
            print(f"  Top论文:")
            for paper in data["papers"][:3]:
                print(f"    - {paper['title'][:60]}...")
        
        print()
    
    # 保存结果到JSON
    output_file = "tech_breakthroughs_search_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"详细结果已保存到: {output_file}\n")
    
    return results

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消搜索")
    except Exception as e:
        print(f"\n\n[ERROR] 搜索失败: {e}")
        import traceback
        traceback.print_exc()
