#!/usr/bin/env python3
"""
SplendOrchestra Installer (Cross-Platform: Windows, macOS, Linux)
Kurulum Yeri: Beyin / SplendBrain
Kullanım:
    python install_splend_orchestra.py
"""

import os
import sys
import shutil
from pathlib import Path

def get_target_dirs():
    home = Path.home()
    codex_skill_dir = home / ".codex" / "skills" / "splend-orchestra"
    gemini_skill_dir = home / ".gemini" / "config" / "skills" / "splend-orchestra"
    return codex_skill_dir, gemini_skill_dir

def install():
    script_dir = Path(__file__).resolve().parent
    source_skill = script_dir / "SKILL.md"
    source_yaml = script_dir / "agents" / "openai.yaml"

    if not source_skill.exists():
        print(f"[HATA] Kaynak SKILL.md bulunamadı: {source_skill}")
        sys.exit(1)

    codex_dir, gemini_dir = get_target_dirs()

    print("=" * 60)
    print("🎼 SplendOrchestra Otomatik Kurulum Aracı")
    print(f"İşletim Sistemi: {sys.platform} ({os.name})")
    print("=" * 60)

    # 1. Codex Kurulumu
    codex_dir.mkdir(parents=True, exist_ok=True)
    (codex_dir / "agents").mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_skill, codex_dir / "SKILL.md")
    if source_yaml.exists():
        shutil.copy2(source_yaml, codex_dir / "agents" / "openai.yaml")
    print(f"[OK] Codex Skill kuruldu: {codex_dir}")

    # 2. Antigravity Kurulumu
    gemini_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_skill, gemini_dir / "SKILL.md")
    print(f"[OK] Antigravity Skill kuruldu: {gemini_dir}")

    # 3. AGENTS.md Kontrolü / Güncellemesi (Codex için tercih)
    codex_agents_md = Path.home() / ".codex" / "AGENTS.md"
    preference_text = "\n# Çalışma tercihi\n\nOrchestration otomatik çalıştırılmaz. Yalnız kullanıcı `/` menüsünden SplendOrchestra (`$splend-orchestra`) skill’ini açıkça çağırdığında uygulanır. Bu tercih önceki otomatik orchestration talimatlarının yerine geçer.\n"
    
    if codex_agents_md.exists():
        content = codex_agents_md.read_text(encoding="utf-8")
        if "splend-orchestra" not in content and "SplendOrchestra" not in content:
            with open(codex_agents_md, "a", encoding="utf-8") as f:
                f.write(preference_text)
            print(f"[OK] ~/.codex/AGENTS.md güncellendi.")
    else:
        codex_agents_md.parent.mkdir(parents=True, exist_ok=True)
        codex_agents_md.write_text(preference_text.strip() + "\n", encoding="utf-8")
        print(f"[OK] ~/.codex/AGENTS.md oluşturuldu.")

    print("=" * 60)
    print("🎉 SplendOrchestra hem Codex hem Antigravity için başarıyla kuruldu!")
    print("Kullanım: Arayüzde /splend-orchestra veya $splend-orchestra yazmanız yeterlidir.")
    print("=" * 60)

if __name__ == "__main__":
    install()
