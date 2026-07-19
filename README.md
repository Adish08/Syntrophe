# Syntrophe

*The automated compilation engine powering [Apostrophe](https://ostrophe.vercel.app/).*

[![License](https://img.shields.io/badge/License-GPL_3.0-blue.svg?style=flat-square)](https://github.com/Adish08/stratophe/blob/main/LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Active-success.svg?style=flat-square)](#)

**Stratophe** is the backend builder repository for the Apostrophe project. It utilises GitHub Actions to automatically fetch, patch, and compile Android applications, which are then distributed directly to the main user-facing hub. 

## ⚙️ Core Features

*   **Automated Pipeline:** Uses robust CI/CD workflows to build patched APKs automatically upon new upstream updates.
*   **Centralised Configuration:** Manage included apps, targeted patches, and build parameters directly through a clean `config.toml` file.
*   **Persistent Signatures:** Ensures patched applications can be updated seamlessly via Obtainium without being overwritten by the Play Store.
*   **Optimised Footprint:** Produces binaries stripped of unnecessary telemetry and bloat for maximum performance.

## 🏗️ How It Works

This repository does not host pre-patched APKs directly in its source code. Instead, it operates as a factory pipeline:
1.  **Fetch:** Retrieves unmodified base APKs from secure, open-source repositories.
2.  **Patch:** Applies selected modifications (such as ad-blocking, enhanced privacy modules, and premium feature unlocking).
3.  **Deploy:** Compiles, signs, and pushes the final APKs securely to the GitHub Releases tab.

## 🔗 The Ecosystem

Stratophe serves strictly as the builder layer. To browse, download, and manage the compiled applications through a modern glassmorphic interface, visit the frontend hub:

*   **App Hub:** [Apostrophe](https://ostrophe.vercel.app/)
*   **Frontend Repository:** [Adish08/Apostrophe](https://github.com/Adish08/Apostrophe)

## 👏 Acknowledgments

This infrastructure relies on robust open-source foundations. Special thanks to:
*   [nvbangg](https://github.com/nvbangg/builder-for-morphe) for the upstream automated builder repository.
*   **j-hc** for laying down the initial Python rewrite foundation.
*   The broader open-source community for maintaining the patches that fuel this ecosystem.

## ⚠️ Disclaimer

This project is intended for educational and personal use only. All builds are executed using publicly available tools via transparent GitHub Actions. Stratophe is not affiliated with the original application developers or the patch creators. Please use responsibly and ensure you trust the sources of your patches.

---
*Maintained with ❤️ for the Apostrophe ecosystem.*
