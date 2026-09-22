![Banner](Media/Banner.png)

```
                              )       \   /      (
                             /|\      )\_/(     /|\ 
    *                       / | \    (/\|/\)   / | \                      *
    |`.____________________/__|__o____\`|'/___o__|__\____________________.'|
    |                           '^`    \|/   '^`                           |
    |                                   V                                  |
    |                                                                      |
    |     /|   _       _______   _____________ ____  ___    _   __  |\     |
    |    //|  | |     / /  _/ | / / ____/ ___// __ \/   |  / | / /  |\\    |
    |   ///|  | | /| / // //  |/ / / __ \__ \/ /_/ / /| | /  |/ /   |\\\   |
    |  ////|  | |/ |/ // // /|  / /_/ /___/ / ____/ ___ |/ /|  /    |\\\\  |
    | /////|  |__/|__/___/_/ |_/\____//____/_/   /_/  |_/_/ |_/     |\\\\\ |
    | .__________________________________________________________________. |
    |'               l    /\ /     \\            \ /\   l                 `|
    *                l  /   V       ))            V   \ l                  *
                     l/            //                  \I
                                   V
```

### Welcome to Wingspan, Server Management and Automation for Pterodactyl!

**Project submitted to Submitted to [Stardance, Hack Club](https://stardance.hackclub.com)**

Are you a shipright? Check out the shipwrights.md <3


---

# Why not Packed?
This project is not packed, so you could use the same python script over at Linux and Windows both, the project's code is made to be compatible with both the platforms. This way, you could transfer files from one system to another without needing to change the main code file. Also, for updates, you could just change the py file, and you're done!

---

# What was the Problem, What I fixed (Project Info)
Pterodactyl is a really famous server management tool, but for hosting owners who have more than a hundred servers, managing each of those individually takes a lot of effort. Making a bulk manager tool was really essential, because it allows admins to perform actions in massive quantities, automatically, saving a lot of time and hard work on repeated work. Actions such as transfers required us to transfer each server one by one and had no automation, with wingspan, you could select the servers to transfer, it manages everything as you set. Not just limited to transfers, it can also bulk search servers, perform server purge functions, take bulk backups, perform bulk resize, reinstalls, updates and more.


---

# Features
- Bulk Suspend/Unsuspend
- Selective Purge 
- Backup download
- Bulk resource resize / copy-paste resources
- Bulk Reinstall
- Bulk Transfer 
- Advanced Search & Filter 
- Node/Panel health dashboard 
- User management 
- Update monitor

---

# Installation

To install, ensure you have Python 3.12 or neighboring versions installed.

Note: The project makes its own venv on boot, and also installs its own dependencies, there is NO dependency install step for both linux and windows.

### DEMO
> For Voters / Shipwrights who are testing this, I have installed a demo readonly pterodactyl, which would be deleted after voting is done on this project. Please use the following credentials.
        
- Panel URL: https://demopanel.thehytalehost.com/
- Admin User API Key: ``ptlc_QQ4DDo1ebJjLuwVVb41iJ4Dc5WuRZmbcZvz3tRv2NJf``
- Application API Key: ``ptla_GCYaHWj6Z9ayQjp3UdQVlSAFsFneyt2sxFNbwOWDwiP``
---

### Installation Method:
### 1. Clone the repo
```git clone https://github.com/brahmtej2009/wingspan```

### 2. Run Wingspan Setup mode
```python3 main-cli.py setup```

### 3. Run again to boot to main mode
```python3 main-cli.py```

---

# Functions & Uses

## Homepage
## 1. Search and Info
- **1. Server Search**: 
    
        Allows you to enter ranges for values of parameters to search and filter servers, then export them to csv or take action on those selected servers.
- **2. Server Info**: 
        
        Allows you to enter a single server ID (Numeric) to fetch all information of it on a single page with good formatting.
## 2. Purge Bot

#### 1. Server Purge
- **1. Name Based Purge**: 

        Simple everyday purge, where a keyword must be present in the server name to make it survive, else would be deleted. For data safety reasons, we dont keep it case sensitive, that means if purge protection word is "Prot", then servers with "prot"/"PrOt"/"pROT" (etc.) in name would be protected too.
- **2. Advanced Purge**: 
        
         It first runs the Server Search function, where you use specific ranges and parameter values to filter servers, and then allows you to precisely delete servers in bulk.
#### 2. User Purge
- **1. Empty Account Removal**: 
        
         Make your panel faster by removing accounts which no longer have any servers attached with them. This function excludes admin accounts.

## Bulk Transfer
        This function takes in the destination node and presents server selector by the Server Search function. Servers could be transferred all at once, or one by one. Allottments and resources are automatically allotted by pterodactyl.



# Contributing
The project is driven by community support only, your efforts would mean a LOT to this project and to all its users. For any suggestions, issues, bugs, please feel free to contribute to this project by either informing me, raising a github issue ticket, or adding a PR with the required changes performed. Also, I'l love to have you work with our core team for this project's development, Contact me! [Details in Bio]

---

# Credits
ASCII art credit

Alan Greep - The banner for Wingspan with the Pterodactyl was an awesome open source ASCII Art which I edited. 

---

# My other libraries used in this project!
Pytterns : https://github.com/brahmtej2009/pytterns

---

# License
AGPLv3
