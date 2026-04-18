#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
AUDIO_DIR = ROOT / "output" / "audio_work" / "free_mixkit_65s"
VIDEO_DIR = ROOT / "output" / "video"
SOURCE_VIDEO = VIDEO_DIR / "student-start-mode-short-88s-max-2160p.mp4"
OUTPUT_V1 = VIDEO_DIR / "student-start-mode-short-88s-audio-final-bundle-refined-v1.mp4"
OUTPUT_STABLE = VIDEO_DIR / "student-start-mode-short-88s-audio-final-bundle-refined.mp4"
SOURCES_MD = VIDEO_DIR / "student-start-mode-short-88s-audio-sources-bundle-refined.md"
EVENTS_MD = VIDEO_DIR / "student-start-mode-short-88s-audio-events-bundle-refined.md"
LICENSE_URL = "https://mixkit.co/license/"


def probe_duration(path: Path) -> float:
    output = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(output)


DEMO_DURATION = probe_duration(SOURCE_VIDEO)


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
    "success_tone": {
        "title": "Success tone",
        "local_name": "sfx-success-tone-2865.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/success/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2865/2865-preview.mp3",
        "role": "approval tone",
    },
    "keyboard_typing": {
        "title": "Typing on a laptop keyboard",
        "local_name": "sfx-typing-on-laptop-keyboard-2531.mp3",
        "page_url": "https://mixkit.co/free-sound-effects/type/",
        "asset_url": "https://assets.mixkit.co/active_storage/sfx/2531/2531-preview.mp3",
        "role": "keyboard typing",
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


EVENTS = [{'time': 0.18,
  'name': 'intro_start',
  'label': 'Intro starts',
  'role': 'intro/start',
  'asset': 'intro_start',
  'trim': 1.25,
  'fade': 0.22,
  'volume': 0.12,
  'tier': 'C'},
 {'time': 4.369,
  'name': 'push_notification',
  'label': 'Push notification appears',
  'role': 'notification',
  'asset': 'notification_pop',
  'trim': 0.42,
  'fade': 0.08,
  'volume': 0.22,
  'tier': 'A'},
 {'time': 11.972,
  'name': 'survey_university_select',
  'label': 'Survey university select',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.16,
  'fade': 0.04,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.05},
 {'time': 12.829,
  'name': 'survey_visa_select',
  'label': 'Survey visa select',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.16,
  'fade': 0.04,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.05},
 {'time': 13.682,
  'name': 'survey_country_select',
  'label': 'Survey country select',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.16,
  'fade': 0.04,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.05},
 {'time': 14.542,
  'name': 'survey_arc_timing_select',
  'label': 'Survey ARC timing select',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.16,
  'fade': 0.04,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.05},
 {'time': 16.0,
  'name': 'survey_need_select_1',
  'label': 'Survey need select 1',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.16,
  'fade': 0.04,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.05},
 {'time': 16.653,
  'name': 'survey_need_select_2',
  'label': 'Survey need select 2',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.16,
  'fade': 0.04,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.05},
 {'time': 15.256,
  'name': 'survey_scroll_2',
  'label': 'Survey scroll',
  'role': 'scroll/transition',
  'asset': 'scroll_sweep',
  'trim': 0.34,
  'fade': 0.09,
  'volume': 0.08,
  'tier': 'C'},
 {'time': 18.109,
  'name': 'survey_submit',
  'label': 'Survey submit',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.16,
  'fade': 0.04,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.05},
 {'time': 22.049,
  'name': 'scenario1_home_banner',
  'label': 'Scenario 1 checklist complete banner',
  'role': 'reveal/info',
  'asset': 'info_reveal',
  'trim': 0.44,
  'fade': 0.1,
  'volume': 0.13,
  'tier': 'B',
  'head_trim': 0.1},
 {'time': 25.521,
  'name': 'scenario1_checklist_tab',
  'label': 'Scenario 1 checklist tab',
  'role': 'tab-switch',
  'asset': 'tab_tick',
  'trim': 0.3,
  'fade': 0.08,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.1},
 {'time': 28.88,
  'name': 'scenario1_calendar_tab',
  'label': 'Scenario 1 smart calendar tab',
  'role': 'tab-switch',
  'asset': 'tab_tick',
  'trim': 0.3,
  'fade': 0.08,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.1},
 {'time': 36.798,
  'name': 'scenario2_checklist_tab',
  'label': 'Scenario 2 checklist tab',
  'role': 'tab-switch',
  'asset': 'tab_tick_alt',
  'trim': 0.3,
  'fade': 0.08,
  'volume': 0.08,
  'tier': 'C',
  'head_trim': 0.06},
 {'time': 41.407,
  'name': 'scenario2_chat_tab',
  'label': 'Scenario 2 chat list tab',
  'role': 'tab-switch',
  'asset': 'tab_tick_alt',
  'trim': 0.3,
  'fade': 0.08,
  'volume': 0.05,
  'tier': 'C',
  'head_trim': 0.06},
 {'time': 42.61,
  'name': 'scenario2_open_chatroom',
  'label': 'Scenario 2 open chat room',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.24,
  'fade': 0.06,
  'volume': 0.07,
  'tier': 'C',
  'head_trim': 0.03},
 {'time': 43.681,
  'name': 'scenario2_typing',
  'label': 'Scenario 2 auto typing',
  'role': 'typing',
  'asset': 'keyboard_typing',
  'trim': 0.56,
  'fade': 0.08,
  'volume': 0.048,
  'tier': 'D',
  'head_trim': 0.0},
 {'time': 44.796,
  'name': 'scenario2_send',
  'label': 'Scenario 2 send message',
  'role': 'send',
  'asset': 'send_cue',
  'trim': 0.14,
  'fade': 0.05,
  'volume': 0.065,
  'tier': 'C',
  'head_trim': 0.0},
 {'time': 47.365,
  'name': 'scenario2_unlock',
  'label': 'Scenario 2 ARC unlock',
  'role': 'unlock/complete',
  'asset': 'success_tone',
  'trim': 0.44,
  'fade': 0.12,
  'volume': 0.17,
  'tier': 'A'},
 {'time': 50.788,
  'name': 'scenario2_next_step_banner',
  'label': 'Scenario 2 next-step banner',
  'role': 'reveal/info',
  'asset': 'info_reveal_alt',
  'trim': 0.3,
  'fade': 0.1,
  'volume': 0.09,
  'tier': 'B',
  'head_trim': 0.06},
 {'time': 57.975,
  'name': 'scenario3_my_page_tab',
  'label': 'Scenario 3 My Page tab',
  'role': 'tab-switch',
  'asset': 'tab_tick',
  'trim': 0.3,
  'fade': 0.08,
  'volume': 0.05,
  'tier': 'C',
  'head_trim': 0.1},
 {'time': 60.433,
  'name': 'scenario3_open_scholarship',
  'label': 'Scenario 3 open scholarship item',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.24,
  'fade': 0.06,
  'volume': 0.08,
  'tier': 'C'},
 {'time': 62.473,
  'name': 'scenario3_updated_checklist_reveal',
  'label': 'Scenario 3 updated checklist reveal',
  'role': 'reveal/info',
  'asset': 'info_reveal',
  'trim': 0.34,
  'fade': 0.1,
  'volume': 0.1,
  'tier': 'B',
  'head_trim': 0.1},
 {'time': 71.809,
  'name': 'scenario4_open_chatroom',
  'label': 'Scenario 4 open chat room',
  'role': 'tap/select',
  'asset': 'select_click',
  'trim': 0.24,
  'fade': 0.06,
  'volume': 0.06,
  'tier': 'C',
  'head_trim': 0.03},
 {'time': 72.879,
  'name': 'scenario4_typing',
  'label': 'Scenario 4 auto typing',
  'role': 'typing',
  'asset': 'keyboard_typing',
  'trim': 1.12,
  'fade': 0.08,
  'volume': 0.048,
  'tier': 'D',
  'head_trim': 0.0},
 {'time': 74.556,
  'name': 'scenario4_send',
  'label': 'Scenario 4 send message',
  'role': 'send',
  'asset': 'send_cue',
  'trim': 0.14,
  'fade': 0.05,
  'volume': 0.065,
  'tier': 'C',
  'head_trim': 0.0},
 {'time': 75.128,
  'name': 'scenario4_ai_answer_pop',
  'label': 'Scenario 4 AI answer appears',
  'role': 'notification',
  'asset': 'notification_pop',
  'trim': 0.4,
  'fade': 0.08,
  'volume': 0.16,
  'tier': 'B',
  'head_trim': 0.05},
 {'time': 77.498,
  'name': 'scenario4_source_reveal',
  'label': 'Scenario 4 source reveal',
  'role': 'reveal/info',
  'asset': 'info_reveal_alt',
  'trim': 0.38,
  'fade': 0.1,
  'volume': 0.12,
  'tier': 'B',
  'head_trim': 0.08}]


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
    if not (24 <= len(EVENTS) <= 28):
        raise ValueError(f"expected 24-28 events, got {len(EVENTS)}")
    min_spacing_by_asset = {"select_click": 0.5}
    grouped: dict[str, list[float]] = {}
    for event in EVENTS:
        grouped.setdefault(event["asset"], []).append(event["time"])
    for asset_name, times in grouped.items():
        ordered = sorted(times)
        min_spacing = min_spacing_by_asset.get(asset_name, 0.8)
        for earlier, later in zip(ordered, ordered[1:]):
            if later - earlier < min_spacing:
                raise ValueError(
                    f"asset {asset_name} reused within {min_spacing:.1f}s at {earlier:.2f}/{later:.2f}"
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
        f"afade=t=out:st={max(DEMO_DURATION - 6.5, 0.0):.3f}:d=6.5"
        "[bgm]"
    )

    for index, event in enumerate(EVENTS):
        asset_label = label_pool[event["asset"]].pop(0)
        delay_ms = int(round(event["time"] * 1000))
        head_trim = event.get("head_trim", 0.0)
        tail_trim = head_trim + event["trim"]
        fade_start = max(event["trim"] - event["fade"], 0.01)
        filter_parts.append(
            f"{asset_label}"
            f"atrim={head_trim:.3f}:{tail_trim:.3f},asetpts=N/SR/TB,"
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
        str(OUTPUT_V1),
    ]
    subprocess.run(command, check=True)
    shutil.copy2(OUTPUT_V1, OUTPUT_STABLE)


def write_sources_md() -> None:
    audible_events = [event for event in EVENTS if event["volume"] > 0.0]
    used_asset_names = ["bgm"] + list(
        dict.fromkeys(event["asset"] for event in audible_events)
    )
    lines = [
        "# 88s Audio Sources (Bundle Refined)",
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
        used_in = [
            event["label"] for event in audible_events if event["asset"] == asset_name
        ]
        lines.extend(
            [
                f"- {asset['title']}",
                f"  - Role: {asset['role']}",
                f"  - Source page: {asset['page_url']}",
                f"  - Asset URL: {asset['asset_url']}",
                f"  - Local file: ../audio_work/free_mixkit_65s/{asset['local_name']}",
                f"  - Used in: {', '.join(used_in)}",
            ]
        )
    SOURCES_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_events_md() -> None:
    lines = [
        "# 88s Audio Event Map (Bundle Refined)",
        "",
        "Applied target",
        "- `student-start-mode-short-88s-audio-final-bundle-refined-v1.mp4`",
        "- `student-start-mode-short-88s-audio-final-bundle-refined.mp4`",
        "",
        "Coverage",
        f"- Total interaction cues: {len(EVENTS)}",
        "- Goal: preserve the 65s bundle-refined mix character while re-anchoring it to the 88s timing",
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
