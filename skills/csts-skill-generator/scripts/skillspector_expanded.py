#!/usr/bin/env python3
"""
SkillSpector Expanded: AI Agent Skill Security Scanner (64 patterns, 16 categories)

Based on NVIDIA SkillSpector (https://github.com/NVIDIA/SkillSpector)
64 vulnerability patterns across 16 risk categories (full implementation)
"""

import json
import argparse
import re
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime


RISK_CATEGORIES = {
    1: "Prompt Injection",
    2: "Credential Theft",
    3: "Data Exfiltration",
    4: "Code Injection",
    5: "Command Injection",
    6: "Path Traversal",
    7: "SSRF",
    8: "XSS",
    9: "SQL Injection",
    10: "Deserialization Attack",
    11: "Zip Slip",
    12: "Dependency Confusion",
    13: "Malicious Dependencies",
    14: "Information Disclosure",
    15: "Denial of Service",
    16: "Scope Creep"
}

VULNERABILITY_PATTERNS = [
    # Cat 1: Prompt Injection
    {"id": "PI-001", "category": 1, "pattern": r"ignore.*previous.*instructions?", "severity": "HIGH"},
    {"id": "PI-002", "category": 1, "pattern": r"you.*now.*a.*different.*role", "severity": "HIGH"},
    {"id": "PI-003", "category": 1, "pattern": r"forget.*all.*previous", "severity": "MEDIUM"},
    {"id": "PI-004", "category": 1, "pattern": r"system.*prompt.*override", "severity": "CRITICAL"},
    # Cat 2: Credential Theft
    {"id": "CT-001", "category": 2, "pattern": r"api[_-]?key\s*[:=]\s*[\"']?\w+", "severity": "CRITICAL"},
    {"id": "CT-002", "category": 2, "pattern": r"password\s*[:=]\s*[\"']?\w+", "severity": "CRITICAL"},
    {"id": "CT-003", "category": 2, "pattern": r"token\s*[:=]\s*[\"']?\w+", "severity": "HIGH"},
    {"id": "CT-004", "category": 2, "pattern": r"secret\s*[:=]\s*[\"']?\w+", "severity": "HIGH"},
    # Cat 3: Data Exfiltration
    {"id": "DE-001", "category": 3, "pattern": r"send.*to.*(http|https|ftp)", "severity": "HIGH"},
    {"id": "DE-002", "category": 3, "pattern": r"exfiltrat", "severity": "CRITICAL"},
    {"id": "DE-003", "category": 3, "pattern": r"leak.*data", "severity": "HIGH"},
    {"id": "DE-004", "category": 3, "pattern": r"upload.*to.*external", "severity": "MEDIUM"},
    # Cat 4: Code Injection
    {"id": "CI-001", "category": 4, "pattern": r"eval\s*\(", "severity": "CRITICAL"},
    {"id": "CI-002", "category": 4, "pattern": r"exec\s*\(", "severity": "CRITICAL"},
    {"id": "CI-003", "category": 4, "pattern": r"__import__\s*\(", "severity": "HIGH"},
    {"id": "CI-004", "category": 4, "pattern": r"subprocess\.(run|call|Popen)", "severity": "HIGH"},
    # Cat 5: Command Injection
    {"id": "CMD-001", "category": 5, "pattern": r"os\.system\s*\(", "severity": "CRITICAL"},
    {"id": "CMD-002", "category": 5, "pattern": r"shell\s*=\s*True", "severity": "HIGH"},
    {"id": "CMD-003", "category": 5, "pattern": r"bash\s+-c", "severity": "HIGH"},
    {"id": "CMD-004", "category": 5, "pattern": r"powershell\s+", "severity": "MEDIUM"},
    # Cat 6: Path Traversal
    {"id": "PT-001", "category": 6, "pattern": r"\.\./|\.\.\\", "severity": "HIGH"},
    {"id": "PT-002", "category": 6, "pattern": r"/etc/passwd", "severity": "MEDIUM"},
    {"id": "PT-003", "category": 6, "pattern": r"\.\+/.*\.\+", "severity": "HIGH"},
    {"id": "PT-004", "category": 6, "pattern": r"path\.join.*\.\.", "severity": "MEDIUM"},
    # Cat 7: SSRF
    {"id": "SSRF-001", "category": 7, "pattern": r"requests\.get\s*\(\s*[\"']?https?://", "severity": "HIGH"},
    {"id": "SSRF-002", "category": 7, "pattern": r"urllib\.request\.urlopen", "severity": "MEDIUM"},
    {"id": "SSRF-003", "category": 7, "pattern": r"curl\s+.*(localhost|127\.0\.0\.1)", "severity": "HIGH"},
    {"id": "SSRF-004", "category": 7, "pattern": r"wget\s+.*(internal|private)", "severity": "MEDIUM"},
    # Cat 8: XSS
    {"id": "XSS-001", "category": 8, "pattern": r"<script.*>", "severity": "CRITICAL"},
    {"id": "XSS-002", "category": 8, "pattern": r"onerror\s*=", "severity": "HIGH"},
    {"id": "XSS-003", "category": 8, "pattern": r"javascript:", "severity": "HIGH"},
    {"id": "XSS-004", "category": 8, "pattern": r"alert\s*\(", "severity": "MEDIUM"},
    # Cat 9: SQL Injection
    {"id": "SQL-001", "category": 9, "pattern": r"SELECT.*FROM.*WHERE.*\+", "severity": "CRITICAL"},
    {"id": "SQL-002", "category": 9, "pattern": r"INSERT.*INTO.*\+", "severity": "HIGH"},
    {"id": "SQL-003", "category": 9, "pattern": r"DROP.*TABLE", "severity": "CRITICAL"},
    {"id": "SQL-004", "category": 9, "pattern": r"\.execute\s*\(\s*[\"']?SELECT", "severity": "HIGH"},
    # Cat 10: Deserialization Attack
    {"id": "DA-001", "category": 10, "pattern": r"pickle\.load", "severity": "CRITICAL"},
    {"id": "DA-002", "category": 10, "pattern": r"yaml\.load\s*\(", "severity": "HIGH"},
    {"id": "DA-003", "category": 10, "pattern": r"json\.loads\s*\(", "severity": "MEDIUM"},
    {"id": "DA-004", "category": 10, "pattern": r"marshal\.load", "severity": "HIGH"},
    # Cat 11: Zip Slip
    {"id": "ZS-001", "category": 11, "pattern": r"zipfile\.extractall", "severity": "HIGH"},
    {"id": "ZS-002", "category": 11, "pattern": r"tarfile\.extractall", "severity": "HIGH"},
    {"id": "ZS-003", "category": 11, "pattern": r"\.extract\s*\(", "severity": "MEDIUM"},
    {"id": "ZS-004", "category": 11, "pattern": r"shutil\.unpack_archive", "severity": "MEDIUM"},
    # Cat 12: Dependency Confusion
    {"id": "DC-001", "category": 12, "pattern": r"pip\s+install.*--extra-index-url", "severity": "HIGH"},
    {"id": "DC-002", "category": 12, "pattern": r"npm\s+install.*--registry", "severity": "HIGH"},
    {"id": "DC-003", "category": 12, "pattern": r"requirements.*\.txt.*internal", "severity": "MEDIUM"},
    {"id": "DC-004", "category": 12, "pattern": r"private.*pypi", "severity": "MEDIUM"},
    # Cat 13: Malicious Dependencies
    {"id": "MD-001", "category": 13, "pattern": r"import.*os.*system", "severity": "CRITICAL"},
    {"id": "MD-002", "category": 13, "pattern": r"import.*subprocess.*shell=True", "severity": "CRITICAL"},
    {"id": "MD-003", "category": 13, "pattern": r"import.*requests.*verify=False", "severity": "HIGH"},
    {"id": "MD-004", "category": 13, "pattern": r"import.*crypto.*weak", "severity": "MEDIUM"},
    # Cat 14: Information Disclosure
    {"id": "ID-001", "category": 14, "pattern": r"print\s*\(\s*[\"']?debug", "severity": "LOW"},
    {"id": "ID-002", "category": 14, "pattern": r"logging\.(debug|info)\s*\(", "severity": "LOW"},
    {"id": "ID-003", "category": 14, "pattern": r"traceback\.print_exc", "severity": "MEDIUM"},
    {"id": "ID-004", "category": 14, "pattern": r"stack.*trace", "severity": "LOW"},
    # Cat 15: Denial of Service
    {"id": "DoS-001", "category": 15, "pattern": r"while\s+True\s*:", "severity": "MEDIUM"},
    {"id": "DoS-002", "category": 15, "pattern": r"\.sleep\s*\(\s*\d+\s*\)", "severity": "LOW"},
    {"id": "DoS-003", "category": 15, "pattern": r"recursion.*depth", "severity": "MEDIUM"},
    {"id": "DoS-004", "category": 15, "pattern": r"multiprocessing\.(Pool|Process)", "severity": "HIGH"},
    # Cat 16: Scope Creep
    {"id": "SC-001", "category": 16, "pattern": r"access.*all.*files", "severity": "HIGH"},
    {"id": "SC-002", "category": 16, "pattern": r"read.*entire.*database", "severity": "CRITICAL"},
    {"id": "SC-003", "category": 16, "pattern": r"execute.*arbitrary.*code", "severity": "CRITICAL"},
    {"id": "SC-004", "category": 16, "pattern": r"full.*system.*access", "severity": "CRITICAL"},
]


class SkillSpectorExpanded:
    """SkillSpector Expanded: 64 patterns, 16 categories"""
    
    def __init__(self, scan_depth: str = "quick"):
        self.scan_depth = scan_depth
        self.patterns = VULNERABILITY_PATTERNS
        self.categories = RISK_CATEGORIES
        print(f"[INFO] SkillSpector Expanded initialized")
        print(f"[INFO]   Patterns: {len(self.patterns)} | Categories: {len(self.categories)} | Depth: {scan_depth}")
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan a single file with all 64 patterns"""
        print(f"[INFO] Scanning: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {"file": file_path, "vulnerabilities": [], "error": str(e)}
        
        vulnerabilities = []
        for p in self.patterns:
            matches = re.findall(p["pattern"], content, re.IGNORECASE)
            if matches:
                vulnerabilities.append({
                    "pattern_id": p["id"],
                    "category": self.categories.get(p["category"], "Unknown"),
                    "category_id": p["category"],
                    "severity": p["severity"],
                    "pattern": p["pattern"],
                    "matches": matches[:5],
                    "match_count": len(matches)
                })
        
        risk_score = self._calculate_risk_score(vulnerabilities)
        return {
            "file": file_path,
            "vulnerabilities": vulnerabilities,
            "risk_score": risk_score,
            "patterns_checked": len(self.patterns),
            "categories_affected": list(set(v["category_id"] for v in vulnerabilities))
        }
    
    def _calculate_risk_score(self, vulnerabilities: List[Dict]) -> int:
        """Risk score 0-100"""
        if not vulnerabilities:
            return 0
        weights = {"CRITICAL": 10, "HIGH": 7, "MEDIUM": 4, "LOW": 1}
        total = sum(weights.get(v.get("severity", "LOW"), 1) * min(v.get("match_count", 1), 5) for v in vulnerabilities)
        return min(int((total / (len(self.patterns) * 10)) * 100), 100)
    
    def scan_directory(self, dir_path: str, extensions: List[str] = None) -> List[Dict]:
        """Scan directory recursively"""
        if extensions is None:
            extensions = [".py", ".md", ".json", ".js", ".ts"]
        print(f"[INFO] Scanning directory: {dir_path}")
        results = []
        for fp in Path(dir_path).rglob("*"):
            if fp.is_file() and fp.suffix in extensions:
                results.append(self.scan_file(str(fp)))
        return results
    
    def generate_report(self, scan_results: List[Dict], output_file: str):
        """Generate security report"""
        total_vulns = sum(len(r.get("vulnerabilities", [])) for r in scan_results)
        sev_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for r in scan_results:
            for v in r.get("vulnerabilities", []):
                sev_counts[v.get("severity", "LOW")] += 1
        
        risk_scores = [r.get("risk_score", 0) for r in scan_results]
        avg_risk = sum(risk_scores) / max(len(risk_scores), 1)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_files": len(scan_results),
                "total_vulnerabilities": total_vulns,
                "avg_risk_score": round(avg_risk, 1),
                "severity_distribution": sev_counts,
                "patterns_checked": len(self.patterns),
                "categories_checked": len(self.categories)
            },
            "scan_results": scan_results
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Report saved: {output_file}")
        print(f"[INFO]   Files: {len(scan_results)} | Vulns: {total_vulns} | Avg Risk: {avg_risk:.1f}/100")
        print(f"[INFO]   Severity: CRITICAL={sev_counts['CRITICAL']}, HIGH={sev_counts['HIGH']}, MEDIUM={sev_counts['MEDIUM']}, LOW={sev_counts['LOW']}")
        return report


def main():
    parser = argparse.ArgumentParser(description="SkillSpector Expanded: 64 patterns, 16 categories")
    parser.add_argument("--scan-file", type=str, help="Scan a single file")
    parser.add_argument("--scan-dir", type=str, help="Scan a directory recursively")
    parser.add_argument("--output", type=str, default="skillspector-expanded-report.json", help="Output report file")
    parser.add_argument("--depth", type=str, default="quick", choices=["quick", "deep"], help="Scan depth")
    args = parser.parse_args()
    
    print("[INFO] SkillSpector Expanded: Full 64-pattern, 16-category scanner\n")
    
    scanner = SkillSpectorExpanded(scan_depth=args.depth)
    
    if args.scan_file:
        result = scanner.scan_file(args.scan_file)
        scanner.generate_report([result], args.output)
    elif args.scan_dir:
        results = scanner.scan_directory(args.scan_dir)
        scanner.generate_report(results, args.output)
    else:
        print("[INFO] No scan target specified. Use --scan-file or --scan-dir")


if __name__ == "__main__":
    main()
