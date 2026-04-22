"""UI rendering for menus, HUD and overlays."""

from __future__ import annotations

import math

import pygame

import config


def draw_gradient_background(screen: pygame.Surface) -> None:
    width, height = screen.get_size()
    for y in range(height):
        blend = y / max(1, height - 1)
        color = (
            int(config.SPACE_TOP[0] * (1 - blend) + config.SPACE_BOTTOM[0] * blend),
            int(config.SPACE_TOP[1] * (1 - blend) + config.SPACE_BOTTOM[1] * blend),
            int(config.SPACE_TOP[2] * (1 - blend) + config.SPACE_BOTTOM[2] * blend),
        )
        pygame.draw.line(screen, color, (0, y), (width, y))


def draw_starfield(screen: pygame.Surface, stars: list[dict]) -> None:
    for star in stars:
        twinkle = 0.6 + 0.4 * abs(math.sin(star["phase"]))
        alpha = int(255 * star["twinkle"] * twinkle)
        color = (*config.STAR_COLOR[:3], max(30, min(255, alpha)))
        star_surface = pygame.Surface((star["radius"] * 2 + 2, star["radius"] * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, color, (star["radius"] + 1, star["radius"] + 1), star["radius"])
        screen.blit(star_surface, (star["x"], star["y"]))


def draw_hud(
    screen: pygame.Surface,
    score: int,
    high_score: int,
    small_font: pygame.font.Font,
    big_font: pygame.font.Font,
) -> None:
    score_text = big_font.render(str(score), True, config.TEXT_MAIN)
    score_shadow = big_font.render(str(score), True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH // 2, 60))
    screen.blit(score_shadow, score_rect.move(3, 3))
    screen.blit(score_text, score_rect)

    hs_text = small_font.render(f"High Score: {high_score}", True, config.TEXT_ACCENT)
    screen.blit(hs_text, (20, 16))


def draw_start_overlay(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
) -> None:
    title = title_font.render("Flappy Nyan Cat PRO", True, config.TEXT_MAIN)
    hint = body_font.render("Press SPACE to Start", True, config.TEXT_ACCENT)
    help_line = body_font.render("SPACE = Jump | P = Pause | M = Menu | ESC = Quit", True, config.TEXT_MAIN)

    panel = pygame.Surface((580, 180), pygame.SRCALPHA)
    pygame.draw.rect(panel, (8, 10, 30, 185), panel.get_rect(), border_radius=18)
    pygame.draw.rect(panel, (96, 226, 255, 210), panel.get_rect(), width=2, border_radius=18)

    panel_rect = panel.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
    screen.blit(panel, panel_rect)
    screen.blit(title, title.get_rect(center=(panel_rect.centerx, panel_rect.top + 50)))
    screen.blit(hint, hint.get_rect(center=(panel_rect.centerx, panel_rect.top + 98)))
    screen.blit(help_line, help_line.get_rect(center=(panel_rect.centerx, panel_rect.top + 140)))


def draw_pause_overlay(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
) -> None:
    panel = pygame.Surface((520, 200), pygame.SRCALPHA)
    pygame.draw.rect(panel, (10, 18, 34, 220), panel.get_rect(), border_radius=16)
    pygame.draw.rect(panel, config.TEXT_ACCENT, panel.get_rect(), width=2, border_radius=16)
    panel_rect = panel.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))

    paused = title_font.render("Paused", True, config.TEXT_MAIN)
    resume_text = body_font.render("Press P to Resume", True, config.TEXT_ACCENT)
    menu_text = body_font.render("Press M for Main Menu", True, config.TEXT_MAIN)

    screen.blit(panel, panel_rect)
    screen.blit(paused, paused.get_rect(center=(panel_rect.centerx, panel_rect.top + 56)))
    screen.blit(resume_text, resume_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 110)))
    screen.blit(menu_text, menu_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 150)))


def draw_game_over_overlay(
    screen: pygame.Surface,
    score: int,
    high_score: int,
    title_font: pygame.font.Font,
    body_font: pygame.font.Font,
) -> None:
    panel = pygame.Surface((520, 220), pygame.SRCALPHA)
    pygame.draw.rect(panel, (30, 5, 20, 220), panel.get_rect(), border_radius=16)
    pygame.draw.rect(panel, config.TEXT_WARNING, panel.get_rect(), width=2, border_radius=16)
    panel_rect = panel.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))

    game_over = title_font.render("Game Over", True, config.TEXT_WARNING)
    score_text = body_font.render(f"Score: {score}", True, config.TEXT_MAIN)
    high_text = body_font.render(f"High Score: {high_score}", True, config.TEXT_ACCENT)
    retry_text = body_font.render("R/SPACE = Restart | M = Main Menu", True, config.TEXT_MAIN)

    screen.blit(panel, panel_rect)
    screen.blit(game_over, game_over.get_rect(center=(panel_rect.centerx, panel_rect.top + 50)))
    screen.blit(score_text, score_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 95)))
    screen.blit(high_text, high_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 128)))
    screen.blit(retry_text, retry_text.get_rect(center=(panel_rect.centerx, panel_rect.top + 174)))
