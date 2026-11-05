# Donkey Kong Bananza notes

Reports from the Eglantine Discord `#donkey-kong-bananza` between 30 Oct and 5 Nov 2026. The channel had about 5,400 user messages and 255 messages with FPS mentions. This page keeps the reports and workarounds that matter.

These are user reports, not benchmarks. A build that works on one GPU can show missing terrain, a purple screen or slow motion on another.

## What matters

- Game speed is tied to frame rate. Below 30 FPS the game runs in slow motion; above 30 it can run at double speed. The 30 FPS cap, slow mode, PokeDinner 2.5's 30 FPS option, or the DynamicFPS mod are the workarounds.
- DynamicFPS is a separate mod made by ZendNevs (DynamicFPS.-DonkeyKong-Bananza v1.1). It fixes the speed changes for some users but not all, and one user notes it needs the matching game update.
- Selevet performance build 3 and 4 are popular with a 30 FPS cap. One 5700X3D and RTX 5070 Ti user got 30 FPS with 60 FPS smooth motion, at the default 0.5x resolution; 1x also worked.
- PokeDinner 2.5 with the 30 FPS option was the best result for one Ryzen 5 9600X and RX 6800 user: no glitches, smooth frame rate and correct speed.
- ZendNevs v2.0.3 was called the best AMD build by one user, and v2.0.5 got positive comments. The repo has only 2 commits and no license, so treat its release-note results as self-reported. Recent independent reports favor Selevet perf 3/4 and PokeDinner 2.5.
- Terrain is a known AMD problem. OpenGL renders no terrain, Vulkan renders it but crashes more. PokeDinner, Zortos and Selevet differ in how much terrain they show.
- Purple screen: press down on the d-pad or enter Photo Mode and go back. Some builds fixed the purple screen; the latest SmileyTatsu build still showed it for one user.
- Build 204's d-pad fix caused continuous stutters and black texture flicker for one AMD user. PokeDinner 2.5 was the fallback.
- Fast and accurate differ. Accurate is around 30 FPS; fast reaches 40-50 FPS but can remove or break visual detail.
- Resolution: Selevet defaults to 0.5x and accepts 1x. One user ran 2x scale with SMAA and got 30 FPS in the open, 60 in tunnels.
- Memory: early builds leaked and hit OOM, especially the Zortos fork. 16 GB is the practical floor, 32 GB is safer.

## Fork notes

- At first, the game only booted on PokeDinner, with black textures and missing terrain.
- Zortos build 31 gave full AMD textures but only 20-25 FPS on an RX 6900 XT and had a memory leak. A 5700X3D and RTX 5070 Ti user hit 17 FPS looking north.
- Selevet performance 3 and 4 became the stable pick for several users, especially with the 30 FPS cap and smooth motion.
- ZendNevs v2.0.3 was called the best AMD build by one user, and v2.0.5 got positive comments. Its repo has 2 commits and no license; treat the release-note numbers as self-reported.
- PokeDinner 2.5 with the 30 FPS option was the cleanest result for one full AMD system.
- Build 202 and 204 had purple-screen, texture and stutter reports. Keep a known-good build.

## Complete configs

| Date | Build | CPU | GPU | RAM | Performance | Notes |
|---|---|---|---|---|---|---|
| 31 Oct | unspecified | Ryzen 7 7700X | RX 6700 XT | not stated | 30-40 FPS accurate, 40-50 fast, 60 in corners | area dependent |
| 1 Nov | zortos build 31 | 5700X3D | RTX 5070 Ti | 32 GB | 17 FPS looking north | before Selevet |
| 1 Nov | Selevet perf 3 | 5700X3D | RTX 5070 Ti | 32 GB | 30 FPS cap, 60 with smooth motion | default 0.5x, 1x works |
| 1 Nov | unspecified | 7800X3D | RTX 5090 | not stated | under 20 FPS underground |  |
| 1 Nov | experimental AMD build 2 | 7800X3D | RX 9070 XT | not stated | about 30 FPS standing still |  |
| 2 Nov | unspecified | 7800X3D | RX 9070 XT | not stated | 60 FPS |  |
| 2 Nov | Selevet perf 4 | 7800X3D | RX 9070 XT | not stated | about 50 FPS walking in less populated areas |  |
| 2 Nov | Selevet perf 3 | 7800X3D | RTX 5090 | not stated | 30 FPS cap works well |  |
| 3 Nov | ZendNevs v2.0.3 | Ryzen 7 5800XT | RX 9070 XT | 32 GB DDR4 | playable |  |
| 4 Nov | PokeDinner 2.5 | Ryzen 5 9600X | RX 6800 16 GB | 16 GB DDR5 | 30 FPS option, no glitches, smooth |  |
| 4 Nov | unspecified | i5-12700KF | RTX 3060 Ti | not stated | 30 FPS, 15 during destruction |  |
| 4 Nov | PokeDinner latest | i5-12400F | RTX 3060 12 GB | 16 GB | 10 FPS on the Hilltop layer |  |
| 3 Nov | Selevet | i5-12400F | RTX 3060 12 GB | 16 GB | over 10 FPS on the Hilltop layer |  |
| 3 Nov | zortos | not stated | RX 6900 XT Linux | not stated | 20-25 FPS, full textures |  |

## Partial configs

These reports are missing the CPU, GPU, RAM or build. Treat them as rough signals, not controlled results.

| Date | Build | CPU | GPU | RAM | Performance | Notes |
|---|---|---|---|---|---|---|
| 1 Nov | unspecified | not stated | NVIDIA | not stated | 20-30 FPS |  |
| 1 Nov | unspecified | not stated | not stated | 4 GB RAM, 4 GB VRAM | 20-60 FPS |  |
| 2 Nov | jojo build | not stated | not stated | not stated | 18 FPS, playable with dynamic FPS |  |
| 1 Nov | unspecified | not stated | not stated | not stated | 30 FPS open, 60 in tunnels | 2x scale, SMAA |
| 3 Nov | unspecified | Ryzen 7 5700X | RTX 5060 | 24 GB | 14 FPS after the first area |  |
| 3 Nov | unspecified | not stated | not stated | not stated | 12 FPS |  |
| 1 Nov | unspecified | not stated | not stated | not stated | 20-30 FPS |  |

## Known issues

- Missing or invisible terrain on AMD, especially with OpenGL.
- Purple screen on some builds; Photo Mode or d-pad down can clear it.
- Game speed follows FPS; 30 FPS cap or DynamicFPS is required for normal speed.
- Build 204's d-pad fix introduced stutters and black texture flicker for one user.
- Memory leaks and OOM on early builds and the Zortos fork.
- Frame drops during destruction and in large rooms, even when standing still is fine.
- Some users see 60 FPS in tunnels or small rooms and 20-30 FPS in open areas, so area matters more than the average.

## Sources

- Eglantine Discord `#donkey-kong-bananza`, 30 Oct to 5 Nov 2026. The export is local and is not committed.
- [ZendNevs v2.0.5 release notes](https://github.com/ZendNevs/Eglantine-ZendNevs/releases/tag/zendnevs-v2.0.5) for the documented DK result.
- [PokeDinner releases](https://git.eden-emu.dev/Franseven/PokeDinner-a-Eglantine-Fork/releases) and [Selevet releases](https://github.com/sylvieistaken/selevet-eglantine/releases).
