# 📋 Plan: Dashboard Visualisasi Timeline Kantor BPS Kabupaten Buton Utara 2026

## Ringkasan Proyek

**Nama App:** `bps-timeline-dashboard.html`  
**Tipe:** Web Statis Satu File (Static HTML/CSS/JS)  
**Target Pengguna:** Koordinator Tim & Kepala BPS Kab. Buton Utara  
**Tujuan:** Visualisasi interaktif jadwal tahunan seluruh tim kerja BPS 2026 dalam satu tampilan terpadu — menggantikan empat file Excel terpisah dengan antarmuka yang dapat di-filter, di-zoom, dan di-eksplorasi secara visual.

***

## 1. Sumber Data

Data dikonsumsi langsung dari file Excel yang sudah distandarisasi. Karena ini web statis, data Excel akan dikonversi menjadi objek JavaScript inline (`const DATA = [...]`) di dalam `<script>` tag.

| File Sumber | Tim | Path |
|---|---|---|
| `Timeline_Bulanan_Kegiatan_Sosial_2026_.xlsx` | Tim Statistik Sosial | `C:\...\Timline-fix\` |
| `Timeline_Bulanan_Kegiatan_Produksi_2026.xlsx` | Tim Statistik Produksi | `C:\...\Timline-fix\` |
| `Timeline_Bulanan_Tim_Umum_2026.xlsx` | Tim Umum | `C:\...\Timline-fix\` |
| `Timeline_Bulanan_Nerwilis_2026.xlsx` | Tim Nerwilis | `C:\...\Timline-fix\` |

> ⚙️ **Konversi Data:** Gunakan skrip Python `convert_to_js.py` (dibuat terpisah) untuk membaca keempat Excel dan mengekspor data ke `data.js` yang di-embed langsung ke HTML.

***

## 2. Arsitektur Halaman

### Struktur Satu File

```
bps-timeline-dashboard.html
├── <head>
│   ├── Meta & title
│   ├── Font CDN (Satoshi + Inter Mono)
│   └── <style> — semua CSS inline
├── <body>
│   ├── #sidebar         — navigasi tim + filter
│   ├── #topbar          — judul, bulan-picker, dark mode toggle
│   ├── #main
│   │   ├── #kpi-strip   — 4 kartu KPI ringkasan
│   │   ├── #heatmap     — heat map beban kerja per minggu
│   │   ├── #gantt       — Gantt chart utama (semua tim)
│   │   └── #detail-panel — panel detail kegiatan (slide dari kanan)
│   └── <script>         — semua JS inline + data embed
```

***

## 3. Fitur Utama

### 3.1 KPI Strip (Baris Atas)
Empat kartu ringkasan yang otomatis terhitung:

| Kartu | Metrik |
|---|---|
| 🗓 Total Kegiatan | Jumlah seluruh baris kegiatan aktif 2026 |
| 📅 Bulan Tersibuk | Bulan dengan jumlah kegiatan terbanyak |
| 🔥 Tim Terpadat | Tim dengan beban minggu aktif terbanyak |
| ⚠️ Tumpang Tindih | Jumlah minggu di mana ≥3 tim aktif sekaligus |

### 3.2 Heat Map Beban Kerja
- Sumbu X: W1–W53 (53 minggu)
- Sumbu Y: 4 Tim (Sosial, Produksi, Umum, Nerwilis)
- Warna: intensitas hijau teal → semakin gelap = semakin banyak kegiatan di minggu itu
- Hover: tooltip menampilkan daftar kegiatan di minggu tersebut
- Klik: membuka panel detail

### 3.3 Gantt Chart Interaktif
- Setiap baris = satu kegiatan dari salah satu tim
- Blok horizontal berwarna sesuai tim (4 warna kategorikal)
- Filter sidebar:
  - [ ] Semua Tim ← default
  - [ ] Tim Sosial
  - [ ] Tim Produksi
  - [ ] Tim Umum
  - [ ] Tim Nerwilis
- Filter tambahan: dropdown Bulan (Januari–Desember)
- Search bar: cari nama kegiatan
- Zoom: Tampilan Tahunan / Triwulanan / Bulanan

### 3.4 Panel Detail (Slide-in dari Kanan)
Muncul saat user mengklik kegiatan di Gantt atau sel di Heat Map:
- Nama kegiatan + Program induk
- Tim penanggung jawab (badge berwarna)
- Jadwal: rentang minggu aktif + deskripsi teks
- Indikator tumpang tindih: "Minggu ini ada X kegiatan dari tim lain"

### 3.5 Mode Tampilan
Tombol toggle di topbar:
- **Timeline View** (default): Gantt chart horizontal
- **Calendar View**: grid bulan × minggu, setiap sel berisi chip kegiatan

***

## 4. Desain Visual

### Palet Warna

**Basis:** Nexus Design System (warm beige surfaces, teal primary)

```
Background:   #f7f6f2   (krem hangat)
Surface:      #f9f8f5
Text:         #28251d
Text muted:   #7a7974
```

**Warna per Tim (Kategorikal):**

| Tim | Warna | Hex |
|---|---|---|
| Tim Sosial | Teal (primary) | `#01696f` |
| Tim Produksi | Biru | `#006494` |
| Tim Nerwilis | Ungu | `#7a39bb` |
| Tim Umum | Oranye hangat | `#da7101` |

**Dark Mode:** Full dark mode support via `[data-theme="dark"]` toggle.

### Tipografi

```css
--font-display: 'Satoshi', sans-serif;   /* Heading, label */
--font-body:    'Satoshi', sans-serif;   /* Body text */
--font-mono:    'JetBrains Mono', monospace;  /* Nomor minggu, KPI angka */
```

CDN:
```html
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
```

### Logo & Identitas

SVG logo inline: stilisasi ikon grafik Gantt + inisial "BPS" dengan aksen warna teal. Ditempatkan di pojok kiri sidebar.

***

## 5. Layout & Responsivitas

### Desktop (≥1024px)
```
┌──────────┬──────────────────────────────────────┐
│          │ TOPBAR: Judul + Bulan Picker + Toggle │
│ SIDEBAR  ├──────────────────────────────────────┤
│ (240px)  │ KPI STRIP (4 kartu sejajar)           │
│          ├──────────────────────────────────────┤
│ Filter   │ HEAT MAP                              │
│ Tim      ├──────────────────────────────────────┤
│ Bulan    │ GANTT CHART (main scrollable area)   │
│ Zoom     │                                      │
│          │                                      │
└──────────┴──────────────────────────────────────┘
```

### Mobile (≤768px)
- Sidebar collapse → hamburger menu
- KPI strip → 2×2 grid
- Gantt chart → horizontal scroll dengan sticky nama kolom
- Heat map → scale 50% + pinch zoom

***

## 6. Interaktivitas (JavaScript)

```javascript
// State yang dikelola in-memory (no localStorage)
const state = {
  activeTeams: ['sosial', 'produksi', 'umum', 'nerwilis'],
  activeMonth: 'all',    // 'all' | 'januari' | ... | 'desember'
  zoomLevel: 'yearly',   // 'yearly' | 'quarterly' | 'monthly'
  viewMode: 'gantt',     // 'gantt' | 'calendar'
  selectedItem: null,    // kegiatan yang sedang dipilih
  searchQuery: '',
  theme: 'light'         // 'light' | 'dark'
};
```

**Event Listeners:**
- Filter checkbox → re-render Gantt
- Bulan dropdown → scroll Gantt ke kolom bulan terpilih + highlight
- Search input → filter rows secara real-time (debounced 300ms)
- Gantt row click → buka detail panel
- Gantt header (nama bulan) click → zoom ke tampilan bulanan
- Keyboard: `Escape` tutup panel detail, `←/→` navigasi bulan

***

## 7. Animasi & Transisi

| Elemen | Animasi |
|---|---|
| KPI angka | Count-up dari 0 saat halaman pertama load (800ms) |
| Heat map cells | Fade-in staggered dari kiri ke kanan (20ms delay per kolom) |
| Gantt bars | Slide masuk dari kiri (600ms cubic-bezier) |
| Detail panel | Slide dari kanan (300ms ease-out) |
| Filter toggle | Gantt rows fade out/in saat filter berubah (200ms) |
| Dark mode toggle | Color transition seluruh halaman (200ms) |

Semua animasi dihormati oleh `prefers-reduced-motion`.

***

## 8. Komponen SVG Heat Map (Opsional Tambahan)

Selain Gantt chart, heat map 2D menggunakan SVG+JS murni:

```
          Jan  Feb  Mar  Apr  ...  Des
Sosial  [  ■   ■    ■    ■         ■  ]
Produksi[      ■    ■              ■  ]
Umum    [  ■   ■    ■    ■    ■    ■  ]
Nerwilis[            ■   ■              ]
```

Setiap sel `<rect>` diberi warna berdasarkan jumlah kegiatan aktif di minggu itu. Tooltip muncul saat hover dengan daftar nama kegiatan.

***

## 9. Struktur Data JavaScript (Embed)

```javascript
const TIMELINE_DATA = [
  {
    id: 1,
    tim: "sosial",
    program: "Sakernas Agustus 2026",
    kegiatan: "Listing dan Pemutakhiran SP2020",
    jadwal_teks: "Maret M1 - Maret M3",
    minggu_aktif: [9, 10, 11]
  },
  // ... baris berikutnya
];

const TIM_META = {
  sosial:   { label: "Tim Statistik Sosial",    color: "#01696f" },
  produksi: { label: "Tim Statistik Produksi",  color: "#006494" },
  nerwilis: { label: "Tim Nerwilis",             color: "#7a39bb" },
  umum:     { label: "Tim Umum",                color: "#da7101" }
};
```

***

## 10. Skrip Konversi Data

File pendukung `convert_to_js.py` yang perlu dibuat terpisah:

```python
# Membaca 4 file Excel → menghasilkan data_embed.js
import pandas as pd
import json

files = {
    "sosial":   "Timeline_Bulanan_Kegiatan_Sosial_2026_.xlsx",
    "produksi": "Timeline_Bulanan_Kegiatan_Produksi_2026.xlsx",
    "umum":     "Timeline_Bulanan_Tim_Umum_2026.xlsx",
    "nerwilis": "Timeline_Bulanan_Nerwilis_2026.xlsx",
}

all_data = []
for tim_key, filename in files.items():
    df = pd.read_excel(filename, header=[0,1], index_col=0)
    # ... ekstrak baris + kolom aktif → append ke all_data

with open("data_embed.js", "w") as f:
    f.write(f"const TIMELINE_DATA = {json.dumps(all_data, ensure_ascii=False, indent=2)};")
```

***

## 11. Stack Teknologi

| Layer | Pilihan | Alasan |
|---|---|---|
| Markup | HTML5 Semantik | Aksesibel, tanpa framework |
| Styling | CSS Variables + CSS Grid | Zero dependency, dark mode native |
| Visualisasi | Chart.js v4 (via CDN) | Gantt via bar chart horizontal, heat map via matrix plugin |
| Ikon | Lucide Icons (via CDN) | Lightweight, konsisten |
| Font | Fontshare (Satoshi) + Google (JetBrains Mono) | Distinctive, modern |
| Data | Objek JS inline | Tanpa server, fully static |

**Total dependensi eksternal:** Chart.js + Lucide Icons + 2 font CDN = 4 request.

***

## 12. Urutan Pengerjaan (Build Steps)

```
1. [ ] Konversi data Excel → JavaScript object (convert_to_js.py)
2. [ ] Setup HTML skeleton + CSS variables (Nexus palette)
3. [ ] Design System Proof (design-test.html) → validasi
4. [ ] Build Sidebar + Topbar + dark mode toggle
5. [ ] Build KPI Strip (4 kartu + count-up animation)
6. [ ] Build Heat Map (SVG atau Chart.js matrix)
7. [ ] Build Gantt Chart (Chart.js horizontal bar)
8. [ ] Build Detail Panel (slide-in overlay)
9. [ ] Implement filter + search + zoom interactions
10.[ ] Mobile responsiveness (375px test)
11.[ ] Final QA: aksesibilitas, keyboard nav, dark mode, performa
12.[ ] Hapus design-test.html → deliver bps-timeline-dashboard.html
```

***

## 13. Kriteria Keberhasilan

- [ ] Semua kegiatan dari 4 tim tampil akurat sesuai data Excel
- [ ] Filter per tim bekerja real-time tanpa reload
- [ ] Heat map menunjukkan puncak beban kerja secara visual intuitif
- [ ] Tumpang tindih antar-tim teridentifikasi dengan jelas (warna atau badge)
- [ ] Dark mode berfungsi penuh
- [ ] Dapat dibuka di browser tanpa server (file:// protocol)
- [ ] Load time < 2 detik di jaringan kantor

***

*Dibuat: 15 April 2026 — BPS Kabupaten Buton Utara*