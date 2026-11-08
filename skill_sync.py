#!/usr/bin/env python3
"""
SplendBrain (Beyin) İki Yönlü Skill Eşitleyici (Cross-Platform: Windows & macOS)

Ne Yapar?
1. Yerel sistemdeki (~/.codex/skills ve ~/.gemini/config/skills) ile Beyin içindeki
   (.agents/skills/) tüm skill'leri karşılaştırır.
2. Karşılaştırma Mantığı:
   - Beyin'de olup yerelde olmayan skill varsa -> Yerel ortama kurar.
   - Yerelde olup Beyin'de olmayan yeni bir skill varsa -> Beyin'e ekler.
   - Her iki tarafta olup içeriği değişmiş olan skill varsa -> Değişiklikleri eşitler (en güncel olanı yansıtır).
3. Çıktı: İnsan tarafından okunabilir temiz bir senkronizasyon raporu sunar.
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path

IGNORE_NAMES = {'.system', '.git', '.DS_Store', '__pycache__', '.pytest_cache'}

def get_paths(vault_dir: Path):
    home = Path.home()
    codex_skills = home / ".codex" / "skills"
    gemini_skills = home / ".gemini" / "config" / "skills"
    beyin_skills = vault_dir / ".agents" / "skills"
    return codex_skills, gemini_skills, beyin_skills

def file_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_skill_snapshot(skill_dir: Path) -> dict:
    snapshot = {}
    if not skill_dir.exists():
        return snapshot
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_NAMES]
        for f in files:
            if f in IGNORE_NAMES or f.startswith('.'):
                continue
            p = Path(root) / f
            rel = p.relative_to(skill_dir).as_posix()
            snapshot[rel] = {
                "hash": file_sha256(p),
                "mtime": p.stat().st_mtime,
                "path": p
            }
    return snapshot

def sync_skills(vault_dir: Path, apply: bool = True):
    codex_skills, gemini_skills, beyin_skills = get_paths(vault_dir)
    beyin_skills.mkdir(parents=True, exist_ok=True)
    codex_skills.mkdir(parents=True, exist_ok=True)
    gemini_skills.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("🧠 SplendBrain Skill Senkronizasyonu (Skill-Sync)")
    print(f"Platform: {sys.platform} | Mod: {'Uygula' if apply else 'Sadece Raporla (Dry-Run)'}")
    print("=" * 65)

    # Bütün skill adlarını topla
    all_skill_names = set()
    for d in [beyin_skills, codex_skills, gemini_skills]:
        if d.exists():
            for p in d.iterdir():
                if p.is_dir() and p.name not in IGNORE_NAMES:
                    all_skill_names.add(p.name)

    actions = []

    for name in sorted(all_skill_names):
        b_dir = beyin_skills / name
        c_dir = codex_skills / name
        g_dir = gemini_skills / name

        b_snap = get_skill_snapshot(b_dir)
        c_snap = get_skill_snapshot(c_dir)
        g_snap = get_skill_snapshot(g_dir)

        # 1. Beyin'de var ama yerelde yoksa -> Beyin'den yerel ortama kopyala
        if b_snap and not c_snap:
            actions.append((f"[YENİ -> CODEX] '{name}' skill'i Beyin'den Codex'e kuruluyor", "b_to_local", b_dir, c_dir))
        if b_snap and not g_snap:
            actions.append((f"[YENİ -> ANTIGRAVITY] '{name}' skill'i Beyin'den Antigravity'ye kuruluyor", "b_to_local", b_dir, g_dir))

        # 2. Yerelde var ama Beyin'de yoksa -> Yerelden Beyin'e al
        if not b_snap and (c_snap or g_snap):
            src = c_dir if c_snap else g_dir
            actions.append((f"[YENİ -> BEYİN] '{name}' skill'i yerelden Beyin kütüphanesine yedekleniyor", "local_to_b", src, b_dir))

        # 3. Her iki tarafta da varsa içerik kontrolü
        if b_snap and (c_snap or g_snap):
            # SKILL.md karşılaştır
            for rel in ["SKILL.md", "agents/openai.yaml"]:
                b_file = b_snap.get(rel)
                c_file = c_snap.get(rel)
                g_file = g_snap.get(rel)

                target_locals = []
                if c_file: target_locals.append((c_file, c_dir / rel))
                if g_file and rel == "SKILL.md": target_locals.append((g_file, g_dir / rel))

                for loc_file, loc_path in target_locals:
                    if b_file and loc_file["hash"] != b_file["hash"]:
                        # Mtime'a göre en yenisini seç
                        if loc_file["mtime"] > b_file["mtime"]:
                            actions.append((f"[GÜNCELLEME -> BEYİN] '{name}/{rel}' yerelde daha yeni, Beyin'e aktarılıyor", "copy_file", loc_file["path"], b_dir / rel))
                        else:
                            actions.append((f"[GÜNCELLEME -> YEREL] '{name}/{rel}' Beyin'de daha yeni, yerel sisteme aktarılıyor", "copy_file", b_file["path"], loc_path))

    if not actions:
        print("✅ Tüm skill'ler tam senkronize! Hiçbir eksik veya fark bulunamadı.")
        print(f"Toplam kontrol edilen skill sayısı: {len(all_skill_names)}")
        return 0

    print(f"Tespit edilen işlem sayısı: {len(actions)}\n")
    for msg, kind, src, dst in actions:
        print(f"  • {msg}")
        if apply:
            if kind == "b_to_local" or kind == "local_to_b":
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif kind == "copy_file":
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    if apply:
        print("\n🎉 Senkronizasyon başarıyla tamamlandı!")
    return len(actions)

if __name__ == "__main__":
    vault = Path(__file__).resolve().parent
    apply_mode = "--check" not in sys.argv and "--dry-run" not in sys.argv
    sync_skills(vault, apply=apply_mode)
