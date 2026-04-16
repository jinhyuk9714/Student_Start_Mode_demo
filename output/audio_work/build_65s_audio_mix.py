#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path("/Users/sungjh/Projects/SSM/HanaEZ_Student_Start_Mode_upstream")
AUDIO_DIR = ROOT / "output" / "audio_work" / "free_mixkit_65s"
VIDEO_DIR = ROOT / "output" / "video"
SOURCE_VIDEO = VIDEO_DIR / "student-start-mode-short-65s-max-2160p.mp4"
OUTPUT_V3 = VIDEO_DIR / "student-start-mode-short-65s-audio-final-v3.mp4"
OUTPUT_FINAL = VIDEO_DIR / "student-start-mode-short-65s-audio-final.mp4"
SOURCES_MD = VIDEO_DIR / "student-start-mode-short-65s-audio-sources.md"
EVENTS_MD = VIDEO_DIR / "student-start-mode-short-65s-audio-events.md"
LICENSE_URL = "https://mixkit.co/license/"
DEMO_DURATION = 64.52


ASSETS = {
    "bgm": {
        "title": "Driving Ambition",
        "local_name": "bgm-driving-ambition-32.mp3",
        "page_url": "https://mixkit.co/free-stock-music/mood/confident/",
        "asset_url": "https://assets.mixkit.co/music/32/32.mp3",
        "role": "background music",
    },
    "intro_start": {
        "title": "Software interface start",
        "local_name": "sfx-interface-start-2574.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/alerts/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2574/2574-preview.mp3",
        "role": "intro/start",
    },
    "notification_pop": {
        "title": "Message pop alert",
        "local_name": "sfx-message-pop-2354.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/alerts/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2354/2354-preview.mp3",
        "role": "notification",
    },
    "soft_tap": {
        "title": "Interface option select",
        "local_name": "sfx-interface-option-select-2573.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/interface/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2573/2573-preview.mp3",
        "role": "soft tap",
    },
    "select_click": {
        "title": "Select click",
        "local_name": "sfx-select-click-1109.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/interface/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/1109/1109-preview.mp3",
        "role": "tap/select",
    },
    "tab_tick": {
        "title": "Page forward single chime",
        "local_name": "sfx-page-forward-chime-1107.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/interface/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/1107/1107-preview.mp3",
        "role": "tab-switch tick",
    },
    "tab_tick_alt": {
        "title": "Page back chime",
        "local_name": "sfx-page-back-chime-1108.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/interface/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/1108/1108-preview.mp3",
        "role": "alternate tab-switch tick",
    },
    "send_cue": {
        "title": "Confirmation tone",
        "local_name": "sfx-confirmation-tone-2867.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/notification/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2867/2867-preview.mp3",
        "role": "send cue",
    },
    "info_reveal": {
        "title": "High tech bleep confirmation",
        "local_name": "sfx-high-tech-bleep-confirmation-2520.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/high-tech/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2520/2520-preview.mp3",
        "role": "info reveal shimmer",
    },
    "info_reveal_alt": {
        "title": "Digital quick tone",
        "local_name": "sfx-digital-quick-tone-2866.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/alerts/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2866/2866-preview.mp3",
        "role": "alternate info reveal shimmer",
    },
    "scroll_sweep": {
        "title": "Explainer video pops whoosh light pop",
        "local_name": "sfx-explainer-whoosh-light-pop-3005.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/whoosh/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/3005/3005-preview.mp3",
        "role": "soft transition sweep",
    },
    "unlock": {
        "title": "Electronic lock success beeps",
        "local_name": "sfx-unlock-success-2852.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/success/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2852/2852-preview.mp3",
        "role": "unlock/complete",
    },
    "source_reveal": {
        "title": "Clear announce tones",
        "local_name": "sfx-clear-announce-tones-2861.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/alerts/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2861/2861-preview.mp3",
        "role": "strong source reveal",
    },
}


EVENTS = [
    {
        "time": 0.18,
        "name": "intro_start",
        "label": "Intro starts",
        "role": "intro/start",
        "asset": "intro_start",
        "trim": 1.25,
        "fade": 0.22,
        "volume": 0.14,
        "tier": "C",
    },
    {
        "time": 1.05,
        "name": "push_notification",
        "label": "Push notification appears",
        "role": "notification",
        "asset": "notification_pop",
        "trim": 0.42,
        "fade": 0.08,
        "volume": 0.24,
        "tier": "A",
    },
    {
        "time": 7.07,
        "name": "survey_university_select",
        "label": "Survey university select",
        "role": "tap/select",
        "asset": "soft_tap",
        "trim": 0.20,
        "fade": 0.05,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 9.02,
        "name": "survey_arc_timing_select",
        "label": "Survey ARC timing select",
        "role": "tap/select",
        "asset": "soft_tap",
        "trim": 0.20,
        "fade": 0.05,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 11.33,
        "name": "survey_scroll_2",
        "label": "Survey scroll",
        "role": "scroll/transition",
        "asset": "scroll_sweep",
        "trim": 0.34,
        "fade": 0.09,
        "volume": 0.08,
        "tier": "C",
    },
    {
        "time": 11.89,
        "name": "survey_submit",
        "label": "Survey submit",
        "role": "tap/select",
        "asset": "select_click",
        "trim": 0.24,
        "fade": 0.06,
        "volume": 0.12,
        "tier": "C",
    },
    {
        "time": 14.80,
        "name": "scenario1_home_banner",
        "label": "Scenario 1 checklist complete banner",
        "role": "reveal/info",
        "asset": "info_reveal",
        "trim": 0.44,
        "fade": 0.10,
        "volume": 0.16,
        "tier": "B",
    },
    {
        "time": 16.60,
        "name": "scenario1_checklist_tab",
        "label": "Scenario 1 checklist tab",
        "role": "tab-switch",
        "asset": "tab_tick",
        "trim": 0.30,
        "fade": 0.08,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 19.51,
        "name": "scenario1_calendar_tab",
        "label": "Scenario 1 smart calendar tab",
        "role": "tab-switch",
        "asset": "tab_tick",
        "trim": 0.30,
        "fade": 0.08,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 25.39,
        "name": "scenario2_checklist_tab",
        "label": "Scenario 2 checklist tab",
        "role": "tab-switch",
        "asset": "tab_tick_alt",
        "trim": 0.30,
        "fade": 0.08,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 27.22,
        "name": "scenario2_calendar_tab",
        "label": "Scenario 2 calendar tab",
        "role": "tab-switch",
        "asset": "tab_tick_alt",
        "trim": 0.30,
        "fade": 0.08,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 29.45,
        "name": "scenario2_chat_tab",
        "label": "Scenario 2 chat list tab",
        "role": "tab-switch",
        "asset": "tab_tick_alt",
        "trim": 0.30,
        "fade": 0.08,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 30.43,
        "name": "scenario2_open_chatroom",
        "label": "Scenario 2 open chat room",
        "role": "tap/select",
        "asset": "select_click",
        "trim": 0.24,
        "fade": 0.06,
        "volume": 0.11,
        "tier": "C",
    },
    {
        "time": 32.18,
        "name": "scenario2_send",
        "label": "Scenario 2 send message",
        "role": "send",
        "asset": "send_cue",
        "trim": 0.30,
        "fade": 0.07,
        "volume": 0.11,
        "tier": "C",
    },
    {
        "time": 33.96,
        "name": "scenario2_unlock",
        "label": "Scenario 2 ARC unlock",
        "role": "unlock/complete",
        "asset": "unlock",
        "trim": 1.02,
        "fade": 0.18,
        "volume": 0.21,
        "tier": "A",
    },
    {
        "time": 37.47,
        "name": "scenario2_next_step_banner",
        "label": "Scenario 2 next-step banner",
        "role": "reveal/info",
        "asset": "info_reveal_alt",
        "trim": 0.42,
        "fade": 0.10,
        "volume": 0.15,
        "tier": "B",
    },
    {
        "time": 41.82,
        "name": "scenario3_my_page_tab",
        "label": "Scenario 3 My Page tab",
        "role": "tab-switch",
        "asset": "tab_tick",
        "trim": 0.30,
        "fade": 0.08,
        "volume": 0.09,
        "tier": "C",
    },
    {
        "time": 43.05,
        "name": "scenario3_my_page_scroll",
        "label": "Scenario 3 My Page scroll",
        "role": "scroll/transition",
        "asset": "scroll_sweep",
        "trim": 0.34,
        "fade": 0.09,
        "volume": 0.08,
        "tier": "C",
    },
    {
        "time": 43.93,
        "name": "scenario3_open_scholarship",
        "label": "Scenario 3 open scholarship item",
        "role": "tap/select",
        "asset": "select_click",
        "trim": 0.24,
        "fade": 0.06,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 46.14,
        "name": "scenario3_updated_checklist_reveal",
        "label": "Scenario 3 updated checklist reveal",
        "role": "reveal/info",
        "asset": "info_reveal",
        "trim": 0.42,
        "fade": 0.10,
        "volume": 0.15,
        "tier": "B",
    },
    {
        "time": 51.57,
        "name": "scenario4_chat_list_tab",
        "label": "Scenario 4 chat list tab",
        "role": "tab-switch",
        "asset": "tab_tick_alt",
        "trim": 0.30,
        "fade": 0.08,
        "volume": 0.10,
        "tier": "C",
    },
    {
        "time": 52.55,
        "name": "scenario4_open_chatroom",
        "label": "Scenario 4 open chat room",
        "role": "tap/select",
        "asset": "select_click",
        "trim": 0.24,
        "fade": 0.06,
        "volume": 0.11,
        "tier": "C",
    },
    {
        "time": 54.85,
        "name": "scenario4_send",
        "label": "Scenario 4 send message",
        "role": "send",
        "asset": "send_cue",
        "trim": 0.30,
        "fade": 0.07,
        "volume": 0.11,
        "tier": "C",
    },
    {
        "time": 55.70,
        "name": "scenario4_ai_answer_pop",
        "label": "Scenario 4 AI answer appears",
        "role": "notification",
        "asset": "notification_pop",
        "trim": 0.40,
        "fade": 0.08,
        "volume": 0.18,
        "tier": "B",
    },
    {
        "time": 56.68,
        "name": "scenario4_answer_scroll",
        "label": "Scenario 4 answer scroll",
        "role": "scroll/transition",
        "asset": "scroll_sweep",
        "trim": 0.34,
        "fade": 0.09,
        "volume": 0.08,
        "tier": "C",
    },
    {
        "time": 59.88,
        "name": "scenario4_source_reveal",
        "label": "Scenario 4 source reveal",
        "role": "reveal/info",
        "asset": "source_reveal",
        "trim": 0.90,
        "fade": 0.16,
        "volume": 0.20,
        "tier": "A",
    },
]


def ensure_assets() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    for asset in ASSETS.values():
        path = AUDIO_DIR / asset["local_name"]
        if path.exists():
            continue
        request = Request(asset["asset_url"], headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=30) as response, path.open("wb") as output:
            output.write(response.read())


def validate_events() -> None:
    if not (24 <= len(EVENTS) <= 26):
        raise ValueError(f"expected 24-26 events, got {len(EVENTS)}")
    grouped: dict[str, list[float]] = {}
    for event in EVENTS:
        grouped.setdefault(event["asset"], []).append(event["time"])
    for asset_name, times in grouped.items():
        ordered = sorted(times)
        for earlier, later in zip(ordered, ordered[1:]):
            if later - earlier < 0.8:
                raise ValueError(
                    f"asset {asset_name} reused within 0.8s at {earlier:.2f}/{later:.2f}"
                )


def build_bgm_expression() -> str:
    base = 0.102
    windows = []
    for event in EVENTS:
        if event["tier"] == "A":
            windows.append((event["time"] - 0.10, event["time"] + 0.36, 0.026))
        elif event["tier"] == "B":
            windows.append((event["time"] - 0.08, event["time"] + 0.30, 0.018))
    expr = f"{base:.3f}"
    for start, end, amount in windows:
        start = max(0.0, start)
        end = min(DEMO_DURATION, end)
        expr += f"-{amount:.3f}*between(t,{start:.3f},{end:.3f})"
    return f"max(0.060,{expr})"


def build_filter_script() -> str:
    input_order = list(ASSETS)
    counts = Counter(event["asset"] for event in EVENTS)
    filter_parts = []
    label_pool: dict[str, list[str]] = {}

    for input_index, asset_name in enumerate(input_order, start=1):
        if asset_name == "bgm":
            continue
        total = counts[asset_name]
        if total == 0:
            continue
        labels = "".join(f"[{asset_name}{i}]" for i in range(total))
        filter_parts.append(f"[{input_index}:a]asplit={total}{labels}")
        label_pool[asset_name] = [f"[{asset_name}{i}]" for i in range(total)]

    bgm_expr = build_bgm_expression()
    filter_parts.append(
        "[1:a]"
        f"atrim=0:{DEMO_DURATION},asetpts=N/SR/TB,volume='{bgm_expr}',"
        "afade=t=in:st=0:d=2.0,"
        "afade=t=out:st=58.0:d=6.52"
        "[bgm]"
    )

    for index, event in enumerate(EVENTS):
        asset_label = label_pool[event["asset"]].pop(0)
        delay_ms = int(round(event["time"] * 1000))
        fade_start = max(event["trim"] - event["fade"], 0.01)
        filter_parts.append(
            f"{asset_label}"
            f"atrim=0:{event['trim']},asetpts=N/SR/TB,"
            "afade=t=in:st=0:d=0.01,"
            f"afade=t=out:st={fade_start:.3f}:d={event['fade']:.3f},"
            f"volume={event['volume']:.3f},"
            f"adelay={delay_ms}|{delay_ms}"
            f"[e{index}]"
        )

    mix_inputs = "[bgm]" + "".join(f"[e{index}]" for index in range(len(EVENTS)))
    filter_parts.append(
        f"{mix_inputs}"
        f"amix=inputs={len(EVENTS) + 1}:normalize=0:dropout_transition=0,"
        "acompressor=threshold=-20dB:ratio=2.0:attack=5:release=115:makeup=1.4,"
        "alimiter=limit=0.92:level=disabled[aout]"
    )
    return ";\n".join(filter_parts)


def render_outputs() -> None:
    input_order = list(ASSETS)
    command = ["ffmpeg", "-y", "-i", str(SOURCE_VIDEO)]
    for asset_name in input_order:
        command += ["-i", str(AUDIO_DIR / ASSETS[asset_name]["local_name"])]

    filter_script = build_filter_script()
    with tempfile.NamedTemporaryFile("w", suffix=".ffscript", delete=False) as handle:
        handle.write(filter_script)
        filter_path = handle.name

    command += [
        "-filter_complex_script",
        filter_path,
        "-map",
        "0:v:0",
        "-map",
        "[aout]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "256k",
        "-movflags",
        "+faststart",
        str(OUTPUT_V3),
    ]
    subprocess.run(command, check=True)
    shutil.copy2(OUTPUT_V3, OUTPUT_FINAL)


def write_sources_md() -> None:
    used_asset_names = ["bgm"] + list(dict.fromkeys(event["asset"] for event in EVENTS))
    lines = [
        "# 65s Audio Sources",
        "",
        "License basis",
        f"- Mixkit License: {LICENSE_URL}",
        "",
        "Music",
    ]
    music = ASSETS["bgm"]
    lines.extend(
        [
            f"- {music['title']}",
            f"  - Role: {music['role']}",
            f"  - Source page: {music['page_url']}",
            f"  - Asset URL: {music['asset_url']}",
            f"  - Local file: ../audio_work/free_mixkit_65s/{music['local_name']}",
        ]
    )
    lines.extend(["", "Sound effects"])
    for asset_name in used_asset_names:
        if asset_name == "bgm":
            continue
        asset = ASSETS[asset_name]
        lines.extend(
            [
                f"- {asset['title']}",
                f"  - Role: {asset['role']}",
                f"  - Source page: {asset['page_url']}",
                f"  - Asset URL: {asset['asset_url']}",
                f"  - Local file: ../audio_work/free_mixkit_65s/{asset['local_name']}",
            ]
        )
    SOURCES_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_events_md() -> None:
    lines = [
        "# 65s Audio Event Map",
        "",
        "Applied target",
        "- `student-start-mode-short-65s-audio-final-v3.mp4`",
        "- `student-start-mode-short-65s-audio-final.mp4`",
        "",
        "Coverage",
        f"- Total interaction cues: {len(EVENTS)}",
        "- Goal: quieter UI bed, stronger meaning hierarchy, no focus-only cues",
        "",
        "| Time (s) | Event | Role | Asset |",
        "| --- | --- | --- | --- |",
    ]
    for event in EVENTS:
        lines.append(
            f"| {event['time']:.2f} | {event['label']} | {event['role']} | {ASSETS[event['asset']]['title']} |"
        )
    EVENTS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_assets()
    validate_events()
    render_outputs()
    write_sources_md()
    write_events_md()


if __name__ == "__main__":
    main()
