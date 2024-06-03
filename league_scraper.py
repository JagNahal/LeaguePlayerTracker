from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def func(user):
    # Initialize the Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=chrome_options)

    #account_id = input("Enter username: ")

    # Navigate to the op.gg page for the specific player
    driver.get(f"https://www.op.gg/summoners/na/{user}?queue_type=SOLORANKED")


    # Click the "Show More" button 5 times
    def nav_page(driver):
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.more"))
        count = 0
        while count < 10:
            try:
                show_more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.more"))
                )
                show_more_button.click()
                time.sleep(2)  # Wait for the page to load new matches
                count += 1 
            except:
                break

        if count < 1:
            print("No ranked games found")
            

    nav_page(driver)

    # Fetch the game dates, results, and types
    game_dates = driver.find_elements(By.CSS_SELECTOR, ".time-stamp")
    game_results = driver.find_elements(By.CSS_SELECTOR, ".result")
    game_types = driver.find_elements(By.CSS_SELECTOR, ".game-type")
    game_kda = driver.find_elements(By.CSS_SELECTOR, ".kda")
    game_kda_r = driver.find_elements(By.CSS_SELECTOR, ".kda-ratio")
    game_champ = driver.find_elements(By.CSS_SELECTOR, "a.champion img")
    game_kp = driver.find_elements(By.CSS_SELECTOR, ".p-kill")
    game_cs = driver.find_elements(By.CSS_SELECTOR, ".game-stats")

    
    match_stats = []
    for date, result, game_type, champ, kda, kda_r, kp, cs in zip(game_dates, game_results, game_types, game_champ, game_kda[8:], game_kda_r, game_kp, game_cs):
        if (game_type.text == "Ranked Solo") and (result.text != "Remake"):
            
            kp = (re.search(r"\d?\d", kp.text)).group()
            cstotal = cs.text.strip().split()[-4]
            csmin = cs.text.strip().split()[-3][1:-1]
            if kda_r.text == "Perfect":
                kda_r = 10.00
            else:    
                kda_r = (re.search(r"\d?\d\.\d{2}", kda_r.text)).group()
            
            uid = float(kp) + float(kda_r) + int(cstotal) + float(csmin)
            # print(date.text)
            # print(result.text)
            # print(champ.get_attribute("alt"))
            # print(cstotal + " cs") 
            # print(csmin)
            # print(kp)
            # print(kda_r)
            # print(kda.text.split())
            match_stats.append([uid, date.text, champ.get_attribute("alt"), result.text, int(kda.text.split()[0]), int(kda.text.split()[2]), int(kda.text.split()[4]), float(kda_r), int(kp), int(cstotal), float(csmin)]) 
        

    # # Print the fetched game dates and results for debugging
    # print("Fetched Game Dates and Results for Ranked Solo:")
    # for date, result, game_type in zip(game_dates, game_results, game_types):
    #     if game_type.text == "Ranked Solo" and "hour" not in date.text:
    #         print(date.text, "-", result.text)
    # print("\nWin Rate and Games Played Per Day for Ranked Solo:")
    # for day, stats in win_rate_per_day.items():
    #     win_rate = (stats["wins"] / stats["total"]) * 100
    #     print(f"{day}: {stats['wins']} wins out of {stats['total']} games ({win_rate:.2f}% win rate)")


    driver.quit()

    return match_stats