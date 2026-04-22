"""Player entity with smooth physics and frame animation."""

from __future__ import annotations

import pygame

import config


class Player:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.velocity_y = 0.0
        self.frames = self._build_frames()
        self.frame_index = 0.0
        self.frame_speed = 10.0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def _build_frames(self) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []
        palette_cycle = [
            (255, 59, 110),
            (255, 156, 59),
            (255, 240, 59),
            (78, 220, 113),
            (80, 166, 255),
        ]

        for phase in range(4):
            surface = pygame.Surface((72, 48), pygame.SRCALPHA)

            for idx, color in enumerate(palette_cycle):
                y_offset = 12 + idx * 5 + ((phase + idx) % 2)
                pygame.draw.rect(surface, color, (2, y_offset, 28, 4), border_radius=2)

            pygame.draw.rect(surface, (238, 202, 173), (24, 8, 36, 32), border_radius=8)
            pygame.draw.rect(surface, (245, 144, 196), (28, 12, 28, 24), border_radius=6)

            sprinkle_colors = [(99, 246, 255), (255, 247, 121), (158, 255, 173)]
            for idx, color in enumerate(sprinkle_colors):
                pygame.draw.rect(
                    surface,
                    color,
                    (32 + idx * 7, 17 + (phase + idx) % 4, 4, 2),
                    border_radius=1,
                )
                pygame.draw.rect(
                    surface,
                    color,
                    (34 + idx * 6, 25 + (phase + idx + 1) % 4, 4, 2),
                    border_radius=1,
                )

            pygame.draw.circle(surface, (211, 211, 211), (56, 23), 12)
            pygame.draw.circle(surface, (45, 45, 45), (52, 22), 2)
            pygame.draw.circle(surface, (45, 45, 45), (60, 22), 2)
            pygame.draw.rect(surface, (45, 45, 45), (55, 26, 3, 2), border_radius=1)

            pygame.draw.ellipse(surface, (199, 199, 199), (42 - phase, 30, 12, 8))
            for lx in (35, 44, 53, 62):
                pygame.draw.rect(surface, (180, 180, 180), (lx, 35 + (phase % 2), 4, 8), border_radius=2)

            frames.append(surface)
        return frames

    def flap(self) -> None:
        self.velocity_y = config.JUMP_VELOCITY

    def update(self, dt: float) -> None:
        self.velocity_y += config.GRAVITY * dt
        self.velocity_y = min(self.velocity_y, config.MAX_FALL_SPEED)
        self.y += self.velocity_y * dt

        self.frame_index = (self.frame_index + self.frame_speed * dt) % len(self.frames)
        self.image = self.frames[int(self.frame_index)]

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface: pygame.Surface) -> None:
        tilt = max(-25, min(35, self.velocity_y * 0.08))
        rotated = pygame.transform.rotozoom(self.image, -tilt, 1.0)
        draw_rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, draw_rect)

    def get_collision_snapshot(self) -> tuple[pygame.Rect, pygame.Mask]:
        return self.rect, self.mask
