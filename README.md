# StickEmpiresLoginMessageExtractor

This project helps you to extract your login message for the [StickEmpiresDailyCoinCollector](https://github.com/kaanoz1/StickEmpiresDailyCoinCollector) project.

First of all, if you do not familiar with software, code or similar concepts you can use any AI in order to get help. They are pretty basic.

## Prerequisites:

- Windows
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Npcap](https://npcap.com/) (required for capturing network packets)
- Flash Player (the program won't work if you play through a web browser)

## Installation and Execution

Open a terminal **as administrator** and run:

```bash
git clone https://github.com/kaanoz1/StickEmpiresLoginMessageExtractor
cd StickEmpiresLoginMessageExtractor
uv run start
```

While the program runs, you should open your FlashPlayer and log in to your StickEmpires account.
Follow the console and your login message should appear as a hex string in the file named `login_messages.txt`
After that, you can continue to follow the instructions of [StickEmpiresDailyCoinCollector](https://github.com/kaanoz1/StickEmpiresDailyCoinCollector).

> **Warning:** The login message contains your account credentials in hashed form. Do not share it with anyone.

## License

This project is licensed under the [MIT License](LICENSE).

This tool is provided as is, without any warranty. You are responsible for complying with the terms of service of the game you use it with.
