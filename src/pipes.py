"""Pipe entities and spawn helpers."""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

import config


@dataclass
class PipePair:
    x: float
    gap_y: int
    gap_size: int
    width: int
    passed: bool = False

    def __post_init__(self) -> None:
        self._build_surfaces()

    def _build_surfaces(self) -> None:
        top_height = max(40, self.gap_y - self.gap_size // 2)
        bottom_y = self.gap_y + self.gap_size // 2
        bottom_height = max(40, config.SCREEN_HEIGHT - bottom_y)

        self.top_surface = pygame.Surface((self.width, top_height), pygame.SRCALPHA)
        self.bottom_surface = pygame.Surface((self.width, bottom_height), pygame.SRCALPHA)

        self._draw_pipe_style(self.top_surface, flip_cap=True)
        self._draw_pipe_style(self.bottom_surface, flip_cap=False)

        self.top_rect = self.top_surface.get_rect(bottomleft=(int(self.x), top_height))
        self.bottom_rect = self.bottom_surface.get_rect(topleft=(int(self.x), bottom_y))

        self.top_mask = pygame.mask.from_surface(self.top_surface)
        self.bottom_mask = pygame.mask.from_surface(self.bottom_surface)

    def _draw_pipe_style(self, surface: pygame.Surface, flip_cap: bool) -> None:
        w, h = surface.get_size()
        body_rect = pygame.Rect(8, 0, max(12, w - 16), h)
        pygame.draw.rect(surface, config.PIPE_BODY, body_rect)
        pygame.draw.rect(surface, config.PIPE_EDGE, body_rect, width=4)

        cap_h = 20
        cap_rect = pygame.Rect(0, 0, w, cap_h)
        if flip_cap:
            cap_rect.bottom = h
        pygame.draw.rect(surface, config.PIPE_CAP, cap_rect, border_radius=4)
        pygame.draw.rect(surface, config.PIPE_EDGE, cap_rect, width=3, border_radius=4)

        for y in range(10, h, 18):
            pygame.draw.line(surface, (178, 255, 190), (10, y), (w - 10, y), 1)

    def update(self, dt: float, speed: float) -> None:
        self.x -= speed * dt
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.top_surface, self.top_rect)
        screen.blit(self.bottom_surface, self.bottom_rect)

    def is_off_screen(self) -> bool:
        return self.top_rect.right < 0

    def collides_with(self, player_rect: pygame.Rect, player_mask: pygame.Mask) -> bool:
        offset_top = (self.top_rect.x - player_rect.x, self.top_rect.y - player_rect.y)
        offset_bottom = (self.bottom_rect.x - player_rect.x, self.bottom_rect.y - player_rect.y)
        return (
            player_mask.overlap(self.top_mask, offset_top) is not None
            or player_mask.overlap(self.bottom_mask, offset_bottom) is not None
        )


def spawn_pipe() -> PipePair:
    margin = 100
    center_min = margin + config.PIPE_GAP // 2
    center_max = config.SCREEN_HEIGHT - margin - config.PIPE_GAP // 2
    gap_y = random.randint(center_min, center_max)
    return PipePair(
        x=float(config.SCREEN_WIDTH + 20),
        gap_y=gap_y,
        gap_size=config.PIPE_GAP,
        width=config.PIPE_WIDTH,
    )
