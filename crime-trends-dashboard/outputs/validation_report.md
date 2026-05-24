# PMK Dataset Validation Report

**Erstellt:** 2026-05-24  
**Datenjahre:** [2023, 2024]  
**Ergebnis:** ✓ BESTANDEN  
**Prüfungen:** 15 bestanden | 0 Hinweise | 0 fehlgeschlagen

## Prüfergebnisse

| Prüfung | Status | Details |
|---------|--------|---------|
| V10_comparability | ✓ PASS | Dataset covers years: [2023, 2024]. Both years use the unified PMK reporting system introduced in 2001. No cross-system comparison issues for the current dataset. Extension to pre-2024 years requires per-year comparability verification. |
| V1_schema_cats | ✓ PASS | Columns present: ['year', 'category', 'category_label_de', 'offenses', 'violent_offenses', 'source', 'source_url', 'access_date', 'notes', 'share_pct', 'violent_share_pct', 'yoy_offenses_change_pct', 'yoy_violent_change_pct'] |
| V1_schema_totals | ✓ PASS | Columns present: ['year', 'total_offenses', 'violent_offenses', 'internet_offenses', 'clearance_rate_pct', 'source', 'source_url', 'access_date', 'notes', 'yoy_change_pct', 'yoy_violent_change_pct'] |
| V2_no_dup_cats | ✓ PASS | 0 duplicate year×category rows |
| V2_no_dup_totals | ✓ PASS | 0 duplicate year rows |
| V3_no_missing_cats | ✓ PASS | 0 missing values in key fields |
| V3_no_missing_totals | ✓ PASS | 0 missing values in key fields |
| V4_allowed_categories | ✓ PASS | All 5 categories recognised |
| V5_nonneg_cats | ✓ PASS | 0 negative offenses values |
| V5_nonneg_totals | ✓ PASS | 0 negative total_offenses values |
| V6_sum_reconciliation | ✓ PASS | 2023: off=60028/60028 ✓, vio=3561/3561 ✓; 2024: off=84172/84172 ✓, vio=4107/4107 ✓ |
| V7_yoy_continuity | ✓ PASS | 0 year-over-year jumps > 300% (0 expected for adjacent years) |
| V8_subcat_bounds_2023 | ✓ PASS | Subcategory sum 5164 vs total 60028: within bounds |
| V8_subcat_bounds_2024 | ✓ PASS | Subcategory sum 29857 vs total 84172: within bounds |
| V9_source_documented | ✓ PASS | Source column: 0 empty in totals, 0 empty in cats |

## Hinweis zur Vergleichbarkeit

Der aktuelle Datensatz umfasst 2023 und 2024. Beide Jahre verwenden das seit 2001 
gültige einheitliche PMK-Erfassungssystem. Eine Erweiterung auf frühere Jahre 
erfordert eine jahresspezifische Prüfung der Kategoriedefinitionen gegen die 
offiziellen BMI/BKA-Jahresberichte. Diese Prüfung ist für zukünftige Versionen vorgesehen.