"""Data-driven weapon visual definitions for player-attached overlays."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WeaponVisualRotationRule:
    """Configurable facing-aware orientation for carried weapon overlays."""

    idle_angle_degrees: float
    moving_angle_degrees: float
    mirror_angle_with_facing: bool = True
    flip_with_facing: bool = True


@dataclass(frozen=True, slots=True)
class WeaponVisualVariantDefinition:
    """Describe a named visual variant for an equipped weapon overlay."""

    variant_id: str
    weapon_id: str
    default_overlay_sprite: str
    anchor_name: str
    offsets_by_facing: dict[str, tuple[float, float]]
    scale: float
    draw_layer: int
    rotation_rule: WeaponVisualRotationRule
    animation_profile: WeaponVisualAnimationProfile | None = None
    # TODO: Use these for future glow, smoke, and trail attachment points.
    vfx_hook_id: str | None = None
    trail_hook_id: str | None = None


@dataclass(frozen=True, slots=True)
class WeaponVisualVariantRule:
    """Rule for selecting an active visual variant from weapon state."""

    variant_id: str
    min_evolution_count: int = 0
    required_form_ids: tuple[str, ...] = ()
    required_tags: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class WeaponVisualAnimationProfile:
    """Optional polish hooks for lightweight weapon overlay motion and effects."""

    bob_amplitude: float = 0.0
    bob_speed: float = 0.0
    idle_sway_degrees: float = 0.0
    recoil_offset: float = 0.0
    firing_flash_hook: str | None = None
    glow_hook_id: str | None = None
    confetti_hook_id: str | None = None


WEAPON_VISUAL_VARIANTS: dict[str, WeaponVisualVariantDefinition] = {
    "bottle_rocket:tier1": WeaponVisualVariantDefinition(
        variant_id="tier1",
        weapon_id="bottle_rocket",
        default_overlay_sprite="bottle_rocket_tier1",
        anchor_name="weapon_mount",
        offsets_by_facing={
            "right": (0.0, 0.0),
            "left": (0.0, 0.0),
        },
        scale=0.75,
        draw_layer=1,
        rotation_rule=WeaponVisualRotationRule(
            idle_angle_degrees=-12.0,
            moving_angle_degrees=-22.0,
            mirror_angle_with_facing=True,
            flip_with_facing=True,
        ),
        animation_profile=WeaponVisualAnimationProfile(
            bob_amplitude=2.0,
            bob_speed=4.0,
            idle_sway_degrees=2.5,
            recoil_offset=5.0,
            firing_flash_hook="todo:bottle_rocket_flash",
            glow_hook_id="todo:bottle_rocket_glow",
            confetti_hook_id="todo:bottle_rocket_confetti",
        ),
        vfx_hook_id="todo:bottle_rocket_glow",
        trail_hook_id="todo:bottle_rocket_smoke",
    ),
    "bottle_rocket:tier2": WeaponVisualVariantDefinition(
        variant_id="tier2",
        weapon_id="bottle_rocket",
        default_overlay_sprite="bottle_rocket_tier1",
        anchor_name="weapon_mount",
        offsets_by_facing={
            "right": (0.0, 0.0),
            "left": (0.0, 0.0),
        },
        scale=0.82,
        draw_layer=1,
        rotation_rule=WeaponVisualRotationRule(
            idle_angle_degrees=-12.0,
            moving_angle_degrees=-24.0,
            mirror_angle_with_facing=True,
            flip_with_facing=True,
        ),
        animation_profile=WeaponVisualAnimationProfile(
            bob_amplitude=2.5,
            bob_speed=4.4,
            idle_sway_degrees=2.8,
            recoil_offset=5.5,
            firing_flash_hook="todo:bottle_rocket_flash",
            glow_hook_id="todo:bottle_rocket_glow",
            confetti_hook_id="todo:bottle_rocket_confetti",
        ),
        vfx_hook_id="todo:bottle_rocket_glow",
        trail_hook_id="todo:bottle_rocket_smoke",
    ),
    "bottle_rocket:tier3": WeaponVisualVariantDefinition(
        variant_id="tier3",
        weapon_id="bottle_rocket",
        default_overlay_sprite="bottle_rocket_tier1",
        anchor_name="weapon_mount",
        offsets_by_facing={
            "right": (0.0, 0.0),
            "left": (0.0, 0.0),
        },
        scale=0.9,
        draw_layer=1,
        rotation_rule=WeaponVisualRotationRule(
            idle_angle_degrees=-12.0,
            moving_angle_degrees=-26.0,
            mirror_angle_with_facing=True,
            flip_with_facing=True,
        ),
        animation_profile=WeaponVisualAnimationProfile(
            bob_amplitude=3.0,
            bob_speed=4.8,
            idle_sway_degrees=3.0,
            recoil_offset=6.0,
            firing_flash_hook="todo:bottle_rocket_flash",
            glow_hook_id="todo:bottle_rocket_glow",
            confetti_hook_id="todo:bottle_rocket_confetti",
        ),
        vfx_hook_id="todo:bottle_rocket_glow",
        trail_hook_id="todo:bottle_rocket_smoke",
    ),
    # Placeholder entry proving the overlay registry is multi-weapon ready.
    "sparkler:tier1": WeaponVisualVariantDefinition(
        variant_id="tier1",
        weapon_id="sparkler",
        default_overlay_sprite="sparkler_tier1_placeholder",
        anchor_name="weapon_mount",
        offsets_by_facing={
            "right": (0.0, -6.0),
            "left": (0.0, -6.0),
        },
        scale=0.7,
        draw_layer=1,
        rotation_rule=WeaponVisualRotationRule(
            idle_angle_degrees=-6.0,
            moving_angle_degrees=-12.0,
            mirror_angle_with_facing=True,
            flip_with_facing=True,
        ),
        vfx_hook_id="todo:sparkler_glow",
        trail_hook_id="todo:sparkler_spark_trail",
    ),
}

WEAPON_VISUAL_VARIANT_RULES: dict[str, tuple[WeaponVisualVariantRule, ...]] = {
    "bottle_rocket": (
        WeaponVisualVariantRule(variant_id="tier3", min_evolution_count=2),
        WeaponVisualVariantRule(variant_id="tier2", min_evolution_count=1),
        WeaponVisualVariantRule(variant_id="tier1", min_evolution_count=0),
    ),
    "sparkler": (
        WeaponVisualVariantRule(variant_id="tier1", min_evolution_count=0),
    ),
}


def list_weapon_visual_variants() -> tuple[WeaponVisualVariantDefinition, ...]:
    return tuple(WEAPON_VISUAL_VARIANTS.values())


def get_weapon_visual_variant(weapon_id: str, variant_id: str = "tier1") -> WeaponVisualVariantDefinition | None:
    key = f"{weapon_id}:{variant_id}"
    return WEAPON_VISUAL_VARIANTS.get(key)


def resolve_weapon_visual_variant_id(
    weapon_id: str,
    *,
    evolution_count: int = 0,
    active_form_id: str | None = None,
    acquired_tags: tuple[str, ...] | list[str] | set[str] = (),
) -> str | None:
    rules = WEAPON_VISUAL_VARIANT_RULES.get(str(weapon_id), ())
    tags = {str(tag) for tag in acquired_tags}
    resolved_form_id = str(active_form_id or "")
    for rule in rules:
        if int(evolution_count) < int(rule.min_evolution_count):
            continue
        if rule.required_form_ids and resolved_form_id not in rule.required_form_ids:
            continue
        if rule.required_tags and not set(rule.required_tags).issubset(tags):
            continue
        return rule.variant_id
    return None


def weapon_ids_with_visuals() -> tuple[str, ...]:
    weapon_ids = {variant.weapon_id for variant in WEAPON_VISUAL_VARIANTS.values()}
    return tuple(sorted(weapon_ids))
