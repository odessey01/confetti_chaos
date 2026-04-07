"""A slower balloon hazard that periodically re-aims toward the player."""

from __future__ import annotations

import math

import pygame

from .balloon_enemy import BalloonEnemy


class TrackingHazard(BalloonEnemy):
    def __init__(
        self,
        size: int = 68,
        speed: float = 170.0,
        retarget_interval: float = 1.25,  # Increased from 0.75 to 1.25 seconds
        max_retargets: int = 5,  # Reduced from 7 to 5
    ) -> None:
        super().__init__(size=size, speed=speed)
        self.base_speed = speed
        self.retarget_interval = retarget_interval
        self.max_retargets = max_retargets
        self._retarget_timer = 0.0
        self._retarget_count = 0

    def launch_toward_target(self, spawn: pygame.Vector2, target_center: pygame.Vector2) -> None:
        super().launch_toward_target(spawn, target_center)
        self._retarget_timer = 0.0
        self._retarget_count = 0

    def update(self, delta_seconds: float, target_center: pygame.Vector2 | None = None) -> None:
        self._retarget_timer += delta_seconds
        if (
            target_center is not None
            and self._retarget_count < self.max_retargets
            and self._retarget_timer >= self.retarget_interval
        ):
            self._retarget_timer = 0.0
            
            # Calculate desired direction toward target
            desired_direction = target_center - self.position
            if desired_direction.length_squared() > 0:
                desired_direction = desired_direction.normalize()
                
                # Get current direction from velocity
                if self.velocity.length_squared() > 0:
                    current_direction = self.velocity.normalize()
                    
                    # Calculate angle between current and desired direction
                    dot_product = current_direction.dot(desired_direction)
                    angle = math.acos(max(-1.0, min(1.0, dot_product)))  # Clamp for numerical stability
                    
                    # If angle > 90 degrees, limit to 90 degrees
                    if angle > math.pi / 2:  # 90 degrees in radians
                        # Calculate the limited direction (90 degrees toward target)
                        # Use cross product to determine turn direction
                        cross = current_direction.x * desired_direction.y - current_direction.y * desired_direction.x
                        turn_direction = 1 if cross > 0 else -1
                        
                        # Rotate current direction by 90 degrees toward target
                        limited_direction = pygame.Vector2(
                            current_direction.x * math.cos(math.pi / 2 * turn_direction) - 
                            current_direction.y * math.sin(math.pi / 2 * turn_direction),
                            current_direction.x * math.sin(math.pi / 2 * turn_direction) + 
                            current_direction.y * math.cos(math.pi / 2 * turn_direction)
                        )
                        self.velocity = limited_direction * self.speed
                        direction = limited_direction
                    else:
                        # Angle <= 90 degrees, can turn directly to target
                        self.velocity = desired_direction * self.speed
                        direction = desired_direction
                    
                    self._float_axis = pygame.Vector2(-direction.y, direction.x)
                    self._retarget_count += 1
        
        super().update(delta_seconds, target_center)
