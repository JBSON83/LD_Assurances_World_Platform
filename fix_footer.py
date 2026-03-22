import os
import re

directories = [
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web",
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web\products",
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web\en",
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web\en\products"
]

# Pattern: detects a <h4>Légal</h4> followed by two <p> blocks (one with NIU, second with legal links)
# We want to merge them into a single <p>
PATTERN = re.compile(
    r'(<h4>Légal</h4>\s*)'
    r'<p>(NIU:.*?)</p>'
    r'\s*<p>\s*'
    r'(<a href="[^"]*politique[^"]*"[^>]*>Politique de confidentialité</a><br>\s*\n?\s*<a href="[^"]*mentions[^"]*"[^>]*>Mentions Légales.*?</a>)'
    r'\s*</p>',
    re.DOTALL
)

def build_replacement(prefix, niu_content, links_html):
    return (
        f'{prefix}'
        f'<p>{niu_content}<br><br>\n'
        f'                        {links_html}\n'
        f'                    </p>'
    )

fixed = 0
for d in directories:
    if not os.path.exists(d):
        continue
    for f in os.listdir(d):
        if not f.endswith(".html"):
            continue
        path = os.path.join(d, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        
        # Determine relative prefix based on depth
        d_unix = d.replace("\\", "/")
        if d_unix.endswith("en/products"): prefix = "../../"
        elif d_unix.endswith("web/products") or d_unix.endswith("web/en"): prefix = "../"
        else: prefix = ""

        def replacer(m):
            h4_part = m.group(1)
            niu_part = m.group(2)
            links_part = m.group(3)
            # Rebuild links with colored style and relative prefix
            links_clean = re.sub(r'href="([^"]*politique[^"]*)"', f'href="{prefix}politique-confidentialite.html"', links_part)
            links_clean = re.sub(r'href="([^"]*mentions[^"]*)"', f'href="{prefix}mentions-legales.html"', links_clean)
            # Ensure color is set to primary green
            links_clean = re.sub(r'style="[^"]*"', 'style="color: var(--primary, #10b981); text-decoration: none;"', links_clean)
            return f'{h4_part}<p>{niu_part}<br><br>\n                        {links_clean}\n                    </p>'
        
        new_content = PATTERN.sub(replacer, content)
        if new_content != content:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_content)
            fixed += 1
            print(f"  ✓ Fixed: {path}")

print(f"\n✅ Done. Fixed {fixed} files.")
