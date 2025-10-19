# YoutubeNotifier

YoutubeNotifier is a Python application hosted 24x7 that notifies clients signed up for the Telegram channel, whenever a new video is uploaded to a specified YouTube channels. It uses the YouTube API to fetch the latest video and the SendGrid API to send notifications to the users via email and Telegram API to notify them.

## Features

- Fetches the latest video from a specified YouTube channel
- Compares the video with the videos stored in the database to check for new videos
- Sends notifications to the users via email and Telegram
- Stores video metadata in a SQLite database

## Prerequisites

- Python 3.x
- SQLite
- SendGrid API key
- YouTube API key
- Telegram Bot API key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/YoutubeNotifier.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment variables:

   - Set the `SENDGRID_API_KEY` environment variable to your SendGrid API key.
   - Set the `YT_API_KEY` environment variable to your YouTube API key.
   - Set the `TELEGRAM_BOT_API_KEY` environment variable to your Telegram Bot API key.

4. Create the SQLite database:

   ```bash
   python database.py initialize
   ```

5. Run the application:

   ```bash
   python app.py
   ```

## Usage

1. Add the YouTube channels you want to monitor in the `database.py` file.

2. Run the application.

3. The application will fetch the latest video from the specified YouTube channels and compare it with the videos stored in the database to check for new videos.

4. If a new video is found, the application will send notifications to the users via email and Telegram.

## Contributing

Contributions are welcome! Please open an issue or a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.