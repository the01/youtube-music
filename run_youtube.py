# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = "d01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2019, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2019-02-07"
# Created: 2019-02-07 13:55

import threading
import time
import os

from flotils import get_logger
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


logger = get_logger()


if __name__ == "__main__":
    import logging.config
    from flotils.logable import default_logging_config

    logging.config.dictConfig(default_logging_config)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.INFO)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.INFO)

    options = webdriver.ChromeOptions()
    udata = "C:\\Users\\f.jung\\AppData\\Local\\Google\\Chrome\\User Data\\"
    #options.add_argument('--user-data-dir="{}"'.format(udata))
    driver = webdriver.Chrome(
        executable_path="bin/chromedriver", chrome_options=options
    )
    driver.get("https://youtube.com")
    #driver.get("https://www.youtube.com/watch?v=WbxH5S9_A3M&list=PLXIdhrTXbAT04KInkIY9666H6Wt8M3b6l&index=27")
    SLEEP_TIME_WAITING = 2.5
    SLEEP_TIME_BTN = 0.7
    sleep_time = SLEEP_TIME_WAITING

    try:
        while True:
            time.sleep(sleep_time)
            one_found = False
            try:
                continue_paused = driver.find_element_by_xpath("//yt-button-renderer[@id='confirm-button']/a/paper-button[@aria-label='Ja']")
            except KeyboardInterrupt:
                break
            except (
                    selenium.common.exceptions.InvalidSelectorException,
                    selenium.common.exceptions.NoSuchElementException,
            ):
                logger.debug("No CntBtn")
            except:
                logger.exception("Failed CntBtn")
            else:
                try:
                    if continue_paused.is_enabled() and continue_paused.is_displayed():
                        continue_paused.click()
                        one_found = True
                    else:
                        logger.debug("CntBtn not ready {}, {}".format(
                            continue_paused.is_enabled(), continue_paused.is_displayed()
                        ))
                except selenium.common.exceptions.ElementNotVisibleException as e:
                    logger.error("CntBtn not clickable: {}".format(e))
                    one_found = True
                    sleep_time = SLEEP_TIME_BTN
                except selenium.common.exceptions.StaleElementReferenceException as e:
                    logger.error("CntBtn stale: {}".format(e))
                except:
                    logger.exception("Failed clicking CntBtn")
            try:
                skipAd = driver.find_element_by_xpath("//button[@class='ytp-ad-skip-button ytp-button']")
            except KeyboardInterrupt:
                break
            except (
                    selenium.common.exceptions.InvalidSelectorException,
                    selenium.common.exceptions.NoSuchElementException,
            ):
                logger.debug("No Btn")
            except:
                logger.exception("Failed Btn")
            else:
                one_found = True

            if not one_found:
                sleep_time = SLEEP_TIME_WAITING
                continue
            logger.debug("Got Btn!")
            try:
                if skipAd.is_enabled() and skipAd.is_displayed():
                    skipAd.click()
                else:
                    logger.debug("Btn not ready")
                    sleep_time = SLEEP_TIME_BTN
                    continue
            except selenium.common.exceptions.ElementNotVisibleException as e:
                logger.error("Btn not clickable: {}".format(e))
            except:
                logger.exception("Failed clicking")
    except KeyboardInterrupt:
        pass
    finally:
        driver.close()
