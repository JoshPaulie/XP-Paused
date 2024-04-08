# XP-Paused
Dead simple script that notifies you when the [OSRS](https://osrs.game) servers are back online after an update

## Usage
Run `XP-Paused` when you notice the servers are offline

You'll be notified when they're back online via a push notification (supports Windows, MacOS, and Linux[^1])

## Install
> [!Important]
> Requires [Python](https://www.python.org/downloads/) 3.12+ & [pipx](https://github.com/pypa/pipx)

```
pipx install git+https://github.com/JoshPaulie/XP-Paused.git
```

### Update
```
pipx upgrade XP-Paused
```

[^1]: [notify-send](https://man.archlinux.org/man/notify-send.1.en) must be installed for Linux support 🐧
