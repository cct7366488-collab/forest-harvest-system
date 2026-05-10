cd C:\Projects\forest-harvest-system\backend

$species = @{
    species_code = "255"
    chinese_name = "相思樹"
    scientific_name = "Acacia confusa Merr."
    family = "Fabaceae"
    genus = "Acacia"
    common_group = "闊葉樹"
    is_native = $true
    notes = "Test species record"
} | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/species/ -Method Post -Body $species -ContentType "application/json"

$volume = @{
    species_code = "255"
    species_name = "相思樹"
    model_name = "Test volume model"
    formula_text = "V = 0.0002045 * D^1.4366684 * H^0.8480426"
    formula_expression = "0.0002045 * (D ** 1.4366684) * (H ** 0.8480426)"
    variables = @{ D = "dbh_cm"; H = "height_m"; V = "volume_m3" }
    coefficients = @{ a = 0.0002045; b = 1.4366684; c = 0.8480426 }
    applicable_region = "Taiwan"
    sample_size = 20
    r_squared = 0.95
    author = "Test"
    publication_year = 1986
    source_reference = "森林資源調查表及樹種立木材積模式"
    notes = "Test volume model record"
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri http://127.0.0.1:8000/volume-models/ -Method Post -Body $volume -ContentType "application/json"

$height = @{
    species_code = "255"
    species_name = "相思樹"
    model_name = "Test height model"
    formula_text = "H = exp(0.580371 + 0.675988 lnD)"
    formula_expression = "exp(0.580371 + 0.675988 * log(D))"
    variables = @{ D = "dbh_cm"; H = "height_m" }
    coefficients = @{ a = 0.580371; b = 0.675988 }
    applicable_region = "Taiwan south"
    sample_size = 20
    r_squared = 0.90
    author = "Test"
    publication_year = 1986
    source_reference = "森林資源調查表及樹種立木材積模式"
    notes = "Test height model record"
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri http://127.0.0.1:8000/height-models/ -Method Post -Body $height -ContentType "application/json"

$tree = @{
    plot_id = 1
    inventory_cycle = "TEST"
    tree_no = "T001"
    tree_status = "alive"
    record_type = "test"
    species_code = "255"
    species_name = "相思樹"
    dbh_cm = 25.5
    height_m = 18.2
    clear_bole_height_m = 8.0
    crown_class = "2"
    estimated_volume_m3 = 0.35
    notes = "First tree insert test"
} | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/trees/ -Method Post -Body $tree -ContentType "application/json"
