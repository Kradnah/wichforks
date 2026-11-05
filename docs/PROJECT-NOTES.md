# Project notes

Notes pulled from public community reports between 30 Oct and 5 Nov 2026. This is not official documentation. Reports are unverified, build numbers move fast, and results change with the GPU, driver and game version.

This page keeps the technical claims that affect which fork or build to use. For the fork shortlist, go back to the [main guide](../README.md).

## Build timeline

| Build | Date | Reported change or status |
|---|---|---|
| 88 | 31 Oct | CI starts producing a Linux tarball alongside the AppImage |
| 96 | 1 Nov | Pokopia working |
| 109 | 2 Nov | One tester called it the most stable build after trying many |
| 129 | 2 Nov | Pokopia runs without the graphical bug seen earlier |
| 135 | 2 Nov | NUP conversion gets icons, titles and versions; about 23 to 40+ FPS on a 7800XT; audio stutter in cup 7 |
| 168 | 3 Nov | Controller rumble works; HD rumble needs a Switch controller |
| 189 | 4 Nov | DLSS support through Streamline; NVIDIA only, and only for games that use DLSS |
| 196 | 4 Nov | Last stable build for one tester; later builds force-closed for them |
| 202 | 4 Nov | Game-status report with several regressions, listed below |
| 212 | 4 Nov | Commit `d6efc8e`; performs normally again for one tester. Another reports 202 to 212 force-closing with one third of the FPS |
| 219 | 4 Nov | DLSS and Streamline fix FPS and lighting, but the build force-closes for one tester |
| v0.1.0-rc1 / 11-5 | 5 Nov | One third of the FPS for one tester; second game-status report |

Dates are the day the build was discussed, not necessarily the release date. A build that is stable for one GPU can fail on another.

## Feature status

### NUP packaging

NUP is a container format for decrypted game dumps, started by a55uka and merged into eden-nx2. It deduplicates and compresses data, packs a game into one file, and can embed the title, version and icon.

- Build 135 and later can convert a loose dump with metadata from the GUI.
- The format changed around 1-2 Nov: a table-of-contents update made older NUPs unusable. Expect more changes.
- DLC is not bundled. Users reported DLC failing after conversion, and the workaround discussed was packaging it separately.
- Performance and compatibility are mixed. Some games crash after conversion, and metadata editing or extracting the dump back out was still planned.
- NUP packs your own dumps. It is not a source of games.

### DLSS

Build 189 added DLSS support through Streamline.

- NVIDIA only.
- Use it only for games that actually use DLSS. Fire Emblem Fortune's Weave is the example in community reports.
- DLSS and Streamline versions need to match the installed driver. Avoid random DLL bundles from file hosts.
- On AMD, one Fire Emblem crash log showed the emulator trying DLSS, then failing to fall back to FSR.

### Rumble

- Build 168 added controller rumble.
- HD rumble needs a Switch controller.
- A DualSense HD rumble pull request was opened on 5 Nov. Check the repo for its status.

### Frame generation

FSR 3 frame generation is available in the UI. Some users found the setting did not stick until they saved it per game. Frame pacing complaints are common.

### Auto-updater

There is no auto-updater as of 5 Nov. A community poll asked 10 people, and 7 said yes. Users asked for signature checks if one is added, because an unsigned updater would be an obvious malware target.

### Android

The Android build is experimental and was not an official target at check time.

- It appeared around 3 Nov and still used Eden branding internally.
- NUP files were not reading on Android, and one user got a black screen with a NUP.
- godpow added two experimental graphics hacks for Android.
- The owner tested on a Snapdragon 8 Gen 3 and called the early Android work cosmetic.
- Desktop parity is not there.

### Online

The documented route for online play is [Droplet with Reservoir](https://gitlab.com/seighttt/droplet). Community users experimented with online on PokeDinner and Eglantine, but that was not the supported path. Treat those experiments as unstable.

### Fork merging

The owner said on 2 Nov that the project wants to merge fork work into the main build where it fits, instead of keeping one emulator per game. That is the reason the central Eglantine build stays the default recommendation.

## Game reports

These are single-user reports from build 202 and the 0.1.0-rc1 build on 4 and 5 Nov, unless noted. They are not benchmarks.

| Game | Build | Report |
|---|---|---|
| Mario Kart World | 135 | About 23 to 40+ FPS on a 7800XT; audio stutter in cup 7 |
| Splatoon Raiders | 1 Nov | Playable on Steam Deck with graphical issues |
| Pokemon Pokopia | 96, 129, 202, rc1 | Working; build 129 had no graphical bug; build 202 had invisible Vespiqueen items and crashed; rc1 boots at 60 FPS |
| Donkey Kong Bananza | 202, rc1 | Loads; purple screen after loading, fixed by entering Photo Mode; choppy with texture glitches; rc1 loads fine with the purple screen absent, and music and rumble persist |
| Hyrule Warriors: Age of Imprisonment | 2 Nov | Boots, but rendering is black |
| Star Fox | 202, rc1 | Infinite loading |
| Yoshi | 202, rc1 | Choppy but loads; rc1 has a green glitch at 45-60 FPS, skips the cutscene and hard-crashes on Plasma and X11 |
| Fire Emblem Fortune's Weave | 202, rc1 | Black screen and crash; on AMD the crash log shows a DLSS attempt and a failed FSR fallback |
| Zelda: OoT remake | rc1 | Infinite loading on Eglantine; use Lichii build 80. Orchid v0.7.4 fixes exposure, fog and vegetation, but OoT performance there is unmeasured |
| Orbitals | 202, rc1 | Black screen; 3-10 FPS with no shader-building indicator |
| Super Mario Bros. Wonder | NUP | DLC did not work after converting the game to NUP |
| Yoshi | 3 Nov | Full game boots, not just the demo |
| Switch Sports | 1 Nov | Limited progress |

A different GPU, driver or game version can change every result in this table.

## Setup notes

- Memory: Switch 2 titles use a 12 GiB memory layout. A `Failed to allocate 20480 MiB of backing memory` error is a pagefile problem. One user fixed it with a 20 GB pagefile; 16 GB RAM is a practical floor, 32 GB is safer.
- PGO builds: some users see crashes or very slow game loading. Use the MSVC or non-PGO build if PGO fails. The PGO profile was made on Eden, not on Switch 2 games, so gains vary.
- Frame generation: save the setting per game if the global toggle does not stick.
- Low VRAM: use the conservative VRAM option and a smaller DRAM setting. Memory use was cut from about 20 GB to 9 GB in early builds, and leak reports dropped in early November.
- DLSS: match DLSS and Streamline versions to your NVIDIA driver. Do not enable it for games without DLSS.
- Rumble: HD rumble needs a Switch controller. A DualSense implementation was still a pull request.

## Open issues

- Builds 202 to 219 have regression reports. One tester calls 196 the last stable; another says 212 works after a rebuild. Keep a known-good build.
- NUP still has DLC and metadata gaps, and the format can change.
- Android does not read NUP reliably and remains experimental.
- There is no auto-updater.
- Online outside Droplet is experimental.
- HD rumble on DualSense was still a pull request on 5 Nov.

## Sources

- Public community reports, 30 Oct to 5 Nov 2026. Usernames are not reproduced.
- [Eglantine releases](https://github.com/Djihads80/Eglantine/releases) for build tags and release notes.
- [Droplet and Reservoir](https://gitlab.com/seighttt/droplet) for the documented online path.
