# Pokopia notes

Reports from the Eglantine Discord `#pokopia` between 31 Oct and 5 Nov 2026. The channel had about 3,800 user messages and 89 messages with FPS mentions. This page keeps the reports and workarounds that matter.

These are user reports, not benchmarks. The same build can show a black sky, missing audio or 60 FPS depending on the GPU and the fork.

## What matters

- Fast and accurate change the result. On an RX 6600M, fast reached 60 FPS. On newer notsapinho builds, accurate reached 60 for another user after fast was faster in earlier builds. Test both.
- A 120 FPS mod exists on notsapinho builds, but the developer says current Eglantine cannot run stable 120 FPS. The mod is not a guarantee.
- Black sky is the common visual bug. Removing the Vulkan pipeline cache fixed it for one user. On Android, one user found MMU had to stay off to avoid crashes or a black sky.
- Memory is a hard constraint. PokeDinner asked for about 20 GB upfront for one user, and one tester traced the hang to an 8 GB Switch 1 memory cap. Reset the memory layout for Pokopia.
- 8 GB of RAM can boot the game, but it crashes when other apps use memory. 16 GB is the practical floor.
- NUP support is inconsistent. Some users converted Pokopia to NUP successfully, others could not run it on PokeDinner, and the version metadata can be wrong.
- Frame generation gives 60 displayed FPS but not real 60. One user called it worse than real 60 FPS; input lag is the tradeoff.
- DLSS 4.5 support was mentioned in the channel, but it is not a fix for the underlying emulator performance.

## Fork notes

- At first, Pokopia only booted on PokeDinner, with black textures and invisible furniture. Fixes were paused while the team worked on MKW, then resumed.
- notsapinho builds became the Pokopia pick: AMD fixes, Linux support and the 120 FPS mod. One RTX 4060 Mobile user reached 80+ FPS with accurate GPU, docked mode and the 120fps mod.
- ZendNevs v2.0.4 fixed a Pokopia startup freeze and v2.0.5 reached 60 FPS for about a minute in the release test. Longer play was not tested.
- Users were still asking whether PokeDinner 2.5 fixes the black sky; the channel did not show a confirmed answer.
- Build 135 ran at 60 FPS on a GTX 1080 for one user, but with stutter, a black sky and no audio.

## Complete configs

| Date | Build | CPU | GPU | RAM | Performance | Notes |
|---|---|---|---|---|---|---|
| 1 Nov | PokeDinner, unspecified | Ryzen 7 7700X | RX 6700 XT | not stated | 50-60 FPS, feels like 40-50 | accurate GPU |
| 1 Nov | unspecified | 5800X3D | RX 7900 XT Linux | not stated | 60 FPS with 2x frame gen, worse than real 60 | frame gen caveat |
| 2 Nov | build 135 | not stated | GTX 1080 | not stated | 60 FPS with stutter, black sky, no audio |  |
| 4 Nov | notsapinho | 12th-gen i5 2.5 GHz | RTX 4060 Mobile 6 GB | 16 GB | 80+ FPS | accurate, docked, 120fps mod |
| 1 Nov | unspecified | not stated | RX 6600M | not stated | 60 FPS on fast | fast instead of accurate |
| 1 Nov | ROG Ally Z1E | Z1 Extreme | Z1 Extreme iGPU | not stated | 45 FPS |  |
| 2 Nov | Steam Deck | Steam Deck APU | Steam Deck APU | 16 GB | 30-40 FPS, later 25-30 | uneven frame pacing |
| 3 Nov | notsapinho | not stated | not stated | not stated | 48 fast / 40 accurate to 60 accurate | newer build improved accurate |

## Partial configs

These reports are missing the CPU, RAM, build or a combination. Treat them as rough signals, not controlled results.

| Date | Build | CPU | GPU | RAM | Performance | Notes |
|---|---|---|---|---|---|---|
| 1 Nov | PokeDinner 2.0.1 | Steam Deck APU | Steam Deck APU | 16 GB | 30-40 FPS | power settings reduced |
| 1 Nov | unspecified | not stated | not stated | 8 GB | 60 FPS but crashes when other apps open |  |
| 1 Nov | unspecified | not stated | not stated | not stated | 1440p 60 FPS |  |
| 4 Nov | notsapinho | not stated | not stated | not stated | 120 FPS gameplay, not stable | 120fps mod |
| 5 Nov | AMD handheld X2 mini pro | not stated | not stated | not stated | steady 80 FPS |  |

## Known issues

- Black sky and black 3D objects on some builds and GPUs.
- Missing audio on some builds, including build 135 on a GTX 1080.
- Invisible furniture and texture issues on early PokeDinner builds.
- Startup freeze fixed in ZendNevs v2.0.4; PokeDinner 2.5 black sky status was still unclear.
- 8 GB RAM boots but crashes with other apps; PokeDinner can ask for about 20 GB upfront.
- NUP conversion is inconsistent and version metadata can be wrong.
- 120 FPS is not stable on current Eglantine according to the notsapinho developer.

## Sources

- Eglantine Discord `#pokopia`, 31 Oct to 5 Nov 2026. The export is local and is not committed.
- [notsapinho/Eglantine](https://github.com/notsapinho/Eglantine) for the Pokopia build and 120fps mod.
- [ZendNevs v2.0.5 release notes](https://github.com/ZendNevs/Eglantine-ZendNevs/releases/tag/zendnevs-v2.0.5) for the documented startup test.
- [PokeDinner releases](https://git.eden-emu.dev/Franseven/PokeDinner-a-Eglantine-Fork/releases).
