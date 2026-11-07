---
{
  "title": "Çoklu Cihaz (macOS & Windows) Git Senkronizasyonu",
  "kind": "fact",
  "visibility": "internal"
}
---
# Çoklu Cihaz (macOS & Windows) Git Senkronizasyonu

Görkem'in MacBook ve Windows bilgisayarı arasında İkinci Beyin V3 vault'u **`SplendBrain`** adlı **Private GitHub Reposu** (`https://github.com/gorkemAlpaslan/SplendBrain.git`) üzerinden eşitlenir.

## Önemli Noktalar
- **Gerçeklik Kaynağı:** Markdown dosyaları Git ile eşitlenir; yerel SQLite indeks (`memory.sqlite3`) her makinenin kendi sistem dizininde (macOS: `~/Library/Application Support/beyin-v3/`, Windows: `%LOCALAPPDATA%\beyin-v3\`) yaşar.
- **Makineye Özel Dosyalar (`.gitignore`):** `.beyin-runtime.json`, `.beyin-note-write/`, istemci yerel hook dosyaları (`.agents/hooks.json`, `.claude/settings.local.json`, `.codex/hooks.json`, `.kiro/hooks/beyin-v3.json`), adaptör dosyaları (`.opencode/plugins/beyin-v3.js`, `.omp/hooks/pre/beyin-v3.ts`, `.claude/hermes-plugin/__init__.py`) ve güncelleme kısayolları Git dışı tutulur.
- **Satır Sonu Koruması (`.gitattributes`):** Windows'ta `core.autocrlf=true` kaynaklı receipt byte/SHA-256 çakışmalarını önlemek için `receipts/** -text` kuralı tanımlıdır.
- **Proje Konumları ve Eşleşme:** macOS'te `/Users/gorkemderinalpaslan/Desktop/Projeler`, Windows'ta `C:\projects` kullanılır (ikisinin de içinde `AnexTour`/`anextour` ve `Kisisel`/`kisisel` alt klasörleri bulunur). Her makinede `beyin.py bridge` kendi yerel köküne (`--project-root`) kurulur; alt klasörlerdeki projeler kendi klasör isimleri üzerinden aynı hafıza kapsamına eşleşir.

## Gerekçe ve Sınırlar
- İki bilgisayarın aynı anda açık olmasını gerektirmemesi (Syncthing'e kıyasla) ve Obsidian'ı açık tutma zorunluluğu olmaması (Obsidian Sync'e kıyasla) nedeniyle Private GitHub Reposu seçilmiştir.

## Kaynaklar
- Kullanıcı beyanı ve kararı (2026-11-07)
- `🔮 850-Companion/Core.md`
- `knowledge/projeler-klasoru-duzeni.md`
- `.gitignore`, `.gitattributes`
