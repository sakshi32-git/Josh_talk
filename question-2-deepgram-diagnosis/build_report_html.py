import re
from pathlib import Path
from markdown_it import MarkdownIt

md_path = Path(r"c:\Users\SAKSHI\Contacts\Downloads\josh_talk_final\question-2-deepgram-diagnosis\Sakshi_Sonker_Report.md")
html_path = md_path.with_suffix(".html")

text = md_path.read_text(encoding="utf-8")

md = MarkdownIt("commonmark", {"breaks": True, "html": True}).enable("table")
body_html = md.render(text)

styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Deepgram Nova-3 Performance Report — Sakshi Sonker</title>
  <style>
    @media print {{
      body {{ font-size: 11pt; line-height: 1.45; }}
      h1 {{ page-break-before: avoid; }}
      table {{ page-break-inside: avoid; }}
      .no-print {{ display: none; }}
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      max-width: 900px;
      margin: 40px auto;
      padding: 0 30px;
      color: #1f2937;
      line-height: 1.6;
    }}
    h1, h2, h3, h4 {{
      color: #111827;
      font-weight: 700;
      margin-top: 1.6em;
      margin-bottom: 0.5em;
    }}
    h1 {{ font-size: 1.9rem; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }}
    h2 {{ font-size: 1.35rem; border-bottom: 1px solid #f3f4f6; padding-bottom: 6px; }}
    h3 {{ font-size: 1.15rem; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 0.92rem;
    }}
    th, td {{
      padding: 8px 12px;
      border: 1px solid #d1d5db;
      text-align: left;
    }}
    th {{
      background: #f9fafb;
      font-weight: 600;
    }}
    tr:nth-child(even) {{ background: #f9fafb; }}
    code {{
      background: #f3f4f6;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 0.88em;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}
    pre {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 14px;
      overflow-x: auto;
      font-size: 0.88em;
    }}
    blockquote {{
      border-left: 4px solid #3b82f6;
      padding-left: 14px;
      margin-left: 0;
      color: #4b5563;
      background: #eff6ff;
      padding-top: 6px;
      padding-bottom: 6px;
      border-radius: 0 4px 4px 0;
    }}
    hr {{
      border: 0;
      height: 1px;
      background: #e5e7eb;
      margin: 30px 0;
    }}
    .print-banner {{
      background: #e0f2fe;
      color: #0369a1;
      padding: 12px 16px;
      border-radius: 8px;
      margin-bottom: 24px;
      font-size: 0.9rem;
      border: 1px solid #bae6fd;
    }}
  </style>
</head>
<body>
  <div class="print-banner no-print">
    📄 <strong>PDF Ready:</strong> Open this page in your browser and press <code>Ctrl + P</code> (or Cmd + P) &rarr; "Save as PDF" to generate <code>Sakshi_Sonker_Report.pdf</code>.
  </div>
  {body_html}
</body>
</html>
"""

html_path.write_text(styled_html, encoding="utf-8")
print(f"Generated clean HTML report at: {html_path}")

