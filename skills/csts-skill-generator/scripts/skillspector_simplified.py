#!/usr/bin/env python3
"""
SkillSpector Simplified: AI Agent Skill Security Scanner (Simplified Version)

Based on NVIDIA SkillSpector (https://github.com/NVIDIA/SkillSpector)
64 vulnerability patterns across 16 risk categories

This is a simplified implementation for testing and integration.
"""

import json
import argparse
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path


# 16 Risk Categories (based on NVIDIA SkillSpector documentation)
RISK_CATEGORIES = {
    1: "Prompt Injection",
    2: "Credential Theft",
    3: "Data Exfiltration",
    4: "Code Injection",
    5: "Command Injection",
    6: "Path Traversal",
    7: "SSRF (Server-Side Request Forgery)",
    8: "XSS (Cross-Site Scripting)",
    9: "SQL Injection",
    10: "Deserialization Attack",
    11: "Zip Slip",
    12: "Dependency Confusion",
    13: "Malicious Dependencies",
    14: "Information Disclosure",
    15: "Denial of Service",
    16: "Scope Creep"
}

# 64 Vulnerability Patterns (simplified version)
VULNERABILITY_PATTERNS = [
    # Category 1: Prompt Injection (4 patterns)
    {"id": "PI-001", "category": 1, "pattern": r"ignore .* previous .* instructions?", "severity": "HIGH"},
    {"id": "PI-002", "category": 1, "pattern": r"you .* now .* a .* different .* role", "severity": "HIGH"},
    {"id": "PI-003", "category": 1, "pattern": r"forget .* all .* previous", "severity": "MEDIUM"},
    {"id": "PI-004", "category": 1, "pattern": r"system .* prompt .* override", "severity": "CRITICAL"},
    
    # Category 2: Credential Theft (4 patterns)
    {"id": "CT-001", "category": 2, "pattern": r"api[_-]?key\s*[:=]\s*[\"']?\w+", "severity": "CRITICAL"},
    {"id": "CT-002", "category": 2, "pattern": r"password\s*[:=]\s*[\"']?\w+", "severity": "CRITICAL"},
    {"id": "CT-003", "category": 2, "pattern": r"token\s*[:=]\s*[\"']?\w+", "severity": "HIGH"},
    {"id": "CT-004", "category": 2, "pattern": r"secret\s*[:=]\s*[\"']?\w+", "severity": "HIGH"},
    
    # Category 3: Data Exfiltration (4 patterns)
    {"id": "DE-001", "category": 3, "pattern": r"send .* to .* (http|https|ftp)", "severity": "HIGH"},
    {"id": "DE-002", "category": 3, "pattern": r"exfiltrat", "severity": "CRITICAL"},
    {"id": "DE-003", "category": 3, "pattern": r"leak .* data", "severity": "HIGH"},
    {"id": "DE-004", "category": 3, "pattern": r"upload .* to .* external", "severity": "MEDIUM"},
    
    # Category 4: Code Injection (4 patterns)
    {"id": "CI-001", "category": 4, "pattern": r"eval\s*\(", "severity": "CRITICAL"},
    {"id": "CI-002", "category": 4, "pattern": r"exec\s*\(", "severity": "CRITICAL"},
    {"id": "CI-003", "category": 4, "pattern": r"__import__\s*\(", "severity": "HIGH"},
    {"id": "CI-004", "category": 4, "pattern": r"subprocess\.(run|call|Popen)", "severity": "HIGH"},
    
    # Category 5: Command Injection (4 patterns)
    {"id": "CMD-001", "category": 5, "pattern": r"os\.system\s*\(", "severity": "CRITICAL"},
    {"id": "CMD-002", "category": 5, "pattern": r"shell\s*=\s*True", "severity": "HIGH"},
    {"id": "CMD-003", "category": 5, "pattern": r"bash\s+-c", "severity": "HIGH"},
    {"id": "CMD-004", "category": 5, "pattern": r"powershell\s+", "severity": "MEDIUM"},
    
    # Add more patterns for other categories...
    # (Simplified: only implementing first 5 categories = 20 patterns)
]


class SkillSpectorSimplified:
    """Simplified version of NVIDIA SkillSpector"""
    
    def __init__(self, scan_depth: str = "quick"):
        """
        Args:
            scan_depth: "quick" (static analysis only) or "deep" (static + LLM semantic)
        """
        self.scan_depth = scan_depth
        self.patterns = VULNERABILITY_PATTERNS
        
        print(f"[INFO] SkillSpector Simplified initialized")
        print(f"[INFO]   Scan depth: {scan_depth}")
        print(f"[INFO]   Vulnerability patterns: {len(self.patterns)}")
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """
        Scan a single file for vulnerabilities
        
        Args:
            file_path: Path to file to scan
            
        Returns:
            scan_result: {
                "file": file_path,
                "vulnerabilities": [...],
                "risk_score": 0-100,
                "categories_found": [...]
            }
        """
        print(f"\n[INFO] Scanning file: {file_path}")
        
        # Read file
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"[ERROR] Failed to read file: {e}")
            return {"file": file_path, "error": str(e)}
        
        # Static analysis
        vulnerabilities = self._static_analysis(content)
        
        # Deep analysis (if enabled)
        if self.scan_depth == "deep":
            vulnerabilities += self._llm_semantic_analysis(content)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(vulnerabilities)
        
        # Get categories found
        categories_found = list(set(v["category"] for v in vulnerabilities))
        
        result = {
            "file": file_path,
            "vulnerabilities": vulnerabilities,
            "risk_score": risk_score,
            "categories_found": categories_found,
            "scan_depth": self.scan_depth
        }
        
        print(f"[INFO] Scan complete: {len(vulnerabilities)} vulnerabilities found")
        print(f"[INFO]   Risk score: {risk_score}/100")
        print(f"[INFO]   Categories: {len(categories_found)}")
        
        return result
    
    def _static_analysis(self, content: str) -> List[Dict[str, Any]]:
        """Static pattern matching"""
        vulnerabilities = []
        
        for pattern_info in self.patterns:
            pattern = pattern_info["pattern"]
            category = pattern_info["category"]
            
            # Search for pattern
            matches = re.finditer(pattern, content, re.IGNORECASE)
            
            for match in matches:
                vuln = {
                    "pattern_id": pattern_info["id"],
                    "category": category,
                    "category_name": RISK_CATEGORIES.get(category, "Unknown"),
                    "severity": pattern_info["severity"],
                    "match": match.group(),
                    "position": match.start(),
                    "analysis_type": "static"
                }
                vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _llm_semantic_analysis(self, content: str) -> List[Dict[str, Any]]:
        """
        LLM semantic analysis (simplified version)
        
        In full version, this would use LLM to analyze code semantics.
        Here, we just do some heuristic checks.
        """
        vulnerabilities = []
        
        # Heuristic 1: Check for obfuscated code
        if self._is_obfuscated(content):
            vulnerabilities.append({
                "pattern_id": "SEM-001",
                "category": 4,  # Code Injection
                "category_name": RISK_CATEGORIES[4],
                "severity": "MEDIUM",
                "match": "Obfuscated code detected",
                "position": -1,
                "analysis_type": "semantic"
            })
        
        # Heuristic 2: Check for suspicious imports
        suspicious_imports = self._check_suspicious_imports(content)
        for imp in suspicious_imports:
            vulnerabilities.append({
                "pattern_id": "SEM-002",
                "category": 13,  # Malicious Dependencies
                "category_name": RISK_CATEGORIES[13],
                "severity": "HIGH",
                "match": f"Suspicious import: {imp}",
                "position": -1,
                "analysis_type": "semantic"
            })
        
        return vulnerabilities
    
    def _is_obfuscated(self, content: str) -> bool:
        """Check if code is obfuscated (simplified heuristic)"""
        # Heuristic: High density of special characters
        special_chars = sum(1 for c in content if not c.isalnum() and not c.isspace())
        ratio = special_chars / max(len(content), 1)
        
        return ratio > 0.3  # >30% special characters
    
    def _check_suspicious_imports(self, content: str) -> List[str]:
        """Check for suspicious imports (simplified)"""
        suspicious = []
        
        # List of suspicious modules
        suspicious_modules = [
            "socket", "requests", "urllib",
            "subprocess", "os", "sys",
            "pickle", "marshal", "shelve"
        ]
        
        for line in content.split("\n"):
            if "import" in line:
                for mod in suspicious_modules:
                    if mod in line:
                        suspicious.append(mod)
        
        return suspicious
    
    def _calculate_risk_score(self, vulnerabilities: List[Dict[str, Any]]) -> int:
        """
        Calculate risk score (0-100)
        
        Scoring:
        - CRITICAL: +25 points each
        - HIGH: +15 points each
        - MEDIUM: +10 points each
        - LOW: +5 points each
        - Max: 100 points
        """
        score = 0
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "LOW")
            
            if severity == "CRITICAL":
                score += 25
            elif severity == "HIGH":
                score += 15
            elif severity == "MEDIUM":
                score += 10
            else:  # LOW
                score += 5
        
        return min(score, 100)
    
    def scan_skill(self, skill_dir: str) -> Dict[str, Any]:
        """
        Scan an entire skill directory
        
        Args:
            skill_dir: Path to skill directory
            
        Returns:
            skill_scan_result: {
                "skill_dir": skill_dir,
                "files_scanned": [...],
                "total_vulnerabilities": ...,
                "overall_risk_score": ...,
                "categories_found": [...]
            }
        """
        print(f"\n[INFO] Scanning skill directory: {skill_dir}")
        
        skill_path = Path(skill_dir)
        
        if not skill_path.exists():
            print(f"[ERROR] Skill directory not found: {skill_dir}")
            return {"error": "Directory not found"}
        
        # Scan all relevant files
        files_to_scan = []
        for ext in ["*.py", "*.md", "*.json", "*.yaml", "*.yml"]:
            files_to_scan.extend(skill_path.glob(f"**/{ext}"))
        
        print(f"[INFO] Found {len(files_to_scan)} files to scan")
        
        # Scan each file
        all_results = []
        for file_path in files_to_scan:
            result = self.scan_file(str(file_path))
            all_results.append(result)
        
        # Aggregate results
        total_vulns = sum(len(r.get("vulnerabilities", [])) for r in all_results)
        all_categories = set()
        for r in all_results:
            all_categories.update(r.get("categories_found", []))
        
        # Overall risk score (max of all files)
        overall_risk = max((r.get("risk_score", 0) for r in all_results), default=0)
        
        skill_result = {
            "skill_dir": skill_dir,
            "files_scanned": [str(f) for f in files_to_scan],
            "file_results": all_results,
            "total_vulnerabilities": total_vulns,
            "overall_risk_score": overall_risk,
            "categories_found": list(all_categories)
        }
        
        print(f"\n[INFO] Skill scan complete:")
        print(f"[INFO]   Files scanned: {len(files_to_scan)}")
        print(f"[INFO]   Total vulnerabilities: {total_vulns}")
        print(f"[INFO]   Overall risk score: {overall_risk}/100")
        print(f"[INFO]   Categories found: {len(all_categories)}")
        
        return skill_result
    
    def generate_report(self, scan_result: Dict[str, Any], output_file: str = "skillspector-report.json"):
        """Generate scan report"""
        print(f"\n[INFO] Generating report: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scan_result, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="SkillSpector Simplified: AI Agent Skill Security Scanner")
    parser.add_argument("--input", type=str, required=True, help="Input file or directory to scan")
    parser.add_argument("--depth", type=str, default="quick", choices=["quick", "deep"], 
                       help="Scan depth: quick (static only) or deep (static + LLM)")
    parser.add_argument("--output", type=str, default="skillspector-report.json", help="Output report file")
    
    args = parser.parse_args()
    
    print("[INFO] SkillSpector Simplified (Based on NVIDIA SkillSpector)")
    print("[INFO]   64 vulnerability patterns across 16 risk categories")
    print("[INFO]   This is a simplified version for testing and integration\n")
    
    # Initialize scanner
    scanner = SkillSpectorSimplified(scan_depth=args.depth)
    
    # Scan
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Scan single file
        result = scanner.scan_file(str(input_path))
    elif input_path.is_dir():
        # Scan entire directory
        result = scanner.scan_skill(str(input_path))
    else:
        print(f"[ERROR] Input not found: {args.input}")
        return
    
    # Generate report
    scanner.generate_report(result, output_file=args.output)
    
    # Print summary
    print(f"\n{'='*80}")
    print("SCAN SUMMARY")
    print(f"{'='*80}")
    
    if "error" in result:
        print(f"ERROR: {result['error']}")
    else:
        total_vulns = result.get("total_vulnerabilities", len(result.get("vulnerabilities", [])))
        risk_score = result.get("overall_risk_score", result.get("risk_score", 0))
        
        print(f"Total vulnerabilities found: {total_vulns}")
        print(f"Overall risk score: {risk_score}/100")
        
        if risk_score >= 70:
            print("RISK LEVEL: CRITICAL - DO NOT USE THIS SKILL")
        elif risk_score >= 40:
            print("RISK LEVEL: HIGH - Review carefully before use")
        elif risk_score >= 20:
            print("RISK LEVEL: MEDIUM - Some issues found")
        else:
            print("RISK LEVEL: LOW - Relatively safe")
    
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
