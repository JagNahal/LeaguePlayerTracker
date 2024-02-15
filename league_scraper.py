# Initialize the Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

#account_id = input("Enter username: ")

# Navigate to the op.gg page for the specific player
#driver.get(f"https://na.op.gg/summoner/userName={account_id}")
driver.get("https://na.op.gg/summoner/userName=brownbuddyguy")

# Click the "Show More" button 5 times
def nav_page(driver):
    count = 0
    while count < 3:
        try:
            show_more_button = WebDriverWait(driver, 10).until(
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
game_cs = driver.find_elements(By.CSS_SELECTOR, ".cs")

# Calculate win rate and games played per day for "Ranked Solo" games

games_stats = {}
for date, result, game_type, champ, kda, kda_r, kp, cs in zip(game_dates, game_results, game_types, game_champ, game_kda, game_kda_r, game_kp, game_cs):
    if (game_type.text == "Ranked Solo") and (result.text != "Remake"):
        day = date.text
        if "hour" and "month" not in day:
            kp = (re.search(r"\d?\d", kp.text)).group()
            csmin = (re.search(r"\d\.\d", cs.text)).group()
            cstotal = (re.search(r"\d?\d?\d", cs.text)).group()
            print(kda_r.text + " cs")
            kda_r = (re.search(r"\d?\d\.\d{2}", kda_r.text)).group()
            
            uid = float(kp) + float(kda_r) + int(cstotal) + float(csmin)
            # print(date.text)
            # print(result.text)
            # print(champ.get_attribute("alt"))
            print(cstotal + " cs") 
            print(csmin + " csmin")
            # print(csmin.text[3:6])
            # print(kp.text)
            # print(kda_r)
            # print(kda.text)
            #games_stats[uid] = (date.text, champ.get_attribute("alt"), result.text, kda.text, kda_r.text[0:4], kp)
            #print(games_stats[uid])


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