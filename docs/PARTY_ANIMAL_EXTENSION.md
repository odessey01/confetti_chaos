## Party Animal Extension Path

This project now uses shared party-animal rendering through `src/systems/party_animals.py`.

### Current default
- Default player variant: `teddy_f` (Softer Plush Deluxe Teddy)

### Add a new party animal (minimal steps)
1. Add a new shape variant in `src/systems/teddy_shape_variants.py`.
2. Add the new variant id to `SOFTER_PLUSH_DELUXE_VARIANT_IDS` (or another active set).
3. Register it in `src/systems/party_animals.py` using `register_party_animal(...)`.
4. Set `player.visual_variant_id` to the new id (or expose a selector later).
5. Validate with:
   - `pytest -q`
   - `python src/main.py` (visual check in gameplay)
   - `python src/playerdemo.py` (sandbox check)

### Notes
- Keep gameplay logic separate from render logic.
- Keep accessory treatment simple and consistent (`party_hat` baseline).
- Preserve readability first (outline contrast and clear ear silhouette).
