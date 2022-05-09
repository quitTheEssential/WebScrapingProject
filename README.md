# Web Scraping and Social Media Scraping Project
*Authors:* Robert Kowalczyk, Szymon Socha, Jan Dudzik
## Instruction how to run our scrapers
### Beautiful Soup (on Windows)
1. Install BeautifulSoup
    * Open Terminal by pressing <kbd>Windows</kbd> + <kbd>R</kbd> and then write `cmd`.
    * Run `pip install beautifulsoup4` command.
2. Install other required packages (`pandas` for data manipulation and `tqdm` to show progress bar)
    * Run `pip install pandas` command.
    * Run `pip install tqdm` command.
3. Run the scraper
    * Open Terminal by pressing <kbd>Windows</kbd> + <kbd>R</kbd> and then write cmd.
    * Navigate to the directory where the script is located using the `cd` command.
    * Run `python bs_scraper.py` command.
### Selenium (in Ubuntu)
1. Install GeckoDriver
    * Open Terminal by pressing <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>. 
    * Run `wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz` command.<br>
   On the GeckoDriver [Github](https://github.com/mozilla/geckodriver/releases) website, you can always find the latest release.
    * Extract downloaded file with `sudo tar -xvf geckodriver-v0.31.0-linux64.tar.gz` command.
    * Run `sudo mv geckodriver /usr/local/bin/` to move GeckoDriver to the desirable location.
    * Change current directory to binary location: `cd /usr/local/bin/`
    * Make GeckDriver executable: `sudo chmod +x geckodriver`
    * Add it to PATH: `export PATH=$PATH:/usr/local/bin/geckodriver`
2. Install Selenium
    * Open Terminal by pressing <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>.
    * Run `pip install selenium` command.
3. Install other required packages (`pandas` for data manipulation and `tqdm` to show progress bar)
    * Run `pip install pandas` command.
    * Run `pip install tqdm` command.
4. Run the scraper
    * Open Terminal by pressing <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd>.
    * Navigate to the directory where the script is located using the `cd` command.
    * Run `python3 selenium_scraper.py` command.
### Scrapy
...
