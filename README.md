# Prismo

Prismo uses [pywal](https://github.com/dylanaraps/pywal/) to generate color schemes from your current Windows wallpaper and apply them to Firefox (including websites), Discord, Obsidian, Alacritty, VS Code, WSL GTK/QT, etc.

This tool was inspired by wpgtk which provides similar functionality in Linux. In it's current state, using Prismo requires basic terminal skill.
  
Prismo is released under the [GNU General Public License v3.0](COPYING).
  - The author is not responsible for any damage, loss, or issues arising from the use or misuse of this GPL3 licensed software.  
The summary below is from [tl;drLegal](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3).
  - You may copy, distribute and modify the software as long as you track changes/dates in source files.
  - Any modifications to or software including (via compiler) GPL-licensed code must also be made available under the GPL along with build & install instructions.
  
  
## Installation  
 
1. Install [ImageMagick](https://imagemagick.org/script/download.php#windows) while making sure "Add application directory to your system path" is enabled then restart your PC.
2. Click "prismo.exe" under Assets in the [Latest Release](https://github.com/rakinishraq/prismo/releases/latest) page to download.  
3. Run the exe once and wait a few seconds to extract resources and templates. Press Enter to exit.  
4. Run the exe again to generate a theme with your current Windows wallpaper.
5. Install any Integrations from the [Integrations section](https://github.com/rakinishraq/prismo#Integrations) right below.  

To make changes to the generated config file, like to enable animated wallpapers or some of the integrations below, use the following [Configuration section](https://github.com/rakinishraq/prismo#configuration).

This is optional if you just want to generate colors for Discord from your static Windows wallpaper. However, Prismo is overkill for this use case so check out my fork of [pywal-discord](https://github.com/rakinishraq/pywal-discord).
  
  
## Integrations

- **Visual Studio Code:** Install the [extension](https://marketplace.visualstudio.com/items?itemName=dlasagno.wal-theme) and enable the theme in the Settings menu.
- **Websites:** Install the Dark Reader extension from the [Chrome Web Store](https://chrome.google.com/webstore/detail/dark-reader/eimadpbcbfnmbkopoojfekhnkhdbieeh) or [Firefox add-ons](https://addons.mozilla.org/en-US/firefox/addon/darkreader/). You can set the background and foreground colors in `See more options > Colors` section.
  - Get the colors for these fields as detailed in the "And More!" integration below.
  - An automation like Pywalfox's native messenger is in progress.
- **Firefox/Thunderbird:** Install the Pywalfox [extension](https://addons.mozilla.org/en-US/firefox/addon/pywalfox/) and [application](https://github.com/Frewacom/pywalfox). The process for the latter may be complex for those new to Python/Pip. Tested with Librewolf.
- **Chrome:** Use [wal-to-crx](https://github.com/mike-u/wal-to-crx) to generate a theme file. Unfortunately, this process is not seamless like Pywalfox and untested.
- **Obsidian:** Edit the entry of your Vault's location in the config file under "obsidian" like the [example config file](https://github.com/rakinishraq/prismo#Configuration) below. For unsupported themes, edit the BG/FG colors using the Style Settings plugin usually (details in the "And More!" integration below).
- **Disclaimer:** _Usage of BetterDiscord to apply themes is subject to user discretion and risk. It's important to note that custom clients are not permitted under Discord's Terms of Service and may result in user penalties, including account bans. As a developer, I bear no responsibility for any repercussions from using BetterDiscord or any other custom client. Please adhere to Discord's Terms of Service._
- **Neovim:** Use this [Neovim theme](https://github.com/AlphaTechnolog/pywal.nvim) for pywal support in WSL and potentially native Windows as well.
- **Windows 10/11 Theme:** The color scheme of Windows can be set to automatically adapt in `Settings > Colors > Accent color (set to Automatic)`.
- **Alacritty:** An Alacritty configuration file is included but enabling it means you must make all edits in the templates file and run the tool to update. A line-replacing update method is in progress to prevent this.
- **WSL GTK/QT:** Set the WSL variable as the name of your WSL OS name if you want [wpgtk](https://github.com/deviantfero/wpgtk) compatibility (more readable terminal color scheme as well as GTK/QT and other Linux GUI app theming). All Pywal supported apps should update automatically, too. If WSL is not installed, leave it empty.
  - **Zathura:** Install and run [this script](https://github.com/GideonWolfe/Zathura-Pywal) within WSL to generate a new themed zathurarc file.
  - There's probably a similar process for many other Linux apps that sync with Linux's pywal theme files, which wpgtk generates. This was tested with GWSL on feh and zathura.
  - wpgtk depends on the imagemagick package
- **And More!** The background and foreground colors are shown in the command line output and the full color scheme is available in `C:/Users/USER/.cache/wal/colors.json` to manually input in any app.
  
  
## Configuration

The default config folder is located at `C:/Users/USER/AppData/Local/Prismo/` containing:
- `config.yaml` - Main configuration file
- `templates/` - Template files (`.prismo` files)
- `licenses/` - License files

You can edit the config with any text editor, or specify a custom config folder using the `-c` flag.

### Using Custom Config Folders

You can maintain multiple config folders for different setups. The `-c` flag expects a **folder path** (not a file path) that contains `config.yaml` and `templates/`:

```bash
# Use custom config folder
.\prismo.exe -c "D:\my-configs\work-theme"

# Or with environment variables
.\prismo.exe -c "%USERPROFILE%\Documents\prismo-configs"
```

The custom folder must contain:
- `config.yaml` - Your configuration file
- `templates/` - Your template files

### Config Example

```yaml
templates:
    alacritty: ~/AppData/Roaming/alacritty/alacritty.yml
    obsidian: ~/Documents/Notes/.obsidian/themes/pywal.css
    win-terminal: %LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json

wsl: 'Ubuntu'
light_mode: false
```

### Path Expansion
- Paths support environment variables and shortcuts:
  - `~` expands to your home directory
  - `%userprofile%` expands to your Windows user profile
  - `$HOME` expands to your home directory (Unix-style)
  - Any Windows environment variable like `%APPDATA%`, `%LOCALAPPDATA%`, etc.
- Use either `/` or `\` for path separators (both work)
- Missing directories are automatically created during color generation

### Template Files
- Templates map a template file (left) to an output file path (right)
- All template files use the `.prismo` extension and directive-based format (see [Template Format docs](docs/TEMPLATE_FORMAT.md))

### Custom Templates
- The default templates (Alacritty, Discord and Obsidian) are located in the "templates" folder next to this config file
- In template files, `{colorname}` is replaced with the hex code **without #** for a color (e.g., `a1b2c3`)
- Add `#` in your templates where needed: `#{colorname}` for CSS, `"#{colorname}"` for JSON
- RGB/HLS components like `{colorname.r}` return numeric values (no # needed)
- Available color names: `color0`, `color1`...`color15`, `background`, `foreground`, `cursor`
- Available components:
  - Hue (0-360): `{colorname.h}`
  - Saturation (0%-100%): `{colorname.s}`
  - Lightness (0%-100%): `{colorname.l}`
  - Red (0-255): `{colorname.r}`
  - Green (0-255): `{colorname.g}`
  - Blue (0-255): `{colorname.b}`

### WSL
- Set the WSL variable to the name of your WSL distribution if you want wpgtk integration. If WSL is not installed, leave it empty ("").

### Light Mode
- Set `light_mode` to `true` to generate light mode color schemes instead of dark mode. Defaults to `false` if not specified.
- Can be overridden with the `-lm` flag when running the tool.

### Automatic Resource Recovery
- Prismo automatically checks and restores missing configuration files on each run
- If the config folder, templates folder, or licenses folder is deleted, it will be recreated
- If individual template files (like `win-terminal.prismo`) or license files are deleted, they will be restored from the bundled resources
- This ensures you can always recover default templates and configuration without reinstalling


  
## CLI Usage

```
Reads current Windows wallpaper, generates pywal color scheme, and applies to templates.

options:
  -h, --help            show this help message and exit
  -c, --config FOLDER   path to custom config folder with config.yaml and templates/ (default: %LOCALAPPDATA%\Prismo)
  -co, --colors-only    generate colors and format JSON only, skip config-based templates and WSL
  -lm, --light-mode     generate light mode color scheme instead of dark mode
  -t, --templates       apply specific templates (comma-separated) or list available templates
  -w, --wsl [DISTRO]    apply WSL/wpgtk theme, optionally specify distro name
```


## Common Uses

- `.\prismo.exe` reads your current Windows wallpaper, generates a pywal color scheme from it, and applies all configured templates and WSL integration.
- `.\prismo.exe -c "path\to\config-folder"` uses a custom config folder (containing config.yaml and templates/) instead of the default location.
- `.\prismo.exe -co` reads your current Windows wallpaper and generates a pywal color scheme, but skips applying templates and WSL integration. This is useful if you only want to generate the colors.json file for use with other tools.
- `.\prismo.exe -lm` generates a light mode color scheme instead of dark mode, overriding the config setting.
- `.\prismo.exe -t discord,obsidian` applies only the specified templates (comma-separated, no spaces).
- `.\prismo.exe -t` lists all available templates configured in config.yaml.
- `.\prismo.exe -co -lm` generates a light mode color scheme and skips templates/WSL integration.

  

## Build Instructions

This is an optional section for those who want to modify the code and execute using a virtual environment:
1. Clone the repo then open a terminal session in the folder or use `cd <path-to-Prismo>/Prismo`
   - For the former, shift-right click in an empty area in the folder, click Open Powershell window here 
2. Execute `python -m venv .venv` to create a virtual environment
3. Install all the required modules with `./.venv/Scripts/pip.exe install -r requirements.txt`
4. To run from source: Execute `./LAUNCH.ps1 <arguments>` or `./.venv/Scripts/python.exe main.py <ARGUMENTS>`
5. To build into .exe: Execute `./COMPILE.ps1` or `./.venv/Scripts/pyinstaller --noconfirm --onefile --console --name "Prismo" --clean --add-data "./resources;resources/" "./main.py"`
  
  
## Credits

The respective licenses are in the [repo resources folder](https://github.com/rakinishraq/prismo/tree/main/resources/licenses) and copied into the Local Appdata folder.

- color scheme file generation from [pywal](https://github.com/dylanaraps/pywal) module by Dylan Araps (MIT)
- hardcoded SVG icons in GUI interface by FontAwesome (CC-BY-4.0)