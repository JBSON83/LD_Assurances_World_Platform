import os
import re

directories = [
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web",
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web\products",
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web\en",
    r"c:\Users\diffo_jb\OneDrive\Documents\WorkflowAntigravity\LD_Assurances_World_Platform\web\en\products"
]

for d in directories:
    if not os.path.exists(d): 
        continue
    for f in os.listdir(d):
        if f.endswith(".html"):
            path = os.path.join(d, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Determine relative prefix based on depth
            d_unix = d.replace("\\", "/")
            if d_unix.endswith("en/products"): prefix = "../../"
            elif d_unix.endswith("web/products") or d_unix.endswith("web/en"): prefix = "../"
            else: prefix = ""

            # Check if pixel.js is loaded
            if "pixel.js" not in content:
                content = content.replace("</head>", f"    <script src=\"{prefix}pixel.js\"></script>\n</head>")
            
            # Replace Légal block in footer
            # We look for <h4>Légal</h4> then the next <p> block. We append our links immediately after. 
            # First, check if we already added it so we don't duplicate.
            if "politique-confidentialite.html" not in content:
                pattern = r"(<h4>Légal</h4>\s*<p>.*?)(</p>)"
                replacement = r'\1\2\n                    <p>\n                        <a href="' + prefix + r'politique-confidentialite.html" style="color: inherit; text-decoration: none;">Politique de confidentialité</a><br>\n                        <a href="' + prefix + r'mentions-legales.html" style="color: inherit; text-decoration: none;">Mentions Légales & CGU</a>\n                    </p>'
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)

            with open(path, "w", encoding="utf-8") as file:
                file.write(content)

print("✅ Updated all HTML files with pixel.js and legal footer links.")
