# Performance reports

Hardware, game, build and FPS reports collected from the Eglantine Discord, the Ocarina of Time Reddit threads and the Orchid README. These are user reports, not benchmarks. The same GPU can produce very different numbers with another driver, game version, settings or shader cache.

Charts and the game-by-setup coverage matrix are in [coverage](COVERAGE.md). The normalized data is in [`data/performance-reports.json`](../data/performance-reports.json).

`Not stated` means the report did not include that field. `Unspecified` means no build number was given. Rows are grouped by game, with the most complete configs first.

## What the reports suggest

- CPU single-core speed matters a lot. OoT remake runs at 54-60 FPS on a 9800X3D, 20-24 FPS on an i3-10100, and an RTX 2070 with a 9800X3D beats a 7900 XTX with a 13400F.
- Build choice can double performance. Mario Kart World went from about 23 FPS on build 122 to 40+ FPS on build 135 for one tester.
- Compatibility fixes are not the same as speed. PokeDinner documents DK rendering fixes; ZendNevs documents higher average FPS with correct game speed.
- 8 GB of RAM can boot a game, but it crashes when other apps use memory. 16 GB is a practical floor, 32 GB is safer.
- 4 GB of VRAM can run games at low settings; 6 GB and up is more comfortable at higher resolution.
- A fast GPU alone does not guarantee 60 FPS. Emulator builds and drivers decide a large part of the result.

## Mario Kart World

MKW has its own page because the report volume is much larger: [Mario Kart World notes](MKW.md). It covers settings, build regressions and nearly 50 configs.

A few representative rows:

| Build | CPU | GPU | RAM | Performance | Notes | Source |
|---|---|---|---|---|---|---|
| v2.0.5 | 5500X3D | RTX 4070 | 16 GB | 56 FPS average, 44-50 in the lowest 10% | 1x handheld, DynamicFPS; not locked 60 | ZendNevs release notes |
| Orchid v0.7.2 | 5800X3D | RX 9070 XT | 32 GB | 30-40 FPS | Linux, Mesa RADV git; asset glitches | Orchid README |
| build 122 to 135 | R5 7600 | RX 7800 XT | not stated | 23 average to 40+ FPS | Windows 11 | Discord, 2 Nov |
| unspecified | i5-14400F | RTX 4060 | 32 GB DDR4 | 43-50 FPS, 60 only in menus and intro | NVMe | Discord, 4 Nov |
| unspecified | i5-6500 | Quadro P1000 | 16 GB DDR4 | 5-25 FPS, heavy stutter | | Discord, 31 Oct |

## Splatoon Raiders

| Build | CPU | GPU | RAM | Performance | Notes | Source |
|---|---|---|---|---|---|---|
| v0.1.0-rc1 PGO | i7-4790K | GTX 980 4 GB | 32 GB DDR3 2133 | about 50 FPS in the first hub after shaders | 1.0 scale, fast, Vulkan; 2.3 GB VRAM | Discord, 5 Nov |
| unspecified | Steam Deck APU | Steam Deck APU | 16 GB | playable with lighting bugs | better than MKW at 15-20 FPS | Discord, 1-2 Nov |

## Pokemon Pokopia

Pokopia has its own page because the workarounds matter: [Pokopia notes](POKOPIA.md). It covers the black sky, the 120fps mod, memory limits and 13 configs.

A few representative rows:

| Build | CPU | GPU | RAM | Performance | Notes | Source |
|---|---|---|---|---|---|---|
| v2.0.5 | 5500X3D | RTX 4070 | 16 GB | 60 FPS game, 116-120 display with frame generation | startup test only, about one minute | ZendNevs release notes |
| notsapinho | 12th-gen i5 2.5 GHz | RTX 4060 Mobile 6 GB | 16 GB | 80+ FPS | accurate, docked, 120fps mod | Discord, 4 Nov |
| PokeDinner, unspecified | Ryzen 7 7700X | RX 6700 XT | not stated | 50-60 FPS, feels like 40-50 | accurate GPU | Discord, 1 Nov |
| build 135 | not stated | GTX 1080 | not stated | 60 FPS with stutter, black sky, no audio | | Discord, 2 Nov |
| Steam Deck | Steam Deck APU | Steam Deck APU | 16 GB | 30-40 FPS, later 25-30 | uneven frame pacing | Discord, 2 Nov |

## Donkey Kong Bananza

DK has its own page because the workarounds matter as much as the FPS: [Donkey Kong Bananza notes](DONKEY-KONG.md). It covers the 30 FPS cap, DynamicFPS, terrain and purple-screen issues, and about 20 configs.

A few representative rows:

| Build | CPU | GPU | RAM | Performance | Notes | Source |
|---|---|---|---|---|---|---|
| ZendNevs v2.0.5 | 5500X3D | RTX 4070 | 16 GB | 33 FPS average, 20.6 low, 99% game speed | 1x handheld; v2.0.1 gave 40 FPS at 83% speed | ZendNevs release notes |
| PokeDinner 2.5 | Ryzen 5 9600X | RX 6800 16 GB | 16 GB DDR5 | 30 FPS option, no glitches, smooth | full AMD system | Discord, 4 Nov |
| Selevet perf 3 | 5700X3D | RTX 5070 Ti | 32 GB | 30 FPS cap, 60 with smooth motion | default 0.5x, 1x works | Discord, 1 Nov |
| v0.1.0-rc1 PGO | 7700X | RX 7900 XTX | not stated | 30+ FPS, purple screen absent, music and rumble present | Linux Nobara | Discord, 5 Nov |
| 202 | 7700X | RX 7900 XTX | not stated | choppy with texture glitches; purple screen fixed by Photo Mode | Linux Nobara | Discord, 4 Nov |

## Yoshi and the Mysterious Book

| Build | CPU | GPU | RAM | Performance | Notes | Source |
|---|---|---|---|---|---|---|
| v0.1.0-rc1 PGO | 7700X | RX 7900 XTX | not stated | 45-60 FPS, green glitch, cutscene skipped, hard crash on Plasma/X11 | Linux Nobara | Discord, 5 Nov |
| 202 | 7700X | RX 7900 XTX | not stated | choppy, loads the cutscene | Linux Nobara | Discord, 4 Nov |
| unspecified | not stated | not stated | not stated | reports 60 FPS but the screen stays black outside menus | audio works | Discord, 3 Nov |

## Zelda: Ocarina of Time remake

All rows use Lichii build 80 unless noted.

| Build | CPU | GPU | RAM | Performance | Notes | Source |
|---|---|---|---|---|---|---|
| Lichii build 80 | 9800X3D | not stated | not stated | 54-60 FPS | heavy bloom, sunrays, flicker | Reddit, 5 Nov |
| Lichii build 80 | 9800X3D | RTX 2070 | not stated | 60 FPS | | Reddit, 5 Nov |
| Lichii build 80 | not stated | RTX 3080 10 GB | not stated | 40-50 FPS in Kokiri, 40-60 in the Deku Tree | | Reddit, 5 Nov |
| Lichii build 80 | i3-10100 | RTX 3060 12 GB | 24 GB | 20-24 FPS in Kokiri Forest | | Reddit, 5 Nov |
| Lichii build 80 | i5-11400H | RTX 2050 | 16 GB DDR4 | 20 FPS | | Reddit, 5 Nov |
| Lichii build 80 | 7800X3D | RX 580 | 32 GB | 15 FPS | | Reddit, 5 Nov |
| Lichii build 80 | 13400F | RX 7900 XTX | not stated | same low FPS as the 20-24 group | exact number not stated | Reddit, 5 Nov |
| Lichii build 80 | 14th-gen i7 | RTX 4070 Ti | not stated | emulator-bound, no FPS given | | Reddit, 5 Nov |
| Eglantine v0.1.0-rc1 | 7700X | RX 7900 XTX | not stated | infinite loading | | Discord, 5 Nov |

Orchid v0.7.3 and v0.7.4 fix OoT exposure, fog and vegetation. There is no OoT FPS report for Orchid yet. The Reddit comment that called performance questionable also said the build had not been tried.

## Other games

| Game | Build | CPU | GPU | RAM | Performance | Notes | Source |
|---|---|---|---|---|---|---|---|
| Mario Tennis Fever | Orchid v0.7.2 | 5800X3D | RX 9070 XT | 32 GB | 60 FPS | Linux, Mesa RADV git | Orchid README |
| Super Mario Bros. Wonder | Orchid v0.7.2 | 5800X3D | RX 9070 XT | 32 GB | 60 FPS | Linux, Mesa RADV git | Orchid README |
| Hyrule Warriors: Age of Imprisonment | unspecified | not stated | not stated | not stated | boots, rendering is black | | Discord, 2 Nov |
| Star Fox | 202, rc1 | 7700X | RX 7900 XTX | not stated | infinite loading | | Discord, 4-5 Nov |
| Fire Emblem Fortune's Weave | 202, rc1 | 7700X | RX 7900 XTX | not stated | black screen then crash | AMD; DLSS attempt then failed FSR fallback | Discord, 4-5 Nov |
| Orbitals | 202, rc1 | 7700X | RX 7900 XTX | not stated | 3-10 FPS, black screen | | Discord, 5 Nov |
| Super Mario Bros. Wonder | NUP | not stated | not stated | not stated | DLC not working after NUP conversion | | Discord, 2 Nov |
| Switch Sports | unspecified | not stated | not stated | not stated | limited progress | | Discord, 1 Nov |
| Kirby Air Riders | unspecified | not stated | not stated | not stated | unstable, runs | | Discord, 2 Nov |

## Corrections

- Donkey Kong Bananza: PokeDinner was the first pick because its release notes target DK rendering. That is compatibility work, not a performance result. ZendNevs documents about 33 FPS average at 99% game speed, and community feedback says it is the better DK pick. The first pick is now ZendNevs, with PokeDinner as the compatibility option.
- ZendNevs was described as "only tested on Mario Kart World". The v2.0.5 notes also cover Donkey Kong Bananza and Pokopia startup.
- "3 builds in 1" means Eglantine build-104, PokeDinner and Selevet Eglantine merged into one build, not three separate executables.
- Mario Kart World: SmileyTatsu was the only first pick. ZendNevs now shares the pick because it documents about 56 FPS average. The results are not directly comparable: SmileyTatsu is a community claim, ZendNevs is a documented run on one PC.
- Pokopia: a tester suspected PokeDinner is not the best, but said they did not test it. The first pick stays notsapinho.

## Missing data

Most Discord reports do not include the GPU driver, game version or 1% lows. A row with `not stated` is incomplete, not a controlled result. Reports that only said "60 FPS" without a game or hardware were left out, as were messages about obtaining games or keys.

## Sources

- Eglantine Discord `#discussion`, 30 Oct to 5 Nov 2026. The export is local and is not committed.
- [ZendNevs v2.0.5 release notes](https://github.com/ZendNevs/Eglantine-ZendNevs/releases/tag/zendnevs-v2.0.5) for the documented MKW, DK and Pokopia results.
- [Mario Kart World notes](MKW.md) for the full MKW table, settings and build notes.
- [Donkey Kong Bananza notes](DONKEY-KONG.md) for the full DK table, 30 FPS and DynamicFPS workarounds, and terrain issues.
- [Pokopia notes](POKOPIA.md) for the full Pokopia table, black sky and 120fps workarounds, and memory limits.
- Ocarina of Time Reddit threads, 5 Nov 2026. Usernames are not reproduced here.
- [Orchid README](https://github.com/MythosOfs/Orchid) for the documented 5800X3D and RX 9070 XT results.
- [Orchid releases](https://github.com/MythosOfs/Orchid/releases) for the OoT exposure, fog and vegetation fixes.
