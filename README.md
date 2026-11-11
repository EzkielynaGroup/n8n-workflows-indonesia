# n8n Workflows Indonesia

Empat workflow [n8n](https://n8n.io) siap impor untuk UMKM dan developer Indonesia: CS toko di Telegram, ringkas PDF ke Google Sheets, draf balasan email, dan API terjemahan. Semua prompt dan catatan dalam Bahasa Indonesia.

Workflow memakai node **OpenAI Chat Model** dengan **Base URL kustom**, jadi bisa dipakai dengan penyedia apa pun yang kompatibel dengan format OpenAI. Contoh default: `https://api.ezkielyna.store/v1` dengan model `deepseek-v4.1-flash`.

> English: four importable n8n workflows (Telegram shop assistant, PDF summary to Google Sheets, Gmail reply drafts, translation webhook) with Indonesian prompts. They use the OpenAI Chat Model node with a custom base URL, so any OpenAI-compatible provider works.

| File | Isi | Node utama |
|---|---|---|
| [`01-cs-toko-telegram.json`](workflows/01-cs-toko-telegram.json) | Bot CS toko di Telegram yang menjawab dari data toko dan ingat 6 pesan terakhir per chat | Telegram Trigger, AI Agent, Simple Memory |
| [`02-ringkas-pdf-ke-google-sheets.json`](workflows/02-ringkas-pdf-ke-google-sheets.json) | Form unggah PDF → ringkasan 5 poin + tindak lanjut → satu baris di Google Sheets | n8n Form, Extract from File, Basic LLM Chain, Google Sheets |
| [`03-draf-balasan-email-gmail.json`](workflows/03-draf-balasan-email-gmail.json) | Email baru → AI menulis **draf** balasan di thread yang sama (tidak terkirim otomatis); promosi dan notifikasi dilewati | Gmail Trigger, Basic LLM Chain, If, Gmail |
| [`04-api-terjemahan-webhook.json`](workflows/04-api-terjemahan-webhook.json) | Endpoint `POST /webhook/terjemah` dengan header kunci, mengembalikan `{"terjemahan": "..."}` | Webhook, Basic LLM Chain, Respond to Webhook |

Setiap workflow punya **sticky note** berisi langkah setup di kanvasnya.

## Cara impor

Semua tipe node dan versinya sudah dicek tersedia di **n8n 2.47** (November 2026). Kalau n8n Anda jauh lebih lama, perbarui dulu.

1. Buka n8n → **Workflows** → **Create workflow**.
2. Klik menu **⋯** (kanan atas) → **Import from File**, pilih file `.json` dari folder [`workflows/`](workflows). Bisa juga salin isi file lalu tempel (Ctrl+V / Cmd+V) di kanvas kosong.
3. Buat credential **OpenAI** (sekali saja, dipakai semua workflow):
   - **API Key**: key dari penyedia kamu (`sk-...`)
   - **Base URL**: alamat API penyedia yang kompatibel dengan OpenAI, misalnya `https://api.ezkielyna.store/v1`
4. Buka node **OpenAI Chat Model** di workflow, pilih credential tadi. Model diisi lewat mode **ID** (`deepseek-v4.1-flash`); ganti dengan nama model lain dari penyedia kamu kalau perlu.
5. Lengkapi credential lain yang diminta workflow (Telegram, Google Sheets, Gmail, atau Header Auth), lalu ikuti sticky note.
6. Klik **Test workflow** untuk mencoba, lalu aktifkan.

Credential di file hanya berupa **nama**, tanpa key. Saat impor, n8n akan meminta kamu memilih atau membuat credential sendiri.

Catatan versi: dibuat untuk n8n versi baru (rilis 2025 ke atas). Kalau ada node yang muncul sebagai "unknown" atau "?", update n8n dulu.

## Tips

- **Maximum Number of Tokens** di node OpenAI Chat Model sudah diisi (400 sampai 2.000). Ini pengaman biaya, jangan dihapus.
- Saat menguji, **pin** output node yang sudah berhasil supaya tidak memanggil AI (dan membayar) berulang kali.
- Workflow PDF memotong teks di 40.000 karakter (±20 halaman). PDF hasil scan berupa gambar tidak punya teks dan perlu OCR dulu.
- Workflow email hanya membuat **draf**. Kalau ingin terkirim otomatis, ubah node Gmail ke operasi **Reply**, tapi uji dulu beberapa hari dengan draf.
- Webhook terjemahan memakai **Header Auth**. Jangan hapus, atau siapa pun yang tahu URL-nya bisa memakai saldo API kamu.
- Bot Telegram butuh n8n yang bisa diakses lewat HTTPS (n8n Cloud, VPS dengan domain, atau tunnel).
- Untuk WhatsApp: ganti Telegram Trigger dan node Telegram dengan **WhatsApp Trigger** dan **WhatsApp Business Cloud** (butuh akun WhatsApp Cloud API dari Meta). Alternatif dalam Python: [EzkielynaGroup/bot-wa-ai-starter](https://github.com/EzkielynaGroup/bot-wa-ai-starter).

## Perkiraan biaya per bulan

Biaya AI dihitung per token dari saldo API. Perkiraan berikut memakai `deepseek-v4.1-flash` di Ezkielyna API dengan harga per 11 November 2026; penyedia dan model lain akan berbeda:

| Workflow | Pemakaian | Perkiraan biaya AI |
|---|---|---|
| CS toko Telegram | 100 pesan/hari | ±Rp3.000 sampai Rp7.000/bulan |
| Ringkas PDF | 20 dokumen 10 halaman/hari | ±Rp3.700/bulan |
| Draf balasan email | 100 email/hari | ±Rp5.000/bulan |
| API terjemahan | 10.000 kata/hari | ±Rp1.400/bulan |

Ini perkiraan, bukan janji: biaya naik kalau prompt sistem panjang, dokumen tebal, atau model lebih mahal. Perhitungan lengkap dan harga live: [biaya AI untuk otomasi n8n](https://ezkielyna.store/biaya/otomasi-n8n?utm_source=github&utm_medium=readme&utm_campaign=n8n-workflows-indonesia), [ringkas dokumen](https://ezkielyna.store/biaya/ringkas-dokumen-pdf?utm_source=github&utm_medium=readme&utm_campaign=n8n-workflows-indonesia), [bot WhatsApp/Telegram](https://ezkielyna.store/biaya/bot-whatsapp-telegram?utm_source=github&utm_medium=readme&utm_campaign=n8n-workflows-indonesia), [terjemahan](https://ezkielyna.store/biaya/terjemahan?utm_source=github&utm_medium=readme&utm_campaign=n8n-workflows-indonesia).

Di luar biaya AI ada biaya **hosting n8n** (n8n Cloud atau VPS sendiri) dan, untuk WhatsApp, tagihan Meta. Telegram, Gmail, dan Google Sheets tidak menagih untuk pemakaian seperti ini.

## Memakai Ezkielyna API (opsional)

Workflow ini bekerja dengan penyedia mana pun. Kalau ingin memakai contoh default:

1. Beli API Credit di [ezkielyna.store](https://ezkielyna.store/beli-api-key?utm_source=github&utm_medium=readme&utm_campaign=n8n-workflows-indonesia), mulai $0.5, bayar QRIS, DANA, GoPay, atau USDT.
2. Tukarkan kodenya di menu **Wallet** di [api.ezkielyna.store](https://api.ezkielyna.store), lalu buat key di **API Keys** (grup **Standard** cukup untuk `deepseek-v4.1-flash`).
3. Panduan n8n bergambar: [ezkielyna.store/panduan/n8n](https://ezkielyna.store/panduan/n8n?utm_source=github&utm_medium=readme&utm_campaign=n8n-workflows-indonesia).

## Kontribusi

Punya workflow lain yang berguna untuk UMKM? Kirim pull request: simpan file di `workflows/` dengan nomor berikutnya, hapus semua credential id dan data pribadi, lalu jalankan:

```bash
python3 scripts/validate.py
```

Lebih banyak tips: [EzkielynaGroup/tips-ai-indonesia](https://github.com/EzkielynaGroup/tips-ai-indonesia).

## Lisensi

MIT. n8n adalah merek milik n8n GmbH; repo ini tidak berafiliasi dengan n8n.
