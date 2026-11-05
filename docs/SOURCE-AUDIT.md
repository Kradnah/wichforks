# Source audit

Checked 5 Nov 2026 against the GitHub, Forgejo and GitLab APIs. A fork is auditable when the full source is in the repository, a license file is present, and the build files are there. A source zip attached to a release is not the same as a public source tree.

| Fork | License | Full source in repo | Release assets | History | Status |
|---|---|---|---|---|---|
| [Djihads80/Eglantine](https://github.com/Djihads80/Eglantine) | GPL-3.0 | Yes, src and CMakeLists | Binaries | Large | Auditable |
| [SmileyTatsu/Eglantine](https://github.com/SmileyTatsu/Eglantine) | GPL-3.0 | Yes, src and CMakeLists | Binaries | Active fork | Auditable |
| [MythosOfs/Orchid](https://github.com/MythosOfs/Orchid) | GPL-3.0 | Yes, src and CMakeLists | Binaries | Active fork | Auditable |
| [PokeDinner](https://git.eden-emu.dev/Franseven/PokeDinner-a-Eglantine-Fork) | GPL-3.0 | Yes, LICENSE.txt and src | Binaries | Active Forgejo | Auditable |
| [notsapinho/Eglantine](https://github.com/notsapinho/Eglantine) | GPL-3.0 | Yes, src and CMakeLists | Binaries | Active | Auditable |
| [zortos293/Lichii](https://github.com/zortos293/Lichii) | GPL-3.0 | Yes, src and CMakeLists | Binaries and Actions artifacts | Active | Auditable |
| [rdenno/Eglantine](https://github.com/rdenno/Eglantine) | GPL-3.0 | Yes, src and CMakeLists | Binaries | Small fork | Auditable |
| [Selevet Eglantine](https://github.com/sylvieistaken/selevet-eglantine) | GPL-3.0 | Yes, src and CMakeLists | Binaries | Tuned fork | Auditable |
| [EglantinePS5](https://github.com/heydemoura/EglantinePS5) | GPL-3.0 | Yes, src and Makefile | No release assets at check | Port | Auditable source |
| [Droplet](https://gitlab.com/seighttt/droplet) | GPL-3.0-or-later | Yes, LICENSE.txt and src | Binaries | GitLab | Auditable |
| [eden-nx2-android](https://git.eden-emu.dev/moceure/eden-nx2-android) | GPL-3.0 | Yes, LICENSE.txt and src | Tags | Forgejo | Auditable |
| [ZendNevs/Eglantine-ZendNevs](https://github.com/ZendNevs/Eglantine-ZendNevs) | None | No, only README and a workflow | Binaries plus source zip | 2 commits | Source zip only, no license |
| [Eglantine 3060Ti 16GB](https://github.com/astralbeexd/Eglantine-3060Ti-16GB) | GPL-3.0 | No, patch set only | Binary zip and hash | Small | Patch set, binary release |

## How to verify a fork

1. Check the root of the repo for `LICENSE`, `LICENSE.txt` or `LICENSES/`, plus `src/` and `CMakeLists.txt` or `Makefile`.
2. Check the commit history. A repo created a few days ago with two commits and no source tree is a release channel, not an auditable project.
3. If the source is only a zip in the release, download it, build it, and compare the build with the binary you plan to run. Without a license, you cannot assume redistribution or modification rights.
4. A binary-only fork is not automatically malicious, but it cannot be reviewed, reproduced or checked against the source. Treat its performance claims as unverified and do not make it a first pick.

## What this means for the guide

All first picks publish their source in the repository under GPL-3.0: SmileyTatsu for Mario Kart World, Selevet or PokeDinner for Donkey Kong Bananza, notsapinho for Pokopia, Lichii or Orchid for Ocarina of Time, and Droplet for online play.

ZendNevs and the 3060Ti build are not first picks. ZendNevs ships a source zip but has no license and no source tree in the repo. The 3060Ti repo is a patch set with a binary release, not a full emulator fork.
