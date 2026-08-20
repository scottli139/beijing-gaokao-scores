#!/usr/bin/env python3
"""Generate analysis charts for Beijing Gaokao admission scores."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
from collections import Counter

# Configure matplotlib for Chinese characters
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'STSong', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# Load data
DATA_DIR = Path(__file__).parent.parent / 'data'
CHARTS_DIR = Path(__file__).parent

def load_all_years():
    """Load all years of data into a dictionary."""
    years_data = {}
    for year in [2023, 2024, 2025, 2026]:
        csv_path = DATA_DIR / f'{year}.csv'
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            years_data[year] = df
    return years_data

def chart_01_record_count_trend(years_data):
    """Chart 1: Record count trend over 4 years."""
    years = sorted(years_data.keys())
    counts = [len(years_data[y]) for y in years]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar chart with trend line
    bars = ax.bar(years, counts, color='#4C78A8', alpha=0.7, width=0.6)
    ax.plot(years, counts, 'o-', color='#E45756', linewidth=2, markersize=8, label='趋势线')
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f'{count}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('记录数', fontsize=12)
    ax.set_title('历年录取记录数变化趋势', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(years)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(counts) * 1.15)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '01_record_count_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 01: Record count trend')

def chart_02_score_distribution(years_data):
    """Chart 2: Score distribution comparison across years."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = ['#4C78A8', '#F58518', '#E45756', '#72B7B2']
    years = sorted(years_data.keys())
    
    for i, year in enumerate(years):
        df = years_data[year]
        scores = df['score'].dropna()
        scores = pd.to_numeric(scores, errors='coerce').dropna()
        ax.hist(scores, bins=30, alpha=0.5, label=f'{year}年', color=colors[i], edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('投档分数', fontsize=12)
    ax.set_ylabel('记录数', fontsize=12)
    ax.set_title('历年投档分数分布对比', fontsize=16, fontweight='bold', pad=20)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '02_score_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 02: Score distribution')

def chart_03_top_schools_trend(years_data):
    """Chart 3: Top schools admission score trend."""
    top_schools = {
        '1021': '北京大学',
        '1023': '清华大学',
        '1022': '中国人民大学',
        '1047': '北京航空航天大学',
        '1032': '北京师范大学'
    }
    
    fig, ax = plt.subplots(figsize=(12, 7))
    years = sorted(years_data.keys())
    colors = ['#E45756', '#4C78A8', '#F58518', '#72B7B2', '#54A24B']
    
    for i, (code, name) in enumerate(top_schools.items()):
        max_scores = []
        for year in years:
            df = years_data[year]
            school_df = df[df['school_code'].astype(str).str.strip() == code]
            if not school_df.empty:
                scores = pd.to_numeric(school_df['score'], errors='coerce').dropna()
                if not scores.empty:
                    max_scores.append(scores.max())
                else:
                    max_scores.append(None)
            else:
                max_scores.append(None)
        
        # Filter out None values
        valid_years = [y for y, s in zip(years, max_scores) if s is not None]
        valid_scores = [s for s in max_scores if s is not None]
        
        if valid_scores:
            ax.plot(valid_years, valid_scores, 'o-', label=name, color=colors[i], 
                   linewidth=2, markersize=8)
    
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('最高投档分数', fontsize=12)
    ax.set_title('顶尖高校投档线趋势（2023-2026）', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(years)
    ax.legend(loc='best')
    ax.grid(alpha=0.3)
    
    ax.set_ylim(630, 710)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '03_top_schools_trend.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 03: Top schools trend')

def chart_04_selection_requirement_2026(years_data):
    """Chart 4: Selection requirement distribution for 2026."""
    if 2026 not in years_data:
        print('✗ Chart 04: 2026 data not available')
        return
    
    df = years_data[2026]
    requirements = df['selection_requirement'].value_counts()
    
    # Take top 10 categories
    top_req = requirements.head(10)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.Set3(range(len(top_req)))
    bars = ax.barh(range(len(top_req)), top_req.values, color=colors, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for i, (bar, count) in enumerate(zip(bars, top_req.values)):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                f'{count} ({count/len(df)*100:.1f}%)', 
                ha='left', va='center', fontsize=10)
    
    ax.set_yticks(range(len(top_req)))
    ax.set_yticklabels(top_req.index)
    ax.invert_yaxis()
    ax.set_xlabel('记录数', fontsize=12)
    ax.set_title('2026年选考要求分布', fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    ax.set_xlim(0, top_req.max() * 1.2)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '04_selection_requirement_2026.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 04: Selection requirement distribution')

def chart_05_beijing_vs_others(years_data):
    """Chart 5: Beijing vs non-Beijing schools comparison."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    years = sorted(years_data.keys())
    
    for idx, year in enumerate(years):
        ax = axes[idx // 2, idx % 2]
        df = years_data[year]
        
        # Beijing schools (code starts with 1)
        beijing = df[df['school_code'].astype(str).str.startswith('1')]
        others = df[~df['school_code'].astype(str).str.startswith('1')]
        
        beijing_scores = pd.to_numeric(beijing['score'], errors='coerce').dropna()
        others_scores = pd.to_numeric(others['score'], errors='coerce').dropna()
        
        # Box plot
        bp = ax.boxplot([beijing_scores, others_scores], 
                       labels=['北京高校', '外地高校'],
                       patch_artist=True,
                       widths=0.5)
        
        # Color boxes
        colors = ['#4C78A8', '#E45756']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
        
        ax.set_title(f'{year}年', fontsize=14, fontweight='bold')
        ax.set_ylabel('投档分数', fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        # Add statistics text
        stats_text = f'北京: {len(beijing_scores)}条, 均值{beijing_scores.mean():.0f}\n外地: {len(others_scores)}条, 均值{others_scores.mean():.0f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    fig.suptitle('北京高校 vs 外地高校投档分数对比', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '05_beijing_vs_others.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 05: Beijing vs others comparison')

def chart_06_score_tier_distribution(years_data):
    """Chart 6: Score tier distribution over years."""
    tiers = [
        (680, 750, '680+'),
        (650, 679, '650-679'),
        (620, 649, '620-649'),
        (590, 619, '590-619'),
        (560, 589, '560-589'),
        (530, 559, '530-559'),
        (500, 529, '500-529'),
        (470, 499, '470-499'),
        (400, 469, '<470')
    ]
    
    years = sorted(years_data.keys())
    tier_counts = {t[2]: [] for t in tiers}
    
    for year in years:
        df = years_data[year]
        scores = pd.to_numeric(df['score'], errors='coerce').dropna()
        
        for low, high, label in tiers:
            count = ((scores >= low) & (scores <= high)).sum()
            tier_counts[label].append(count)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Stacked bar chart
    bottom = [0] * len(years)
    colors = plt.cm.RdYlGn_r([i / len(tiers) for i in range(len(tiers))])
    
    for i, (low, high, label) in enumerate(tiers):
        counts = tier_counts[label]
        bars = ax.bar(years, counts, bottom=bottom, label=label, color=colors[i], 
                     edgecolor='black', linewidth=0.5, width=0.6)
        bottom = [b + c for b, c in zip(bottom, counts)]
    
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('记录数', fontsize=12)
    ax.set_title('历年分数段分布（堆叠柱状图）', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(years)
    ax.legend(title='分数段', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '06_score_tier_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 06: Score tier distribution')

def chart_07_school_landscape(years_data):
    """Chart 7: School landscape changes (new/exited schools)."""
    years = sorted(years_data.keys())
    
    school_codes_by_year = {}
    for year in years:
        df = years_data[year]
        codes = set(df['school_code'].astype(str).str.strip().unique())
        school_codes_by_year[year] = codes
    
    new_schools = {year: school_codes_by_year[year] - school_codes_by_year[year-1] for year in years[1:]}
    exited_schools = {year: school_codes_by_year[year-1] - school_codes_by_year[year] for year in years[1:]}
    
    new_counts = [0] + [len(new_schools[y]) for y in years[1:]]
    exited_counts = [0] + [len(exited_schools[y]) for y in years[1:]]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(years))
    width = 0.35
    bars1 = ax.bar([i - width/2 for i in x], new_counts, width, label='新增学校', color='#54A24B', alpha=0.7)
    bars2 = ax.bar([i + width/2 for i in x], exited_counts, width, label='退出学校', color='#E45756', alpha=0.7)
    
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('学校数', fontsize=12)
    ax.set_title('历年招生学校版图变化', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    for bar in bars1[1:]:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=10)
    for bar in bars2[1:]:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '07_school_landscape.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 07: School landscape')

def chart_08_major_group_count(years_data):
    """Chart 8: Major group count trend."""
    years = sorted(years_data.keys())
    group_counts = {}
    for year in years:
        df = years_data[year]
        df['code_group'] = df['school_code'].astype(str).str.strip() + '_' + df['major_group'].astype(str).str.strip()
        group_counts[year] = df['code_group'].nunique()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, [group_counts[y] for y in years], 'o-', linewidth=2, markersize=8, color='#4C78A8')
    for year, count in zip(years, [group_counts[y] for y in years]):
        ax.text(year, count + 10, str(count), ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('专业组数量', fontsize=12)
    ax.set_title('历年专业组数量变化', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(years)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '08_major_group_count.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 08: Major group count')

def chart_09_trend_schools(years_data):
    """Chart 9: Schools with continuous upward/downward trends."""
    import statistics
    years = sorted(years_data.keys())
    
    # Find common schools across all years
    school_codes_by_year = {}
    for year in years:
        df = years_data[year]
        codes = set(df['school_code'].astype(str).str.strip().unique())
        school_codes_by_year[year] = codes
    
    common_codes = school_codes_by_year[years[0]]
    for year in years[1:]:
        common_codes &= school_codes_by_year[year]
    
    four_year_up = []
    four_year_down = []
    for code in common_codes:
        scores = []
        name = ""
        for year in years:
            df = years_data[year]
            school_df = df[df['school_code'].astype(str).str.strip() == code]
            if not school_df.empty:
                s = pd.to_numeric(school_df['score'], errors='coerce').dropna()
                if not s.empty:
                    scores.append(int(s.max()))
                    if not name:
                        name = school_df.iloc[0]['school_name']
        if len(scores) == 4:
            if scores[0] < scores[1] < scores[2] < scores[3]:
                four_year_up.append((name, scores))
            elif scores[0] > scores[1] > scores[2] > scores[3]:
                four_year_down.append((name, scores))
    
    four_year_up.sort(key=lambda x: x[1][3] - x[1][0], reverse=True)
    four_year_down.sort(key=lambda x: x[1][0] - x[1][3], reverse=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 10))
    
    # Upward trend
    ax = axes[0]
    top_up = four_year_up[:10]
    for i, (name, scores) in enumerate(top_up):
        ax.plot(years, scores, 'o-', linewidth=2, markersize=6, alpha=0.7)
        ax.text(years[-1], scores[-1], f' {name} (+{scores[3]-scores[0]})', 
                fontsize=9, va='center')
    ax.set_xlabel('年份', fontsize=11)
    ax.set_ylabel('投档分数', fontsize=11)
    ax.set_title(f'连续四年上涨 Top 10 (共{len(four_year_up)}所)', fontsize=13, fontweight='bold')
    ax.set_xticks(years)
    ax.grid(alpha=0.3)
    
    # Downward trend
    ax = axes[1]
    top_down = four_year_down[:10]
    for i, (name, scores) in enumerate(top_down):
        ax.plot(years, scores, 'o-', linewidth=2, markersize=6, alpha=0.7)
        ax.text(years[-1], scores[-1], f' {name} ({scores[3]-scores[0]})', 
                fontsize=9, va='center')
    ax.set_xlabel('年份', fontsize=11)
    ax.set_ylabel('投档分数', fontsize=11)
    ax.set_title(f'连续四年下降 Top 10 (共{len(four_year_down)}所)', fontsize=13, fontweight='bold')
    ax.set_xticks(years)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '09_trend_schools.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✓ Chart 09: Trend schools (↑{len(four_year_up)} ↓{len(four_year_down)})')

def chart_10_volatile_schools(years_data):
    """Chart 10: Schools with highest score volatility."""
    import statistics
    years = sorted(years_data.keys())
    
    school_codes_by_year = {}
    for year in years:
        df = years_data[year]
        codes = set(df['school_code'].astype(str).str.strip().unique())
        school_codes_by_year[year] = codes
    
    common_codes = school_codes_by_year[years[0]]
    for year in years[1:]:
        common_codes &= school_codes_by_year[year]
    
    volatile = []
    for code in common_codes:
        scores = []
        name = ""
        for year in years:
            df = years_data[year]
            school_df = df[df['school_code'].astype(str).str.strip() == code]
            if not school_df.empty:
                s = pd.to_numeric(school_df['score'], errors='coerce').dropna()
                if not s.empty:
                    scores.append(int(s.max()))
                    if not name:
                        name = school_df.iloc[0]['school_name']
        if len(scores) == 4 and scores[0] > 400:
            std = statistics.stdev(scores)
            volatile.append((name, scores, std))
    
    volatile.sort(key=lambda x: x[2], reverse=True)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    top_volatile = volatile[:15]
    for i, (name, scores, std) in enumerate(top_volatile):
        ax.plot(years, scores, 'o-', linewidth=2, markersize=6, alpha=0.7)
        ax.text(years[-1], scores[-1], f' {name} (σ={std:.0f})', 
                fontsize=9, va='center')
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('投档分数', fontsize=12)
    ax.set_title('断档风险学校 Top 15 (标准差最大)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(years)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '10_volatile_schools.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 10: Volatile schools')

def chart_11_group_score_gap(years_data):
    """Chart 11: Score gap between major groups within same school (2026)."""
    if 2026 not in years_data:
        print('✗ Chart 11: 2026 data not available')
        return
    
    df_2026 = years_data[2026].copy()
    df_2026['school_code_str'] = df_2026['school_code'].astype(str).str.strip()
    
    group_diff = []
    for code in df_2026['school_code_str'].unique():
        school_df = df_2026[df_2026['school_code_str'] == code]
        if len(school_df) >= 3:
            scores = pd.to_numeric(school_df['score'], errors='coerce').dropna()
            if len(scores) >= 3:
                name = school_df.iloc[0]['school_name']
                diff = int(scores.max() - scores.min())
                group_diff.append((name, len(school_df), int(scores.max()), int(scores.min()), diff))
    
    group_diff.sort(key=lambda x: x[4], reverse=True)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    top_diff = group_diff[:20]
    names = [x[0] for x in top_diff]
    max_scores = [x[2] for x in top_diff]
    min_scores = [x[3] for x in top_diff]
    
    y = range(len(names))
    ax.barh(y, max_scores, height=0.4, label='最高分', color='#E45756', alpha=0.7)
    ax.barh([i - 0.4 for i in y], min_scores, height=0.4, label='最低分', color='#4C78A8', alpha=0.7)
    
    for i, (name, n, max_s, min_s, diff) in enumerate(top_diff):
        ax.text(max_s + 2, i, f'{max_s} (-{diff})', va='center', fontsize=9)
    
    ax.set_yticks(y)
    ax.set_yticklabels([f"{x[0]} ({x[1]}组)" for x in top_diff])
    ax.invert_yaxis()
    ax.set_xlabel('投档分数', fontsize=12)
    ax.set_title('2026年同一学校专业组分数差异 Top 20', fontsize=16, fontweight='bold', pad=20)
    ax.legend()
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '11_group_score_gap.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Chart 11: Group score gap')

def main():
    """Generate all charts."""
    print('Loading data...')
    years_data = load_all_years()
    
    if not years_data:
        print('Error: No data found')
        return
    
    print(f'Loaded {len(years_data)} years of data\n')
    print('Generating charts...')
    
    chart_01_record_count_trend(years_data)
    chart_02_score_distribution(years_data)
    chart_03_top_schools_trend(years_data)
    chart_04_selection_requirement_2026(years_data)
    chart_05_beijing_vs_others(years_data)
    chart_06_score_tier_distribution(years_data)
    chart_07_school_landscape(years_data)
    chart_08_major_group_count(years_data)
    chart_09_trend_schools(years_data)
    chart_10_volatile_schools(years_data)
    chart_11_group_score_gap(years_data)
    
    print(f'\n✓ All 11 charts saved to {CHARTS_DIR}')

if __name__ == '__main__':
    main()
