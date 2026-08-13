import subprocess, datetime, os, json, sys

repo = r'D:\QClawX\data\workspace-ua58rsb93veqtxl7'
today = datetime.date.today().isoformat()
report_lines = []
all_ok = True

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', timeout=120)
    return r

# 1. git add .
r1 = run(['git', 'add', '.'], repo)
report_lines.append('[git add] rc=%s' % r1.returncode)
if r1.stderr:
    s = r1.stderr.strip()
    if s: report_lines.append('  stderr: ' + s[:200])

# 2. git status -s
r2 = run(['git', 'status', '-s'], repo)
changed = r2.stdout.strip()
cnt = len(changed.splitlines()) if changed else 0
report_lines.append('[git status] changed=%d' % cnt)
if changed:
    for line in changed.splitlines()[:15]:
        report_lines.append('  ' + line)
    if cnt > 15:
        report_lines.append('  ... (+%d more)' % (cnt - 15))

# 3. git commit (only if changes)
msg = 'Sync ' + today
r3 = run(['git', 'commit', '-m', msg], repo)
has_changes = 'nothing to commit' not in r3.stdout.lower() and 'nothing to commit' not in r3.stderr.lower()
commit_ok = (r3.returncode == 0 and has_changes) or 'nothing to commit' in r3.stdout.lower() or 'nothing to commit' in r3.stderr.lower()
report_lines.append('[git commit] rc=%s changed=%s' % (r3.returncode, has_changes))
if r3.stdout.strip(): report_lines.append('  stdout: ' + r3.stdout.strip()[:200])
if r3.stderr.strip(): report_lines.append('  stderr: ' + r3.stderr.strip()[:200])

# 4. git push
r4 = run(['git', 'push'], repo)
pushed = r4.returncode == 0
report_lines.append('[git push] rc=%s ok=%s' % (r4.returncode, pushed))
if r4.stdout.strip(): report_lines.append('  stdout: ' + r4.stdout.strip()[:300])
if r4.stderr.strip(): report_lines.append('  stderr: ' + r4.stderr.strip()[:200])

final_ok = pushed
report = '\n'.join(report_lines)

out = {}
out['date'] = today
out['changed_files'] = cnt
out['committed'] = has_changes or cnt == 0
out['pushed'] = pushed
out['report'] = report
out['success'] = final_ok

print('===REPORT_START===')
print(json.dumps(out, ensure_ascii=False, indent=2))
print('===REPORT_END===')

# Write JSON file for downstream scripts
json_file = os.path.join(repo, 'github_sync_report_%s.json' % today.replace('-', ''))
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print('JSON written to: ' + json_file)
