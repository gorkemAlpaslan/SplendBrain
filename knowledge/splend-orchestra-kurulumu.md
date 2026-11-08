# SplendOrchestra Kurulum ve Senkronizasyon Rehberi

Bu not, **SplendOrchestra** (Seviye 5 & 6 Ekip Lideri) skill'inin Windows veya yeni bir bilgisayara tek komutla kurulması için referans rehberdir.

## Skill Dosyaları Nerede?
Kaynak dosyalar bu kasanın içinde güvenle saklanmaktadır:
- `.agents/skills/splend-orchestra/SKILL.md`
- `.agents/skills/splend-orchestra/agents/openai.yaml`
- `.agents/skills/splend-orchestra/install_splend_orchestra.py`

## Kurulum Komutu (Windows & macOS Çapraz Platform)
Windows bilgisayarınızda Beyin (SplendBrain) açıkken terminalde şu komutu çalıştırmak yeterlidir:

```bash
python .agents/skills/splend-orchestra/install_splend_orchestra.py
```

Bu script otomatik olarak:
1. Windows kullanıcınızın `%USERPROFILE%\.codex\skills\splend-orchestra\` dizinine dosyaları kopyalar ve UI kartını (`openai.yaml`) ekler.
2. Windows kullanıcınızın `%USERPROFILE%\.gemini\config\skills\splend-orchestra\` dizinine Antigravity skill'ini kopyalar.
3. `%USERPROFILE%\.codex\AGENTS.md` dosyasına isteğe bağlı çağırma kuralını ekler.

