---
name: beyin-skill-sync
description: >-
  SplendBrain (Beyin) ile yerel Codex ve Antigravity ortamları arasındaki skill'leri senkronize et. Yeni eklenen, güncellenen veya eksik olan skill'leri tespit edip çift yönlü olarak eşitler. Kullanıcı skill senkronizasyonu, kontrolü veya Windows/Mac geçişi istediğinde kullan.
---

# Beyin Skill Sync (`beyin-skill-sync`)

Bu skill, **SplendBrain (Beyin)** kasasını merkezi referans kütüphanesi olarak kullanarak yerel sistemdeki (`~/.codex/skills` ve `~/.gemini/config/skills` ya da Windows karşılıkları) skill'leri senkronize eder.

## Ne Zaman Kullanılır?
- Windows'tan Mac'e veya Mac'ten Windows'a geçtiğinizde.
- Codex veya Antigravity'ye yeni bir skill eklediğinizde ya da bir skill'i güncellediğinizde.
- "Skill'leri eşitle", "Skill sync yap", "Brain ile senkronize et" denildiğinde.

## Çalıştırma Komutu

Vault kökündeki `skill_sync.py` betiğini çalıştır:

```bash
# macOS / Linux:
python3 skill_sync.py

# Windows:
py -3 skill_sync.py
```

Sadece kontrol edip değişiklikleri görmek için `--check` parametresi verilebilir:
```bash
python3 skill_sync.py --check
```

## Senkronizasyon Mantığı
1. **Beyin'de Var, Yerelde Yok:** Beyin'den yerel Codex ve Antigravity dizinlerine otomatik kurulur.
2. **Yerelde Yeni Bir Skill Var, Beyin'de Yok:** Yereldeki yeni skill otomatik olarak Beyin'e kopyalanır ve korunur.
3. **Her İki Tarafta da Var Ama İçerik Farklı:** Dosya SHA-256 hash'lerine ve son değiştirilme zamanına (`mtime`) bakılarak en güncel sürüm diğer tarafa aktarılır.

