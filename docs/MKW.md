# Mario Kart World notes

Reports from public community posts between 30 Oct and 5 Nov 2026, plus the documented ZendNevs and Orchid results already used in the main guide. This page keeps the performance reports and settings that matter.

These are user reports, not benchmarks. A build that works for one GPU can fail on another, and the same config can lose or gain 20 FPS between two builds.

## Settings that matter

- Handheld and docked can differ a lot. One 780M iGPU user got 60 FPS handheld and 40 docked; other users run docked for better results. Test both before changing anything else.
- Fast and accurate are not just quality presets. On some AMD systems, fast removes trees, cacti and other foliage, while accurate shows them but flickers. Check the visual result, not only the FPS.
- Resolution scale is the quickest win. Reports use 0.25x, 0.5x, 0.75x, 1x and 2x. 0.5x is common on low-end GPUs; one RX 9070 XT report showed 20 FPS at 2x resolution.
- The 30 FPS mod or 30 FPS cap is the usual workaround for low-end hardware. Several users report normal game speed at 30 FPS, while running above 30 can make the game run faster than normal. Dynamic FPS is the newer alternative.
- Frame generation is only useful when the base game is near 60 FPS. Below 50 FPS it adds latency and feels bad; SmileyTatsu said frame generation has no priority because of this.
- Shader cache matters. The first minutes stutter while pipelines compile. Do not benchmark a cold run.
- RAM and pagefile matter. 8 GB can boot the game but crashes when other apps use memory. 16 GB is a practical floor, 32 GB is safer. Early builds had memory leaks and used 20 GB or more.
- PGO builds can crash or load slowly for some users. Use the MSVC or non-PGO build if PGO fails.

## Build notes

- Builds 109, 113 and 116: 109 was called the most stable by one tester; 113 worked well on an RX 6650 XT; 116 gave 60 FPS on an RX 6800 XT but 12-15 FPS on an RTX 3060.
- Build 122 to 135: one RX 7800 XT user went from about 23 FPS to 40+ FPS. Build 135 also added NUP metadata.
- Build 167 and 168: 167 gave 30-40 FPS on an RX 6650 XT; 168 dropped to 20-30 FPS for the same user.
- Build 196: last stable build for one tester, 55-60 FPS on an Intel Ultra 255HX.
- Builds 202 to 212: one tester reports force-closes and one third of the FPS; another says 212 works after a rebuild. Keep a known-good build.
- SmileyTatsu build 11 and 12: build 11 gave 45-50 FPS average on an RX 7800 XT; build 12 was almost locked 60 on AMD when docked for another user.
- ZendNevs v2.0.5: 56 FPS average and 44-50 in the lowest 10% on a 5500X3D and RTX 4070. This is a release-note claim from a 2-commit, unlicensed repo.
- PokeDinner: 60 FPS at 270p on an RX 9070 XT in one report; 25-30 FPS in races on an RTX 3050 laptop in another.
- Selevet Eglantine: one user on an older Zen CPU gained about 8 FPS over the build in community reports.

## Complete configs

| Date | Build | CPU | GPU | RAM | Performance | Notes |
|---|---|---|---|---|---|---|
| 4 Nov | Eglantine build 212 PGO | Steam Deck APU | Steam Deck APU | 16 GB | unplayable, very bad stutter | community; did not start a race |
| 3 Nov | unspecified | i7-14700K | RTX 5070 | 32 GB | 60 FPS 98% of the time | community; no flicker or dropped frames; fork not named |
| 3 Nov | unspecified | Ryzen 5 3600 | GTX 1660 Super | 16 GB | 34-45 FPS | community; Mario Circuit; fork not named |
| 3 Nov | unspecified | Ryzen 7 2700 | RTX 4060 8 GB | 32 GB | close to 30 FPS, unstable frametimes | community; fork not named |
| 3 Nov | ZendNevs v2.0.5 | 5500X3D | RTX 4070 | 16 GB | 56 FPS average, 44-50 in the lowest 10% | release notes; 2-commit repo; 1x handheld, DynamicFPS, not locked 60 |
| 5 Nov | Orchid v0.7.2 | 5800X3D | RX 9070 XT | 32 GB | 30-40 FPS | release notes; Linux, Mesa RADV git; asset glitches |
| 31 Oct | unspecified | i7-13620H | RTX 4070 Laptop | 16 GB DDR5 | 43 FPS | community preset, handheld |
| 31 Oct | unspecified | Ryzen 5 5600 | RTX 3060 Ti | 16 GB DDR4 | 5-15 FPS | lowest settings, 0.5x resolution |
| 31 Oct | unspecified | Core Ultra 9 185H | RTX 4070 Laptop | 32 GB | under 15 FPS |  |
| 31 Oct | unspecified | i5-14600KF | RTX 3060 12 GB | 16 GB | 30 FPS or less | freezes during races |
| 31 Oct | unspecified | i5-12450H | RTX 3050 Laptop | 32 GB DDR4 | 10-20 FPS |  |
| 1 Nov | unspecified | Ryzen 5 8400F | RTX 5060 | 32 GB | about 40 FPS |  |
| 1 Nov | unspecified | Ryzen 5 5600G | RX 7600 | 16 GB | 30 FPS |  |
| 1 Nov | unspecified | i7-12650H | RTX 4060 Laptop 8 GB | 16 GB DDR5 | 30 FPS |  |
| 1 Nov | unspecified | i7-8700 | GTX 1660 Ti 6 GB | 32 GB 2400 | 40-60 FPS | NVMe |
| 1 Nov | unspecified | 9800X3D | RX 9070 XT | 32 GB DDR5 | 20-30 FPS | experimental build, no glitches or leaks |
| 2 Nov | build 113 | Ryzen 5 5600X | RX 6650 XT 8 GB | 16 GB DDR4 | 40+ FPS | under 5 GB RAM |
| 2 Nov | build 116 | Ryzen 7 5800X | RX 6800 XT | 32 GB | 60 FPS | accurate, docked, FSR3 |
| 2 Nov | unspecified | i9-9900KF | RTX 3070 8 GB | 20 GB | 20-30 FPS | premade config |
| 2 Nov | build 109 | i5-12400F | RTX 3050 6 GB | 16 GB DDR5 | 30-45 FPS |  |
| 2 Nov | unspecified | Ryzen 9 5900HS | RTX 3060 Mobile 6 GB | 40 GB DDR4 | 45-55 FPS after shaders, 9-15 while saving | 0.5x resolution |
| 2 Nov | unspecified | i7-9700T | RTX A2000 6 GB | 16 GB | 16-25 FPS |  |
| 2 Nov | build 131 PGO | Ryzen 3 5300G | RTX 5050 8 GB | 16 GB single-channel DDR4 | 25-30 FPS | stall at results screen |
| 3 Nov | build 135 | Ryzen 7 5800XT | RX 9070 XT | 32 GB DDR4 | time trials playable, 30 FPS lock with multiple racers |  |
| 3 Nov | unspecified | i7-14700F | RTX 4070 Super | 32 GB DDR5 | 60 FPS, drops to 50 |  |
| 4 Nov | unspecified | Core Ultra 7 265KF | RTX 5070 Ti | 32 GB | most of the game at 60, drops near CPUs |  |
| 4 Nov | unspecified | i5-14400F | RTX 4060 | 32 GB DDR4 | 43-50 max, 60 only in menus | NVMe |

## Partial configs

These reports are missing the CPU, RAM, build or a combination. They are still useful for a rough GPU comparison, but do not treat them as controlled results.

| Date | Build | CPU | GPU | RAM | Performance | Notes |
|---|---|---|---|---|---|---|
| 3 Nov | PokeDinner latest | Z1 Extreme | Z1 Extreme | not stated | 20-30 FPS | community; ROG Ally; Lossless Scaling only works on loading |
| 3 Nov | unspecified | Ryzen 7 3800X | RX 9070 XT | not stated | 25-50 FPS | community; user said 8 GB; depends on camera |
| 31 Oct | unspecified | Ryzen 5 5600 | RTX 3050 | not stated | 20-30 FPS |  |
| 31 Oct | unspecified | Ryzen 7 7800X3D | RTX 5070 | not stated | 20-30 FPS |  |
| 31 Oct | unspecified | Ryzen 5 5600X | RTX 2060 Super | not stated | about 7 FPS |  |
| 31 Oct | unspecified | i5-13400F | RTX 5060 Ti | not stated | 27 FPS |  |
| 31 Oct | unspecified | not stated | 780M iGPU | not stated | 60 FPS handheld, 40 docked |  |
| 31 Oct | unspecified | i5-10300H | RTX 2060 | not stated | 20 FPS |  |
| 31 Oct | unspecified | Ryzen 5 5600 | RTX 3060 | not stated | 27 FPS |  |
| 31 Oct | unspecified | i5-14400F | RTX 4060 | 16 GB | 3 FPS on the highway, then crash | 8 GB VRAM setting |
| 31 Oct | unspecified | not stated | RTX 3050 Laptop | 16 GB | 40-60 FPS | config adjusted |
| 31 Oct | unspecified | not stated | GTX 1650 Laptop | not stated | 25 FPS, 50-60 after settings, 40 in races |  |
| 31 Oct | unspecified | not stated | GTX 970 | not stated | up to 30 FPS |  |
| 1 Nov | PokeDinner | i5-13420H | RTX 3050 6 GB Laptop | not stated | 40 free roam, 25-30 races | 1080p |
| 1 Nov | unspecified | i5-13400F | RTX 2060 Super | not stated | about 30 FPS with spikes |  |
| 1 Nov | unspecified | not stated | RTX 3060 Ti | not stated | 20-60 FPS, 60 in tunnels |  |
| 2 Nov | build 116 | Ryzen 5 7600X | RTX 3060 | not stated | 12-15 FPS |  |
| 3 Nov | build 167 then 168 | i5-12400F | RX 6650 XT | not stated | 30-40 then 20-30 |  |
| 3 Nov | SmileyTatsu build 11 | Ryzen 5 7600 | RX 7800 XT | not stated | 45-50 average |  |
| 3 Nov | unspecified | Ryzen 7 5700X | RTX 5060 Ti | not stated | 60 before, 30-40 on newer build |  |
| 3 Nov | build 130 then recent | not stated | RTX 4070 Super | not stated | 60 then 40 |  |
| 4 Nov | SmileyTatsu build 12 | not stated | AMD | not stated | almost locked 60 | docked |
| 4 Nov | build 196 | Intel Ultra 255HX | not stated | not stated | 55-60 FPS |  |
| 4 Nov | unspecified | 7800X3D | RX 9070 XT | not stated | close to 60, 40 while compiling |  |
| 4 Nov | unspecified | i7-14700KF | RTX 5080 | not stated | about 60 time trial, 30 in water races |  |
| 5 Nov | unspecified | Ryzen 7 7840HS | RTX 4060 Laptop | not stated | 20 FPS |  |
| 5 Nov | unspecified | Ryzen 5 5600X | RTX 5070 | not stated | 30 FPS |  |

## Known issues

- Some builds lock to 30 FPS when multiple racers are on screen. Time trials can run at 60 FPS while a full race drops.
- Game speed is tied to frame rate on some builds. Above 30 FPS the game can run faster than normal; the 30 FPS mod is the workaround.
- Foliage and terrain can disappear on fast mode or flicker on accurate mode, especially on AMD.
- 2-player and 3-4 player modes are much heavier. One user reports 16 FPS in 3-4 player mode.
- Shader compilation causes stutter and large frame drops until the cache warms up.
- Early builds leaked memory and used very high RAM. Later builds improved this, but 16 GB remains the practical floor.
- Frame generation below 50 FPS adds latency and feels worse than the base frame rate.
- Some users see a random 30 FPS lock, black textures or a crash on newer builds. Report the build and log if it happens.

## Sources

- Public community reports, 30 Oct to 5 Nov 2026. Usernames are not reproduced.
- [ZendNevs v2.0.5 release notes](https://github.com/ZendNevs/Eglantine-ZendNevs/releases/tag/zendnevs-v2.0.5) for the documented MKW result.
- [Orchid README](https://github.com/MythosOfs/Orchid) for the documented 5800X3D and RX 9070 XT result.
