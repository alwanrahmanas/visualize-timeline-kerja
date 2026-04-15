#!/usr/bin/env python3
"""
Convert Excel timeline files to JavaScript data format for BPS Timeline Dashboard.
Reads 4 Excel files and outputs data_embed.js with all activities.
"""

import pandas as pd
import json

def parse_weeks_from_row(row, week_start_col):
    """Extract active weeks from a row. Returns list of week numbers (1-53)."""
    active_weeks = []
    week_num = 1
    
    for col in range(week_start_col, len(row)):
        val = row[col]
        if pd.notna(val) and str(val).strip() == '■':
            active_weeks.append(week_num)
        week_num += 1
    
    return active_weeks

def process_sosial(file_path):
    """Process Sosial file with columns: Program, Kegiatan, Mulai, Selesai"""
    df = pd.read_excel(file_path, header=None)
    activities = []
    
    for idx in range(3, len(df)):
        row = df.iloc[idx]
        
        if pd.isna(row[1]) and pd.isna(row[2]):
            continue
            
        program = row[1] if pd.notna(row[1]) else None
        kegiatan = row[2] if pd.notna(row[2]) else None
        mulai = row[3] if pd.notna(row[3]) else None
        selesai = row[4] if pd.notna(row[4]) else None
        
        if not kegiatan:
            continue
            
        active_weeks = parse_weeks_from_row(row, week_start_col=5)
        
        if active_weeks:
            activities.append({
                'tim': 'sosial',
                'program': str(program) if program else '',
                'kegiatan': str(kegiatan),
                'mulai': str(mulai) if mulai else '',
                'selesai': str(selesai) if selesai else '',
                'minggu_aktif': active_weeks
            })
    
    return activities

def process_produksi(file_path):
    """Process Produksi file with columns: Program, Kegiatan, Jadwal"""
    df = pd.read_excel(file_path, header=None)
    activities = []
    
    for idx in range(3, len(df)):
        row = df.iloc[idx]
        
        if pd.isna(row[1]) and pd.isna(row[2]):
            continue
            
        program = row[1] if pd.notna(row[1]) else None
        kegiatan = row[2] if pd.notna(row[2]) else None
        jadwal = row[3] if pd.notna(row[3]) else None
        
        if not kegiatan:
            continue
            
        active_weeks = parse_weeks_from_row(row, week_start_col=4)
        
        if active_weeks:
            activities.append({
                'tim': 'produksi',
                'program': str(program) if program else '',
                'kegiatan': str(kegiatan),
                'jadwal_teks': str(jadwal) if jadwal else '',
                'minggu_aktif': active_weeks
            })
    
    return activities

def process_umum(file_path):
    """Process Umum file with columns: Bagian, Kegiatan, Jadwal"""
    df = pd.read_excel(file_path, header=None)
    activities = []
    
    for idx in range(3, len(df)):
        row = df.iloc[idx]
        
        if pd.isna(row[1]) and pd.isna(row[2]):
            continue
            
        bagian = row[1] if pd.notna(row[1]) else None
        kegiatan = row[2] if pd.notna(row[2]) else None
        jadwal = row[3] if pd.notna(row[3]) else None
        
        if not kegiatan:
            continue
            
        active_weeks = parse_weeks_from_row(row, week_start_col=4)
        
        if active_weeks:
            activities.append({
                'tim': 'umum',
                'program': str(bagian) if bagian else '',
                'kegiatan': str(kegiatan),
                'jadwal_teks': str(jadwal) if jadwal else '',
                'minggu_aktif': active_weeks
            })
    
    return activities

def process_nerwilis(file_path):
    """Process Nerwilis file with columns: Program, Kegiatan"""
    df = pd.read_excel(file_path, header=None)
    activities = []
    
    for idx in range(3, len(df)):
        row = df.iloc[idx]
        
        if pd.isna(row[1]) and pd.isna(row[2]):
            continue
            
        program = row[1] if pd.notna(row[1]) else None
        kegiatan = row[2] if pd.notna(row[2]) else None
        
        if not kegiatan:
            continue
            
        active_weeks = parse_weeks_from_row(row, week_start_col=3)
        
        if active_weeks:
            activities.append({
                'tim': 'nerwilis',
                'program': str(program) if program else '',
                'kegiatan': str(kegiatan),
                'minggu_aktif': active_weeks
            })
    
    return activities

def main():
    files = {
        'sosial': 'Timline-fix/Timeline_Bulanan_Kegiatan_Sosial_2026_Revisi.xlsx',
        'produksi': 'Timline-fix/Timeline_Bulanan_Kegiatan_Produksi_2026_Revisi.xlsx',
        'umum': 'Timline-fix/Timeline_Bulanan_Tim_Umum_2026.xlsx',
        'nerwilis': 'Timline-fix/Timeline_Bulanan_Nerwilis_2026.xlsx'
    }
    
    all_data = []
    
    print("Processing files...")
    for tim_key, file_path in files.items():
        print(f"\n=== Processing {tim_key.upper()} ===")
        if tim_key == 'sosial':
            data = process_sosial(file_path)
        elif tim_key == 'produksi':
            data = process_produksi(file_path)
        elif tim_key == 'umum':
            data = process_umum(file_path)
        else:
            data = process_nerwilis(file_path)
        
        print(f"Found {len(data)} activities")
        all_data.extend(data)
    
    print(f"\n\nTotal activities: {len(all_data)}")
    
    # Write to data_embed.js
    with open("data_embed.js", "w", encoding="utf-8") as f:
        f.write("// Auto-generated data for BPS Timeline Dashboard 2026\n")
        f.write("// Source: 4 Excel files from Timline-fix/\n\n")
        f.write("const TIMELINE_DATA = ")
        f.write(json.dumps(all_data, ensure_ascii=False, indent=2))
        f.write(";\n")
    
    print("\n✓ Written to data_embed.js")

if __name__ == "__main__":
    main()
