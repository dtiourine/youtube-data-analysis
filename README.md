# YouTube Analysis Project

## Overview
This project uses the YouTube API to analyze video data from various medical school information channels. These channels primarily create content for premed students and current medical school students, focusing on educational and informational topics about medical school. The purpose of this project is to uncover insights about what types of content are most effective in engaging this specific audience.

## Getting Started

### Prerequisites
Before you can run the analysis, you'll need to have Python installed on your machine, as well as the following packages:

- `dotenv`
- `google-api-python-client`
- `pandas`
- `python-dateutil`
- `wordcloud`
- `nltk`
- `isodate`
- `seaborn`

### Installation
To install the necessary packages, run the following command in your terminal:

`pip install python-dotenv google-api-python-client pandas python-dateutil wordcloud nltk isodate seaborn`

### API Key
You will need a valid YouTube API key to fetch data:

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Navigate to the APIs & Services dashboard, enable the YouTube Data API v3 for your project.
4. Go to the credentials page and create credentials to get your API key.

**Note:** Store your API key in a `.env` file as `YOUTUBE_API_KEY='your_api_key_here'` to keep it secure and separate from your main code.

## Credits
- Inspired by [YouTube API Analysis by Thu Vu](https://github.com/original/repo)
- Watch the [Original Project Walkthrough on YouTube](https://youtu.be/D56_Cx36oGY)
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
