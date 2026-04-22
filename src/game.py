"""Main game loop, states and orchestration."""

from __future__ import annotations

from enum import Enum, auto

import pygame

import config
from src.player import Player
from src.pipes import PipePair, spawn_pipe
from src.ui import (
    draw_game_over_overlay,
    draw_gradient_background,
    draw_hud,
    draw_starfield,
    draw_start_overlay,
)
from src.utils import (
    build_starfield,
    load_high_score,
    make_chime,
    make_tone,
    save_high_score,
    update_starfield,
)


class GameState(Enum):
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(config.TITLE)
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.SysFont("verdana", 56, bold=True)
        self.big_font = pygame.font.SysFont("verdana", 48, bold=True)
        self.body_font = pygame.font.SysFont("verdana", 30, bold=True)
        self.small_font = pygame.font.SysFont("verdana", 24)

        self.state = GameState.START
        self.running = True

        self.high_score = load_high_score(config.HIGH_SCORE_FILE)
        self.stars = build_starfield(95, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        self._setup_audio()
        self.reset_round(full_reset=True)

    def _setup_audio(self) -> None:
        self.sfx_jump = None
        self.sfx_hit = None
        self.music = None
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.sfx_jump = make_tone(640.0, duration=0.08, volume=0.35)
            self.sfx_hit = make_tone(170.0, duration=0.24, volume=0.4)
            self.music = make_chime([330.0, 392.0, 440.0, 392.0], note_duration=0.12, volume=0.08)
            if self.music:
                self.music.play(loops=-1)
        except pygame.error:
            # Audio is optional; game works silently when no mixer is available.
            self.sfx_jump = None
            self.sfx_hit = None
            self.music = None

    def reset_round(self, full_reset: bool = False) -> None:
        self.player = Player(config.PLAYER_START_X, config.PLAYER_START_Y)
        self.pipes: list[PipePair] = []
        self.score = 0
        self.pipe_spawn_timer = 0.0
        self.current_pipe_interval = config.PIPE_SPAWN_SECONDS
        self.pipe_speed = config.PIPE_SPEED_BASE
        self.flash_timer = 0.0

        if full_reset:
            self.state = GameState.START
        else:
            self.state = GameState.PLAYING

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._render()

        save_high_score(config.HIGH_SCORE_FILE, self.high_score)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_SPACE:
                    if self.state == GameState.START:
                        self.state = GameState.PLAYING
                        self.player.flap()
                        if self.sfx_jump:
                            self.sfx_jump.play()
                    elif self.state == GameState.PLAYING:
                        self.player.flap()
                        if self.sfx_jump:
                            self.sfx_jump.play()
                    elif self.state == GameState.GAME_OVER:
                        self.reset_round(full_reset=False)

                if event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                    self.reset_round(full_reset=False)

    def _update(self, dt: float) -> None:
        update_starfield(self.stars, dt, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        if self.state != GameState.PLAYING:
            return

        self.player.update(dt)

        self.pipe_spawn_timer += dt
        if self.pipe_spawn_timer >= self.current_pipe_interval:
            self.pipe_spawn_timer = 0.0
            self.pipes.append(spawn_pipe())

        self._increase_difficulty()

        player_rect, player_mask = self.player.get_collision_snapshot()

        for pipe in self.pipes:
            pipe.update(dt, self.pipe_speed)

            if not pipe.passed and pipe.top_rect.right < player_rect.left:
                pipe.passed = True
                self.score += config.POINTS_PER_PIPE
                self.high_score = max(self.high_score, self.score)

            if pipe.collides_with(player_rect, player_mask):
                self._on_crash()
                return

        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        if player_rect.top <= 0 or player_rect.bottom >= config.SCREEN_HEIGHT:
            self._on_crash()

    def _increase_difficulty(self) -> None:
        target_speed = config.PIPE_SPEED_BASE + self.score * config.PIPE_SPEED_SCORE_MULTIPLIER
        self.pipe_speed = min(config.PIPE_SPEED_MAX, target_speed)

        interval_reduction = self.score * 0.015
        self.current_pipe_interval = max(config.PIPE_SPAWN_MIN, config.PIPE_SPAWN_SECONDS - interval_reduction)

    def _on_crash(self) -> None:
        if self.sfx_hit:
            self.sfx_hit.play()
        self.state = GameState.GAME_OVER
        self.flash_timer = 0.18
        save_high_score(config.HIGH_SCORE_FILE, self.high_score)

    def _render(self) -> None:
        draw_gradient_background(self.screen)
        draw_starfield(self.screen, self.stars)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        self.player.draw(self.screen)

        draw_hud(self.screen, self.score, self.high_score, self.small_font, self.big_font)

        if self.state == GameState.START:
            draw_start_overlay(self.screen, self.title_font, self.body_font)
        elif self.state == GameState.GAME_OVER:
            draw_game_over_overlay(self.screen, self.score, self.high_score, self.title_font, self.body_font)
            if self.flash_timer > 0:
                alpha = int(120 * (self.flash_timer / 0.18))
                flash = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
                flash.fill((255, 90, 120, max(0, min(180, alpha))))
                self.screen.blit(flash, (0, 0))
                self.flash_timer = max(0.0, self.flash_timer - (1 / config.FPS))

        speed_label = self.small_font.render(
            f"Speed x {self.pipe_speed / config.PIPE_SPEED_BASE:.2f}",
            True,
            config.TEXT_ACCENT,
        )
        self.screen.blit(speed_label, (config.SCREEN_WIDTH - speed_label.get_width() - 20, 16))

        pygame.display.flip()
